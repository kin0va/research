# CO₂ Occupancy Estimation

A Python project for estimating room occupancy from time-series CO₂ concentration measurements using multiple modelling approaches.

The objective of this project is to investigate and compare several occupancy estimation techniques based on indoor CO₂ measurements. Each algorithm is implemented independently while sharing a common set of data models, calculation utilities, and visualisation tools.

---

## Project Overview

Indoor CO₂ concentration is strongly correlated with human occupancy. By analysing how CO₂ levels change over time, it is possible to estimate the number of occupants within a space.

This repository provides a framework for implementing, testing, and comparing several occupancy estimation methods, including:

* **Decay Approach** – Estimates ventilation characteristics from periods of decreasing CO₂ concentration.
* **Build-Up Approach** – Estimates occupancy from increasing CO₂ concentration during occupied periods.
* **Kalman Filter Approach** – Uses recursive state estimation to infer occupancy over time.
* **Machine Learning Approach** – Learns occupancy patterns from historical CO₂ datasets.

Each approach is implemented within its own directory to allow independent development while sharing common infrastructure.

---

## Repository Structure

```text
.
├── 1-decay-approach/
├── 2-build-up-approach/
├── 3-kalman-approach/
├── 4-ml-approach/
│
├── calculations/
│   ├── ach.py
│   ├── occupancy.py
│   ├── safety_tolerance.py
│   ├── tracer_decay.py
│   └── ventilation_rate.py
│
├── classes/
│   ├── algo_output.py
│   ├── cycles.py
│   ├── monitor_output.py
│   ├── occupancy_params.py
│   ├── room_params.py
│   ├── sitedata.py
│   └── termuserguide.py
│
├── data/
│   ├── csv/
│   └── json/
│
├── docs/
│
├── functions/
│   ├── csvintake.py
│   ├── interpretation.py
│   └── jsonintake.py
│
├── out/
│   ├── base.py
│   ├── box_plot.py
│   ├── daily.py
│   ├── monthly.py
│   ├── scatter_plot.py
│   ├── style.py
│   └── weekly.py
│
├── progress-reports/
├── results/
└── requirements.txt
```

---

## Directory Description

### `1-decay-approach/`

Implementation of occupancy estimation using CO₂ decay analysis.

### `2-build-up-approach/`

Implementation based on CO₂ accumulation during occupied periods.

### `3-kalman-approach/`

State-space modelling and Kalman filtering techniques for occupancy estimation.

### `4-ml-approach/`

Machine learning models trained to predict occupancy from environmental measurements.

### `calculations/`

Reusable mathematical models and engineering calculations including:

* Air Changes per Hour (ACH)
* Ventilation rate calculations
* Tracer gas decay
* Occupancy calculations
* Safety tolerance calculations

### `classes/`

Shared data models used across every algorithm.

These classes standardise the exchange of information between algorithms, data loaders, and visualisation modules.

### `functions/`

Utility functions responsible for:

* Importing CSV datasets
* Loading room configuration from JSON
* Data preprocessing and interpretation

### `out/`

Common plotting and reporting framework used by every occupancy estimation approach.

Includes:

* Scatter plots
* Box plots
* Daily summaries
* Weekly summaries
* Monthly summaries
* Shared plotting styles

### `data/`

Input datasets.

```
data/
├── csv/
└── json/
```

CSV files contain environmental monitor exports (CO₂, temperature, humidity, timestamps, etc.).

JSON files contain room-specific configuration such as dimensions and ventilation parameters.

### `results/`

Generated output from algorithm execution including:

* Occupancy estimates
* Figures
* Performance metrics
* Exported reports

### `docs/`

Project documentation and supporting material.

### `progress-reports/`

Development notes, research progress, and experiment summaries.

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository>
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Requirements

The project currently depends on:

```text
numpy
matplotlib
pandas
scipy
scikit-learn
rich
```

---

## Typical Workflow

1. Place monitor CSV files into:

```
data/csv/
```

2. Configure room parameters:

```
data/json/room.json
```

3. Run one of the occupancy estimation approaches.

4. Review generated plots and occupancy estimates in:

```
results/
```

---

## Shared Architecture

Every occupancy estimation approach shares the same supporting framework.

```
CSV Data
    │
    ▼
CSV Import
    │
    ▼
Shared Data Classes
    │
    ├─────────────┬──────────────┬──────────────┬───────────────┐
    ▼             ▼              ▼              ▼
Decay        Build-Up        Kalman        Machine Learning
Approach     Approach        Approach         Approach
    │             │              │               │
    └─────────────┴──────────────┴───────────────┘
                  │
                  ▼
Shared Plotting & Reporting
                  │
                  ▼
Results
```

This design ensures that:

* all algorithms consume identical input data
* outputs are standardised for comparison
* visualisations remain consistent across methods
* new occupancy estimation techniques can be added with minimal changes to the surrounding infrastructure

---

## Future Development

Potential future additions include:

* Bayesian occupancy estimation
* Particle filter implementation
* Real-time streaming support
* Sensor fusion with temperature and humidity
* Performance benchmarking across datasets
* Automated model evaluation and comparison
* Interactive dashboards

---

## Project Goals

This project aims to:

* Investigate multiple CO₂-based occupancy estimation techniques.
* Provide a common framework for comparing algorithm performance.
* Separate shared infrastructure from algorithm-specific implementations.
* Produce reproducible visualisations and evaluation metrics.
* Support research into indoor environmental quality and smart building analytics.

---

