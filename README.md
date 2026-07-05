# 📡 Radar Detection System Simulation

A 2D simulation of a **pulse-based radar system** that detects aerial objects such as UAVs, visually demonstrates the transmission and return of radar pulses, and computes the **shortest path between the radar and a detected object** using **Dijkstra's Algorithm**.

![Language](https://img.shields.io/badge/language-Python-yellow)
![Library](https://img.shields.io/badge/visualization-Matplotlib-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## ✨ Features

- 📶 **Gaussian-Modulated Radar Pulse Simulation** — models realistic outgoing radar pulses
- 🎞️ **Animated 2D Visualization** — shows outgoing and returning pulses in real time
- ✈️ **Aerial Object Detection** — simulates detection of objects (e.g. UAVs) within the environment
- 🧭 **Dijkstra's Algorithm** — computes the shortest path between the radar and a detected object
- 🗺️ **Path Visualization** — renders the computed shortest path directly on the simulation

---

## 🧠 How It Works

1. **Pulse Generation** — the radar emits a Gaussian-modulated pulse into the simulated 2D environment.
2. **Propagation & Detection** — the pulse travels outward; when it reaches an object (e.g. a UAV), a return signal is triggered.
3. **Animation** — both outgoing and returning pulses are animated frame-by-frame with Matplotlib, mimicking real radar pulse-echo behavior.
4. **Shortest Path Computation** — once an object is detected, Dijkstra's Algorithm calculates the shortest path from the radar to that object.
5. **Path Rendering** — the computed shortest path is drawn on the same 2D plot for visual confirmation.

---

## 🛠️ Tech Stack

- **Python** — core simulation logic and orchestration
- **Matplotlib** — 2D animation and real-time visualization
- **NumPy** *(likely used)* — numerical computation for pulse/signal modeling

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install matplotlib numpy
```
## 📌 Concepts Demonstrated

- Radar pulse-echo principles
- Signal propagation & animation modeling
- Graph-based shortest path algorithms (Dijkstra's)
- Real-time simulation using Matplotlib

---

## ⭐ Support

If you found this project useful, consider giving it a star!
