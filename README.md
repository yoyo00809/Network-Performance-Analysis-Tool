# Network Performance Analysis Tool (NPAT)

A Python-based Network Performance Analysis Tool designed to monitor, measure, analyze, and report network performance using practical network diagnostic techniques.

NPAT collects network performance data, calculates important metrics such as latency, jitter, and packet loss, analyzes the results using configurable thresholds, generates recommendations, stores test history in SQLite, and provides a graphical dashboard for visualization.

---

## 📌 Project Overview

Network performance directly affects the reliability and quality of applications and services that depend on computer networks.

The **Network Performance Analysis Tool (NPAT)** provides a centralized application for performing basic network performance analysis.

The system combines:

- Network data collection
- Performance metric calculation
- Performance classification
- Automated recommendations
- Network monitoring
- Database storage
- Report generation
- Graphical visualization
- Automated software testing

The project is being developed as a **BCA 5th Semester Minor Project**.

---

## 🎯 Objectives

The main objectives of NPAT are:

1. Measure network latency using ping requests.
2. Calculate average, minimum, and maximum latency.
3. Calculate network jitter.
4. Measure packet loss.
5. Analyze network performance using configurable thresholds.
6. Generate recommendations based on detected network conditions.
7. Store network test results in a SQLite database.
8. Generate text and CSV reports.
9. Visualize ping response times through a graphical dashboard.
10. Provide additional network diagnostic capabilities such as scanning, traceroute, and bandwidth measurement.
11. Maintain automated tests for the application's core functionality.

---

## ✨ Features

### Network Monitoring

- Ping-based network testing
- Packet loss measurement
- Network device scanning
- Traceroute
- Download bandwidth measurement
- Upload bandwidth measurement

### Performance Analysis

NPAT currently analyzes:

- **Latency**
- **Jitter**
- **Packet Loss**
- **Overall Network Status**

Each metric is classified using configurable thresholds.

Possible classifications include:

```text
Good
Average
Poor
Unavailable


system Architecture
                         ┌─────────────────────┐
                         │      NPAT GUI       │
                         │     Dashboard       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Network Monitoring  │
                         │     Pipeline        │
                         └──────────┬──────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │     Ping     │    │   Scanner    │    │  Traceroute  │
        └──────┬───────┘    └──────────────┘    └──────────────┘
               │
               ▼
        ┌──────────────┐
        │    Metrics   │
        │  Calculation │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │  Performance │
        │   Analyzer   │
        └──────┬───────┘
               │
        ┌──────┴───────────────┐
        │                      │
        ▼                      ▼
┌──────────────┐       ┌──────────────┐
│Recommendations│       │   Database   │
└──────────────┘       └──────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │   Reports    │
                       │ TXT / CSV    │
                       └──────────────┘


⚙️ Installation
1. Clone the repository
git clone https://github.com/yoyo00809/Network-Performance-Analysis-Tool.git
2. Open the project
cd Network-Performance-Analysis-Tool
3. Create a virtual environment

Windows PowerShell:

python -m venv .venv
4. Activate the virtual environment
.\.venv\Scripts\Activate.ps1
5. Install dependencies
python -m pip install -r requirements.txt
▶️ Running the Command-Line Application

From the project root:

python -m app.main

The application will ask for a hostname or IP address.

Example:

Enter IP address or hostname: google.com

The application then performs the complete monitoring pipeline and generates reports.

🖥️ Running the GUI Dashboard

Run:

python -m app.gui.dashboard

The dashboard provides:

Target host input
Network testing
Latency
Jitter
Packet loss
Overall status
Performance analysis
Recommendations
Ping response-time graph
🧪 Testing

NPAT uses Pytest for automated testing.

Run all tests:

pytest -v

Current test status:

34 passed

The test suite covers:

Metric calculations
Performance analysis
Recommendations
Database operations
Monitoring
Network scanning
Traceroute parsing
Packet loss
Bandwidth calculations
Report generation
CSV export
Ping functionality
📄 Report Generation

NPAT generates reports inside:

data/reports/

Available report formats:

network_report.txt
network_report.csv

Generated reports contain the measured network performance data and analysis results.

🔐 Project Data and Git

The following local files are intentionally excluded from Git:

.venv/
instance/
*.db
__pycache__/
.pytest_cache/
data/reports/*.csv
data/reports/*.txt

This prevents local environments, databases, caches, and generated reports from being committed to the repository.

🚧 Current Development Status
Completed
 Project structure
 Configuration module
 Ping module
 Network metrics
 Performance analyzer
 Recommendation engine
 Network scanner
 Traceroute
 Packet loss measurement
 Bandwidth measurement
 SQLite database
 Network monitoring pipeline
 Text report generation
 CSV report export
 Tkinter GUI
 Ping response-time graph
 Automated test suite
 Git/GitHub integration
Planned
 Test history dashboard
 Network scanner GUI
 Traceroute GUI
 Bandwidth test interface
 Report download/export controls
 Improved dashboard styling
 Real-time monitoring
 Additional visualizations
 Extended network analysis
🔮 Future Scope

Future versions of NPAT may include:

Real-time network monitoring
Historical performance graphs
Advanced network diagnostics
More detailed bandwidth testing
Network anomaly detection
Configurable performance thresholds
Scheduled monitoring
Advanced reporting
Web-based dashboard
Multi-device monitoring
Additional network protocols and diagnostics
👨‍💻 Project

Project: Network Performance Analysis Tool (NPAT)

Academic Level: BCA 5th Semester Minor Project

Primary Language: Python

Repository:
https://github.com/yoyo00809/Network-Performance-Analysis-Tool

📜 License

This project is currently developed for academic and educational purposes.


### Step 2 — Save it

Press:

```text
Ctrl + S
Step 3 — Check it locally

You don't need to run the application yet.

In the terminal run:

git status

You should see:

modified: README.md