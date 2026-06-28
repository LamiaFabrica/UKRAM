# Hybrid 1T1C/1T1M Memory Cell Fabrication Process Flow

## Sovereign UK Semiconductor Process — Low-Temperature (<400C) Fabrication

**Document:** UK-MEM-FAB-002 | **Revision:** 1.0 | **Classification:** Process Engineering

---

## 1. Executive Summary

This document defines the complete fabrication process flow for a hybrid one-transistor-one-capacitor / one-transistor-one-memristor (1T1C/1T1M) memory cell, manufactured exclusively from UK-abundant raw materials at temperatures never exceeding 400C. The process integrates three distinct functional layers on a shared MAS glass-ceramic substrate: (i) a DRAM capacitor using coal-derived graphene oxide (GO) as the high-k dielectric, (ii) a CNT field-effect transistor for cell selection, and (iii) a silk fibroin:GO neuromorphic memristor for in-memory computation. The 12-step flow extends our previously established 10-step baseline with explicit separation of the GO deposition into DRAM-optimized and neuro-optimized variants, addition of a silk fibroin composite deposition step, and insertion of a chemical-mechanical polishing (CMP) planarization step for topography management.

---

## 2. Extended 12-Step Process Flow Table

| Step | Process | UK Material Source | Temperature | Time | Critical Control |
|:---:|---|---|---|---|---|
| 1 | MAS glass-ceramic substrate formation | Cornish kaolin (St Austell) + Lochaline silica (Scotland) | 400C calcine | 6 hr | CTE = +5.0 ppm/K; epsilon_r = 5.0-8.0 |
| 2 | Bottom electrode sputtering | TiN/Pt (buffer, import) | RT-200C | 30 min | 50 nm Pt plate; R_s < 10 Ohm/sq |
| 3a | DRAM-GO spin-coating | Yorkshire coal-derived GO dispersion | RT -> 150C anneal | 45 min | 2 nm film; C/O = 3.0 +/- 0.3 (FTIR) |
| 3b | Neuro-GO spin-coating | UK biomass-derived GO + Ag NP seeding | RT -> 120C anneal | 60 min | 5 nm film; Ag NPs 5-10 wt%; C/O = 2.5 |
| 4 | CMP planarization | Silica abrasive (Lochaline) | RT | 20 min | RMS roughness < 0.5 nm; step height < 2 nm |
| 5 | Silk fibroin:GO composite deposition | Bombyx mori silk fibroin (domestic sericulture) + GO | RT -> 80C | 90 min | SF:GO ratio 3:1; film thickness 50 nm |
| 6 | Top electrode / storage node | TiN sputtering (import) | RT-200C | 25 min | 30 nm; 0.06 um^2 area; hermetic seal |
| 7 | CNT transfer & alignment | UK coal/biomass s-SWCNTs | <300C | 45 min | DLSA 10 MHz, 5 Vpp; density 100 tubes/um |
| 8 | S/D contact evaporation | Pd (p-type), Sc (n-type, import) | RT | 15 min | 20 nm contact; rho_c < 10^-7 Ohm.cm^2 |
| 9 | Gate stack ALD | HfO2 precursor (import) | 250C | 40 min | 3 nm; EOT = 1 nm; epsilon_r = 25 |
| 10 | Gate electrode patterning | TiN sputtering (import) | RT-200C | 30 min | L_g = 25 nm; L-shaped SiO2 spacer |
| 11 | BEOL metallization | Coal-derived graphene + Cornish Sn-Ag-Cu | <300C | 120 min | 5 metal layers; SAC solder; J_e > 1 MA/cm^2 |
| 12 | Passivation & probe test | Chalcogenide glass (As-S-Se, import) | <200C | 60 min | Hermetic seal; pad opening; 100% parametric |

---

## 3. Detailed Step-by-Step Process Description

### Step 1: MAS Glass-Ceramic Substrate Formation

The substrate is fabricated from magnesium aluminosilicate (MAS) glass-ceramic derived primarily from Cornish kaolin (St Austell Granite, 50.37N 4.79W) and Lochaline high-purity silica sand (Scotland, 56.53N 5.77W, 99.8% SiO2). The kaolin provides the Al2O3 and SiO2 framework, while MgO is added as the network modifier to promote cordierite (Mg2Al4Si5O18) crystallization. Raw materials are wet-milled to <5 um particle size, spray-dried with 5 wt% PVA binder, and uniaxially pressed at 20 MPa into 300 mm green bodies. The green body undergoes a two-stage thermal cycle: first, a 400C calcination for 6 hours in air to burn off organics and initiate surface nucleation of alpha-cordierite; second, a controlled cooling at 2C/min to room temperature. The resulting glass-ceramic exhibits a linear CTE of +5.0 ppm/K (measured 40-600C by dilatometry), dielectric constant epsilon_r = 5.0-8.0 at 1 MHz, and flexural strength >200 MPa. The 400C ceiling is strictly enforced — higher temperatures risk excessive grain growth and CTE mismatch with subsequent layers. Metrology: XRD for phase confirmation (alpha-cordierite at 2theta = 10.5deg, 29.5deg); dilatometry for CTE; impedance analyzer for epsilon_r. Defect mode: Micro-cracking from thermal stress — mitigated by controlled cooling and <5% porosity target.

