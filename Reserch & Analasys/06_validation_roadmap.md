# Validation Plan, Test Chip Specification & Development Roadmap

## Sovereign UK Semiconductor Memory: Hybrid 1T1C/1T1M (DRAM + Neuromorphic)

**Document Version:** 1.0 | **Date:** June 2025 | **Classification:** UK Strategic Technology Programme

---

## Executive Summary

This document presents the comprehensive validation strategy, 128Mb test chip specification, and 7-phase development roadmap for the UK's sovereign hybrid memory programme. The target is a 1Gb hybrid 1T1C/1T1M memory array combining volatile DRAM with neuromorphic in-memory compute, fabricated via an all-carbon process flow (CNTFET + GO-RRAM, T_max < 400 C). The 18-month validation programme spans device, array, and system levels, culminating in JEDEC DDR5-6400 compliance and AI benchmark demonstration. The 10-year roadmap (2025-2035) advances from single-device characterisation to UK pilot production.

---

## 1. Phase 1: 128Mb Test Chip Specification

### 1.1 Core Specification

| Parameter | Specification | Notes |
|---|---|---|
| Capacity | 128 Mb (16 MB) | 1/8th scale of 1Gb production target |
| Die Size | 5 mm x 5 mm (25 mm^2) | Probe-card compatible; scribe-line DFT structures |
| Package | QFP-208 (characterisation) / WLCSP-81 (system) | Re-bondable for debug |
| Organisation | 4 x 32Mb sub-arrays | Bank-independent operation |
| Cell Size | 0.06 um^2 (6F^2 at 100 nm equivalent) | GO-RRAM integrated in BEOL |
| Array Efficiency | >= 72% | Peripheral circuits in CMOS periphery |
| Operating Voltage | 0.8 V (DRAM) / 0.3-1.5 V (neuro) | Bipolar GO-RRAM switching |
| Clock Frequency | 6.4 GHz (DDR) | DDR5-6400 equivalent |
| Bandwidth | 102.4 GB/s | 16-bit prefetch, 8 banks active |
| Temperature | 0 C to 85 C standard; -40 C to 105 C automotive | Guard-banded for AEC-Q100 Grade 2 |
| Process | UK-Material Flow (T_max < 400 C) | CNTFET + GO-RRAM, all-carbon |
| Substrate | 200 mm Si handle wafer | Transfer-printed CNT channels |
| Metal Stack | 4-layer Cu BEOL | M1-M4 for array routing |
| ESD Protection | HBM 2 kV, CDM 500 V | Full DDR5 I/O compliance |

### 1.2 Peripheral Circuits

| Circuit Block | Key Features | Performance Target |
|---|---|---|
| Row Decoder | 12-to-4096, TMR-protected, level-shifted WL drivers | Access time < 2 ns |
| Word-Line Driver | Dual-rail (0.8 V DRAM, 1.5 V neuro RESET) | Rise/fall < 500 ps |
| Sense Amplifier | Differential latch-type, digital offset trim | Resolution < 10 mV |
| Write Driver | Programmable impedance, predriver with de-emphasis | 40-60 Ohm range |
| Mode Controller | SPI-programmable state machine | Mode switch < 100 ns |
| BIST Engine | March C-, March C+, checkerboard | Full array < 2 s @ 400 MHz |
| GO-RRAM Programmer | 10-bit DAC, charge pump, closed-loop verify | SET/RESET 50 ns-10 us, < 5% accuracy |
| PLL/DLL | Fractional-N PLL, digital DLL for DQ alignment | Jitter < 1 ps RMS |
| Temperature Sensor | Bandgap PTAT, 8-bit ADC | +/- 2 C accuracy |

### 1.3 Test Modes

| Test Mode | Access Method | Function |
|---|---|---|
| Scan Test | JTAG TAP (IEEE 1149.1) | Full chain coverage of all sequential elements |
| BIST Mode | JTAG instruction or pin-trigger | Autonomous March testing with pass/fail signature |
| Direct Array Access (DAA) | JTAG bypass or SPI | Direct read/write to any row/column |
| Neuro Programming | Analog pins or SPI-over-JTAG | Weight read/write, STDP timing calibration |
| Burn-In Mode | Elevated V/T | 125 C, 1.1x VDD, 168-hour stress |
| IDDQ Test | Static current measurement | < 10 uA quiescent per bank |

### 1.4 Pinout Description

