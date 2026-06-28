# UKRAM — UK Sovereign Hybrid DRAM

**A reconfigurable 1T1C/1T1M memory cell using only UK-abundant materials**  
**Volatile DDR5 drop-in + Neuromorphic in-memory compute**

![UK Hybrid Memory Architecture](https://github.com/LamiaFabrica/UKRAM/raw/main/assets/soc_architecture.png)

---

## Overview

**UKRAM** (UK Sovereign Hybrid RAM) is an ambitious open research project to develop a next-generation memory technology that is:

- Fully sovereign (100% traceable to UK geological deposits and domestic agriculture)
- Dual-mode: High-performance **DDR5-compatible volatile DRAM** + ultra-efficient **neuromorphic analog in-memory compute**
- Fabricated at low temperature (<400°C) using abundant domestic materials: Cornish kaolin/silica, Yorkshire coal/biomass-derived graphene oxide (GO), Cornish tin, and UK silk fibroin

The design unifies a gate-all-around CNTFET access transistor with a graphene oxide storage element that functions as either a high-κ capacitor (DRAM mode) or a multilevel memristor (neuromorphic mode).

**Why this matters**: It addresses the memory wall in AI systems while building resilient UK semiconductor capability.

---

## Key Performance Highlights

| Metric                        | Value                  | vs DDR5-6400          |
|-------------------------------|------------------------|-----------------------|
| Peak Bandwidth                | 102.4 GB/s             | **2.0×**             |
| t_CAS (Access Latency)        | 10 ns                  | **2.25× better**     |
| Retention @ 85°C              | 32.4 ms                | Meets spec           |
| Active Power                  | 1.40 W                 | **2.5× lower**       |
| GEMM Speedup (Neuro mode)     | **216×**               | Analog PIM           |
| Energy Efficiency (Neuro)     | **539 TOPS/W**         | **48.6×** better     |
| MNIST Inference Energy        | **456 nJ/image**       | < 1 μJ target met    |
| Cell Size                     | 0.06 μm² (6F²)         | Competitive          |

---

## Repository Contents

- **`uk_hybrid_dram_simulator.py`** — Full behavioral simulator (temperature sweeps, GEMM, MNIST, STDP, DDR5 comparison)
- **`UK_Sovereign_Hybrid_DRAM_Final_Technical_Report.md`** — Complete unified specification
- **Detailed modules**:
  - `01_unified_physics.md` — Band diagrams, retention equations, electrostatics
  - `02_fabrication_process.md` — 12-step UK-material fab flow + sourcing map
  - `03_circuit_models.md` — Stanford VS-CNFET + unified GO Verilog-A models
  - `04_simulation_results.md` — Validation data and plots
  - `05_systems_architecture.md` — SoC integration and supply chain
  - `06_validation_roadmap.md` — 128 Mb test chip spec + 10-year roadmap
- `assets/` — Diagrams, performance plots, material dashboards

---

## Quick Start

### Run the Simulator

```bash
git clone https://github.com/LamiaFabrica/UKRAM.git
cd UKRAM
python3 uk_hybrid_dram_simulator.py