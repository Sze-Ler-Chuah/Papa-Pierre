# 🗺️ Papa Pierre's Pâtisseries Global Route Planner

A Python-based routing engine built for **Papa Pierre’s Pâtisseries**, a fictional global dessert delivery company. The system determines the **most efficient delivery path** between cities using a fleet of specialized vehicles with unique travel constraints.

This project demonstrates graph algorithms, geographical constraints, and path optimization in a playful, narrative-driven simulation.

---

## 🍩 Project Background

**Papa Pierre’s Pâtisseries** delivers French desserts to nearly **1,000 global cities**. Each type of delivery vehicle has different strengths and movement rules, and your job is to design an algorithm that helps these vehicles travel optimally across the globe.

---

## 🚚 Vehicle Types & Rules

### 🛩 CrappyCrepeCar
- Can fly between **any two cities**, globally.
- **Slowest** mode of transport — used as a last resort.

### 🛥 DiplomacyDonutDinghy
- A diplomatic boat that:
  - Travels **very fast** between **capital cities** via hyperlanes.
  - Can travel freely between **any two cities within the same country**.
  - Can cross countries **only through their capital cities**.

### 🚌 TeleportingTarteTrolley
- Can **teleport** between any two cities **within a short range**.
- Teleportation takes time to program, so it’s not always the fastest.
- Ignores country borders.

---

## Features

- Dynamic shortest path routing based on available vehicles
- Enforced geographical and political constraints for travel
- Modular graph-based representation of cities, countries, and routes
- Custom weighting system for different vehicle costs
- Visualizable trip logs (e.g., Paris ➝ Kuala Lumpur ➝ Melbourne)

---

## Concepts Demonstrated

- Graph Theory & Pathfinding
- Real-World Simulation Modeling
- Object-Oriented Programming in Python
