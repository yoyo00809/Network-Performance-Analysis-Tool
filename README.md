Network Performance Analysis Tool (NPAT)

A Python-based Network Performance Analysis Tool (NPAT) for monitoring, measuring, analyzing, and reporting network performance using practical network diagnostic techniques.

Current status: Core functionality is implemented and verified with 86 automated tests passing. The project is currently being enhanced for final academic submission.

1. Project Overview

NPAT provides a centralized application for network performance analysis and diagnostics.

The current system supports:

Ping-based network testing

Latency, jitter, and packet-loss analysis

Performance classification

Network health scoring

Automated recommendations

Anomaly detection

Network failure and recovery detection

Active monitoring

Download and upload bandwidth measurement

Local network device scanning

Traceroute

SQLite test-history storage

Historical trend analysis

Graphical visualization

TXT and CSV reports

Automated testing

Academic project: BCA 5th Semester Minor Project
Primary language: Python

2. Objectives

Measure network latency using ping requests.

Calculate average, minimum, and maximum latency.

Calculate network jitter.

Measure packet loss.

Analyze network performance using configurable thresholds.

Calculate an overall network health score.

Generate recommendations from measured network conditions.

Detect unusual network-performance conditions.

Detect network failures and recoveries.

Measure download and upload bandwidth.

Scan the local network for active devices.

Store network-test results in SQLite.

Analyze historical network-performance data.

Generate TXT and CSV reports.

Provide a graphical dashboard.

Maintain automated tests for core functionality.

3. Current Features

Network Performance Testing

Ping hostname or IP address

Response-time collection

Average, minimum, and maximum latency

Jitter calculation

Packet-loss measurement

Performance Analysis

NPAT analyzes:

Latency

Jitter

Packet loss

Overall network status

Metric conditions are evaluated using configurable thresholds.

Network Health Score

The health score combines:

Latency

Jitter

Packet loss

The current weighting is:

Metric

Weight

Latency

40%

Jitter

30%

Packet Loss

30%

Health-score classifications currently include:

Excellent

Good

Fair

Poor

Automated Recommendations

NPAT generates recommendations based on detected network-performance conditions.

Anomaly Detection

The system can identify conditions such as:

Latency spikes

High jitter

Significant packet loss

Abnormal performance patterns

Anomalies can be classified by severity.

Failure and Recovery Detection

The monitoring system tracks availability transitions:

Available -> Unavailable
Unavailable -> Available

Failure and recovery events are stored with monitoring history.

Bandwidth Measurement

NPAT measures:

Download speed

Upload speed

Example output:

Download Speed : 32.71 Mbps
Upload Speed   : 13.23 Mbps

Bandwidth values can also be saved with network-test results and used in historical analysis.

Network Scanner

The scanner:

Detects the local network.

Identifies the local subnet.

Checks network hosts.

Uses concurrent scanning for faster discovery.

Returns active IP addresses.

Example:

192.168.0.1
192.168.0.105

Traceroute

NPAT includes traceroute functionality for examining the network path between the local system and a target host.

SQLite Database and History

Network-test results are stored in SQLite.

The stored information can include:

Host

Packets sent

Packets received

Packet loss

Average latency

Jitter

Health score

Network state

Failure/recovery information

Download speed

Upload speed

Test history

Historical Trend Analysis

Historical data can be analyzed for:

Latency

Jitter

Packet loss

Health score

Download speed

Upload speed

Availability

Failure events

Recovery events

Graphical Dashboard

The Tkinter dashboard provides:

Target host input

Network testing

Performance metrics

Health score

Bandwidth results

Recommendations

Anomaly information

Network scanner

Test history

Historical trend charts

TXT/CSV report generation

The dashboard uses a scrollable layout so the monitoring interface can be accessed within the application window.

4. System Architecture

                         +----------------------+
                         |     NPAT Dashboard   |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Network Monitoring   |
                         |      Pipeline        |
                         +----------+-----------+
                                    |
             +----------------------+----------------------+
             |                      |                      |
             v                      v                      v
       +-----------+          +-----------+          +-----------+
       |   Ping    |          | Bandwidth |          |  Scanner  |
       +-----+-----+          +-----------+          +-----------+
             |
             v
       +-----------+
       |  Metrics  |
       +-----+-----+
             |
             v
       +----------------+
       |   Analyzer     |
       +--------+-------+
                |
       +--------+---------+----------------+
       |                  |                |
       v                  v                v
 +-----------+     +-------------+  +-------------+
 | Health    |     |  Anomaly    |  |Recommendations|
 |   Score   |     |  Detection  |  +-------------+
 +-----------+     +-------------+
                |
                v
       +----------------------+
       | SQLite Test History  |
       +----------+-----------+
                  |
                  v
       +----------------------+
       | Historical Analysis  |
       +----------+-----------+
                  |
             +----+----+
             |         |
             v         v
        Dashboard   TXT / CSV
         Charts      Reports

5. Project Structure

Network-Performance-Analysis-Tool/
|
+-- app/
|   +-- analysis/
|   |   +-- analyzer.py
|   |   +-- metrics.py
|   |   +-- recommendations.py
|   |   +-- trend_analysis.py
|   |
|   +-- config/
|   |   +-- settings.py
|   |
|   +-- database/
|   |   +-- database.py
|   |
|   +-- gui/
|   |   +-- dashboard.py
|   |
|   +-- monitoring/
|   |   +-- monitor.py
|   |
|   +-- network/
|   |   +-- bandwidth.py
|   |   +-- packet_loss.py
|   |   +-- ping.py
|   |   +-- scanner.py
|   |   +-- traceroute.py
|   |
|   +-- reports/
|   |   +-- export.py
|   |   +-- report_generator.py
|   |
|   +-- main.py
|
+-- tests/
|   +-- test_database.py
|   +-- test_monitoring.py
|   +-- test_network.py
|   +-- test_trend_analysis.py
|   +-- test_trend_database.py
|
+-- data/
|   +-- reports/
|
+-- requirements.txt
+-- README.md
+-- .gitignore