**DDR5-Compatible Digital Interface (QFP-208):**

| Pin Group | Count | Type |
|---|---|---|
| DQ[15:0] | 16 | SSTL-0.8V |
| DQS_t, DQS_c | 2 | Differential SSTL |
| DM_n | 1 | SSTL-0.8V |
| CA[5:0] | 6 | SSTL-0.8V |
| CK_t, CK_c | 2 | Differential SSTL |
| CS_n, CKE | 2 | SSTL-0.8V |
| RESET_n, TEN | 2 | LVCMOS-1.2V |
| ALERT_n | 1 | Open-drain |
| Power (VDD/VDDQ/VPP/VSS) | 108 | Power/Ground |

**Neuromorphic Analog Interface (WLCSP bumps):**

| Pin | Count | Range |
|---|---|---|
| NWE[3:0] (neuro WL enable) | 4 | 0-1.5 V |
| NRE[3:0] (spike input) | 4 | 0-0.8 V pulse |
| NBIAS[1:0] (analog bias) | 2 | 0-0.8 V DC |
| NMON (current monitor) | 1 | Analog output |
| NSPI (SCK/SDI/SDO/CS_n) | 4 | LVCMOS-0.8V |

---

## 2. Validation Plan

### Phase 1A: Device Characterisation (Months 1-6)

#### Device Characterisation Targets

| Parameter | Target | Acceptance Criteria | Test Method |
|---|---|---|---|
| CNTFET I_on/I_off | > 2 x 10^10 | >= 10^10 at V_ds = 0.8 V | I_d-V_g, 30 dies x 5 wafers |
| Subthreshold Swing | < 70 mV/dec | < 75 mV/dec @ 300 K | Log(I_d)-V_g linear fit |
| Storage Capacitance (C_s) | 39.8 +/- 4 fF | 35.8-43.8 fF | C-V @ 1 MHz |
| GO-RRAM ON/OFF Ratio | > 10^3 | >= 500 | R-V hysteresis sweep |
| 64-Level Variation | < 5% | < 7% (3 sigma) | 1000 cycles, statistical |
| GO-RRAM SET/RESET | 0.3 V / 1.5 V | 0.25-0.35 V / 1.3-1.7 V | 100 ns pulse sweep |
| Endurance | > 10^6 cycles | >= 10^5 cycles | Automated cycling |
| Retention | > 10 yr @ 85 C | < 10% drift @ 125 C, 1000 hr | High-temp bake |
| CNTFET Mobility | > 1000 cm^2/Vs | >= 500 cm^2/Vs | Split C-V |
| Contact Resistance | < 100 Ohm-um | < 200 Ohm-um | TLM 4-point |

#### Environmental & Corner Characterisation

| Condition | Range | Purpose |
|---|---|---|
| Temperature sweep | -40 C to +125 C | Arrhenius extraction, activation energy |
| Humidity bias | 85 C / 85% RH | GO dielectric stability, 1000 hr |
| High-temp storage | 150 C unbiased | GO-RRAM retention acceleration, 1000 hr |
| Thermal cycling | -40 C to +125 C | Package/board reliability, 1000 cycles |
| BTI stress | V_gs = +/- 1.0 V, 125 C | CNTFET threshold drift, 1000 hr |

**Process Corners:** Typical (TT), Fast-Fast (FF), Slow-Slow (SS), Fast-Slow (FS), Slow-Fast (SF) -- all five corners must pass device specs for Milestone M3.

### Phase 1B: Array Validation (Months 4-12)

#### DRAM Mode Array Testing

| Test | Algorithm | Acceptance Criteria |
|---|---|---|
| Functional integrity | March C- | Zero bit failures, all corners |
| Address decoder fault | Galloping pattern | 100% address space coverage |
| Retention | Variable pause March (1-1000 ms) | 32 ms min @ 85 C, < 0.1 ppm fail |
| Refresh distribution | Per-row retention | All rows >= 32 ms |
| SA offset | Differential pattern stress | < 10 mV equivalent offset |
| Write/read disturb | Aggressor/victim | < 10^-15 disturb probability |
| DDR5 protocol | APG full protocol | Full conformance (see Section 4) |
| Power | Per-bank current | < 50 mW active, < 1 mW standby |
| Burn-in (HTOL) | 125 C, 1.1x VDD, dynamic | < 0.1% cumulative failure |

