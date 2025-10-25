# 🌍 ICT Infrastructure Dashboard

## Project Overview

This project is a comprehensive ICT infrastructure monitoring system designed for international organizations with distributed offices worldwide. It monitors network devices across multiple countries, integrates external APIs for contextual data (weather, geolocation, time, news), provides **real-time SNMP device monitoring**, and delivers actionable analytics through a responsive web dashboard.

**Key Features:**
- RESTful API with 25+ endpoints
- Interactive map showing global office locations
- Real-time performance analytics and trending
- Alert management system
- SNMP protocol integration for real network device monitoring**
- External API integration (Weather, Geolocation, Time, News)
- Data visualization with charts and graphs
- Multi-region support (Africa, Asia-Pacific, Europe, Latin America)
- Live news ticker with latest technology updates

```
## Architecture
┌─────────────────┐
│  Web Dashboard  │ ← HTML5, Chart.js, Leaflet Maps
└────────┬────────┘
         │ HTTP/REST
┌────────▼────────┐
│   Flask API     │ ← Python, Flask, RESTful design
├─────────────────┤
│ • Office Routes │
│ • Device Routes │
│ • Analytics     │
│ • External APIs │
│ • SNMP Routes   │ ← Real device monitoring
└────────┬────────┘
         │
┌────────▼────────┐
│  Data Services  │
├─────────────────┤
│ • Weather API   │ ← OpenWeatherMap
│ • Geo API       │ ← ip-api, REST Countries
│ • Time API      │ ← World Time API
│ • News API      │ ← TheNewsAPI
│ • SNMP Service  │ ← PySNMP for device monitoring
│ • Analytics     │ ← Custom aggregation
└────────┬────────┘
         │
┌────────▼────────┐
│  Data Storage   │
│ • JSON Files    │
│ • File Cache    │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for external APIs)
- *Optional: Network devices with SNMP enabled for real monitoring*

### Installation

1. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment** (optional)
```bash
cp .env.example .env
# Edit .env with your API keys (optional - works with mock data)
```

Available API keys to configure:
- `OPENWEATHER_API_KEY` - For real weather data
- `NEWS_API_KEY` - For real news from TheNewsAPI

4. **Run the application**
```bash
python run.py
```

Access the dashboard at: **http://localhost:8000**

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints Overview

#### Offices
```http
GET    /offices                    # List all offices
GET    /offices/{id}               # Get office details
GET    /offices/{id}/devices       # Get office devices
```

#### Devices
```http
GET    /devices                    # List all devices
GET    /devices/{id}               # Get device details
GET    /devices/{id}/metrics       # Get performance metrics
```

#### Analytics
```http
GET    /analytics/summary          # Global statistics
GET    /analytics/alerts           # System alerts
GET    /analytics/trends           # Performance trends
GET    /analytics/device-distribution  # Device type stats
```

#### External APIs
```http
GET    /external/weather/{office_id}        # Office weather
GET    /external/time/{office_id}           # Office local time
GET    /external/news                       # Latest technology news
```

#### SNMP Monitoring (NEW)
```http
GET    /snmp/device/{host}/info             # Device information
GET    /snmp/device/{host}/cpu              # CPU usage (Cisco)
GET    /snmp/device/{host}/memory           # Memory usage (Cisco)
GET    /snmp/device/{host}/interface/{idx}  # Interface statistics
GET    /snmp/device/{host}/metrics          # All metrics combined
```

### SNMP Examples

**Query device information:**
```bash
curl "http://localhost:8000/api/v1/snmp/device/192.168.1.1/info?community=public"
```

**Get CPU usage:**
```bash
curl "http://localhost:8000/api/v1/snmp/device/192.168.1.1/cpu"
```

**Get all metrics:**
```bash
curl "http://localhost:8000/api/v1/snmp/device/192.168.1.1/metrics"
```

## 🔧 SNMP Configuration

### Requirements for Real Device Monitoring

1. **Enable SNMP on target devices**
   - Cisco: `snmp-server community public RO`
   - Linux: Install and configure `snmpd`

2. **Firewall configuration**
   - Allow UDP port 161

3. **Community string**
   - Default: `public` (read-only)

### Supported Devices

- **Cisco Routers/Switches** - Full support (CPU, memory, interfaces)
- **Generic SNMP devices** - Basic info and interface stats
- **Linux servers** - With net-snmp installed

### Testing Without Real Devices

If you don't have access to real network equipment:
- Use the **Demo Mode** button in the dashboard
- Try public SNMP test servers (if available)
- View simulated data in the dashboard


## Project Structure
```
undp-ict-dashboard/
├── api/
│   ├── app.py                 # Flask application
│   ├── routes/
│   │   ├── offices.py         # Office endpoints
│   │   ├── devices.py         # Device endpoints
│   │   ├── analytics.py       # Analytics endpoints
│   │   ├── external.py        # External API endpoints
│   │   └── snmp.py            # SNMP monitoring endpoints
│   ├── models/
│   │   ├── office.py          # Office data model
│   │   └── device.py          # Device data model
│   └── services/
│       ├── weather_service.py # Weather API integration
│       ├── geo_service.py     # Geolocation services
│       ├── time_service.py    # Time/timezone services
│       ├── news_service.py    # News API integration
│       ├── snmp_service.py    # SNMP protocol implementation
│       └── analytics_service.py # Analytics logic
├── data/
│   ├── cache/                 # API cache files
│   └── seed_data.json         # Initial data (5 offices, 20 devices)
├── templates/
│   └── dashboard.html         # Web dashboard with SNMP panel
├── run.py                     # Convenient startup script
├── config.py                  # Configuration
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```
