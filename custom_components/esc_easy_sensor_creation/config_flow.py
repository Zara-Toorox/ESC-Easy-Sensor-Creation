"""Config flow for ESC Easy Sensor Creation."""
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN, SENSOR_TYPE_SUM, SENSOR_TYPE_SQL, SENSOR_TYPE_KWH_HELPER,
    SQL_STAT_AVG_TODAY, SQL_STAT_AVG_MONTH, SQL_STAT_AVG_YEAR,
    SQL_STAT_MAX_TODAY, SQL_STAT_MAX_MONTH, SQL_STAT_MAX_YEAR,
    SQL_STAT_MIN_TODAY, SQL_STAT_MIN_MONTH, SQL_STAT_MIN_YEAR,
    DEVICE_CLASSES, DEVICE_CLASS_NONE
)

async def _get_helper_names(hass: HomeAssistant) -> list[str]:
    """Return a list of existing integration helper names."""
    return [
        entry.data.get("name")
        for entry in hass.config_entries.async_entries("integration")
        if entry.data.get("name")
    ]


class ESCConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ESC."""
    VERSION = 3
    data: dict

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            self.data = user_input
            sensor_type = self.data["sensor_type"]

            if sensor_type == SENSOR_TYPE_SQL:
                return await self.async_step_select_single_sensor()
            if sensor_type == SENSOR_TYPE_KWH_HELPER:
                return await self.async_step_kwh_config()
            # Default to SUM sensor
            return await self.async_step_select_sensors()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("sensor_type"): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=[
                        {"label": "kWh Sensor (erstellt Riemann Sensor für Energie-Dashboard)", "value": SENSOR_TYPE_KWH_HELPER},
                        {"label": "Summe (mehrere Sensoren addieren)", "value": SENSOR_TYPE_SUM},
                        {"label": "Verlaufs-Statistik (Durchschnitt, MIN, MAX)", "value": SENSOR_TYPE_SQL},
                    ], mode=selector.SelectSelectorMode.LIST)
                ),
            })
        )

    async def async_step_kwh_config(self, user_input=None):
        """Handle the configuration for the kWh helper."""
        if user_input is not None:
            existing_names = await _get_helper_names(self.hass)
            if user_input["sensor_name"] in existing_names:
                return self.async_show_form(
                    step_id="kwh_config",
                    data_schema=self.add_suggested_values_to_schema(
                        vol.Schema({
                            vol.Required("source_sensor"): selector.EntitySelector(
                                selector.EntitySelectorConfig(domain="sensor")
                            ),
                            vol.Required("sensor_name"): str,
                        }),
                        user_input,
                    ),
                    errors={"base": "name_exists"},
                )

            # Create the native integration helper
            await self.hass.config_entries.flow.async_init(
                "integration",
                context={"source": "user"},
                data={
                    "name": user_input["sensor_name"],
                    "source": user_input["source_sensor"],
                    "unit_prefix": "k",
                    "unit_time": "h",
                    "method": "left",
                },
            )
            return self.async_abort(reason="kwh_helper_created")

        return self.async_show_form(
            step_id="kwh_config",
            data_schema=vol.Schema({
                vol.Required("source_sensor"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Required("sensor_name", default="Täglicher Verbrauch"): str,
            }),
        )

    async def async_step_select_sensors(self, user_input=None):
        """Handle sensor selection for Sum."""
        if user_input is not None:
            self.data.update(user_input)
            return await self.async_step_device_class()

        return self.async_show_form(
            step_id="select_sensors",
            data_schema=vol.Schema({
                vol.Required("source_sensors"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", multiple=True)
                ),
            })
        )

    async def async_step_select_single_sensor(self, user_input=None):
        """Handle sensor selection for History Statistics."""
        if user_input is not None:
            self.data["source_sensors"] = [user_input["source_sensors"]]
            return await self.async_step_select_sql_stat_type()

        return self.async_show_form(
            step_id="select_single_sensor",
            data_schema=vol.Schema({
                vol.Required("source_sensors"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
            })
        )

    async def async_step_select_sql_stat_type(self, user_input=None):
        """Select statistic type for History sensor."""
        if user_input is not None:
            self.data.update(user_input)
            return await self.async_step_device_class()

        return self.async_show_form(
            step_id="select_sql_stat_type",
            data_schema=vol.Schema({
                vol.Required("sql_stat_type"): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=[
                        {"label": "Durchschnitt - Heute", "value": SQL_STAT_AVG_TODAY},
                        {"label": "Durchschnitt - Dieser Monat", "value": SQL_STAT_AVG_MONTH},
                        {"label": "Durchschnitt - Dieses Jahr", "value": SQL_STAT_AVG_YEAR},
                        {"label": "Maximum - Heute", "value": SQL_STAT_MAX_TODAY},
                        {"label": "Maximum - Dieser Monat", "value": SQL_STAT_MAX_MONTH},
                        {"label": "Maximum - Dieses Jahr", "value": SQL_STAT_MAX_YEAR},
                        {"label": "Minimum - Heute", "value": SQL_STAT_MIN_TODAY},
                        {"label": "Minimum - Dieser Monat", "value": SQL_STAT_MIN_MONTH},
                        {"label": "Minimum - Dieses Jahr", "value": SQL_STAT_MIN_YEAR},
                    ], mode=selector.SelectSelectorMode.DROPDOWN)
                ),
            })
        )
        
    async def async_step_device_class(self, user_input=None):
        """Select the device class."""
        if user_input is not None:
            device_class = user_input["device_class"]
            self.data["device_class"] = None if device_class == DEVICE_CLASS_NONE else device_class
            return await self.async_step_name_sensor()

        return self.async_show_form(
            step_id="device_class",
            data_schema=vol.Schema({
                vol.Required("device_class", default=DEVICE_CLASS_NONE): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=DEVICE_CLASSES, mode=selector.SelectSelectorMode.DROPDOWN)
                ),
            })
        )

    async def async_step_name_sensor(self, user_input=None):
        """Final step to name the sensor."""
        if user_input is not None:
            self.data["sensor_name"] = user_input["sensor_name"]
            return self.async_create_entry(title=self.data["sensor_name"], data=self.data)

        suggested_name = "Neuer Sensor"
        if self.data["sensor_type"] == SENSOR_TYPE_SUM:
            suggested_name = "Summen-Sensor"
        elif self.data["sensor_type"] == SENSOR_TYPE_SQL:
            suggested_name = self.data.get("sql_stat_type", "Statistik").replace("_", " ").title()

        return self.async_show_form(
            step_id="name_sensor",
            data_schema=vol.Schema({vol.Required("sensor_name", default=suggested_name): str}),
        )
        