#### Neuromorphic Mode Array Testing

| Test | Method | Acceptance Criteria |
|---|---|---|
| STDP timing | Pre/post spike pair sweep | tau = 25 +/- 2 ms |
| Weight programming | Closed-loop verify-after-write | RMS error < 3% full scale |
| 64-level discrimination | Uniform programming | All levels > 7 sigma separation |
| Sneak-path | Half-select bias patterns | < 1% read error, all 32Mb |
| Write endurance | 10^6 cycles/cell | < 10% R drift post-cycling |
| Analog read linearity | Ramp sweep INL/DNL | INL < +/- 1 LSB, DNL < +/- 0.5 LSB |
| Cross-array uniformity | All 4 sub-arrays | Sigma/mu < 0.1 all levels |

### Phase 1C: System Integration (Months 10-18)

#### Milestone Acceptance Criteria Table

| ID | Milestone | Phase | Acceptance Criteria | Target |
|---|---|---|---|---|
| M1 | CNTFET parametric sign-off | 1A | I_on/I_off > 10^10, SS < 75 mV/dec, 30 dies x 5 wafers | Month 3 |
| M2 | GO-RRAM single-cell baseline | 1A | 64 levels < 5% variation, endurance > 10^5 | Month 4 |
| M3 | Process corner qualification | 1A | All 5 corners pass device specs | Month 5 |
| M4 | 32Mb DRAM functional | 1B | March C- zero fails, all corners | Month 6 |
| M5 | Retention qualified | 1B | 32.4 ms @ 85 C, Arrhenius to 10 yr | Month 8 |
| M6 | DDR5 protocol compliance | 1B | All timing within spec | Month 9 |
| M7 | STDP verified | 1B | Measured tau = 25 +/- 2 ms, 100 cells | Month 7 |
| M8 | 64-level programming | 1B | < 5% RMS error, all 32Mb | Month 9 |
| M9 | Full 128Mb functional | 1C | All 4 sub-arrays, DRAM + neuro | Month 11 |
| M10 | MNIST benchmark | 1C | > 90% accuracy, < 1 uJ/inference | Month 13 |
| M11 | CIFAR-10 benchmark | 1C | > 75% accuracy | Month 14 |
| M12 | GEMM 1024^2 | 1C | < 1 us in neuro mode | Month 12 |
| M13 | JEDEC compliance report | 1C | Formal report, all parameters pass | Month 15 |
| M14 | LLM inference demo | 1C | < 2 ms/token, 4-stack | Month 16 |
| M15 | Final qualification | 1C | Complete docs, Cpk > 1.33 all | Month 18 |

**Final Deliverables:** Device Characterisation Report (PDF + CSV); Array Test Report (PDF + STDF); JEDEC Compliance Report; AI Benchmark Report (PDF + Jupyter); Reliability Report (Weibull); Design Archive (encrypted GDS/LEF/LIB/SPICE).

---

## 3. 7-Phase Development Roadmap (2025-2035)

### Roadmap Overview

| Phase | Years | TRL | Focus | Key Deliverable |
|---|---|---|---|---|
| 1 | 2025-2026 | 3->4 | Single-device characterisation | CNTFET I-V, GO C-V, RRAM R-V |
| 2 | 2026-2027 | 4->5 | Small circuits | Ring oscillators, 6T-SRAM, inverters |
| 3 | 2027-2028 | 5->6 | Memory arrays | GO-RRAM 32Mb, ML cell demo |
| 4 | 2028-2029 | 6->7 | Neuromorphic | Synaptic arrays, MNIST > 90% |
| 5 | 2029-2031 | 7->8 | CPU prototype | RISC-V core, > 10,000 CNT FETs |
| 6 | 2031-2033 | 8->9 | NPU integration | 8 TOPS/W CNT-NPU + GO-RRAM |
| 7 | 2033-2035 | 9 | Pilot production | UK pilot line, defence/space/AI |

### Phase 1: Single-Device Characterisation (2025-2026)

Establishes electrical behaviour of CNTFETs, GO capacitors, and GO-RRAM elements. Produces statistically significant parametric data for compact model extraction (BSIM-CMG equivalent). Work includes CNT density/chirality optimisation, GO oxidation control, and RRAM forming process development.