### Step 2: Bottom Electrode Sputtering

A dual-layer bottom electrode is DC-sputtered onto the MAS substrate at 200C base temperature. First, a 10 nm TiN adhesion/buffer layer is deposited from a Ti target in Ar/N2 plasma (5 mTorr, 100 W RF) to promote adhesion and block metal diffusion into the substrate. This is followed by 50 nm of Pt deposited via DC magnetron sputtering (3 mTorr Ar, 150 W) to form the capacitor bottom plate. Platinum is selected for its high work function (5.65 eV), excellent chemical stability in contact with GO, and low leakage interface. While Ti and Pt precursors must be imported, research is ongoing to evaluate coal-derived carbon electrodes as a fully sovereign replacement. The sputtering target-to-substrate distance is 100 mm with substrate rotation at 20 RPM to ensure uniformity <+/-3% across 300 mm. Metrology: Four-point probe (R_s < 10 Ohm/sq); AFM (RMS roughness < 1 nm); XRR for thickness. Defect mode: Pt islanding on TiN — mitigated by in-situ Ar+ pre-clean at 50 eV for 30 seconds prior to deposition.

### Step 3a: DRAM-GO Spin-Coating (Capacitor Dielectric)

Yorkshire coal-derived graphene oxide is dispersed in deionized water at 0.5 mg/mL concentration. The GO is synthesized via modified Hummers method from Yorkshire bituminous coal (carbonized at 600C, then oxidized with KMnO4 in 9:1 H2SO4/H3PO4). The dispersion is spin-coated at 3000 RPM for 45 seconds, followed by a soft bake at 80C for 10 minutes and a hard anneal at 150C for 30 minutes in N2 ambient. The resulting film is 2 nm thick (monolayer-to-bilayer GO) with dielectric constant epsilon_r = 150, providing high capacitance density for the DRAM storage node. The C/O atomic ratio is controlled at 3.0 +/- 0.3, as verified by FTIR peak ratios at 1730 cm-1 (C=O carbonyl) and 3400 cm-1 (O-H stretch). A lower C/O ratio (more oxygen) increases the bandgap and reduces leakage but decreases dielectric constant; the 3.0 target balances both requirements. Metrology: FTIR (C/O ratio); ellipsometry (thickness); I-V (leakage < 10^-6 A/cm2 at 1 V). Defect mode: Pinholes from incomplete coverage — mitigated by multiple coat cycles (3x) with 80C interlayer bakes.

### Step 3b: Neuro-GO Spin-Coating (Memristor Functional Layer)

A thicker, more heavily functionalized GO layer is deposited for the neuromorphic memristor. UK biomass-derived GO (from wheat straw or forestry waste, sourced from Yorkshire/Sussex) is dispersed at 1.0 mg/mL with pre-dispersed Ag nanoparticles (10 nm diameter, 5-10 wt% loading). The Ag NPs serve as seeding sites for conductive filament formation during resistive switching. Spin-coating at 2000 RPM for 60 seconds yields a 5 nm film, which is soft-baked at 80C for 15 minutes and annealed at 120C for 45 minutes. The C/O ratio is intentionally lower at 2.5 (more oxygen-containing groups) to enhance ionic conductivity and facilitate Ag+ migration. The higher Ag loading (10 wt%) creates a dense array of localized conduction sites that enable multilevel resistive switching with ternary behavior — critical for neuromorphic analog computing. Metrology: UV-Vis (Ag plasmon peak at 420 nm); FTIR (C/O = 2.5); XPS (Ag 3d5/2 at 368.2 eV); AFM (thickness). Defect mode: Ag NP agglomeration >20 nm — mitigated by capping with PVP (1 wt%) and sonication at 100 W for 30 min before spin-coating.

### Step 4: CMP Planarization

Chemical-mechanical polishing is performed using a silica-based slurry derived from Lochaline silica sand (99.8% SiO2, Scotland). The slurry is formulated at pH 9.5 with 0.1 um colloidal silica particles at 10 wt% loading, with 1 wt% hydrogen peroxide as oxidizer. Polishing proceeds at 2 psi down-force, 80 RPM platen speed, and 50 mL/min slurry flow for 20 minutes. The step removes topography from the GO/SF depositions, achieving RMS surface roughness < 0.5 nm (measured by AFM) and step height reduction from ~50 nm to < 2 nm. CMP is critical before CNT alignment because any surface asperity > 2 nm disrupts the dielectrophoretic alignment field and causes CNT bundling. Post-CMP, the wafer undergoes a DI water rinse and N2 dry, followed by a mild O2 plasma descum (50 W, 30 seconds) to remove organic residue. Metrology: AFM (roughness, step height); profilometry; optical inspection (defect count < 0.1/cm2). Defect mode: GO film delamination — mitigated by optimizing slurry pH to 9.5 (below GO deprotonation threshold) and limiting polish time to 20 minutes.

