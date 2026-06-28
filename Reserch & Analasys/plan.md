# UK Sovereign Hybrid DRAM — Full Agentic Swarm Execution Plan

## Objective
Synthesize the BEST UK-sovereign hybrid DRAM replacement: a reconfigurable 1T1C/1T1M cell (volatile DDR5 drop-in + neuromorphic in-memory compute) using ONLY abundant UK materials, producing a unified production-viable design document.

## Prior Research Consolidation
From 10 uploaded documents, the swarm has access to:
- **1T1C CNT+GO volatile DRAM**: Band diagrams, retention equations, Stanford VS-CNFET parameters, 1Gb array sim (102.4 GB/s, 17.7 TOPS/W), 10-step fab flow
- **2T1C/1T1M neuromorphic extension**: STDP equations, analog MAC, 20,950 TOPS/W in neuro mode, 64-level conductance
- **Full SoC diagrams**: M3D stack, photonic I/O, material mapping
- **Supply chain**: Lochaline silica, Cornish kaolin, Yorkshire coal, biomass, Cornish tin
- **Risk matrices**: Quantitative mitigations for all critical risks
- **Roadmaps**: 7-phase trajectory (2025-2035), 128Mb test chip spec

## Swarm Architecture

### Stage 1: Physics & Process Foundation (Parallel)
- **Agent 1: Device_Physicist** — Unified band diagrams, retention/STDP equations in LaTeX, electrostatic screening length derivation, temperature dependence models
- **Agent 2: Process_Engineer** — 10-12 step fab flow with UK material mapping, critical controls, process windows, defect mitigation

### Stage 2: Circuit & Simulation (Parallel, depends on Stage 1)
- **Agent 3: Circuit_Modeler** — Stanford VS-CNFET SPICE parameters, GO unified model (capacitor + memristor), full cell netlist, Verilog-A code
- **Agent 4: Array_Simulator** — Extend Python model with mode switching, STDP, full GEMM in both modes, temperature sweeps, DDR5 comparison, neuromorphic MAC — RUN code and output results

### Stage 3: Systems & Validation (Parallel, depends on Stage 2)
- **Agent 5: Systems_Architect** — Full SoC integration diagram, supply chain flowchart, power/thermal analysis, die area estimates
- **Agent 6: Validation_Roadmap_Lead** — 128Mb test chip spec, JEDEC compliance plan, Phase 1-7 roadmap, AI benchmark targets (MNIST, GEMM, LLM scaling)

### Stage 4: Risk Review & Integration (depends on Stage 3)
- **All agents** review risks, refine, converge
- **Orchestrator** assembles final unified markdown report

## Deliverables
1. Unified physics (band diagrams, equations in LaTeX)
2. Complete runnable Python simulator + example outputs
3. SPICE/Verilog-A netlist snippets
4. 10-12 step fab flow with UK material mapping
5. SoC diagram + supply chain flowchart
6. 128Mb Phase 1 test chip spec + validation plan
7. Risk matrix with quantitative mitigations
8. LLM training cluster projections

## Skill Usage
- `deep-research-swarm`: For any supplementary research needed
- `vibecoding-general-swarm`: For Python simulator development and code execution
- Built-in tools: Python execution, file I/O
