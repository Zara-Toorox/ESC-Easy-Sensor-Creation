# ESC Easy Sensor Creation

### _Escape the Madness of YAML_

![Logo](https://raw.githubusercontent.com/Zara-Toorox/ESC-Easy-Sensor-Creation/main/logo.png)

**Create powerful sensors in Home Assistant – without a single line of code.**

This integration is your shortcut to useful and intelligent sensors. If you're new to Home Assistant and don't want to write complex YAML files or templates, ESC is the perfect tool for you.

---

## ✨ What can this integration do for you?

ESC provides a simple, guided menu interface for tasks that would otherwise require deep technical knowledge.

* **Create kWh Energy Sensors:** Automatically convert your device's power consumption (in Watts) into energy (in kWh). Perfect for Home Assistant's official **Energy Dashboard**.
* **Create Sum Sensors:** Sum the values of multiple sensors. Ideal for determining the total consumption of all lights in a room.
* **Create History Statistics Sensors:** Easily find the **highest, lowest, or average value** of a sensor for today, this month, or the entire year.
* **Sensor Classification:** Assign a class to your sensors (e.g., Energy, Power, Temperature) to help Home Assistant display the correct icon and format.
* **Clean Organization:** All created sensors are neatly grouped under a single device in your device list.

---

## 🚀 Installation (HACS)

The easiest way to install is via the [Home Assistant Community Store (HACS)](https://hacs.xyz/).

1.  Open HACS and go to **Integrations**.
2.  Click the 3 dots in the top right corner and select **Custom repositories**.
3.  Add this repository's URL: `https://github.com/Zara-Toorox/ESC-Easy-Sensor-Creation`
4.  Select the category **Integration**.
5.  Search for **"ESC Easy Sensor Creation"** and click "Install".
6.  Restart Home Assistant when prompted.

---

## 🛠️ How-To: Creating Your Sensors

After installation, you can find ESC here: **Settings > Devices & Services > Add Integration > ESC Easy Sensor Creation**.

### Example 1: Create a kWh sensor for the Energy Dashboard

Do you have a smart plug that shows the current power consumption in Watts? Here's how to turn it into a counter for the Energy Dashboard:

1.  Start the ESC configuration.
2.  Select "**kWh Sensor (creates Riemann Sensor for Energy Dashboard)**".
3.  For "Source Sensor (W)", select your smart plug.
4.  Give the new sensor a name, e.g., "Washing Machine Consumption kWh".
5.  Click "Submit".
6.  **IMPORTANT:** This sensor is a native Home Assistant helper. You can now find it under **Settings > Devices & Services > Helpers**.

### Example 2: Calculate the total consumption of three lamps

1.  Start the ESC configuration.
2.  Select "**Sum (add multiple sensors)**".
3.  For "Which sensors do you want to add?", select all the lamps you want to sum up.
4.  Follow the next steps to give the sensor a name.
5.  **Done!** You now have a new sensor that will always show you the total consumption.

### Example 3: Determine the average temperature for today

1.  Start the ESC configuration.
2.  Select "**History Statistics (Average, MIN, MAX)**".
3.  Choose your temperature sensor as the base sensor.
4.  In the next step, select the statistic type, e.g., "**Average - Today**".
5.  Give the sensor a name and finish the configuration.
6.  **Done!** Your new sensor will now display the average temperature for the current day.

---

Enjoy the integration! If you run into any problems or have feature requests, feel free to [open an Issue on GitHub](https://github.com/Zara-Toorox/ESC-Easy-Sensor-Creation/issues).