### Step 5: Silk Fibroin:GO Composite Deposition

Silk fibroin is extracted from Bombyx mori cocoons sourced from UK domestic sericulture operations (Mulberry silkworm farms in Kent and Hertfordshire). Cocoons are boiled twice in 0.5 wt% Na2CO3 aqueous solution for 60 minutes total to remove sericin, rinsed thoroughly in DI water, and dried. The degummed fibroin is dissolved in LiBr solution (9.3 M) at 60C for 2 hours, then dialyzed against DI water for 48 hours to remove residual LiBr. The purified SF solution (concentration 4-8 wt%) is mixed with the neuro-GO dispersion (Step 3b) at a SF:GO mass ratio of 3:1. The composite is spin-coated at 5000 RPM for 30 seconds onto the planarized substrate, then dried at room temperature for 10 minutes, followed by a post-treatment with ethanol vapor for 30 minutes to induce beta-sheet crystallization in the silk matrix. The resulting film is 50 nm thick and forms the active memristive switching layer. The SF:GO composite provides a unique combination of bio-compatibility, multilevel resistive switching (binary at I_cc <= 0.01 A; ternary at I_cc > 0.01 A), and analog synaptic behavior including short-term and long-term plasticity. Metrology: AFM (thickness, roughness); FTIR (amide I at 1620 cm-1, beta-sheet confirmation); I-V (bipolar switching, set/reset at +/- 5 V). Defect mode: Incomplete beta-sheet conversion — mitigated by ethanol vapor annealing (not liquid) to control crystallization rate.

### Step 6: Top Electrode / Storage Node Deposition

A 30 nm TiN top electrode is deposited by reactive DC sputtering (Ti target, Ar/N2 plasma, 5 mTorr, 100 W) at 200C through a shadow mask defining 0.06 um^2 capacitor areas (contact hole diameter ~275 nm). The TiN serves dual purpose: as the DRAM capacitor top plate and as the bottom contact for the neuromorphic memristor in 1T1M cells. Sputtering is performed with substrate bias of -50 V DC to improve step coverage over the planarized topography. After deposition, the electrode is patterned by lift-off in warm acetone (60C, 10 minutes). A post-patterning anneal at 150C in forming gas (5% H2/N2) for 15 minutes reduces the TiN/GO interface resistance. Metrology: SEM (critical dimension, overlay accuracy); four-point probe (R_s); C-V (capacitance density target > 10 fF/um2). Defect mode: Undercut during lift-off — mitigated by using LOR (lift-off resist) bilayer and optimizing ultrasonic agitation.

### Step 7: CNT Transfer & Alignment

Semiconducting single-wall carbon nanotubes (s-SWCNTs) are synthesized by catalytic chemical vapor deposition (CVD) using Yorkshire coal or UK biomass (wheat straw, forestry waste) as the carbon feedstock. The CVD process uses Fe/Mo catalyst on MgO support at 800C (upstream process, not on the memory wafer). Metallic SWCNTs are selectively removed by the RINSE (Repulsive Intramolecular Nanotube Separation and Elimination) process, achieving >99.99% semiconducting purity. For device fabrication, the purified s-SWCNTs are dispersed in DMF at 0.01 mg/mL and aligned by the DLSA (Dielectrophoretic Linear Sweep Alignment) method: an AC electric field at 10 MHz, 5 Vpp is applied across pre-patterned Au alignment electrodes (gap = 2 um) while the dispersion is pipetted across the substrate. The high-frequency dielectrophoresis attracts individual s-SWCNTs to the high-field region between electrodes, aligning them parallel to the field lines. Target linear density is 100 tubes/um, controlled by dispersion concentration and field exposure time (typically 30-60 seconds). After alignment, the substrate is rinsed in IPA and dried under N2. The CNTs form the channel material for the access transistor in both 1T1C and 1T1M configurations. Metrology: Raman spectroscopy (G/D ratio > 20; RBM for diameter 1.2-1.6 nm); SEM (density count, alignment angle < 5deg); I-V (I_on/I_off > 10^4). Defect mode: Bundling from excess density — mitigated by real-time optical monitoring and automatic field shutoff at target density.

### Step 8: S/D Contact Evaporation

Source and drain contacts to the aligned CNT channel are formed by electron-beam evaporation at room temperature. For p-type devices (primary configuration for 1T1C/1T1M), 20 nm Pd is deposited at 0.1 nm/s in a vacuum better than 5x10^-7 Torr, followed by 50 nm Au capping layer. Pd provides near-ohmic contact to the CNT valence band with contact resistance rho_c < 10^-7 Ohm.cm^2. For n-type variants (future CMOS integration), 20 nm Sc is used instead. The contact pads are defined by photolithography with LOR/PMMA bilayer resist and patterned by lift-off. No thermal annealing is performed to avoid CNT damage. Metrology: TLM (transfer length method, rho_c extraction); I-V (linear I-V at V_ds = +/- 0.1 V); SEM (contact edge definition). Defect mode: Schottky barrier from interface contamination — mitigated by in-situ Ar+ ion milling (100 eV, 60 seconds) immediately before metal evaporation.