6. Technology Stack

Technology

Purpose

Python

Core programming language

Tkinter

Desktop graphical interface

SQLite

Local test-history database

Flask-SQLAlchemy

Database/application support

NumPy

Numerical processing

Pandas

Data processing

Matplotlib

Charts and visualization

psutil

System/network utilities

Pytest

Automated testing

Git

Version control

GitHub

Source-code hosting

7. Installation

Clone the repository

git clone https://github.com/yoyo00809/Network-Performance-Analysis-Tool.git

Enter the project directory

cd Network-Performance-Analysis-Tool

Create a virtual environment

python -m venv .venv

Activate the virtual environment

.\.venv\Scripts\Activate.ps1

Upgrade pip

python -m pip install --upgrade pip

Install dependencies

python -m pip install -r requirements.txt

8. Verify the Environment

Check Python:

python --version

Check pip:

python -m pip --version

List installed packages:

python -m pip list

Check Pytest:

pytest --version

9. Run NPAT

Command-line application

From the project root:

python -m app.main

Example:

Enter IP address or hostname: google.com

GUI dashboard

python -m app.gui.dashboard

10. Testing

NPAT uses Pytest for automated testing.

Run all tests

pytest -q

or:

pytest -v

Current verified result

86 passed

The current full test suite contains 86 passing tests.

Run a specific test file

pytest tests/test_network.py -v

pytest tests/test_monitoring.py -v

pytest tests/test_database.py -v

pytest tests/test_trend_analysis.py -v

Run a specific test

Example:

pytest tests/test_network.py::test_scan_network_with_mocked_devices -v

Stop at the first failure

pytest -x -v

11. Reports

Generated reports are stored in:

data/reports/

Current report formats:

network_report.txt
network_report.csv

Reports can contain:

Host

Packets sent and received

Packet loss

Latency

Jitter

Performance status

Download speed

Upload speed

Analysis information

PDF report

A professional PDF report is a planned enhancement for the next development stage. It is not listed as a completed feature.

12. Git and GitHub Commands

Check repository status:

git status

Show short status:

git status --short

Show changes:

git diff

Show README changes only:

git diff -- README.md

Show changed-file statistics:

git diff --stat

View recent commits:

git log --oneline -5

View the latest commit:

git log -1 --oneline

Pull the latest changes:

git pull origin main

Stage a file:

git add README.md

Commit:

git commit -m "Update README"

Push to GitHub:

git push origin main

13. Recommended Development Workflow

Make a change
     |
     v
Run focused tests
     |
     v
Run the complete test suite
     |
     v
Verify the application/dashboard
     |
     v
Check git status
     |
     v
Review git diff
     |
     v
Commit
     |
     v
Push to GitHub

Example:

pytest -q
git status
git diff --stat
git add <files>
git commit -m "Describe the change"
git push origin main

14. Git-Ignored Local Data

The project excludes local/generated data such as:

.venv/
instance/
*.db
__pycache__/
.pytest_cache/
data/reports/*.csv
data/reports/*.txt

This keeps local environments, databases, caches, and generated reports out of source control.

15. Example NPAT Workflow

Launch NPAT
    |
    v
Enter Target Host
    |
    v
Run Network Test
    |
    v
Collect Ping Data
    |
    v
Calculate Latency / Jitter / Packet Loss
    |
    v
Measure Bandwidth
    |
    v
Calculate Network Health Score
    |
    v
Analyze Performance
    |
    v
Detect Anomalies
    |
    v
Generate Recommendations
    |
    v
Save Result to SQLite
    |
    v
Update Historical Data
    |
    v
Display Charts
    |
    v
Generate TXT / CSV Report

16. Current Development Status

Completed

Project structure and configuration

Ping module

Latency analysis

Jitter calculation

Packet-loss measurement

Performance analyzer

Recommendation engine

Network health score

Anomaly detection

Failure detection

Recovery detection

Active monitoring

Network scanner

Traceroute

Download bandwidth measurement

Upload bandwidth measurement

SQLite database

Test history

Historical trend analysis

Historical bandwidth analysis

Tkinter GUI dashboard

Scrollable dashboard

Network scanner dashboard integration

Performance charts

TXT report generation

CSV report export

Automated test suite

Git/GitHub integration

Next Planned Enhancement

Professional PDF report generation

Printable historical report

Additional report presentation improvements

Final academic documentation

Final presentation and viva preparation

17. Future Scope

Possible future enhancements include:

Scheduled network monitoring

Multi-device monitoring

More detailed network diagnostics

Additional network protocols

Advanced bandwidth testing

Web-based dashboard

Remote monitoring

Additional visualization options

More configurable monitoring parameters

Extended reporting capabilities

18. Academic Information

Project: Network Performance Analysis Tool (NPAT)

Academic Level: BCA 5th Semester Minor Project

Primary Language: Python

Project Type: Network Monitoring and Performance Analysis

Repository:
https://github.com/yoyo00809/Network-Performance-Analysis-Tool

19. Project Status

The core NPAT system is functional and currently verified with:

86 passed

The project is continuing through the enhancement, documentation, and final academic-submission stages.



From your main project folder:
to run main app
python -m app.gui.dashboard
