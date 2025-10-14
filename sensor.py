"""Sensor platform for ESC Easy Sensor Creation."""
import logging
from datetime import datetime, timedelta
import sqlite3

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event, async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.const import (
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    UnitOfEnergy,
)
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    SENSOR_TYPE_KWH_INTEGRATION,
    SENSOR_TYPE_SUM,
    SENSOR_TYPE_SQL_STATISTICS,
    CONF_SENSOR_TYPE,
    CONF_SOURCE_ENTITIES,
    CONF_SENSOR_NAME,
    CONF_DB_TYPE,
    CONF_SQL_STAT_TYPE,
    CONF_BASE_ENTITY,
    DB_TYPE_HOMEASSISTANT,
    CONF_DB_HOST,
    CONF_DB_PORT,
    CONF_DB_USER,
    CONF_DB_PASSWORD,
    CONF_DB_NAME,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up ESC sensor based on a config entry."""
    config = hass.data[DOMAIN][entry.entry_id]
    sensor_type = config.get(CONF_SENSOR_TYPE)
    
    _LOGGER.info("Setting up ESC sensor: %s (type: %s)", config.get(CONF_SENSOR_NAME), sensor_type)
    
    if sensor_type == SENSOR_TYPE_SQL_STATISTICS:
        sensor = ESCSQLStatisticsSensor(hass, config, entry.entry_id)
    elif sensor_type == SENSOR_TYPE_KWH_INTEGRATION:
        sensor = ESCKwhIntegrationSensor(hass, config, entry.entry_id)
    else:
        sensor = ESCSumSensor(hass, config, entry.entry_id)
    
    async_add_entities([sensor], True)


class ESCBaseSensor(SensorEntity):
    """Base class for ESC sensors."""

    def __init__(self, hass: HomeAssistant, config: dict, entry_id: str) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._config = config
        self._entry_id = entry_id
        self._attr_name = config.get(CONF_SENSOR_NAME)
        self._attr_unique_id = f"{DOMAIN}_{entry_id}"
        self._attr_should_poll = False
        self._source_entities = config.get(CONF_SOURCE_ENTITIES, [])
        
        if isinstance(self._source_entities, str):
            self._source_entities = [self._source_entities]

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "ESC Easy Sensor Creation",
            "manufacturer": "ESC",
            "model": "Easy Sensor",
        }


class ESCSumSensor(ESCBaseSensor):
    """Representation of a Sum Sensor."""

    def __init__(self, hass: HomeAssistant, config: dict, entry_id: str) -> None:
        """Initialize the sum sensor."""
        super().__init__(hass, config, entry_id)
        self._attr_state_class = None
        self._attr_device_class = None

    async def async_added_to_hass(self) -> None:
        """Handle added to hass."""
        @callback
        def async_state_changed_listener(event):
            self.async_schedule_update_ha_state(True)

        self.async_on_remove(
            async_track_state_change_event(
                self.hass, self._source_entities, async_state_changed_listener
            )
        )
        await self.async_update()

    async def async_update(self) -> None:
        """Update the sensor."""
        total = 0
        valid_values = 0
        unit = None
        state_class = None

        for entity_id in self._source_entities:
            state = self.hass.states.get(entity_id)
            
            if state is None or state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
                continue
            
            try:
                total += float(state.state)
                valid_values += 1
                
                if unit is None:
                    unit = state.attributes.get("unit_of_measurement")
                    state_class = state.attributes.get("state_class")
            except (ValueError, TypeError):
                continue

        if valid_values > 0:
            self._attr_native_value = round(total, 3)
            self._attr_native_unit_of_measurement = unit
            
            if state_class == "total":
                self._attr_state_class = SensorStateClass.TOTAL
            elif state_class == "total_increasing":
                self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        else:
            self._attr_native_value = None


class ESCKwhIntegrationSensor(ESCBaseSensor, RestoreEntity):
    """Representation of a kWh Integration Sensor."""

    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, hass: HomeAssistant, config: dict, entry_id: str) -> None:
        """Initialize the kWh integration sensor."""
        super().__init__(hass, config, entry_id)
        self._last_update = {}
        self._last_power = {}
        self._total_energy = 0.0

    async def async_added_to_hass(self) -> None:
        """Handle added to hass."""
        await super().async_added_to_hass()
        
        last_state = await self.async_get_last_state()
        if last_state and last_state.state not in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            try:
                self._total_energy = float(last_state.state)
            except (ValueError, TypeError):
                self._total_energy = 0.0

        @callback
        def async_state_changed_listener(event):
            self._calculate_energy(event)

        self.async_on_remove(
            async_track_state_change_event(
                self.hass, self._source_entities, async_state_changed_listener
            )
        )
        
        now = dt_util.utcnow()
        for entity_id in self._source_entities:
            state = self.hass.states.get(entity_id)
            if state and state.state not in (STATE_UNAVAILABLE, STATE_UNKNOWN):
                try:
                    self._last_power[entity_id] = float(state.state)
                    self._last_update[entity_id] = now
                except (ValueError, TypeError):
                    pass
        
        self._attr_native_value = round(self._total_energy, 3)

    @callback
    def _calculate_energy(self, event):
        """Calculate energy using LEFT-SIDE integration."""
        entity_id = event.data.get("entity_id")
        new_state = event.data.get("new_state")
        
        if new_state is None or new_state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            return
        
        now = dt_util.utcnow()
        
        try:
            current_power = float(new_state.state)
        except (ValueError, TypeError):
            return
        
        if entity_id in self._last_update and entity_id in self._last_power:
            time_diff_hours = (now - self._last_update[entity_id]).total_seconds() / 3600
            energy_kwh = (self._last_power[entity_id] * time_diff_hours) / 1000
            self._total_energy += energy_kwh
        
        self._last_power[entity_id] = current_power
        self._last_update[entity_id] = now
        
        self._attr_native_value = round(self._total_energy, 3)
        self.async_write_ha_state()


class ESCSQLStatisticsSensor(ESCBaseSensor):
    """Representation of a SQL Statistics Sensor."""

    def __init__(self, hass: HomeAssistant, config: dict, entry_id: str) -> None:
        """Initialize the SQL statistics sensor."""
        super().__init__(hass, config, entry_id)
        self._db_type = config.get(CONF_DB_TYPE)
        self._stat_type = config.get(CONF_SQL_STAT_TYPE)
        self._base_entity = config.get(CONF_BASE_ENTITY)
        self._metadata_id = None
        
        self._db_host = config.get(CONF_DB_HOST)
        self._db_port = config.get(CONF_DB_PORT, 3306)
        self._db_user = config.get(CONF_DB_USER)
        self._db_password = config.get(CONF_DB_PASSWORD)
        self._db_name = config.get(CONF_DB_NAME)
        
        if "energy" in self._stat_type:
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING

    async def async_added_to_hass(self) -> None:
        """Handle added to hass."""
        await self._async_get_metadata_id()
        
        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                self._async_update_callback,
                timedelta(hours=1),
            )
        )
        
        await self.async_update()

    @callback
    async def _async_update_callback(self, now):
        """Update callback."""
        await self.async_update()
        self.async_write_ha_state()

    async def _async_get_metadata_id(self):
        """Get metadata_id for the base entity."""
        if self._db_type == DB_TYPE_HOMEASSISTANT:
            await self._get_metadata_id_sqlite()
        else:
            await self._get_metadata_id_mariadb()

    async def _get_metadata_id_sqlite(self):
        """Get metadata_id from SQLite."""
        def _query():
            db_path = self.hass.config.path("home-assistant_v2.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT metadata_id FROM states_meta WHERE entity_id = ?",
                (self._base_entity,)
            )
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
        
        try:
            self._metadata_id = await self.hass.async_add_executor_job(_query)
            if self._metadata_id:
                _LOGGER.info("SQL Sensor %s: Found metadata_id %s", self._attr_name, self._metadata_id)
        except Exception as e:
            _LOGGER.error("SQL Sensor %s: Error getting metadata_id: %s", self._attr_name, e)

    async def _get_metadata_id_mariadb(self):
        """Get metadata_id from MariaDB."""
        def _query():
            import pymysql
            
            conn = pymysql.connect(
                host=self._db_host,
                port=self._db_port,
                user=self._db_user,
                password=self._db_password,
                database=self._db_name,
                connect_timeout=10
            )
            
            cursor = conn.cursor()
            cursor.execute(
                "SELECT metadata_id FROM states_meta WHERE entity_id = %s",
                (self._base_entity,)
            )
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
        
        try:
            self._metadata_id = await self.hass.async_add_executor_job(_query)
            if self._metadata_id:
                _LOGGER.info("SQL Sensor %s: Found metadata_id %s", self._attr_name, self._metadata_id)
        except Exception as e:
            _LOGGER.error("SQL Sensor %s: Error: %s", self._attr_name, e)

    def _get_time_range(self, period: str):
        """Get timestamp range for a given period."""
        now = datetime.now()
        
        if period == "day":
            start = datetime(now.year, now.month, now.day)
            end = None
        elif period == "month":
            start = datetime(now.year, now.month, 1)
            end = None
        elif period == "year":
            start = datetime(now.year, 1, 1)
            end = None
        elif period == "previous_month":
            if now.month == 1:
                start = datetime(now.year - 1, 12, 1)
                end = datetime(now.year, 1, 1)
            else:
                start = datetime(now.year, now.month - 1, 1)
                end = datetime(now.year, now.month, 1)
        elif period == "previous_year":
            start = datetime(now.year - 1, 1, 1)
            end = datetime(now.year, 1, 1)
        else:
            return None, None
        
        return start.timestamp(), end.timestamp() if end else None

    async def async_update(self) -> None:
        """Update the sensor."""
        if self._metadata_id is None:
            _LOGGER.warning("SQL Sensor %s: No metadata_id", self._attr_name)
            self._attr_native_value = None
            return
        
        if self._db_type == DB_TYPE_HOMEASSISTANT:
            await self._query_sqlite()
        else:
            await self._query_mariadb()

    async def _query_sqlite(self):
        """Query SQLite - with fallback to states table."""
        try:
            value = await self._calculate_stat_sqlite()
            self._attr_native_value = round(value, 2) if value else 0
            _LOGGER.info("SQL Sensor %s: Value = %.2f", self._attr_name, self._attr_native_value)
        except Exception as e:
            _LOGGER.error("SQL Sensor %s: Error: %s", self._attr_name, e)
            self._attr_native_value = None

    async def _calculate_stat_sqlite(self) -> float:
        """Calculate statistic from SQLite with fallback to states."""
        def _query():
            db_path = self.hass.config.path("home-assistant_v2.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            if "day" in self._stat_type:
                period = "day"
            elif "month" in self._stat_type:
                period = "previous_month" if "previous" in self._stat_type else "month"
            elif "year" in self._stat_type:
                period = "previous_year" if "previous" in self._stat_type else "year"
            else:
                period = "day"
            
            start_ts, end_ts = self._get_time_range(period)
            
            # Try statistics table first
            if "energy" in self._stat_type:
                agg_func = "SUM(sum)"
            elif "average" in self._stat_type:
                agg_func = "AVG(mean)"
            elif "max" in self._stat_type:
                agg_func = "MAX(max)"
            elif "min" in self._stat_type:
                agg_func = "MIN(min)"
            else:
                agg_func = "SUM(sum)"
            
            if end_ts:
                query = f"SELECT {agg_func} FROM statistics WHERE metadata_id = ? AND start_ts >= ? AND start_ts < ?"
                cursor.execute(query, (self._metadata_id, start_ts, end_ts))
            else:
                query = f"SELECT {agg_func} FROM statistics WHERE metadata_id = ? AND start_ts >= ?"
                cursor.execute(query, (self._metadata_id, start_ts))
            
            result = cursor.fetchone()
            
            # If statistics returned NULL, use states table as fallback
            if not result or result[0] is None:
                _LOGGER.info("SQL Sensor: statistics returned NULL, using states table fallback")
                
                # Fallback to states table
                if "average" in self._stat_type:
                    if end_ts:
                        query = """
                            SELECT AVG(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = ?
                            AND last_updated_ts >= ?
                            AND last_updated_ts < ?
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, start_ts, end_ts))
                    else:
                        query = """
                            SELECT AVG(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = ?
                            AND last_updated_ts >= ?
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, start_ts))
                    
                elif "max" in self._stat_type:
                    if end_ts:
                        query = """
                            SELECT MAX(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = ?
                            AND last_updated_ts >= ?
                            AND last_updated_ts < ?
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, start_ts, end_ts))
                    else:
                        query = """
                            SELECT MAX(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = ?
                            AND last_updated_ts >= ?
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, start_ts))
                    
                elif "min" in self._stat_type:
                    if end_ts:
                        query = """
                            SELECT MIN(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = ?
                            AND last_updated_ts >= ?
                            AND last_updated_ts < ?
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, start_ts, end_ts))
                    else:
                        query = """
                            SELECT MIN(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = ?
                            AND last_updated_ts >= ?
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, start_ts))
                
                result = cursor.fetchone()
            
            conn.close()
            return float(result[0]) if result and result[0] else 0.0
        
        return await self.hass.async_add_executor_job(_query)

    async def _query_mariadb(self):
        """Query MariaDB with fallback to states."""
        try:
            value = await self._calculate_stat_mariadb()
            self._attr_native_value = round(value, 2) if value else 0
            _LOGGER.info("SQL Sensor %s: Value = %.2f", self._attr_name, self._attr_native_value)
        except Exception as e:
            _LOGGER.error("SQL Sensor %s: Error: %s", self._attr_name, e)
            self._attr_native_value = None

    async def _calculate_stat_mariadb(self) -> float:
        """Calculate statistic from MariaDB with fallback."""
        def _query():
            import pymysql
            
            if "day" in self._stat_type:
                period = "day"
            elif "month" in self._stat_type:
                period = "previous_month" if "previous" in self._stat_type else "month"
            elif "year" in self._stat_type:
                period = "previous_year" if "previous" in self._stat_type else "year"
            else:
                period = "day"
            
            start_ts, end_ts = self._get_time_range(period)
            
            if "energy" in self._stat_type:
                agg_func = "SUM(sum)"
            elif "average" in self._stat_type:
                agg_func = "AVG(mean)"
            elif "max" in self._stat_type:
                agg_func = "MAX(max)"
            elif "min" in self._stat_type:
                agg_func = "MIN(min)"
            else:
                agg_func = "SUM(sum)"
            
            conn = pymysql.connect(
                host=self._db_host,
                port=self._db_port,
                user=self._db_user,
                password=self._db_password,
                database=self._db_name,
                connect_timeout=10
            )
            
            cursor = conn.cursor()
            
            if end_ts:
                query = f"SELECT COALESCE({agg_func}, 0) FROM statistics WHERE metadata_id = %s AND start_ts >= %s AND start_ts < %s"
                cursor.execute(query, (self._metadata_id, int(start_ts), int(end_ts)))
            else:
                query = f"SELECT COALESCE({agg_func}, 0) FROM statistics WHERE metadata_id = %s AND start_ts >= %s"
                cursor.execute(query, (self._metadata_id, int(start_ts)))
            
            result = cursor.fetchone()
            
            # Fallback to states if NULL
            if not result or result[0] == 0 or result[0] is None:
                if "average" in self._stat_type:
                    if end_ts:
                        query = """
                            SELECT AVG(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = %s
                            AND last_updated_ts >= %s
                            AND last_updated_ts < %s
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, int(start_ts), int(end_ts)))
                    else:
                        query = """
                            SELECT AVG(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = %s
                            AND last_updated_ts >= %s
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, int(start_ts)))
                    
                elif "max" in self._stat_type:
                    if end_ts:
                        query = """
                            SELECT MAX(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = %s
                            AND last_updated_ts >= %s
                            AND last_updated_ts < %s
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, int(start_ts), int(end_ts)))
                    else:
                        query = """
                            SELECT MAX(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = %s
                            AND last_updated_ts >= %s
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, int(start_ts)))
                    
                elif "min" in self._stat_type:
                    if end_ts:
                        query = """
                            SELECT MIN(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = %s
                            AND last_updated_ts >= %s
                            AND last_updated_ts < %s
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, int(start_ts), int(end_ts)))
                    else:
                        query = """
                            SELECT MIN(CAST(state AS DECIMAL(10,2)))
                            FROM states
                            WHERE metadata_id = %s
                            AND last_updated_ts >= %s
                            AND state NOT IN ('unavailable', 'unknown', '')
                        """
                        cursor.execute(query, (self._metadata_id, int(start_ts)))
                
                result = cursor.fetchone()
            
            conn.close()
            return float(result[0]) if result and result[0] else 0.0
        
        return await self.hass.async_add_executor_job(_query)
