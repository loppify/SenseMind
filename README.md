# SenseMind — Intelligent Psycho-Emotional Monitoring System

**SenseMind** is an advanced software and analytics platform designed for objective real-time assessment of a person's psycho-emotional state. By leveraging physiological indicators (HRV and GSR) and Machine Learning, it provides actionable insights into stress and focus levels.

## Core Objective
To bridge the gap between subjective self-assessment and expensive medical diagnostics by providing an accessible, IoT-driven tool for continuous emotional feedback.

## Key Features
*   **Two-Factor AI Classification (MF-2):** Real-time classification into "Calm", "Concentrated", and "Stress" using Scikit-learn models (Random Forest).
*   **Proactive Alert System (MF-3):** Contextual recommendations triggered by physiological trends.
*   **Multi-User & Device Management:** Full authentication system and device registry, moving beyond the initial single-user MVP.
*   **Persistent Data Storage:** Integrated SQLite database (SQLAlchemy) for historical state records and recommendation logs.
*   **IoT Simulation:** A dedicated client module for streaming physiological data via REST API.

## Project Structure
*   `core_engine/` — Flask-based REST API with Auth, Admin, and Device routes.
*   `iot_device/` — Simulation client and configuration.
*   `services/` — Core logic for signal processing and ML inference.
*   `database/` — SQLAlchemy models and storage logic.

## Technology Stack
*   **Backend:** Python 3.x, Flask, SQLAlchemy.
*   **ML & Data:** Scikit-learn, Pandas, Neurokit2.
*   **Database:** SQLite.

## Getting Started
1. **Installation:**
   ```bash
   poetry install
   ```
2. **Server Setup:**
   ```bash
   python -m core_engine.app
   ```
3. **Client Simulation:**
   ```bash
   python -m iot_device.client
   ```
