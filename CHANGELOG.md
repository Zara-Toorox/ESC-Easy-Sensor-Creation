# Changelog

## [5.1.0-rc6] - 2025-10-17
### Added
- Delta Sensor: Vergleicht historische Mittelwerte (z. B. heute vs. gestern) mit dynamischen Perioden (stündlich/täglich) und Behandlung fehlender Daten (Status "waiting for history").
- Battery Charge/Discharge Sensor: Filtert Power-Sensoren auf positive/absolute negative Werte, erstellt W-Sensor + Riemann-kWh-Helper für Energy Dashboard.
- Binary Threshold Sensor: Event-gesteuerter On/Off-Alarm bei Schwellenüberschreitung, mit Device-Class-Support.
- Toggle Switch: Virtueller Schalter zum Pausieren/Zurücksetzen von Sensoren, mit Attribut-Sync.

### Fixed
- Unit-Verlust: Persistent Caching aus Sources/Device-Class, für korrekte Anzeige in UI/Charts.
- Delta-Sensor zeigt immer 0: Long-Term-Fallback, Debug-Logs und None bei No-Data.
- Battery-Flow-NameError: Imports robustifiziert.
- Allgemein: Mehr Logs, Status-Attribute und Validierungen.

### Improved
- Multilingual: Vollständige de.json/en.json für Flows.
- Error-Resilienz: Graceful Fallbacks und Extra-Attrs.

## [5.1.0-rc5] - 2025-10-10
- Initialer Support für Sum- und Stats-Sensoren mit zentralem Device.
- kWh-Helper-Integration für Energy Dashboard.

## [5.0.x] - 2025-09
- Erste Version: Basis-Sum, History-Stats und Riemann-Helpers.