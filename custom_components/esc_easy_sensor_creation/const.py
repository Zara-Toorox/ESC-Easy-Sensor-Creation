"""Constants for ESC Easy Sensor Creation."""

DOMAIN = "esc_easy_sensor_creation"

# Sensor Types
SENSOR_TYPE_SUM = "sum"
SENSOR_TYPE_SQL = "sql_statistics"
SENSOR_TYPE_KWH_HELPER = "kwh_helper" # Neuer Typ zur Unterscheidung im Flow

# SQL Statistics Types
SQL_STAT_AVG_TODAY = "avg_today"
SQL_STAT_AVG_MONTH = "avg_month"
SQL_STAT_AVG_YEAR = "avg_year"

SQL_STAT_MAX_TODAY = "max_today"
SQL_STAT_MAX_MONTH = "max_month"
SQL_STAT_MAX_YEAR = "max_year"

SQL_STAT_MIN_TODAY = "min_today"
SQL_STAT_MIN_MONTH = "min_month"
SQL_STAT_MIN_YEAR = "min_year"

# Device Classes
DEVICE_CLASS_POWER = "power"
DEVICE_CLASS_ENERGY = "energy"
DEVICE_CLASS_TEMPERATURE = "temperature"
DEVICE_CLASS_HUMIDITY = "humidity"
DEVICE_CLASS_BATTERY = "battery"
DEVICE_CLASS_MONETARY = "monetary"
DEVICE_CLASS_VOLTAGE = "voltage"
DEVICE_CLASS_CURRENT = "current"
DEVICE_CLASS_NONE = "none"

DEVICE_CLASSES = [
    DEVICE_CLASS_NONE,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_MONETARY,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
]
