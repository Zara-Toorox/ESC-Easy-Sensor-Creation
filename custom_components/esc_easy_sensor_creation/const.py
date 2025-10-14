"""Constants for ESC Easy Sensor Creation."""

DOMAIN = "esc_easy_sensor_creation"

# Main Sensor Types
SENSOR_TYPE_KWH_INTEGRATION = "kwh_integration"  # Power (W) → Energy (kWh)
SENSOR_TYPE_SUM = "sum"  # Simple addition
SENSOR_TYPE_SQL_STATISTICS = "sql_statistics"  # Database statistics

SENSOR_TYPES = [
    SENSOR_TYPE_KWH_INTEGRATION,
    SENSOR_TYPE_SUM,
    SENSOR_TYPE_SQL_STATISTICS,
]

# SQL Statistics Types
SQL_STAT_ENERGY_DAY = "energy_day"
SQL_STAT_ENERGY_MONTH = "energy_month"
SQL_STAT_ENERGY_YEAR = "energy_year"
SQL_STAT_ENERGY_PREVIOUS_MONTH = "energy_previous_month"
SQL_STAT_ENERGY_PREVIOUS_YEAR = "energy_previous_year"

SQL_STAT_AVERAGE_DAY = "average_day"
SQL_STAT_AVERAGE_MONTH = "average_month"
SQL_STAT_AVERAGE_YEAR = "average_year"

SQL_STAT_MAX_DAY = "max_day"
SQL_STAT_MAX_MONTH = "max_month"
SQL_STAT_MAX_YEAR = "max_year"

SQL_STAT_MIN_DAY = "min_day"
SQL_STAT_MIN_MONTH = "min_month"
SQL_STAT_MIN_YEAR = "min_year"

SQL_STATISTICS_TYPES = [
    SQL_STAT_ENERGY_DAY,
    SQL_STAT_ENERGY_MONTH,
    SQL_STAT_ENERGY_YEAR,
    SQL_STAT_ENERGY_PREVIOUS_MONTH,
    SQL_STAT_ENERGY_PREVIOUS_YEAR,
    SQL_STAT_AVERAGE_DAY,
    SQL_STAT_AVERAGE_MONTH,
    SQL_STAT_AVERAGE_YEAR,
    SQL_STAT_MAX_DAY,
    SQL_STAT_MAX_MONTH,
    SQL_STAT_MAX_YEAR,
    SQL_STAT_MIN_DAY,
    SQL_STAT_MIN_MONTH,
    SQL_STAT_MIN_YEAR,
]

# Source count
SOURCE_SINGLE = "single"
SOURCE_MULTIPLE = "multiple"

# SQL Database types
DB_TYPE_MARIADB = "mariadb"
DB_TYPE_HOMEASSISTANT = "homeassistant"

DB_TYPES = [
    DB_TYPE_MARIADB,
    DB_TYPE_HOMEASSISTANT,
]

# Configuration keys
CONF_SENSOR_TYPE = "sensor_type"
CONF_SOURCE_COUNT = "source_count"
CONF_SOURCE_ENTITIES = "source_entities"
CONF_SENSOR_NAME = "sensor_name"
CONF_DB_TYPE = "db_type"
CONF_DB_HOST = "db_host"
CONF_DB_PORT = "db_port"
CONF_DB_USER = "db_user"
CONF_DB_PASSWORD = "db_password"
CONF_DB_NAME = "db_name"
CONF_SQL_STAT_TYPE = "sql_stat_type"
CONF_BASE_ENTITY = "base_entity"