**Facilities:** Imperial (CNT growth, CVD, Raman/AFM); Manchester NGI (GO synthesis, XPS/SEM); Cambridge (electrical characterisation suite); Southampton (PL mapping).
**Budget:** PS3-5M (UKRI/EPSRC + defence R&T).
**Key Risks:** CNT chirality control (mitigation: commercial sorted CNTs); GO pinholes (mitigation: multi-cycle oxidation); high contact resistance (mitigation: Pd/Au edge contacts).
**Go/No-Go:** I_on/I_off > 10^10 on > 50% devices; GO-RRAM > 100 reliable cycles; C_s within +/- 10% target.

### Phase 2: Small Circuits (2026-2027)

Integrates devices into functional circuit blocks: 101-stage ring oscillators; 6T-SRAM cells using CNTFETs; standard cell libraries (INV, NAND, NOR, DFF); 4-bit flash ADCs. Develops custom PDK for Cadence/Synopsys and DRC/LVS decks.

**Facilities:** Manchester NGI (cleanroom, e-beam lithography, ALD); Cambridge (MPW via Europractice); Imperial (CNT transfer printing, probe stations).
**Budget:** PS5-8M.
**Key Risks:** Logic speed insufficient (mitigation: optimise L, end-bonded contacts); SRAM stability low (mitigation: WL underdrive, 8T backup); e-beam throughput (mitigation: develop stepper process for Phase 3).
**Go/No-Go:** RO frequency > 100 MHz @ 0.8 V; SRAM SNM > 150 mV; > 20 standard cells validated.

### Phase 3: Memory Arrays (2027-2028)

First medium-scale integration: 32Mb GO-RRAM array with CNTFET access devices. Demonstrates array-level programming with closed-loop verify-after-write, full retention/endurance/read-disturb characterisation, and ML cell demonstration for simple pattern classification.

**Facilities:** Manchester NGI (200 mm processing, stepper lithography); Imperial (FPGA-based test platform); Cambridge (design/verification); External (LETI/IMEC for risk mitigation runs).
**Budget:** PS8-12M.
**Key Risks:** Array yield < 50% (mitigation: 2 spare rows/cols, BIST repair); sneak-path dominance (mitigation: 1T1M selector, optimise non-linearity).
**Go/No-Go:** 32Mb functional, > 70% yield; 64-level programming across full array; 2-layer NN on 1000 MNIST > 85%.

### Phase 4: Neuromorphic Integration (2028-2029)

Integrates 32Mb tiles into full 128Mb test chip. Demonstrates dual-mode operation (DDR5 DRAM + neuromorphic), formal JEDEC compliance, and AI benchmarks (MNIST > 90%, CIFAR-10 > 75%). Produces complete validation dataset; design scales directly to 1Gb by tiling.

**Facilities:** Manchester NGI (custom fabrication); Imperial (DDR5 test platform, AI benchmarking); Cambridge (WLCSP packaging); External (JEDEC test house, AI benchmarking partner).
**Budget:** PS12-18M.
**Key Risks:** DDR5 compliance failure (mitigation: pre-compliance Months 6-8); neuro accuracy low (mitigation: quantisation-aware training).
**Go/No-Go:** JEDEC DDR5-6400 passed; MNIST > 90% @ < 1 uJ/inference; full 128Mb both modes functional.

### Phase 5: CPU Prototype (2029-2031)

RISC-V RV32IMAC core in CNTFET logic (> 10,000 transistors) integrated with 128Mb hybrid memory as complete SoC. Runs compiled code (GCC toolchain), executes CoreMark/Dhrystone. Validates standard cell library, synthesis flow, and signal integrity. Serves as reliability qualification vehicle.

**Facilities:** Manchester NGI (SoC fabrication); Cambridge (digital design flow, physical design); Imperial (verification, JTAG debug); External (ARM/Imagination IP consultation).
**Budget:** PS15-22M.
**Key Risks:** Transistor count scaling (mitigation: modular design, BIST per module); high static power (mitigation: doping optimisation, power gating, multi-V_th).
**Go/No-Go:** CNT-RISC-V boots RTOS/Linux; CoreMark > 10/MHz; full ISA compliance.

### Phase 6: NPU Integration (2031-2033)

CNTFET NPU with hybrid memory as complete AI accelerator. Systolic arrays, vector units, on-chip interconnects in CNTFET logic targeting 8 TOPS/W with GO-RRAM weight storage. Demonstrates LLM and CV inference at competitive performance. Produces licensable IP portfolio.

