"""Config flow for ESC Easy Sensor Creation."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    SENSOR_TYPE_KWH_INTEGRATION,
    SENSOR_TYPE_SUM,
    SENSOR_TYPE_SQL_STATISTICS,
    SOURCE_SINGLE,
    SOURCE_MULTIPLE,
    DB_TYPE_MARIADB,
    DB_TYPE_HOMEASSISTANT,
    CONF_SENSOR_TYPE,
    CONF_SOURCE_COUNT,
    CONF_SOURCE_ENTITIES,
    CONF_SENSOR_NAME,
    CONF_DB_TYPE,
    CONF_SQL_STAT_TYPE,
    CONF_BASE_ENTITY,
    CONF_DB_HOST,
    CONF_DB_PORT,
    CONF_DB_USER,
    CONF_DB_PASSWORD,
    CONF_DB_NAME,
)

_LOGGER = logging.getLogger(__name__)


class ESCConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ESC Easy Sensor Creation."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.data = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step - show menu."""
        return self.async_show_menu(
            step_id="user",
            menu_options=["kwh_integration", "sum_sensor", "sql_statistics"],
        )

    async def async_step_kwh_integration(self, user_input=None):
        """Handle kWh integration sensor setup."""
        self.data[CONF_SENSOR_TYPE] = SENSOR_TYPE_KWH_INTEGRATION
        return await self.async_step_source_count()

    async def async_step_sum_sensor(self, user_input=None):
        """Handle sum sensor setup."""
        self.data[CONF_SENSOR_TYPE] = SENSOR_TYPE_SUM
        return await self.async_step_source_count()

    async def async_step_sql_statistics(self, user_input=None):
        """Handle SQL statistics sensor setup."""
        self.data[CONF_SENSOR_TYPE] = SENSOR_TYPE_SQL_STATISTICS
        return self.async_show_menu(
            step_id="sql_statistics",
            menu_options=[
                "sql_energy_day",
                "sql_energy_month",
                "sql_energy_year",
                "sql_energy_previous_month",
                "sql_energy_previous_year",
                "sql_average_day",
                "sql_average_month",
                "sql_average_year",
                "sql_max_day",
                "sql_max_month",
                "sql_max_year",
                "sql_min_day",
                "sql_min_month",
                "sql_min_year",
            ],
        )

    # SQL Statistics sub-steps
    async def async_step_sql_energy_day(self, user_input=None):
        """Energy - Today."""
        self.data[CONF_SQL_STAT_TYPE] = "energy_day"
        return await self.async_step_sql_database()

    async def async_step_sql_energy_month(self, user_input=None):
        """Energy - Current Month."""
        self.data[CONF_SQL_STAT_TYPE] = "energy_month"
        return await self.async_step_sql_database()

    async def async_step_sql_energy_year(self, user_input=None):
        """Energy - Current Year."""
        self.data[CONF_SQL_STAT_TYPE] = "energy_year"
        return await self.async_step_sql_database()

    async def async_step_sql_energy_previous_month(self, user_input=None):
        """Energy - Previous Month."""
        self.data[CONF_SQL_STAT_TYPE] = "energy_previous_month"
        return await self.async_step_sql_database()

    async def async_step_sql_energy_previous_year(self, user_input=None):
        """Energy - Previous Year."""
        self.data[CONF_SQL_STAT_TYPE] = "energy_previous_year"
        return await self.async_step_sql_database()

    async def async_step_sql_average_day(self, user_input=None):
        """Average - Today."""
        self.data[CONF_SQL_STAT_TYPE] = "average_day"
        return await self.async_step_sql_database()

    async def async_step_sql_average_month(self, user_input=None):
        """Average - Current Month."""
        self.data[CONF_SQL_STAT_TYPE] = "average_month"
        return await self.async_step_sql_database()

    async def async_step_sql_average_year(self, user_input=None):
        """Average - Current Year."""
        self.data[CONF_SQL_STAT_TYPE] = "average_year"
        return await self.async_step_sql_database()

    async def async_step_sql_max_day(self, user_input=None):
        """Maximum - Today."""
        self.data[CONF_SQL_STAT_TYPE] = "max_day"
        return await self.async_step_sql_database()

    async def async_step_sql_max_month(self, user_input=None):
        """Maximum - Current Month."""
        self.data[CONF_SQL_STAT_TYPE] = "max_month"
        return await self.async_step_sql_database()

    async def async_step_sql_max_year(self, user_input=None):
        """Maximum - Current Year."""
        self.data[CONF_SQL_STAT_TYPE] = "max_year"
        return await self.async_step_sql_database()

    async def async_step_sql_min_day(self, user_input=None):
        """Minimum - Today."""
        self.data[CONF_SQL_STAT_TYPE] = "min_day"
        return await self.async_step_sql_database()

    async def async_step_sql_min_month(self, user_input=None):
        """Minimum - Current Month."""
        self.data[CONF_SQL_STAT_TYPE] = "min_month"
        return await self.async_step_sql_database()

    async def async_step_sql_min_year(self, user_input=None):
        """Minimum - Current Year."""
        self.data[CONF_SQL_STAT_TYPE] = "min_year"
        return await self.async_step_sql_database()

    async def async_step_source_count(self, user_input=None):
        """Handle source count selection."""
        return self.async_show_menu(
            step_id="source_count",
            menu_options=["single_sensor", "multiple_sensors"],
        )

    async def async_step_single_sensor(self, user_input=None):
        """Handle single sensor selection."""
        self.data[CONF_SOURCE_COUNT] = SOURCE_SINGLE
        return await self.async_step_select_entities()

    async def async_step_multiple_sensors(self, user_input=None):
        """Handle multiple sensors selection."""
        self.data[CONF_SOURCE_COUNT] = SOURCE_MULTIPLE
        return await self.async_step_select_entities()

    async def async_step_select_entities(self, user_input=None):
        """Handle entity selection."""
        errors = {}

        if user_input is not None:
            self.data[CONF_SOURCE_ENTITIES] = user_input[CONF_SOURCE_ENTITIES]
            return await self.async_step_name_sensor()

        multiple = self.data[CONF_SOURCE_COUNT] == SOURCE_MULTIPLE

        sensor_type = self.data.get(CONF_SENSOR_TYPE)
        if sensor_type == SENSOR_TYPE_KWH_INTEGRATION:
            description = "Wähle Leistungs-Sensoren in Watt (W) aus."
        else:
            description = "Wähle die Sensoren aus."

        data_schema = vol.Schema({
            vol.Required(CONF_SOURCE_ENTITIES): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["sensor"],
                    multiple=multiple,
                )
            ),
        })

        return self.async_show_form(
            step_id="select_entities",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={"info": description}
        )

    async def async_step_name_sensor(self, user_input=None):
        """Handle sensor naming."""
        errors = {}

        if user_input is not None:
            self.data[CONF_SENSOR_NAME] = user_input[CONF_SENSOR_NAME]
            
            return self.async_create_entry(
                title=self.data[CONF_SENSOR_NAME],
                data=self.data,
            )

        data_schema = vol.Schema({
            vol.Required(CONF_SENSOR_NAME): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                )
            ),
        })

        return self.async_show_form(
            step_id="name_sensor",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_sql_database(self, user_input=None):
        """Handle SQL database selection."""
        return self.async_show_menu(
            step_id="sql_database",
            menu_options=["db_sqlite", "db_mariadb"],
        )

    async def async_step_db_sqlite(self, user_input=None):
        """Handle SQLite database."""
        self.data[CONF_DB_TYPE] = DB_TYPE_HOMEASSISTANT
        return await self.async_step_sql_base_entity()

    async def async_step_db_mariadb(self, user_input=None):
        """Handle MariaDB database."""
        self.data[CONF_DB_TYPE] = DB_TYPE_MARIADB
        return await self.async_step_mariadb_credentials()

    async def async_step_mariadb_credentials(self, user_input=None):
        """Handle MariaDB credentials."""
        errors = {}

        if user_input is not None:
            self.data.update(user_input)
            return await self.async_step_sql_base_entity()

        data_schema = vol.Schema({
            vol.Required(CONF_DB_HOST, default="core-mariadb"): str,
            vol.Required(CONF_DB_PORT, default=3306): int,
            vol.Required(CONF_DB_NAME, default="homeassistant"): str,
            vol.Required(CONF_DB_USER, default="homeassistant"): str,
            vol.Required(CONF_DB_PASSWORD): str,
        })

        return self.async_show_form(
            step_id="mariadb_credentials",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_sql_base_entity(self, user_input=None):
        """Handle base entity selection for SQL."""
        errors = {}

        if user_input is not None:
            self.data[CONF_BASE_ENTITY] = user_input[CONF_BASE_ENTITY]
            return await self.async_step_name_sensor()

        data_schema = vol.Schema({
            vol.Required(CONF_BASE_ENTITY): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["sensor"],
                )
            ),
        })

        return self.async_show_form(
            step_id="sql_base_entity",
            data_schema=data_schema,
            errors=errors,
        )