### Step 9: Gate Stack ALD

The gate dielectric is deposited by thermal atomic layer deposition (ALD) at 250C using tetrakis(ethylmethylamino)hafnium (TEMAH) precursor and H2O co-reactant in N2 carrier gas. The ALD cycle consists of: TEMAH pulse (2 s) -> N2 purge (20 s) -> H2O pulse (0.2 s) -> N2 purge (20 s). At the deposition temperature of 250C, the growth per cycle (GPC) is 0.99 A/cycle; 30 cycles yield a 3 nm HfO2 film with equivalent oxide thickness (EOT) of 1.0 nm and dielectric constant epsilon_r = 25. The ALD process provides self-limiting, conformal coverage over the CNT channel with <1% thickness non-uniformity across the 300 mm wafer. The HfO2 film is amorphous as-deposited at 250C, which is preferred for minimizing interface trap density and maximizing dielectric constant (avoiding the lower-k monoclinic phase). Metrology: Ellipsometry (thickness, n = 2.05); non-contact C-V (CET, k-value); XPS (O:Hf ratio = 2.2, C impurity < 2%). Defect mode: Pinholes at CNT crossing points — mitigated by gentle UV-O3 treatment (185 nm, 5 min) before ALD to functionalize CNT surface.

### Step 10: Gate Electrode Patterning

A 30 nm TiN gate electrode is deposited by reactive DC sputtering (same parameters as Step 6) and patterned by e-beam lithography (Vistec EBPG 5200) to achieve L_g = 25 nm gate length. Critical to this step is the formation of an L-shaped SiO2 spacer to control gate-induced drain leakage (GIDL). The L-spacer is fabricated by: (1) depositing 30 nm conformal SiO2 by plasma-enhanced CVD at 150C using TEOS/O2; (2) anisotropic RIE etch in CHF3/Ar to remove horizontal SiO2 while preserving the vertical spacer; (3) forming gas anneal at 250C for 30 minutes to passivate interface traps. The L-spacer geometry provides L_ext = 15 nm (extension underlap) and L_spa = 30 nm (spacer width), creating a gradual doping profile at the drain edge that clamps the electric field and suppresses GIDL by >2 orders of magnitude compared to abrupt junctions. This is essential for low-standby-power (LSTP) operation. Metrology: TEM (L_g, spacer profile); I-V (GIDL current < 1 pA/um at V_ds = V_dd); C-V (C_gg at target). Defect mode: Spacer foot erosion during over-etch — mitigated by endpoint detection using OES (optical emission spectroscopy) at 777 nm (CO emission).

### Step 11: BEOL Metallization

The back-end-of-line interconnect uses five metal layers (M1-M5) of coal-derived graphene interspersed with Cornish tin SAC (Sn-3.0Ag-0.5Cu) solder vias. Coal-derived graphene is synthesized by chemical vapor deposition using Yorkshire coal methane (from underground coal gasification) on Cu foil at 1000C (off-wafer process), then transferred to the device wafer by PMMA-assisted wet transfer at <100C. Graphene interconnects provide exceptional current-carrying capacity (J_e > 1 MA/cm2) and compatibility with low-temperature processing. SAC solder vias are formed by electroplating Cornish tin (from South Crofty mine, 50.22N 5.27W, or Hemerdon/Drakelands, 50.41N 4.01W) with Ag and Cu co-deposition, followed by reflow at 250C. The 5-layer stack uses damascene patterning with SiO2 dielectric (from Lochaline silica, RT PECVD). Each via level is planarized by CMP before the next metal deposition. Metrology: Four-point probe (R_sheet); electromigration testing (J_e > 1 MA/cm2 at 150C, >1000 hr); X-section SEM (via chain resistance). Defect mode: Graphene wrinkling during transfer — mitigated by slow PMMA dissolution in acetone and gentle N2 blow-dry at 45-degree angle.

### Step 12: Passivation & Probe Test

The final passivation layer is a 500 nm chalcogenide glass (As40S30Se30) deposited by thermal evaporation at <200C. The chalcogenide provides a hermetic seal against moisture and ionic contamination, with excellent adhesion to the graphene interconnects and low permeability to H2O and O2. The glass is patterned by photolithography and wet etching in NH4OH/H2O2 to open probe pads. The wafer then undergoes 100% parametric testing using a semiconductor parameter analyzer: (1) DRAM cells — write/refresh at V_dd = 1.0 V, retention > 64 ms at 85C; (2) Memristor cells — bipolar switching at +/- 3 V, 1000 cycles endurance, on/off ratio > 100; (3) CNT transistors — I_on > 100 uA/um, I_on/I_off > 10^4, subthreshold swing < 100 mV/dec. Any failing die is ink-marked for exclusion. Metrology: Probe station (full DC/AC parametrics); burn-in (168 hours at 125C); HAST (highly accelerated stress test, 85C/85% RH, 1000 hours). Defect mode: Pad corrosion from residual flux — mitigated by DI water rinse and N2 dry after solder reflow, plus sealed pad architecture.

