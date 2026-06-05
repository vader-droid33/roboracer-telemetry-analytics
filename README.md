# RoboRacer Telemetry Analytics Engine

A high-performance, lightweight analytical engine designed for autonomous 1:10 scale racecars (F1TENTH). This tool interfaces directly with native **ROS 2 bag serialization subsystems** (`rosbag2_py`) to unpack and parse high-frequency dataset parameters offline—**completely eliminating the need to spin up a live ROS 2 computational graph, simulator, or bag player.**

---

## 🏎️ Kinematics & Analytical Insights Extracted
Rather than simply playing logs back, this script treats datasets as raw databases to extract physical vehicle dynamics:
* **Asynchronous Velocity Profiling:** Reconstructs continuous velocity vectors from state telemetry.
* **Side-Slip Angle ($\beta$) Anomaly Detection:** Dynamically monitors the relationship between lateral ($v_y$) and longitudinal ($v_x$) velocities using:
$$\beta = \arctan2(v_y, v_x)$$
If the structural threshold slips beyond $\approx 23^\circ$ during high-velocity states, the engine automatically flags a dynamic instability event (drifting, spinout, or wall impact).

---

## 📦 Environment & Prerequisites
* **OS:** Ubuntu 24.04 LTS (WSL2 / Native)
* **Middleware:** ROS 2 (Jazzy / Rolling)
* **Python Storage Extensions:** `ros-jazzy-rosbag2-storage-mcap`
* **Dependencies:** Defined in `requirements.txt`

---

## 🛠️ Installation & Usage Guide

### 1. Set Up Storage Plugins
Ensure your Ubuntu layer possesses the necessary MCAP/SQLite unpacking dependencies:
```bash
sudo apt-get install ros-jazzy-rosbag2-storage-mcap
pip install -r requirements.txt --break-system-packages


---

## 📊 Sample Analytical Output

Executing the engine on a native F1TENTH experimental MCAP log (`layout_00_fast_run_01_mcap`) yields the following runtime report:

```text
--- Processing F1TENTH Dataset: /home/purujitv/f1tenth_ws/raw/layout_00_fast_run_01_mcap ---

[Parsing high-frequency data streams...]

================ RACE ENGINEER REPORT ================
Processed Message Count : 22656
Top Speed Clocked       : 3.00 m/s (10.8 km/h)
Lateral Slip Anomalies  : 0 events detected
Status Evaluation       : Clean run. Traction control optimal.
=======================================================