**Facilities:** Manchester NGI (advanced 2.5D/3D packaging); Cambridge (NPU architecture, RTL-to-GDSII); Imperial (AI benchmarking at scale); External (cloud benchmarking vs. H100).
**Budget:** PS20-30M.
**Key Risks:** TOPS/W miss (mitigation: mixed-precision INT4/INT8, sparsity); bandwidth wall (mitigation: HBM stacking, 2.5D interposer); software stack (mitigation: PyTorch/ONNX partnership).
**Go/No-Go:** 8 TOPS/W on ResNet-50; Llama-3 70B < 2 ms/token; PyTorch integration.

### Phase 7: Pilot Production (2033-2035)

UK-based pilot production line (1,000-10,000 wafers/year) targeting defence/security (rad-hard space memories), AI compute (sovereign infrastructure), and automotive/industrial. Transfers process to production facility, develops CNT/GO supply chains, achieves AEC-Q100 and DEF-STAN qualification.

**Facilities:** UK Sovereign Semiconductor Facility (200 mm, Class 10-100); Manchester NGI (process transfer, training); External (CNT supplier qualification, GO chemical supply chain).
**Budget:** PS80-120M (capital equipment, qualification, staffing).
**Key Risks:** Capital funding (mitigation: phased build, Catapult shared facility, MoD commitment); CNT supply (mitigation: dual-source, domestic production); yield ramp (mitigation: SPC from Phase 1, yield engineering team).
**Go/No-Go:** Pilot line > 50% yield on 128Mb; AEC-Q100 Grade 2; first defence contract; path to 10,000 wafers/year.

---

## 4. JEDEC Compliance Plan

### DDR5-6400 Compliance Checklist

| Parameter | JEDEC Spec | Our Target | Margin | Pass Criteria |
|---|---|---|---|---|
| t_RCD | 14.16 ns | 12.0 ns | -15.3% | <= 14.16 ns, all corners |
| t_CAS (CL) | 14.16 ns | 10.0 ns | -29.4% | <= 14.16 ns, all corners |
| t_RP | 14.16 ns | 12.0 ns | -15.3% | <= 14.16 ns, all corners |
| t_RAS | 32.0 ns | 24.0 ns | -25.0% | <= 32.0 ns, all corners |
| t_RC | 46.16 ns | 36.0 ns | -22.0% | <= 46.16 ns |
| t_REF1 | 32.0 ms | 32.4 ms | +1.3% | >= 32.0 ms @ 85 C |
| f_CK | 3200 MHz | 3200 MHz | 0% | >= 3200 MHz |
| Bandwidth | 51.2 GB/s | 102.4 GB/s | +100% | >= 51.2 GB/s sustained |
| t_WR | 15.0 ns | 13.0 ns | -13.3% | <= 15.0 ns |
| t_FAW | 40.0 ns | 35.0 ns | -12.5% | <= 40.0 ns |
| Burst Length | 16 | 16 | 0% | BL=16 supported |
| DQ R_ON | 34 +/- 10% Ohm | 34 +/- 5% Ohm | Tighter | 30.6-37.4 Ohm |
| Input Levels | Per JEDEC Table 246 | Compliant | — | Within limits |
| t_DQSQ skew | +/- 100 ps | +/- 80 ps | Tighter | < +/- 100 ps |
| t_QH hold | 0.38 x UI | 0.40 x UI | Better | > 0.38 x UI |
| VDD | 1.1 +/- 0.055 V | 1.1 +/- 0.033 V | Tighter | 1.045-1.155 V |
| Temperature | 0-95 C | 0-85 C | Within | Functional across range |

### Compliance Test Flow

1. Pre-compliance simulation (SI, timing) -- 2 weeks
2. ATPG generation -- 1 week
3. Shmoo plot (V vs. f) -- 2 weeks
4. Corner lot testing (TT/FF/SS/FS/SF) -- 1 week
5. Protocol analyser verification -- 1 week
6. Temperature sweep (-40 C to +105 C) -- 2 weeks
7. Formal report generation -- 2 weeks

---

## 5. AI Benchmark Targets

### Primary Benchmark Suite