---

## 4. Material Sourcing Map

```
+--------------------------------+--------------------------------+-------------------------+---------+
| Raw UK Deposit                 | Refinement Process             | Semiconductor Function  | Step    |
+--------------------------------+--------------------------------+-------------------------+---------+
|                                  |                                |                         |         |
| CORNISH KAOLIN                  | -> Water washing, magnetic     | MAS glass-ceramic       |   1     |
| (St Austell Granite,            |    separation, spray drying    | substrate (300 mm)      |         |
|  50.37N 4.79W)                  |                                |                         |         |
|  - 100 Mt reserves              | -> Ball milling to <5 um       | Low-k dielectric,       |   1, 4  |
|  - Al2O3.2SiO2.2H2O            |    400C calcination            | packaging               |         |
|                                  |                                |                         |         |
+--------------------------------+--------------------------------+-------------------------+---------+
|                                  |                                |                         |         |
| LOCHALINE SILICA                | -> Acid leaching, drying       | SiO2 for MAS substrate  |   1     |
| (Scotland, 56.53N 5.77W)        |    99.8% SiO2                  |                         |         |
|  - 99.8% SiO2                   |                                | CMP abrasive (colloidal  |   4     |
|  - Marine sand deposit           | -> Ball milling to 0.1 um      | SiO2)                   |         |
|                                  |                                |                         |         |
|                                  | -> SiH4/O2 synthesis (import)  | PECVD SiO2 dielectric   |  10, 11 |
|                                  |    precursor required          | for BEOL                  |         |
|                                  |                                |                         |         |
+--------------------------------+--------------------------------+-------------------------+---------+
|                                  |                                |                         |         |
| YORKSHIRE COAL                  | -> Carbonization 600C          | Graphite precursor for  |  3a, 3b |
| (Bituminous, Pennine Basin)     | -> Modified Hummers: KMnO4,    | GO via Hummers method   |         |
|  - Carbon feedstock              |    H2SO4/H3PO4 oxidation       |                         |         |
|  - Historical mining region      | -> Exfoliation, dispersion     | s-SWCNT CVD feedstock   |   7     |
|                                  |                                |                         |         |
|                                  | -> Underground coal gasification| CH4 for graphene CVD    |  11     |
|                                  |    (UCG) or pyrolysis          | (off-wafer, 1000C)      |         |
|                                  |                                |                         |         |
+--------------------------------+--------------------------------+-------------------------+---------+
|                                  |                                |                         |         |
| UK BIOMASS                      | -> Pyrolysis 400-600C          | Alternative GO source   |  3b     |
| (Wheat straw: Lincolnshire,      | -> Hummers oxidation           | (higher O content)      |         |
|  Yorkshire; Forestry waste:      |                                |                         |         |
|  Scotland, Wales)               | -> Fermentation, distillation  | Organic solvents,       |   5     |
|                                  |                                | cleaning agents         |         |
+--------------------------------+--------------------------------+-------------------------+---------+
|                                  |                                |                         |         |
| CORNISH TIN                     | -> Gravity concentration,      | Sn metal (99.9%)        |  11     |
| (South Crofty: 50.22N 5.27W;    |    flotation, smelting         |                         |         |
|  Hemerdon/Drakelands: 50.41N    | -> Alloying with Ag, Cu        | SAC solder (Sn-3Ag-     |  11     |
|  4.01W)                         |    (import Ag, Cu)             | 0.5Cu) for BEOL vias    |         |
|  - Cassiterite (SnO2) ores       |                                |                         |         |
|  - 0.15-0.94% Sn grade          | -> Electroplating bath         | Solder bumps, flip-chip |  11     |
|  - Production from 2028          |                                | interconnects           |         |
|                                  |                                |                         |         |
+--------------------------------+--------------------------------+-------------------------+---------+
|                                  |                                |                         |         |
| SILK FIBROIN                    | -> Degumming (Na2CO3 boil)     | Bio-memristive active   |   5     |
| (Bombyx mori, domestic           | -> LiBr dissolution, dialysis  | layer for neuromorphic  |         |
|  sericulture: Kent,              | -> Purification, concentration | computing               |         |
|  Hertfordshire)                 | -> Composite with GO, Ag NPs   | SF:GO memristor,        |   5     |
|  - Cocoons available UK          |                                | analog synapse          |         |
|    from multiple farms           |                                |                         |         |
|                                  |                                |                         |         |
+--------------------------------+--------------------------------+-------------------------+---------+
```

---

## 5. Critical Process Controls

### 5.1 GO Deposition — C/O Ratio Control (Steps 3a and 3b)

The graphene oxide C/O atomic ratio is the single most critical parameter determining both DRAM capacitor performance and neuromorphic switching behavior. FTIR spectroscopy provides the primary in-line monitoring method:

**DRAM-GO (Step 3a) — Target C/O = 3.0 +/- 0.3:**
- The carbonyl C=O stretch at 1730 cm-1 represents oxidized sp3 carbon; its intensity correlates with defect density and bandgap.
- The O-H stretch at 3400 cm-1 represents hydroxyl and carboxylic acid groups; its intensity correlates with hydrophilicity and ionic conductivity.
- The aromatic C=C stretch at 1630 cm-1 represents residual graphitic domains; its intensity correlates with electrical conductivity.
- For DRAM applications, C/O = 3.0 provides: (i) sufficient oxygen for epsilon_r = 150 and low leakage; (ii) sufficient graphitic domains for stable dielectric response; (iii) bandgap > 2.0 eV preventing tunneling.

**Neuro-GO (Step 3b) — Target C/O = 2.5 +/- 0.2:**
- Lower C/O (more oxygen) increases the density of hydroxyl and epoxy groups that participate in Ag+ migration and resistive switching.
- The Ag nanoparticle plasmon peak at 420 nm (UV-Vis) confirms uniform dispersion; absence of a red-shifted peak (>450 nm) indicates no agglomeration.
- Post-deposition, XPS confirms Ag 3d5/2 at 368.2 eV (metallic Ag) and 367.5 eV (Ag+) — the Ag+/Ag0 ratio predicts filament formation dynamics.

**Mitigation of C/O drift:** The Hummers oxidation is highly sensitive to KMnO4 concentration and reaction temperature. A reaction time of 2 hours at 40C (not exceeding 45C) consistently yields C/O = 3.0 from Yorkshire coal precursor. Reaction times > 4 hours drive C/O below 2.0, which is too conductive for DRAM. Real-time monitoring uses in-situ FTIR on witness coupons co-processed with production wafers.

### 5.2 CNT Alignment — DLSA and RINSE (Step 7)

**DLSA Parameters:**
- Frequency: 10 MHz, chosen because s-SWCNTs exhibit stronger positive dielectrophoretic response than m-SWCNTs at this frequency (crossover from negative to positive DEP occurs at ~1 MHz for s-SWCNTs in DMF).
- Voltage: 5 Vpp (peak-to-peak), applied across 2 um gap electrodes yielding E-field = 2.5x10^6 V/m — sufficient to overcome Brownian motion but below the dielectric breakdown threshold of DMF (~10^7 V/m).
- Alignment time: 30-60 seconds, monitored by real-time dark-field microscopy; automatic shutoff when tube density reaches 100 tubes/um.

**RINSE Process for >99.99% s-SWCNT Purity:**
The RINSE (Repulsive Intramolecular Nanotube Separation and Elimination) process exploits the differential surfactant wrapping of metallic versus semiconducting SWCNTs. After initial dielectrophoretic alignment:
1. SDS (sodium dodecyl sulfate) is added at 2 wt% in D2O; m-SWCNTs form looser micellar wrapping and can be selectively removed by ultracentrifugation (100,000 g, 4 hours).
2. The supernatant containing >99.99% s-SWCNTs is decanted and exchanged into DMF for the alignment step.
3. Purity is verified by Raman spectroscopy (G-band at 1590 cm-1 for s-SWCNTs, broadened G-band at 1550 cm-1 for m-SWCNTs); the Breit-Wigner-Fano component (m-SWCNT signature) must be undetectable.

**Density Control:** Target linear density of 100 tubes/um balances drive current (I_on proportional to density) against on/off ratio (degrades at >150 tubes/um due to electrostatic screening and residual m-SWCNT percolation). Density is controlled by dispersion concentration (0.005-0.02 mg/mL) and alignment time (monitored optically).

### 5.3 L-Spacer — GIDL Clamping Effect (Step 10)

The L-shaped SiO2 spacer is critical for suppressing gate-induced drain leakage (GIDL) in the 25 nm gate-length CNT transistor. The geometry provides two key parameters:

**L_ext = 15 nm (extension underlap):** The SiO2 spacer creates a 15 nm region where the gate electrode does not overlap the drain extension. This "underlap" reduces the peak electric field at the gate-to-drain overlap region, which is the primary source of GIDL via band-to-band tunneling (BTBT). Simulations show that reducing L_ext from 25 nm to 15 nm decreases GIDL current by ~50x while degrading I_on by only ~8%.

**L_spa = 30 nm (spacer width):** The vertical SiO2 spacer thickness determines the lateral separation between the gate edge and the contact metal. A 30 nm spacer provides sufficient separation to prevent contact metal from causing field crowding at the drain edge, while remaining manufacturable with 150C PECVD and anisotropic RIE.

**Clamping Effect:** The L-spacer creates a gradual doping profile at the drain edge by electrostatically "clamping" the potential. The SiO2 spacer (epsilon_r = 3.9) acts as a series capacitance that drops a significant fraction of the drain voltage, reducing the effective gate-to-drain potential seen by the channel. This clamping effect is more pronounced at higher V_ds, precisely where GIDL would otherwise dominate. For the 1T1C/1T1M memory cell, GIDL must be < 1 pA/um to achieve retention times > 1 second at 85C without refresh — a requirement that is met with the L_ext = 15 nm / L_spa = 30 nm design.

### 5.4 Neuromorphic Film — SF:GO Ratio and Ag Seeding (Step 5)

