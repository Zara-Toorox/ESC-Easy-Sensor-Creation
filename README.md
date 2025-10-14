cat > README.md << 'EOF'
# ESC Easy Sensor Creation

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/DEIN_USERNAME/esc_easy_sensor_creation.svg)](https://github.com/DEIN_USERNAME/esc_easy_sensor_creation/releases)

Eine leistungsstarke Home Assistant Integration zum einfachen Erstellen von benutzerdefinierten Sensoren.

## ✨ Features

### 🔋 kWh Integration Sensor
- Integriert Leistung (W) zu Energie (kWh)
- **Linksseitige Integration** für präzise Berechnungen
- Perfekt für's Energie-Dashboard
- State Restore nach Neustart

### ➕ Summen-Sensor
- Addiert mehrere Sensoren
- Automatische Unit-Erkennung
- Unterstützt beliebige Sensor-Typen

### 📊 SQL Statistik-Sensoren (14 Typen!)

**Energie:**
- Heute (kWh)
- Aktueller Monat (kWh)
- Aktuelles Jahr (kWh)
- Vormonat (kWh)
- Vorjahr (kWh)

**Durchschnitt:**
- Heute
- Aktueller Monat
- Aktuelles Jahr

**Maximum:**
- Heute
- Aktueller Monat
- Aktuelles Jahr

**Minimum:**
- Heute
- Aktueller Monat
- Aktuelles Jahr

### 🗄️ Datenbank-Support
- ✅ Home Assistant SQLite Datenbank
- ✅ MariaDB via Netzwerk
- ✅ Automatischer Fallback zu `states` Tabelle wenn `statistics` leer sind

## 📦 Installation

### HACS (empfohlen)

1. Öffne HACS
2. Gehe zu "Integrationen"
3. Klicke auf die 3 Punkte oben rechts
4. Wähle "Benutzerdefinierte Repositories"
5. Füge hinzu: `https://github.com/DEIN_USERNAME/esc_easy_sensor_creation`
6. Kategorie: "Integration"
7. Installiere "ESC Easy Sensor Creation"
8. Starte Home Assistant neu

### Manuell

1. Kopiere den `custom_components/esc_easy_sensor_creation` Ordner in dein `config/custom_components` Verzeichnis
2. Starte Home Assistant neu
3. Gehe zu Einstellungen → Geräte & Dienste
4. Klicke auf "+ Integration hinzufügen"
5. Suche nach "ESC Easy Sensor Creation"

## 🚀 Verwendung

### kWh Integration Sensor erstellen

1. Gehe zu Einstellungen → Geräte & Dienste → Integration hinzufügen
2. Suche nach "ESC Easy Sensor Creation"
3. Wähle "kWh Integration"
4. Wähle einen oder mehrere **Leistungs-Sensoren (W)**
5. Benenne deinen Sensor
6. Fertig! Der Sensor berechnet nun kontinuierlich die Energie

**Beispiel:** 3 Steckdosen mit je 100W → kWh Sensor zeigt den Gesamtverbrauch

### SQL Statistik-Sensor erstellen

1. Wähle "SQL Statistik-Sensor"
2. Wähle den Typ (z.B. "Durchschnitt - Heute")
3. Wähle die Datenbank:
   - Home Assistant Datenbank (SQLite) - meist die richtige Wahl
   - MariaDB - für fortgeschrittene Nutzer
4. Wähle den Basis-Sensor
5. Benenne deinen Sensor
6. Fertig!

**Beispiel:** Durchschnitts-Temperatur des heutigen Tages aus einem Temperatursensor

## ⚙️ MariaDB Konfiguration

Für MariaDB Add-on Nutzer:
- **Host:** `core-mariadb`
- **Port:** `3306`
- **User:** `homeassistant`
- **Database:** `homeassistant`
- **Password:** Dein MariaDB Passwort

## 🔧 Technische Details

### Linksseitige Integration
Der kWh Sensor verwendet **linksseitige Integration** für die Energie-Berechnung:
Das bedeutet: Bei jeder Änderung wird der **vorherige** Leistungswert verwendet, nicht der Durchschnitt.

### SQL Fallback
Wenn die `statistics` Tabelle keine Daten hat (z.B. bei Sensoren ohne Langzeit-Statistiken), 
wird automatisch auf die `states` Tabelle zurückgegriffen und die Werte live berechnet.

## 🐛 Fehlerbehebung

### SQL Sensor zeigt 0 an
- Prüfe ob der Sensor Langzeit-Statistiken hat: Entwicklerwerkzeuge → Statistiken
- Kein Problem! Der Sensor nutzt automatisch die `states` Tabelle als Fallback

### kWh Sensor zählt nicht
- Prüfe ob die Quell-Sensoren **Watt (W)** ausgeben
- Prüfe ob die Sensoren regelmäßig Updates liefern

### Icon wird nicht angezeigt
- Browser-Cache leeren (Strg + F5)
- Home Assistant neu starten
- Nicht schlimm - funktioniert auch ohne Icon!

## 📝 Changelog

### Version 0.2.2
- SQL Fallback zu states Tabelle
- Verbesserte MariaDB Unterstützung
- Menü-basierte Config Flow

### Version 0.1.0
- Erste Version
- kWh Integration, Summen-Sensor, SQL Statistiken

## 🤝 Beitragen

Contributions sind willkommen! Bitte erstelle einen Pull Request oder Issue auf GitHub.

## 📄 Lizenz

MIT License

## 👏 Credits

Entwickelt für die Home Assistant Community
