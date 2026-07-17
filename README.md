# IoT Smart Farm Monitoring and Actuation System

## Overview

This project implements an IoT-based Smart Farm system for real-time environmental monitoring and remote actuator control.

The system uses an ESP8266 microcontroller to collect environmental measurements from multiple sensors, communicates using MQTT through a Mosquitto broker, stores data in a SQLite database, provides a web dashboard for visualization, and enables remote actuator control.

The system also integrates Telegram notifications to alert the user when monitored parameters exceed predefined thresholds.

---

# System Demonstration

## Web Dashboard

The dashboard provides real-time visualization of sensor measurements, including temperature, humidity, soil moisture, and light intensity.

It displays:
- Real-time KPI values
- Historical sensor charts
- Alert notifications
- Relay actuator control

![Smart Farm Dashboard](images/dashboard.png)


## Hardware Setup

The hardware prototype consists of an ESP8266 NodeMCU connected to environmental sensors and a relay actuator.

Components:

- ESP8266 NodeMCU
- DHT11 temperature and humidity sensor
- Soil moisture sensor
- LDR light sensor
- Relay module for actuator control

![Hardware Setup](images/hardware_setup.jpg)

---

# System Architecture

```
Sensors
   |
   |
ESP8266 NodeMCU
   |
   |
MQTT Communication
   |
   |
Mosquitto Broker
   |
   |
Python Backend
   |
   |
SQLite Database
   |
   |
Flask REST API
   |
   |
Web Dashboard
```

---

# Monitoring Flow

The monitoring process follows these steps:

1. The ESP8266 reads sensor measurements every 10 seconds:

   - Temperature and humidity using DHT11
   - Soil moisture using analog input
   - Light intensity using LDR sensor

2. The ESP8266 connects to the local Mosquitto MQTT broker and publishes each measurement to its corresponding MQTT topic.

3. The Python subscriber (`subscriber.py`) receives MQTT messages and:

   - Stores sensor measurements in the SQLite database
   - Processes incoming values
   - Checks measurements against predefined thresholds
   - Sends Telegram alerts when abnormal conditions are detected

4. The Flask application (`app.py`) provides REST API endpoints:

```
GET /api/latest
```

Returns the latest sensor measurements.

```
GET /api/history
```

Returns historical sensor data for visualization.

5. The dashboard (`dashboard.html`):

- Requests new measurements every 5 seconds
- Updates KPI cards
- Updates charts
- Displays alerts

When the dashboard loads, it retrieves the last 60 measurements using `/api/history` to initialize the historical graphs.

---

# Actuation Flow

The system supports remote actuator control through the dashboard.

The sequence is:

1. The user presses the relay control button on the dashboard.

2. The dashboard sends a POST request:

```
POST /api/relay
```

to the Flask backend.

3. Flask publishes an MQTT command:

Topic:

```
farm/relay/command
```

Messages:

```
ON
OFF
```

4. The ESP8266 receives the command and changes the relay state.

5. The ESP8266 publishes the relay confirmation:

Topic:

```
farm/relay/status
```

---

# MQTT Topics

## Sensor Topics

| Sensor | MQTT Topic |
|---|---|
| Temperature | `farm/temperature` |
| Humidity | `farm/humidity` |
| Soil Moisture | `farm/soil` |
| Light Intensity | `farm/light` |


## Relay Topics

| Function | MQTT Topic |
|---|---|
| Relay Command | `farm/relay/command` |
| Relay Status | `farm/relay/status` |

---

# Features

## Monitoring

- Real-time environmental monitoring
- Temperature measurement
- Humidity measurement
- Soil moisture monitoring
- Light intensity monitoring

## Data Management

- MQTT-based communication
- SQLite data storage
- Historical data retrieval
- REST API interface

## Alert System

- Threshold-based monitoring
- Automatic Telegram notifications

## Remote Actuation

- Dashboard relay control
- MQTT command transmission
- Relay status feedback

---

# Technologies Used

## Hardware

- ESP8266 NodeMCU
- DHT11 sensor
- Soil moisture sensor
- LDR sensor
- Relay module


## Embedded Programming

- Arduino IDE
- C/C++


## Backend

- Python
- Flask
- SQLite
- Paho MQTT


## Frontend

- HTML
- CSS
- JavaScript
- Chart.js


## Communication

- MQTT
- REST API

---

# Project Structure

```
IOT_SmartFarm/

├── temperature.ino
│       ESP8266 firmware
│
├── subscriber.py
│       MQTT subscriber and database handler
│
├── app.py
│       Flask REST API server
│
├── create_db.py
│       Database initialization
│
├── seed_test_data.py
│       Test data generation
│
├── templates/
│       └── dashboard.html
│           Web dashboard interface
│
├── images/
│       ├── dashboard.png
│       └── hardware_setup.jpg
│
└── README.md
```

---

# Future Improvements

Possible extensions:

- Cloud MQTT deployment
- Mobile application
- Additional agricultural sensors
- Machine learning based prediction
- Automated irrigation control