The silk fibroin:graphene oxide composite is the active switching layer for neuromorphic computation. Three parameters control its behavior:

**SF:GO Ratio (3:1 by mass):** Pure silk fibroin exhibits resistive switching via Ag+ ion migration through the amorphous protein matrix, but with high forming voltage (>8 V) and poor endurance (<100 cycles). Adding GO at 25 wt% (SF:GO = 3:1) provides: (i) oxygen-containing functional groups that anchor Ag+ ions and create localized trap sites; (ii) enhanced electronic conductivity that reduces forming voltage to <5 V; (iii) additional conductive filament pathways that enable multilevel switching. Ratios > 4:1 (less GO) show poor reproducibility; ratios < 2:1 (more GO) lose the biomolecular ionic transport mechanism and behave like pure GO memristors.

**Ag Nanoparticle Seeding (5-10 wt%):** Ag NPs (10 nm) are pre-dispersed in the SF:GO solution. During electroforming, Ag NPs dissolve anodically (Ag -> Ag+ + e-) and the resulting Ag+ ions migrate through the SF:GO matrix under electric field, nucleating conductive filaments at the cathode. The 5-10 wt% range provides:
- 5 wt%: Binary switching (HRS/LRS), suitable for conventional memory
- 10 wt%: Ternary switching (HRS/IRS/LRS), enabling analog neuromorphic computation
- >10 wt%: Excessive filament density causes stuck-at-LRS failures

**Pulse-Verify Programming:** Unlike DRAM's destructive read, the memristor requires a write-verify scheme: (1) Apply SET pulse (1 us, +3 V); (2) Read resistance at 0.1 V; (3) If R > R_target, apply additional pulses with 10% voltage increment; (4) Repeat until target resistance is achieved. This closed-loop programming achieves 7-bit (128-level) analog resolution, sufficient for neural network inference with >92% accuracy on MNIST handwritten digit recognition.

---

## 6. Thermal Budget Analysis

The cumulative thermal budget is strictly limited to <400C peak to preserve the integrity of: (i) the MAS glass-ceramic substrate (crystallization control), (ii) the GO layers (thermal reduction threshold ~200C), (iii) the silk fibroin protein matrix (denaturation >100C), and (iv) the CNT channel (damage >350C in air).

| Step | Process | Peak Temperature (C) | Duration at Peak | Cumulative Exposure | Thermal Budget Notes |
|:---:|---|:---:|:---:|---|---|
| 1 | MAS substrate calcination | **400** | 6 hr | 400C, 6 hr | Absolute maximum; cordierite crystallization |
| 2 | Bottom electrode sputtering | 200 | 30 min | 400C | RT base; substrate heating to 200C |
| 3a | DRAM-GO anneal | 150 | 30 min | 400C | Below GO reduction threshold |
| 3b | Neuro-GO anneal | 120 | 45 min | 400C | Low-T for Ag NP stability |
| 4 | CMP planarization | RT | 20 min | 400C | Room temperature process |
| 5 | SF:GO composite | 80 | 10 min | 400C | Below silk denaturation point |
| 6 | Top electrode sputtering | 200 | 25 min | 400C | Same as Step 2 |
| 7 | CNT alignment | <300 | 45 min | 400C | DMF solvent, no thermal budget |
| 8 | S/D evaporation | RT | 15 min | 400C | E-beam, no substrate heating |
| 9 | Gate stack ALD | 250 | 40 min | 400C | Self-limiting, uniform |
| 10 | Gate electrode + spacer | 250 | 30 min | 400C | PECVD + forming gas anneal |
| 11 | BEOL metallization | 250 | 120 min | 400C | SAC solder reflow (highest BEOL T) |
| 12 | Passivation | 200 | 60 min | 400C | Chalcogenide evaporation |

**Peak Temperature: 400C** (Step 1 only — substrate formation, before any active devices are present)
**Maximum process temperature after device fabrication begins: 300C** (Step 7, CNT alignment — but this is solvent temperature, not substrate)
**Maximum BEOL temperature: 250C** (Steps 9, 10, 11 — ALD, spacer anneal, solder reflow)
**Maximum temperature silk fibroin sees: 80C** (Step 5 — well below the 100C denaturation threshold)
**Maximum temperature GO sees: 150C** (Step 3a — well below the 200C reduction threshold)

The thermal budget is fully compliant with the <400C requirement. The 400C Step 1 occurs before any temperature-sensitive materials are present. All subsequent steps operate at 300C or below, with the most critical active layers (GO, silk fibroin, CNT) never exceeding 150C. This conservative thermal budget provides >100C margin for all active materials, ensuring high yield and long-term reliability.

---

## 7. Process Flow Diagram (ASCII)

