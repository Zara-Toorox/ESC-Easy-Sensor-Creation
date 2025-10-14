# ESC Easy Sensor Creation

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/Zara-Toorox/esc_easy_sensor_creation.svg)](https://github.com/Zara-Toorox/esc_easy_sensor_creation/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Home Assistant integration for easily creating custom sensors.

## ✨ Features

### 🔋 kWh Integration Sensor
- Integrates power (W) to energy (kWh)
- **Left-side integration** for precise calculations
- Perfect for the Energy Dashboard
- State restore after restart
- Supports multiple power sensors

### ➕ Sum Sensor
- Adds multiple sensors together
- Automatic unit detection
- Supports any sensor type
- Real-time calculation

### 📊 SQL Statistics Sensors (14 Types!)

**Energy Statistics:**
- Today (kWh)
- Current Month (kWh)
- Current Year (kWh)
- Previous Month (kWh)
- Previous Year (kWh)

**Average Statistics:**
- Today
- Current Month
- Current Year

**Maximum Statistics:**
- Today
- Current Month
- Current Year

**Minimum Statistics:**
- Today
- Current Month
- Current Year

### 🗄️ Database Support
- ✅ Home Assistant SQLite Database
- ✅ MariaDB via Network
- ✅ Automatic fallback to `states` table when `statistics` table is empty

## 📦 Installation

### HACS (Recommended)

1. Open HACS
2. Go to "Integrations"
3. Click the 3 dots in the top right
4. Select "Custom repositories"
5. Add: `https://github.com/Zara-Toorox/esc_easy_sensor_creation`
6. Category: "Integration"
7. Install "ESC Easy Sensor Creation"
8. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/esc_easy_sensor_creation` folder to your `config/custom_components` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services
4. Click "+ Add Integration"
5. Search for "ESC Easy Sensor Creation"

## 🚀 Usage

### Creating a kWh Integration Sensor

1. Go to Settings → Devices & Services → Add Integration
2. Search for "ESC Easy Sensor Creation"
3. Select "kWh Integration"
4. Choose one or more **power sensors (W)**
5. Name your sensor
6. Done! The sensor will now continuously calculate energy

**Example:** 3 power outlets with 100W each → kWh sensor shows total energy consumption

### Creating a Sum Sensor

1. Select "Sum Sensor"
2. Choose single or multiple sensors
3. Select the sensors to add
4. Name your sensor
5. Done! The sensor will show the sum of all selected sensors

**Example:** Sum of all room temperatures

### Creating a SQL Statistics Sensor

1. Select "SQL Statistics Sensor"
2. Choose the type (e.g., "Average - Today")
3. Select database:
   - Home Assistant Database (SQLite) - usually the right choice
   - MariaDB - for advanced users
4. Select the base sensor
5. Name your sensor
6. Done!

**Example:** Average temperature of today from a temperature sensor

## ⚙️ MariaDB Configuration

For MariaDB Add-on users:
- **Host:** `core-mariadb`
- **Port:** `3306`
- **User:** `homeassistant`
- **Database:** `homeassistant`
- **Password:** Your MariaDB password

## 🔧 Technical Details

### Left-Side Integration

The kWh sensor uses **left-side integration** for energy calculation:
This means: At each change, the **previous** power value is used, not the average.

### SQL Fallback

When the `statistics` table has no data (e.g., for sensors without long-term statistics),
the system automatically falls back to the `states` table and calculates values in real-time.

## 🐛 Troubleshooting

### SQL Sensor shows 0

- Check if the sensor has long-term statistics: Developer Tools → Statistics
- No problem! The sensor automatically uses the `states` table as fallback

### kWh Sensor not counting

- Check if source sensors output **Watts (W)**
- Check if sensors provide regular updates

### Icon not displayed

- Clear browser cache (Ctrl + F5)
- Restart Home Assistant
- Not critical - works without icon!

### MariaDB connection fails

- Check host, port, username, and password
- Verify MariaDB Add-on is running
- Check firewall settings

## 📝 Changelog

### Version 0.2.2
- SQL fallback to states table
- Improved MariaDB support
- Menu-based config flow
- Bug fixes and improvements

### Version 0.1.0
- First version
- kWh Integration, Sum Sensor, SQL Statistics

## 🤝 Contributing

Contributions are welcome! Please create a Pull Request or Issue on GitHub.

### Development Setup

1. Fork the repository
2. Clone your fork
3. Create a branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Test thoroughly
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature`
8. Create a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Credits

Developed for the Home Assistant Community

## 💬 Support

- **Issues:** [GitHub Issues](https://github.com/Zara-Toorox/esc_easy_sensor_creation/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Zara-Toorox/esc_easy_sensor_creation/discussions)
- **Home Assistant Forum:** Coming soon

## ⭐ Star History

If you find this integration useful, please consider giving it a star on GitHub!

---

**Made with ❤️ for Home Assistant**