| Benchmark | Target | Measurement | Configuration |
|---|---|---|---|
| MNIST | > 90% accuracy | 10,000 test images | Single 128Mb, 784-128-10 |
| CIFAR-10 | > 75% accuracy | 10,000 test images | 4-chip stack, INT8 |
| GEMM 1024^2 | < 1 us | Wall-clock neuro mode | Single 128Mb, bit-serial MAC |
| LLM (Llama-3 70B) | < 2 ms/token | 1000-token average | 4-stack, 512 Mb weights |
| Energy/Inference | < 1 uJ | Full forward pass | MNIST, single chip |
| Training Throughput | > 50% of H100 | Images/sec equivalent | ResNet-50, 128-chip array |

### Extended Benchmark Suite

| Benchmark | Target | Notes |
|---|---|---|
| ResNet-50 (ImageNet) | > 74.5% top-1 | Standard CV backbone, INT8 |
| BERT-base (GLUE) | > 80 avg score | 9 GLUE tasks, NLP inference |
| GPT-2 (WikiText-2) | < 25 perplexity | Generative LM benchmark |
| Keyword Spotting | > 95% accuracy | Google Speech Commands, < 100 uJ |
| Anomaly Detection | > 0.95 AUC-ROC | MVTec AD, PaDiM algorithm |
| Object Detection (YOLO-tiny) | > 30 mAP @ 0.5 | COCO subset, 30 FPS target |
| Reinforcement Learning (DQN) | > 90% CartPole | 1000 episodes, on-chip learning |
| Graph Neural Network | > 85% accuracy | OGBN-Arxiv, 2-layer GCN |
| Spiking Neural Network | > 85% accuracy | MNIST, 100 time steps |
| Recommendation (DLRM) | > 78% accuracy | Criteo 1TB, embedding lookup |

### Energy Efficiency Targets

| Metric | Target | Competitive Reference |
|---|---|---|
| TOPS/W (neuro) | 539.2 | H100: ~150 TOPS/W (sparse) |
| TOPS/W (DRAM) | 11.1 | DDR5-6400: ~5 TOPS/W eq. |
| MNIST energy | 456 nJ/inference | Typical MCU: 10-100 uJ |
| Idle power | < 1 mW | LPDDR5: ~3 mW self-refresh |
| Active power (read) | < 50 mW/chip | DDR5: ~100 mW/chip |

---

## 6. Resource Estimates

### Phase 1 (128Mb Test Chip)

| Resource | Requirement |
|---|---|
| Core Team | 25-30 FTE: 8 IC design, 6 device physics, 5 test, 4 process integration, 3 PCB/systems, 2 PM, 2 technicians |
| PIs | 3 (Imperial, Manchester, Cambridge) |
| Postdocs | 8-10 across three sites |
| PhD Students | 6-8 (EPSRC + industry co-funded) |
| Facilities | 3 cleanrooms (Manchester NGI Class 100; Imperial/Cambridge Class 1000) |
| Test Equipment | PS1.5M (probe stations x3, B1500A x2, 4200A-SCS x2, DDR5 FPGA platform, thermal chambers x2) |
| Fabrication | PS4M (3 MPW iterations, mask NRE, materials) |
| Design Tools | PS0.5M/yr (Cadence, Synopsys, Mentor) |
| Packaging | PS0.3M (QFP-208 + WLCSP-81) |
| **Total Phase 1** | **PS8-10M over 18 months** |

### Full Roadmap Cumulative Budget

| Phase | Years | Budget (PSM) | Cumulative (PSM) |
|---|---|---|---|
| 1: Device Characterisation | 2025-2026 | 4 | 4 |
| 2: Small Circuits | 2026-2027 | 7 | 11 |
| 3: Memory Arrays | 2027-2028 | 10 | 21 |
| 4: Neuromorphic | 2028-2029 | 15 | 36 |
| 5: CPU Prototype | 2029-2031 | 18 | 54 |
| 6: NPU Integration | 2031-2033 | 25 | 79 |
| 7: Pilot Production | 2033-2035 | 100 | 179 |
| **Total** | **2025-2035** | **PS179M** | — |

### UK Facilities to Leverage

| Facility | Location | Role | Key Capability |
|---|---|---|---|
| Imperial College | London | Device physics, CNT growth, validation | CVD furnaces, probe stations, FPGA platforms |
| Manchester NGI | Manchester | Process dev, pilot fab | 750 m^2 Class 100 cleanroom, e-beam, ALD |
| Cambridge Graphene Centre | Cambridge | IC design, packaging | Design suites, bonding, SEM/FIB |
| Southampton Zepler Institute | Southampton | Photonics, characterisation | Optical lithography, Raman/PL, ellipsometry |
| Compound Semiconductor Centre | Cardiff | III-V option, supply chain | MOCVD, compound semiconductor processing |
| UK Catapult Network | Multiple | Scale-up, industry engagement | Manufacturing readiness, supply chain dev |
| Dstl | Portsdown | Defence apps, rad-hard testing | Proton/gamma radiation facilities |

