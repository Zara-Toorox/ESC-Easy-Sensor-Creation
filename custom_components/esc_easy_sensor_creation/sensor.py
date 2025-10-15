"""ESC Sensor Platform."""
from __future__ import annotations
import logging
from datetime import datetime, timedelta
import statistics

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.components.recorder import get_instance
from homeassistant.components.recorder.statistics import statistics_during_period

from .const import DOMAIN, SENSOR_TYPE_SUM, SENSOR_TYPE_SQL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the sensor platform."""
    config = config_entry.data
    sensor_type = config.get("sensor_type")

    if sensor_type not in [SENSOR_TYPE_SUM, SENSOR_TYPE_SQL]:
        _LOGGER.debug(f"Sensor type '{sensor_type}' does not create an entity in this domain.")
        return
        
    sensor_map = {
        SENSOR_TYPE_SUM: ESCSumSensor,
        SENSOR_TYPE_SQL: ESCStatisticsSensor,
    }
    sensor_class = sensor_map.get(sensor_type)
    
    async_add_entities([sensor_class(hass, config_entry, config)])
    _LOGGER.info(f"Setting up ESC entity: {config.get('sensor_name')}")


class ESCBaseSensor(SensorEntity):
    """Base class for ESC sensors."""
    _attr_should_poll = False
    
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry, config: dict):
        self.hass = hass
        self._config = config
        self._attr_name = config.get("sensor_name", "Unnamed Sensor")
        # The unique ID of the ENTITY is the unique ID of the config entry
        self._attr_unique_id = config_entry.entry_id
        
        if device_class := config.get("device_class"):
            self._attr_device_class = SensorDeviceClass(device_class)
            
        # This links the ENTITY to the central DEVICE
        self._attr_device_info = {
            "identifiers": {(DOMAIN, DOMAIN)}, # Link to the static identifier
            # The name here is the name of the central device, NOT the entity
            "name": "ESC Easy Sensor Creation", 
        }

class ESCSumSensor(ESCBaseSensor):
    """Sensor that sums multiple sensors."""
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:sigma"

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry, config: dict):
        super().__init__(hass, config_entry, config)
        self._source_sensors = self._config["source_sensors"]
        self._attr_extra_state_attributes = {"source_sensors": self._source_sensors}

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self.async_on_remove(
            async_track_state_change_event(self.hass, self._source_sensors, self._handle_state_change)
        )
        await self._async_update_state()

    @callback
    def _handle_state_change(self, event): 
        self.async_schedule_update_ha_state(True)

    async def async_update(self):
        await self._async_update_state()

    async def _async_update_state(self):
        """Update the sensor's state."""
        total = 0.0
        units = set()
        
        for entity_id in self._source_sensors:
            if (state := self.hass.states.get(entity_id)) and state.state not in ("unknown", "unavailable"):
                try:
                    total += float(state.state)
                    if unit := state.attributes.get("unit_of_measurement"):
                        units.add(unit)
                except (ValueError, TypeError):
                    _LOGGER.warning(f"Could not parse state of {entity_id} as a number.")
        
        if len(units) > 1:
            _LOGGER.error(f"Sensor '{self.name}' has mixed units: {units}. Cannot calculate sum.")
            self._attr_available = False
            self._attr_extra_state_attributes["error"] = f"Mixed units: {sorted(list(units))}"
            self._attr_native_value = None
            self._attr_native_unit_of_measurement = None
        else:
            self._attr_available = True
            self._attr_extra_state_attributes.pop("error", None)
            self._attr_native_value = round(total, 2)
            self._attr_native_unit_of_measurement = units.pop() if units else None

class ESCStatisticsSensor(ESCBaseSensor):
    """Sensor that calculates statistics using the Recorder API."""
    _attr_state_class = SensorStateClass.MEASUREMENT
    # This sensor polls the database, so we enable polling for it
    _attr_should_poll = True 
    
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry, config: dict):
        super().__init__(hass, config_entry, config)
        self._source_sensor_id = self._config["source_sensors"][0]
        self._stat_type = self._config["sql_stat_type"]
        self._attr_extra_state_attributes = {"source_sensor": self._source_sensor_id}
        
        icon_map = {"avg": "mdi:chart-line", "max": "mdi:arrow-up-bold", "min": "mdi:arrow-down-bold"}
        self._attr_icon = icon_map.get(self._stat_type.split('_')[0])
        
        if source_state := self.hass.states.get(self._source_sensor_id):
            self._attr_native_unit_of_measurement = source_state.attributes.get("unit_of_measurement")

    # The polling interval is defined by the integration's update_interval
    # which defaults to 1 minute, but can be set in async_setup_entry if needed
    
    async def async_update(self) -> None:
        """Fetch new state data."""
        now = datetime.now()
        stat_time_range = self._stat_type.split('_')[-1]
        
        if stat_time_range == 'today':
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif stat_time_range == 'month':
            start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif stat_time_range == 'year':
            start_time = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            _LOGGER.error(f"Invalid time range '{stat_time_range}' for statistic sensor.")
            self._attr_native_value = None
            return

        stat_func = self._stat_type.split('_')[0]
        stat_map = {'avg': 'mean', 'min': 'min', 'max': 'max'}
        required_stat = stat_map.get(stat_func)
        
        if not required_stat:
            _LOGGER.error(f"Invalid statistic function '{stat_func}'.")
            self._attr_native_value = None
            return

        try:
            stats = await get_instance(self.hass).async_add_executor_job(
                statistics_during_period,
                self.hass, start_time, None,
                [self._source_sensor_id], "hour", None, {required_stat}
            )
        except Exception as e:
            _LOGGER.error(f"Error fetching statistics for {self._source_sensor_id}: {e}")
            self._attr_native_value = None
            return

        values = [
            s[required_stat] for s in stats.get(self._source_sensor_id, [])
            if s.get(required_stat) is not None
        ]

        if not values:
            self._attr_native_value = 0 if stat_func == 'avg' else None
            return

        try:
            if stat_func == 'avg': self._attr_native_value = statistics.mean(values)
            elif stat_func == 'max': self._attr_native_value = max(values)
            elif stat_func == 'min': self._attr_native_value = min(values)
            
            if self._attr_native_value is not None:
                self._attr_native_value = round(self._attr_native_value, 2)
        except statistics.StatisticsError:
            self._attr_native_value = 0 # No data to compute mean
        except ValueError:
            self._attr_native_value = None # No data for min/max
            