# Delay-Compensated NMPC and PINN for Greenhouse Tomato Microclimate Regulation

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![LaTeX](https://img.shields.io/badge/Written%20in-LaTeX-blue.svg)](https://www.latex-project.org/)
[![MDPI Format](https://img.shields.io/badge/Format-MDPI%20Journal-green.svg)](https://www.mdpi.com/)

> **Adithiya Kumaran R K** · 2026 · *Under Review*

---

## 📄 Abstract

High-value greenhouse tomato (*Solanum lycopersicum*) cultivation requires precise regulation of four strongly coupled climate variables: **air temperature**, **relative humidity**, **CO₂ concentration**, and **canopy leaf temperature**.

This paper proposes a comprehensive, **delay-compensated Nonlinear Model Predictive Control (NMPC)** framework integrated with a **Physics-Informed Neural Network (PINN)** canopy observer. Key highlights:

- 🏗️ **8-state nonlinear plant model** with four first-order Padé filter states for actuator transport delay compensation (10–60 s)
- 📐 **Terminal penalty via DARE** — formally certifies local asymptotic stability (ρ_max = 0.9754 < 1.0)
- 🧠 **PINN canopy observer** (6→3×64→2) embedding Penman–Monteith transpiration thermodynamics — RMSE = 0.1942 °C, R² = 0.9997
- ⚡ **48.09% reduction in IAE** vs. PID (45.32 vs. 87.31 °C·h) over a 24-hour diurnal benchmark
- 🌡️ **34.52% peak overshoot suppression** (8.52 vs. 13.01 °C)
- 🔗 Exploratory **Ethereum smart-contract** proof-of-concept for tokenisation of energy & water conservation credits

---

## 📁 Repository Structure

```
Control_paper/
├── new/
│   ├── main.tex                               # Primary MDPI-format LaTeX source
│   ├── mdpi_journal.tex                       # Alternative journal format
│   ├── generate_drawio.py                     # Generates draw.io architecture diagrams
│   ├── render_architecture_figures.py         # Renders figures via Matplotlib
│   ├── fig1_greenhouse_nmpc_pinn_architecture.*   # System architecture (drawio / PDF / PNG)
│   ├── fig1_crop_disease_architecture.*           # Crop disease pipeline figure
│   ├── fig1_system_architecture.*                 # Alternate system figure
│   ├── fig2_stability_spectrum.*                  # Eigenvalue / stability spectrum
│   ├── fig3_pinn_loss_convergence.*               # PINN training loss curves
│   ├── fig4_temp_tracking.*                       # Closed-loop temperature tracking
│   ├── fig5_actuator_effort.*                     # Actuator input effort
│   ├── fig6_secondary_states.*                    # Secondary state variables
│   ├── fig7_humidity_co2.*                        # Humidity & CO₂ profiles
│   ├── fig8_pinn_estimation.*                     # PINN canopy-temperature estimation
│   ├── fig9_pinn_parity_scatter.*                 # Parity / scatter plot
│   └── fig10_transpiration_comp.*                 # Transpiration comparison
└── README.md
```

---

## 🔬 System Overview

```
┌─────────────────────────────────────────────────────┐
│              Greenhouse Microclimate Plant            │
│  States: T_air, RH, CO₂, T_leaf + 4 Padé delay      │
│          states (actuator transport compensation)     │
└──────────────────────┬──────────────────────────────┘
                       │ y (measurements)
           ┌───────────▼───────────┐
           │   PINN Canopy Observer │  ← Penman–Monteith physics
           │   (6→3×64→2 layers)   │     embedded in loss function
           └───────────┬───────────┘
                       │ T_leaf estimate (RMSE 0.1942 °C)
           ┌───────────▼───────────┐
           │   Delay-Compensated   │
           │        NMPC           │  ← DARE terminal penalty
           │  (Horizon N=20, dt=1s)│     stability guarantee
           └───────────┬───────────┘
                       │ u (heating, ventilation, CO₂, irrigation)
                       └──────────────► Plant
```

---

## 📊 Key Results

| Metric | PID | NMPC (Proposed) | Improvement |
|---|---|---|---|
| Temperature IAE (°C·h) | 87.31 | 45.32 | **−48.09%** |
| Peak Overshoot (°C) | 13.01 | 8.52 | **−34.52%** |
| PINN RMSE (°C) | — | 0.1942 | R² = 0.9997 |
| Max Eigenvalue ρ | — | 0.9754 | Stable |

---

## 🚀 Compiling the Paper

### Prerequisites
- A TeX distribution: [TeX Live](https://tug.org/texlive/) (Linux/macOS) or [MiKTeX](https://miktex.org/) (Windows)
- Or use **[Overleaf](https://www.overleaf.com)** (recommended for zero-setup)

### Compile Locally

```bash
cd new/
pdflatex main.tex
pdflatex main.tex   # run twice for cross-references
```

### Regenerate Figures

```bash
cd new/

# Regenerate draw.io XML diagrams
python generate_drawio.py

# Re-render architecture figures (requires matplotlib)
pip install matplotlib
python render_architecture_figures.py
```

---

## 🛠️ Dependencies

| Tool | Purpose |
|---|---|
| `pdflatex` | Compile LaTeX paper |
| `python >= 3.8` | Run figure-generation scripts |
| `matplotlib` | Render architecture diagrams |
| `draw.io` / `diagrams.net` | View/edit `.drawio` files |

LaTeX packages used: `amsmath`, `graphicx`, `booktabs`, `siunitx`, `mhchem`, `hyperref`, `fancyhdr`, `mathpazo`, `subcaption`, `listings`

---

## 📝 Citation

If you find this work useful, please cite:

```bibtex
@article{adithiya2026greenhouse,
  title   = {Delay-Compensated Nonlinear Model Predictive Control and
             Physics-Informed Neural Network Estimation for Greenhouse
             Tomato Microclimate Regulation},
  author  = {Adithiya Kumaran, R. K. and others},
  journal = {Journal Name},
  year    = {2026},
  volume  = {xx},
  pages   = {xxxx},
  doi     = {10.3390/xxxxx}
}
```

---

## 📜 License

This work is submitted for open-access publication under the **Creative Commons Attribution (CC BY 4.0)** license.  
See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Adithiya Kumaran R K**  
Department of Electrical and Computer Engineering  
Chennai 600025, India  
✉️ adithiya@example.edu