### Key Hiring Requirements

| Role | Phase | Count | Skills |
|---|---|---|---|
| CNTFET Device Physicist | 1-3 | 3 | CNTs, transport, TCAD |
| GO/2D Materials Chemist | 1-4 | 2 | Graphene oxide, RRAM, thin-film |
| Memory IC Designer | 3-7 | 5 | SRAM/DRAM, sense amps, array architecture |
| Neuromorphic Architect | 4-6 | 3 | SNN/STDP, in-memory compute |
| Digital IC Designer | 5-7 | 6 | RISC-V, RTL, synthesis, STA |
| Physical Design Engineer | 5-7 | 4 | P&R, DRC/LVS, signoff |
| Test Engineer | 1-7 | 4 | ATE, JEDEC compliance, FA |
| Process Integration Engineer | 1-7 | 5 | BEOL/FEOL, yield, SPC |
| Packaging Engineer | 4-7 | 2 | WLCSP, flip-chip, thermal |
| AI/ML Engineer | 4-7 | 3 | PyTorch/TensorFlow, model optimisation |
| Project Manager | 1-7 | 2 | Semiconductor programme management |

### Funding Strategy

| Source | Amount (PSM) | Timeline |
|---|---|---|
| UKRI/EPSRC Programme Grant | 15-20 | 2025-2030 |
| Innovate UK (CR&D) | 10-15 | 2025-2030 |
| MoD/Dstl R&T | 15-25 | 2025-2035 |
| NATO DIANA | 5-10 | 2026-2030 |
| Private/Strategic Partners | 20-30 | 2028-2035 |
| Government Strategic Investment | 50-80 | 2030-2035 |
| EU Horizon (if eligible) | 5-10 | 2025-2030 |

---

## 7. Risk Register Summary

| ID | Risk | Phase | Impact | Likelihood | Mitigation |
|---|---|---|---|---|---|
| R1 | CNTFET yield insufficient for large arrays | 3-5 | Critical | Medium | Redundancy, fault tolerance, process optimisation |
| R2 | GO-RRAM retention fails automotive | 1-4 | Critical | Medium | Hafnia alternative, refresh-based scheme |
| R3 | DDR5 compliance failure | 4 | Critical | Medium | Pre-compliance testing, margin reserves |
| R4 | Schedule slip cascades | All | High | Medium | Overlapping phases, risk-based gating |
| R5 | Key personnel departure | All | High | Medium | Succession planning, knowledge docs |
| R6 | CNT supply disruption | 1-7 | Critical | Medium | Dual-source, strategic stockpile |
| R7 | Cleanroom capacity limit | 3-7 | High | Medium | Europractice partnership, shared facility |
| R8 | Competitive technology leapfrog | 4-7 | High | Medium | IP protection, continuous differentiation |
| R9 | Funding gap between phases | 5-7 | Critical | High | Diversified funding, MoD commitment |
| R10 | ESD/latch-up vulnerability | 4-5 | High | Low | Conservative protection, full ESD testing |

---

## 8. Conclusion

This validation plan and roadmap provide a rigorous pathway from experimental proof-of-concept to UK pilot production of sovereign hybrid memory. The 18-month 128Mb test chip validation will definitively establish CNTFET/GO-RRAM compliance with JEDEC DDR5 and neuromorphic AI targets. The 10-year roadmap advances systematically to TRL 9 with clear go/no-go criteria and a PS179M cumulative budget envelope.

Three critical success factors: (1) maintaining I_on/I_off > 10^10 and SS < 75 mV/dec through scaling; (2) achieving > 70% 128Mb array yield with redundancy; and (3) securing sustained investment through Phase 7. The UK possesses unique advantages -- world-leading CNT/GO research at Manchester NGI and Imperial, strong IC design at Cambridge, and strategic imperative for sovereign semiconductor capability. This roadmap converts those advantages into measurable, actionable progress.

---

*Document approved for release. Parameters subject to revision based on Phase 1A experimental results.*
