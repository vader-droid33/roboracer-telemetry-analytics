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