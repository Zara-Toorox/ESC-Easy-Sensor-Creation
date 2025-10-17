Easy Sensor Creation

### _Escape the Madness of YAML_

<img src="https://raw.githubusercontent.com/Zara-Toorox/ESC-Easy-Sensor-Creation/main/logo.png" width="200" alt="ESC Logo">

**Create powerful sensors in Home Assistant – without a single line of code.**

This integration is your shortcut to useful and intelligent sensors. If you're new to Home Assistant and don't want to write complex YAML files or templates, ESC is the perfect tool for you. It uses a simple, guided wizard in the UI to build everything from energy trackers to smart alarms.

---

## ✨ What can this integration do for you?

ESC provides an intuitive, step-by-step menu interface for common sensor tasks that would otherwise require deep technical knowledge. All sensors are grouped under a single "ESC Easy Sensor Creation" device for easy management.

| Sensor Type | Description | Use Case |
|-------------|-------------|----------|
| **kWh Sensor** | Converts a power sensor (W/kW) into an energy counter (kWh) using Riemann integration. Creates a native HA helper. | Track daily/monthly consumption in the Energy Dashboard (e.g., washing machine or solar panel). |
| **Sum Sensor** | Adds values from multiple sensors, with unit validation to prevent errors. | Total power draw from all lights in a room or combined temperature averages. |
| **History Statistics** | Calculates avg, min, or max from historical data (today, month, year) via Recorder. | Daily high/low temps, monthly energy peaks – no SQL needed. |
| **Delta Sensor** | Compares trends (e.g., today vs. yesterday mean) using HA's stats API. | Spot changes like "energy use up 20% this week" for alerts or dashboards. |
| **Battery Charge/Discharge** | Filters a power sensor for positive (charge) or negative (discharge) values, creates W sensor + kWh Riemann helper. | Solar charging (positive only) or EV battery drain (absolute negatives) for clean Energy Dashboard integration. |
| **Binary Threshold** | Triggers on/off based on a value crossing a threshold (e.g., >25°C). | Alarms like "overheat alert" or "low battery warning" with HA notifications. |
| **Toggle Switch** | Simple on/off control to pause or reset linked sensors. | Temporarily disable a sum sensor during maintenance or reset counters. |

**Bonus:** Optional device class assignment for proper icons/units, and all entities link to a central device for clutter-free organization.

---

## 🚀 Installation (HACS)

The easiest way to install is via the [Home Assistant Community Store (HACS)](https://hacs.xyz/).

1. Open HACS and go to **Integrations**.
2. Click the 3 dots in the top right corner and select **Custom repositories**.
3. Add this repository's URL: `https://github.com/Zara-Toorox/ESC-Easy-Sensor-Creation`
4. Select the category **Integration**.
5. Search for **"ESC Easy Sensor Creation"** and click "Install".
6. Restart Home Assistant when prompted.

**Requirements:** Recorder integration must be enabled (default in HA).

---

## 🛠️ How-To: Creating Your Sensors

After installation, find ESC here: **Settings > Devices & Services > Add Integration > ESC Easy Sensor Creation**. Follow the wizard – it's self-explanatory with tooltips!

### Example 1: Create a kWh sensor for the Energy Dashboard

Turn a smart plug's power (W) into energy tracking (kWh):

1. Start ESC and select "**kWh Sensor**".
2. Pick your power sensor as "Source Sensor (W)".
3. Name it (e.g., "Washing Machine kWh").
4. Submit – it's now a native helper under **Settings > Devices & Services > Helpers**. Add to Energy Dashboard!

### Example 2: Sum multiple lamps' power

1. Select "**Sum**".
2. Choose multiple sensors (e.g., three lamps).
3. Optionally classify as "Power" for Watt icon.
4. Name it "Room Total Power".
5. Done – real-time total in W!

### Example 3: Average temperature today

1. Select "**History Statistics**".
2. Pick a single temp sensor.
3. Choose "**Average - Today**".
4. Name it "Daily Avg Temp".
5. It polls Recorder data – value updates every minute.

### Example 4: Battery charge filter for solar

1. Select "**Battery Charge/Discharge**".
2. Choose "Positive Values (Charge, e.g., PV/Solar)".
3. Pick your inverter's power sensor.
4. It creates a filtered W sensor + kWh helper – perfect for Energy Dashboard (ignores negatives).

### Example 5: Overheat binary alarm

1. Select "**Binary Threshold**".
2. Pick a temp sensor and set threshold (e.g., 25°C).
3. Choose "On if > Threshold".
4. Classify as "Heat" for icon.
5. Name it "Overheat Alert" – use in automations for notifications!

---

## 📝 Changelog

### v5.1.0-rc6 (October 17, 2025)
- **Added:** Delta Sensor – Compares historical means (e.g., today vs. yesterday) with dynamic periods (hourly/daily stats) and graceful handling for missing data (shows "waiting for history" instead of 0).
- **Added:** Battery Charge/Discharge Sensor – Filters power values (positive for charge, absolute negatives for discharge), creates a dedicated W sensor + Riemann kWh helper for seamless Energy Dashboard use.
- **Added:** Binary Threshold Sensor – Event-driven on/off binary sensor for thresholds (e.g., alarm if temp > 25°C), with device class support for icons/alerts.
- **Added:** Toggle Switch – Virtual switch to pause/reset linked sensors, with optimistic updates and attribute syncing.
- **Fixed:** Unit loss in sensors – Added caching, source-based updates, and suggested units from device class (e.g., "°C" for temperature) for persistent display in UI/charts.
- **Fixed:** Delta sensor always showing 0 – Improved stats fetching with long-term fallback, debug logs, and None-state for no-data scenarios.
- **Fixed:** NameError in Battery flow – Imported missing constants (e.g., DEVICE_CLASS_POWER) and robustified config handling.
- **Improved:** Multilingual support – Full de.json and en.json for wizard steps, with consistent descriptions.
- **Improved:** Error resilience – More logs, extra attributes for status (e.g., "data_status: waiting_for_history"), and validation in flows.

### Previous Versions
- **v5.0.x:** Initial sum, stats, and kWh helpers with central device grouping.

---

Enjoy the integration! If you run into any problems or have feature requests, feel free to [open an Issue on GitHub](https://github.com/Zara-Toorox/ESC-Easy-Sensor-Creation/issues).

**Version:** 5.1.0-rc6  
**HACS:** Search "ESC Easy Sensor Creation"  
**Docs & Screenshots:** More coming soon – stay tuned!