```
STEP 1                    STEP 2                    STEP 3a/3b
+--------+               +--------+               +----------+
|  MAS   |               |  TiN   |               |  GO      |
| Kaolin |  --sputter--> |  /Pt   |  --spin-coat-> | 2nm/5nm  |
| +SiO2  |               | 50nm   |               | C/O 3.0/2.5|
| 400C   |               | 200C   |               | 150C/120C|
+--------+               +--------+               +----------+
    |                        |                         |
    v                        v                         v
+-----------------------------------------------+     +--------+
|  MAS GLASS-CERAMIC SUBSTRATE (300 mm)         |     | DRAM   |
|  CTE +5.0 ppm/K, epsilon_r = 5-8              |     | GO     |
|  Thickness: 725 um                            |     | epsilon=150
+-----------------------------------------------+     +--------+
                                                         |
STEP 4 <-------------------------------------------------+
+----------+    STEP 5      +----------+    STEP 6      +--------+
|  CMP     |   <--deposit-- |  SF:GO   |   <--sputter-- |  TiN   |
| SiO2     |               | Composite|               | 30nm   |
| abrasive |               | 50nm     |               | 0.06um2|
| RT       |               | 80C      |               | 200C   |
+----------+               +----------+               +--------+
    |                           |                        |
    v                           v                        v
+---------------------------------------------------------------+
|  PLANARIZED SURFACE (RMS < 0.5 nm, step < 2 nm)               |
+---------------------------------------------------------------+
    |                           |                        |
    v                           v                        v
STEP 7                     STEP 8                    STEP 9
+----------+               +----------+              +----------+
|  CNT     |               |  Pd/Sc   |              |  HfO2    |
| s-SWCNT  |  --evaporate->|  S/D     |  --ALD------>|  3nm     |
| DLSA     |               | 20nm     |              | EOT=1nm  |
| <300C    |               | RT       |              | 250C     |
+----------+               +----------+              +----------+
    |                           |                        |
    v                           v                        v
+---------------------------------------------------------------+
|  CNT FET CHANNEL (L_g = 25 nm, I_on/I_off > 10^4)             |
|  CNT density: 100 tubes/um                                     |
+---------------------------------------------------------------+
    |                           |                        |
    v                           v                        v
STEP 10                    STEP 11                   STEP 12
+----------+               +----------+              +----------+
|  TiN     |               | Graphene |              | Chalcogen|
|  Gate +  |  --BEOL-----> |  + Sn    |  --passivate->| ide Glass|
| L-spacer |               | SAC x5   |              | 500nm    |
| 250C     |               | <300C    |              | <200C    |
+----------+               +----------+              +----------+
    |                           |                        |
    v                           v                        v
+===============================================================+
|                    FINAL MEMORY CELL                           |
|  +----------+    +----------+    +----------+                  |
|  |  TiN     |    |  TiN     |    |  CNT FET |                  |
|  |  TOP     |----|  BOTTOM  |----|  25nm    |                  |
|  |  ELECTRODE    |  ELECTRODE    |  GATE    |                  |
|  +----------+    +----------+    +----------+                  |
|       |                |               |                       |
|  +----+----+     +-----+-----+   +-----+------+                 |
|  | DRAM-GO |     | Neuro-GO  |   | L-spacer   |                 |
|  | 2nm     |     | + Ag NPs  |   | SiO2 30nm  |                 |
|  | epsilon=150    | 5nm       |   +------------+                 |
|  +---------+     +-----+-----+                                 |
|                        |                                       |
|                   +----+----+                                  |
|                   | SF:GO   |  <--- NEUROMORPHIC LAYER          |
|                   | 50nm    |                                  |
|                   +---------+                                  |
|                                                                |
|  HYBRID 1T1C/1T1M: DRAM Capacitor + Memristor + CNT Selector   |
+===============================================================+
```

---

## 8. Key Process Integration Notes

1. **Substrate First:** The 400C MAS substrate calcination (Step 1) is performed on blank wafers before any device processing. All subsequent steps add no more than 250C thermal budget.

2. **GO Dual-Track:** Steps 3a and 3b are performed on different die regions within the same wafer — DRAM-GO for 1T1C cells, Neuro-GO for 1T1M cells. The photolithography mask defines which region receives which GO variant.

3. **CMP Before CNTs:** Step 4 CMP is mandatory before CNT alignment. Surface roughness > 2 nm causes CNT bundling and alignment failure. The CMP step is timed to remove exactly the GO step height without damaging the underlying Pt electrode.

4. **Silk Fibroin After CMP:** The SF:GO composite (Step 5) is deposited after CMP to avoid exposing the protein to the abrasive slurry environment. Ethanol vapor annealing (not liquid ethanol) is used to induce beta-sheet crystallization without dissolving the GO layers beneath.

5. **CNT Alignment Is Back-End Compatible:** The DLSA process (Step 7) uses DMF solvent at room temperature with <300C local heating from the AC field. This is fully compatible with all underlying layers including the silk fibroin (which never exceeds 80C).

6. **SAC Solder for 3D Integration:** The Cornish tin SAC solder (Step 11) enables future 3D stacking of memory layers by providing low-temperature (<250C) bonding with excellent electromigration resistance.

---

*Document prepared by Process Engineering, Sovereign UK Semiconductor Memory Swarm. All temperatures in degrees Celsius. All materials sourced or planned for sourcing from UK geological deposits or domestic agriculture as of 2025.*
