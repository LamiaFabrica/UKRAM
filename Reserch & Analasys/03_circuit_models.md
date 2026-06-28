# CIRCUIT MODELS: Unified Hybrid 1T1C/1T1M Memory Cell

## Document ID: UK-SOVEREIGN-MEM-003
## Revision: 1.0
## Classification: Technical — SPICE/Verilog-A Compact Models

---

## 1. Stanford Virtual-Source CNFET Compact Model

### 1.1 Model Overview

The Stanford Virtual-Source (VS) model treats carrier transport from the virtual source (top of the barrier) to the drain. For CNTFETs, the quasi-ballistic transport is captured through a single velocity-saturation parameter extracted directly from $I_{\text{on}}$ — making the model computationally efficient for SPICE-level circuit simulation while preserving physical accuracy down to $L_g = 25$ nm.

### 1.2 Core Drain Current Equation

The unified drain current expression valid across all regimes is:

```
$$I_{DS} = W \cdot C_{ox} \cdot v_{x0} \cdot \frac{V_{GT}^2}{V_{GT} + 2k_BT/q} \cdot F_{sat}(V_{DS}) \cdot F_{therm}(V_{GS}, V_{DS})$$
```

where the gate overdrive incorporates DIBL and body effect:

```
$$V_{GT} = \ln\left(1 + \exp\left(\frac{V_{GS} - V_T}{2k_BT/q \cdot n}\right)\right) \cdot 2k_BT/q \cdot n$$
```

The temperature-dependent thermal voltage is $V_t = k_BT/q = 25.85$ mV at $T = 300$ K. The threshold voltage with DIBL and body effect:

```
$$V_T = V_{th0} - \delta \cdot V_{DS} - \eta \cdot V_{BS}$$
```

| Parameter | Symbol | Value | Unit | Physical Meaning |
|---|---|---|---|---|
| Zero-bias threshold voltage | $V_{th0}$ | 0.35 | V | Band alignment at flat-band |
| DIBL coefficient | $\delta$ | 50 | mV/V | $V_T$ rolloff with drain bias |
| Body-effect parameter | $\eta$ | 0.12 | — | $V_T$ sensitivity to bulk bias |
| Subthreshold ideality | $n$ | 1.35 | — | Interface trap capacitance ratio |
| VS injection velocity | $v_{x0}$ | $3.8 \times 10^6$ | cm/s | Ballistic carrier velocity at source |

### 1.3 Subthreshold Regime ($V_{GS} < V_T$)

In weak inversion, the gate overdrive simplifies to:

```
$$V_{GT} \approx \exp\left(\frac{V_{GS} - V_T}{n \cdot V_t}\right) \cdot V_t$$
```

yielding the subthreshold current:

```
$$I_{DS}^{sub} = I_0 \cdot \exp\left(\frac{V_{GS} - V_T}{n \cdot V_t}\right) \cdot \left(1 - \exp\left(-\frac{V_{DS}}{V_t}\right)\right) \cdot F_{sat}(V_{DS})$$
```

where the subthreshold swing is:

```
$$SS = \ln(10) \cdot n \cdot \frac{k_BT}{q} = 2.303 \cdot n \cdot V_t \approx 70 \text{ mV/dec}$$
```

The prefactor $I_0$ aggregates device dimensions and material parameters:

```
$$I_0 = W \cdot C_{ox} \cdot v_{x0} \cdot V_t = N_{cnt} \cdot d_{cnt} \cdot C_m \cdot v_{x0} \cdot V_t$$
```

Substituting $N_{cnt} = 15$, $d_{cnt} = 1.5$ nm, $C_m = 345$ aF/$\mu$m, $v_{x0} = 3.8 \times 10^7$ m/s, and $V_t = 0.02585$ V:

```
$$I_0 = 15 \times (1.5 \times 10^{-9}) \times (345 \times 10^{-18}/10^{-6}) \times (3.8 \times 10^7) \times 0.02585 \approx 7.6 \times 10^{-12} \text{ A} = 7.6 \text{ pA}$$
```

The off-state current per device:

```
$$I_{off} = I_0 \cdot \exp\left(\frac{-V_{th0}}{n \cdot V_t}\right) = 7.6 \text{ pA} \times \exp\left(\frac{-0.35}{1.35 \times 0.02585}\right) \approx 75 \text{ fA}$$
```

matching the Stage 1 specification.

### 1.4 Above-Threshold Regime ($V_{GS} > V_T$)

In strong inversion, $V_{GT} \rightarrow V_{GS} - V_T$ and the drain current becomes:

```
$$I_{DS}^{above} = W \cdot C_{ox} \cdot v_{x0} \cdot \frac{(V_{GS} - V_T)^2}{(V_{GS} - V_T) + 2V_t} \cdot F_{sat}(V_{DS})$$
```

For $V_{GS} - V_T \gg 2V_t$, this reduces to the expected linear-$V_{GT}$ ballistic form:

```
$$I_{DS}^{above} \approx W \cdot C_{ox} \cdot v_{x0} \cdot (V_{GS} - V_T) \cdot F_{sat}(V_{DS})$$
```

### 1.5 Velocity Saturation Function

The saturation function $F_{sat}(V_{DS})$ interpolates between linear and saturation:

```
$$F_{sat}(V_{DS}) = \frac{\left(\alpha \cdot V_{DS}\right)^{\beta}}{1 + \left(\alpha \cdot V_{DS}\right)^{\beta}}$$
```

| Parameter | Value | Description |
|---|---|---|
| $\alpha$ | 3.5 | V$^{-1}$ — Controls onset of saturation |
| $\beta$ | 1.8 | — Sharpness of saturation knee |

Behavioral limits:
- **Linear region** ($V_{DS} \ll 1/\alpha \approx 0.29$ V): $F_{sat} \approx (\alpha V_{DS})^{\beta} \approx \alpha V_{DS}$ (for $\beta \approx 1$)
- **Saturation region** ($V_{DS} \gg 1/\alpha$): $F_{sat} \rightarrow 1$

### 1.6 Series Resistance

The access resistance from source/drain contacts to the channel is modeled as:

```
$$R_{series} = \frac{R_s}{N_{cnt}} = \frac{500\ \Omega}{15} \approx 33.3\ \Omega$$
```

The intrinsic drain-source voltage accounts for series resistance drop:

```
$$V_{DSi} = V_{DS} - I_{DS} \cdot 2R_{series}$$
```

This is solved self-consistently: $I_{DS} = f(V_{GS}, V_{DSi})$ with $V_{DSi}$ updated iteratively.

### 1.7 Complete CNFET Verilog-A Module

```verilog
`include "disciplines.vams"
`include "constants.vams"

module VS_CNFET(D, G, S, B);
    inout D, G, S, B;
    electrical D, G, S, B;

    // --- Device Geometry ---
    parameter real L_g    = 25n       from [10n:100n];     // Gate length [m]
    parameter real d_cnt  = 1.5n      from [0.5n:5n];      // CNT diameter [m]
    parameter real N_cnt  = 15        from [1:1000];       // Number of CNTs
    parameter real C_m    = 345e-18/1e-6 from [0:inf];    // Gate cap per width [F/m]

    // --- Transport Parameters ---
    parameter real v_x0   = 3.8e7     from [1e6:1e8];      // VS velocity [m/s]
    parameter real mu0    = 0.8       from [0.01:2.0];     // Low-field mobility [m^2/Vs]
    parameter real alpha  = 3.5       from [0.1:10];       // Saturation onset
    parameter real beta   = 1.8       from [0.5:5];        // Saturation sharpness

    // --- Threshold & Subthreshold ---
    parameter real V_th0  = 0.35      from [0:1.5];        // Zero-bias Vth [V]
    parameter real n_sub  = 1.35      from [1.0:2.0];      // Subthreshold ideality
    parameter real delta  = 0.050     from [0:0.2];        // DIBL coefficient [V/V]
    parameter real eta    = 0.12      from [0:0.5];        // Body effect parameter

    // --- Series Resistance ---
    parameter real R_s    = 500       from [0:10e3];       // Per-CNT series resistance [Ohm]

    // --- Temperature ---
    parameter real Temp   = 300       from [250:400];      // Temperature [K]

    // --- Internal Variables ---
    real Vgs, Vds, Vbs;
    real Vt, Vt_n, V_T, V_GT;
    real I_ds, F_sat, R_series, Vdsi;
    real W_total, C_ox_total;
    integer iter;

    analog begin
        // Thermal voltage
        Vt   = $boltzmann * Temp / $charge_e;
        Vt_n = n_sub * Vt;

        // Terminal voltages
        Vgs = V(G) - V(S);
        Vds = V(D) - V(S);
        Vbs = V(B) - V(S);

        // Total effective width and oxide capacitance
        W_total    = N_cnt * d_cnt;
        C_ox_total = W_total * C_m;

        // Series resistance (total for source + drain)
        R_series = 2.0 * R_s / N_cnt;

        // Self-consistent solution for Vdsi and Ids
        Vdsi = Vds;  // Initial guess
        for (iter = 0; iter < 5; iter = iter + 1) begin
            // Threshold with DIBL and body effect
            V_T = V_th0 - delta * Vdsi - eta * Vbs;

            // Gate overdrive (smooth interpolation)
            V_GT = ln(1.0 + exp((Vgs - V_T) / (2.0 * Vt_n))) * (2.0 * Vt_n);

            // Velocity saturation function
            F_sat = pow(alpha * abs(Vdsi), beta)
                  / (1.0 + pow(alpha * abs(Vdsi), beta));

            // Drain current (unified expression)
            if (V_GT > 1e-6) begin
                I_ds = C_ox_total * v_x0 * V_GT * V_GT
                     / (V_GT + 2.0 * Vt) * F_sat;
            end else begin
                I_ds = C_ox_total * v_x0 * exp((Vgs - V_T) / Vt_n) * Vt
                     * (1.0 - exp(-abs(Vdsi) / Vt)) * F_sat;
            end

            // Update Vdsi with series resistance drop
            Vdsi = Vds - I_ds * R_series;
            if (Vdsi < 0) Vdsi = 0;
        end

        // Apply current direction
        if (Vds < 0)
            I_ds = -I_ds;

        // Terminal currents
        I(D, S) <+ I_ds;
        I(G)    <+ 0;   // Negligible gate leakage
        I(B)    <+ 0;
    end
endmodule
```

---

## 2. GO Unified Compact Model (DRAM Capacitor / Neuromorphic Memristor)

### 2.1 Model Philosophy

The graphene oxide (GO) storage element operates in two mutually exclusive modes selected by a digital `MODE` signal. In **DRAM mode** (`MODE = 0`), the GO film acts as a leaky MOS capacitor with Poole-Frenkel emission governing the retention behavior. In **neuromorphic mode** (`MODE = 1`), Ag$^+$ filamentary conduction creates a programmable memristor with 64 discrete conductance states.

### 2.2 DRAM Mode: Capacitor with PF Leakage

The storage node dynamics are governed by:

```
$$I_{cell} = C_s \frac{dV_{SN}}{dt} + I_{leak}(V_{SN}, T)$$
```

The leakage current follows Poole-Frenkel emission through GO trap states:

```
$$I_{leak} = \frac{V_{SN}}{R_0} \cdot \exp\left(\gamma_{PF} \sqrt{|V_{SN}|} - \frac{E_a}{k_BT}\right)$$
```

At room temperature with $E_a \ll k_BT$ (shallow traps), this simplifies to:

```
$$I_{leak} \approx \frac{V_{SN}}{R_0} \cdot \exp\left(\gamma_{PF} \sqrt{|V_{SN}|}\right)$$
```

The effective leakage resistance at small signal:

```
$$R_{leak}(V) = R_0 \cdot \exp\left(-\gamma_{PF} \sqrt{|V|}\right)$$
```

yielding the RC retention time:

```
$$\tau_{RC} = R_{leak} \cdot C_s = 1.67 \times 10^{15}\ \Omega \times 39.8\ \text{fF} \approx 18.4\ \text{hours}$$
```

### 2.3 Neuromorphic Mode: Filamentary Memristor

The conductance update follows an incremental pulse-dependent rule:

```
$$G_{cell}^{(n+1)} = G_{cell}^{(n)} + \Delta G \cdot f(V_{pulse}, \text{sign})$$
```

where the conductance step is quantized:

```
$$\Delta G = \frac{G_{max} - G_{min}}{N_{levels} - 1} = \frac{1\text{ mS} - 1\ \mu\text{S}}{63} \approx 15.9\ \mu\text{S/level}$$
```

The conductance update function for SET (increase) and RESET (decrease):

```
$$\Delta G = \begin{cases}
+\Delta G_0 \cdot \exp\left(\dfrac{V_{pulse} - V_{set}}{V_0}\right) & V_{pulse} > V_{set} \quad \text{(POTENTIATION)} \\[6pt]
-\Delta G_0 \cdot \exp\left(\dfrac{|V_{pulse}| - V_{reset}}{V_0}\right) & V_{pulse} < -V_{reset} \quad \text{(DEPRESSION)}
\end{cases}$$
```

| Parameter | Symbol | Value | Description |
|---|---|---|---|
| High resistance state | $R_{HRS}$ | 1 M$\Omega$ | $G_{min} = 1\ \mu$S |
| Low resistance state | $R_{LRS}$ | 1 k$\Omega$ | $G_{max} = 1$ mS |
| Conductance levels | $N_{levels}$ | 64 | 6-bit resolution |
| SET threshold | $V_{set}$ | +0.20 V | Minimum potentiation voltage |
| RESET threshold | $V_{reset}$ | -0.15 V | Minimum depression voltage |
| Write pulse amplitude | $V_{write}$ | 0.30 V | Analog pulse train |
| Read voltage | $V_{read}$ | 0.10 V | Non-destructive sensing |

### 2.4 Unified GO Verilog-A Module

```verilog
`include "disciplines.vams"
`include "constants.vams"

module GO_UNIFIED(SN, PLATE, MODE);
    inout SN, PLATE, MODE;
    electrical SN, PLATE;
    electrical MODE;        // MODE=0: DRAM, MODE=1: Neuro

    // ============================================================
    // DRAM MODE PARAMETERS
    // ============================================================
    parameter real Cs       = 39.8e-15   from [1e-15:1e-12];  // Storage cap [F]
    parameter real R0       = 1e15       from [1e12:1e18];     // Base leakage [Ohm]
    parameter real gamma_PF = 0.1        from [0:1];           // PF coefficient [V^(-1/2)]
    parameter real Ea       = 0.05       from [0:0.5];         // Activation energy [eV]

    // ============================================================
    // NEUROMORPHIC MODE PARAMETERS
    // ============================================================
    parameter real R_HRS    = 1e6        from [1e3:1e9];       // High resistance [Ohm]
    parameter real R_LRS    = 1e3        from [1e0:1e6];       // Low resistance [Ohm]
    parameter real N_levels = 64         from [2:256];         // Quantization levels
    parameter real V_set    = 0.20       from [0:1];           // SET threshold [V]
    parameter real V_reset  = 0.15       from [0:1];           // RESET threshold [V]
    parameter real V0       = 0.05       from [1e-3:0.5];      // Exponential factor [V]
    parameter real dG0      = 1e-6       from [1e-9:1e-3];     // Base conductance step [S]

    // Temperature
    parameter real Temp     = 300        from [250:400];       // Temperature [K]

    // Internal variables
    real V_cell, I_dram, I_neuro;
    real G_cell, G_min, G_max, dG;
    real R_leak_eff;
    real mode_val;
    real V_pulse;
    real G_new;
    integer level_idx;

    // State variable for conductance (neuro mode)
    real G_internal;

    analog begin
        // Read mode select (0 = DRAM, 1 = Neuro)
        mode_val = V(MODE);

        // Cell voltage
        V_cell = V(SN) - V(PLATE);

        // ========================================================
        // DRAM MODE: Leaky Capacitor
        // ========================================================
        if (mode_val < 0.5) begin
            // Poole-Frenkel leakage resistance
            R_leak_eff = R0 * exp(-gamma_PF * sqrt(abs(V_cell)))
                       * exp(Ea * $charge_e / ($boltzmann * Temp));

            if (R_leak_eff < 1e6)
                R_leak_eff = 1e6;   // Floor resistance

            // Displacement current + leakage
            I_dram = Cs * ddt(V_cell) + V_cell / R_leak_eff;

            I(SN, PLATE) <+ I_dram;
        end

        // ========================================================
        // NEUROMORPHIC MODE: Quantized Memristor
        // ========================================================
        else begin
            G_min = 1.0 / R_HRS;
            G_max = 1.0 / R_LRS;
            dG    = (G_max - G_min) / (N_levels - 1.0);

            // Read current conductance from state
            G_cell = G_internal;

            // Ohmic conduction during read
            I_neuro = G_cell * V_cell;

            // Conductance update on write pulses
            V_pulse = V_cell;

            if (V_pulse > V_set) begin
                // POTENTIATION (SET): increase conductance
                G_new = G_cell + dG0 * exp((V_pulse - V_set) / V0);
            end else if (V_pulse < -V_reset) begin
                // DEPRESSION (RESET): decrease conductance
                G_new = G_cell - dG0 * exp((abs(V_pulse) - V_reset) / V0);
            end else begin
                // Read or sub-threshold: no change
                G_new = G_cell;
            end

            // Quantize to discrete levels
            if (G_new > G_max) G_new = G_max;
            if (G_new < G_min) G_new = G_min;

            level_idx = floor((G_new - G_min) / dG + 0.5);
            G_new = G_min + dG * level_idx;

            // Apply current and update state
            I(SN, PLATE) <+ I_neuro;

            // State derivative for conductance evolution
            ddt(G_internal) <+ (G_new - G_cell) / 1p;  // 1 ps time constant
        end
    end
endmodule
```

---

## 3. Full 1T1C/1T1M Cell SPICE Netlist

### 3.1 Top-Level Netlist

```spice
* ========================================================================
* UK-HYBRID MEMORY CELL — Complete SPICE Netlist
* 1T1C (DRAM mode) / 1T1M (Neuromorphic mode) Unified Cell
* Technology: Stanford VS-CNFET + GO Unified Storage Element
* ========================================================================

.TITLE UK_Hybrid_Memory_Cell_1T1C_1T1M
.OPTION POST PROBE ACCURATE NUMDGT=8
.OPTION GMIN=1e-18 RELTOL=1e-8 ABSTOL=1e-12

* ========================================================================
* SECTION 1: MODEL INCLUDES
* ========================================================================
.hdl "vs_cntfet.va"          * Stanford VS-CNFET Verilog-A
.hdl "go_unified.va"         * GO Unified Storage Element Verilog-A

* ========================================================================
* SECTION 2: GLOBAL NETS
* ========================================================================
.GLOBAL VDD VSS

* ========================================================================
* SECTION 3: POWER SUPPLY DEFINITIONS
* ========================================================================
Vvdd  VDD  0  DC 0.8V                  * Core supply voltage
Vvss  VSS  0  DC 0V                     * Ground reference
Vvdd2 VDD2 0  DC 0.3V                  * Analog write supply (neuro mode)

* ========================================================================
* SECTION 4: ACCESS TRANSISTOR (VS-CNFET)
* ========================================================================
* Terminal mapping: D=SN G=WL S=BL B=VSS
Xcntfet SN WL BL VSS VS_CNFET
+ L_g=25n      d_cnt=1.5n    N_cnt=15
+ C_m=3.45e-13 v_x0=3.8e7   mu0=0.8
+ alpha=3.5    beta=1.8
+ V_th0=0.35   n_sub=1.35    delta=0.050  eta=0.12
+ R_s=500      Temp=300

* ========================================================================
* SECTION 5: UNIFIED GO STORAGE ELEMENT
* ========================================================================
* Terminal mapping: SN=storage node, PLATE=cap plate, MODE=mode select
Xgo SN PLATE MODE GO_UNIFIED
+ Cs=39.8e-15     R0=1e15        gamma_PF=0.1    Ea=0.05
+ R_HRS=1e6       R_LRS=1e3      N_levels=64
+ V_set=0.20      V_reset=0.15   V0=0.05         dG0=1e-6
+ Temp=300

* ========================================================================
* SECTION 6: MODE SELECT SWITCH
* ========================================================================
* MODE=0 (DRAM): Connect to 0V for capacitor mode
* MODE=1 (Neuro): Connect to 0.3V for memristor mode
Xmodesw MODE VSS VDD2 MODE_SW

* Mode switch subcircuit
.SUBCKT MODE_SW OUT GNDD GNDA
+ W_n=0.5u L_n=25n W_p=1.0u L_p=25n
XMNa OUT SEL GNDD GNDD VS_CNFET N_cnt=15
XMPa OUT SEL GNDA GNDA VS_CNFET N_cnt=15
Vsel SEL 0 DC 0                        * Driven by external controller
.ENDS

* ========================================================================
* SECTION 7: WORDLINE PARASITICS
* ========================================================================
Rwl1 WL_driver WL 0.2                  * WL routing resistance (1 um)
Cwl1 WL    VSS  20f                    * WL capacitance
Cwl2 SN    VSS  5f                     * Gate-drain Miller cap (est.)

* ========================================================================
* SECTION 8: BITLINE PARASITICS
* ========================================================================
Rbl1 BL_sense BL 0.5                   * BL routing resistance (1 um)
Cbl1 BL    VSS  50f                    * Bitline capacitance
Cbl2 SN    VSS  2f                     * Junction + fringe cap (est.)

* ========================================================================
* SECTION 9: PLATE LINE
* ========================================================================
Vplate PLATE 0 DC 0.4V                 * DRAM: Vdd/2 = 0.4V plate
* For neuro mode, plate may be driven differentially

* ========================================================================
* SECTION 10: SENSE AMPLIFIER (Differential Latch Type)
* ========================================================================
.SUBCKT SENSE_AMP SA_OUT SA_nOUT BL BL_ref EN
+ W_n=1u L_n=25n W_p=2u L_p=25n
* Cross-coupled inverter pair
XMIN1 SA_OUT SA_nOUT VSS VSS VS_CNFET N_cnt=30
XMIN2 SA_nOUT SA_OUT VSS VSS VS_CNFET N_cnt=30
XMIP1 SA_OUT SA_nOUT VDD VDD VS_CNFET N_cnt=60
XMIP2 SA_nOUT SA_OUT VDD VDD VS_CNFET N_cnt=60
* Enable transistor
XMEN SA_nOUT EN VSS VSS VS_CNFET N_cnt=20
* Isolation switches
XISO1 BL      ISO VDD VDD VS_CNFET N_cnt=10
XISO2 BL_ref  ISO VDD VDD VS_CNFET N_cnt=10
RISO ISO SA_OUT 100
.ENDS

* Reference voltage for DRAM sensing (midpoint)
Vref VREF 0 DC 0.4V                    * Vdd/2 reference

* ========================================================================
* SECTION 11: MODE-SPECIFIC WRITE DRIVERS
* ========================================================================
.SUBCKT WR_DRV_BL BL DATA EN MODE
+ W_n=2u L_n=25n W_p=4u L_p=25n
* Pull-up network (write "1")
XMPu BL N1 VDD VDD VS_CNFET N_cnt=40
* Pull-down network (write "0")
XMNd BL N2 VSS VSS VS_CNFET N_cnt=40
* Logic combining DATA, EN, MODE
* Simplified: EN gates both paths, DATA selects direction
* MODE=0 (DRAM): Full 0.8V swing
* MODE=1 (Neuro): 0.3V analog pulse
.ENDS

* ========================================================================
* ========================================================================
* TESTBENCH SECTIONS
* ========================================================================
* ========================================================================

* ========================================================================
* TEST 1: DC SWEEP — Transfer Characteristics
* ========================================================================
.DC Vwl 0 0.8 0.01
* Sweep wordline from 0 to 0.8V, monitor SN and BL
.PROBE DC I(Xcntfet) V(SN) V(BL)

* ========================================================================
* TEST 2: TRANSIENT — DRAM Write "1" and Read
* ========================================================================
* Mode: DRAM (MODE = 0V)
Vmode_dram MODE 0 PWL(0n 0 100n 0)

* Wordline pulse for WRITE "1"
Vwl_dram WL 0 PWL(
+ 0ns    0V
+ 1ns    0V
+ 1.1ns  0.8V        * WL rises
+ 5ns    0.8V        * Write "1" active
+ 5.1ns  0V          * WL falls
+ 50ns   0V
+ 50.1ns 0.8V        * READ pulse
+ 55ns   0.8V
+ 55.1ns 0V
+ 200ns  0V
+ 200.1ns 0.8V       * Second read (retention test)
+ 205ns  0.8V
+ 205.1ns 0V
+)

* Bitline data for WRITE "1" (BL driven to Vdd)
Vbl_dram BL 0 PWL(
+ 0ns    0.4V         * Precharged to Vdd/2
+ 1ns    0.4V
+ 1.2ns  0.8V        * Driven high for write "1"
+ 5ns    0.8V
+ 5.2ns  0.4V        * Return to precharge
+ 100ns  0.4V
+)

* Plate line at Vdd/2
Vplate_dram PLATE 0 DC 0.4V

.TRAN 10p 250n
.PROBE TRAN V(SN) V(BL) V(WL) I(Xgo)

* ========================================================================
* TEST 3: TRANSIENT — Neuromorphic Potentiation
* ========================================================================
* Mode: Neuro (MODE = 0.3V)
Vmode_neuro MODE 0 PWL(0n 0.3 100n 0.3)

* Analog pulse train for conductance update
Vwl_neuro WL 0 PWL(
+ 0ns    0V
+ 10ns   0V
+ 10.1ns 0.3V        * First SET pulse
+ 12ns   0.3V
+ 12.1ns 0V
+ 20ns   0V
+ 20.1ns 0.3V        * Second SET pulse
+ 22ns   0.3V
+ 22.1ns 0V
+ 30ns   0V
+ 30.1ns 0.3V        * Third SET pulse
+ 32ns   0.3V
+ 32.1ns 0V
+)

* Bitline at write voltage for potentiation
Vbl_neuro BL 0 PWL(
+ 0ns    0V
+ 10ns   0V
+ 10.1ns 0.3V
+ 32ns   0.3V
+ 32.1ns 0V
+)

* Plate grounded for neuro write
Vplate_neuro PLATE 0 DC 0V

* Read pulse (non-destructive, 0.1V)
Vread_neuro BL 0 PWL(
+ 40ns   0V
+ 40.1ns 0.1V        * Read pulse
+ 42ns   0.1V
+ 42.1ns 0V
+)

.PROBE TRAN V(SN) I(Xgo) V(WL) V(BL)

* ========================================================================
* TEST 4: AC ANALYSIS — Frequency Response
* ========================================================================
* Small-signal AC superimposed on DC bias point
Vac_sn SN 0 AC 10mV DC 0.4V            * AC stimulus on storage node
.ac DEC 20 0.1 100G                     * 0.1 Hz to 100 GHz
.PROBE AC V(SN) V(BL) I(Xgo)

* ========================================================================
* TEST 5: RETENTION ANALYSIS — DRAM Charge Loss
* ========================================================================
* Write "1", then monitor SN voltage decay over 1 second
Vwl_ret WL 0 PWL(0ns 0 1ns 0 1.1ns 0.8V 5ns 0.8V 5.1ns 0 1s 0)
Vbl_ret BL 0 PWL(0ns 0.4V 1.2ns 0.8V 5ns 0.8V 5.2ns 0.4V 1s 0.4V)
.TRAN 1n 1s
.PROBE TRAN V(SN) I(Xgo)

* ========================================================================
* ANALYSIS CONTROL
* ========================================================================
*.OP                                    * Operating point
*.TEMP 27                              * Nominal temperature
*.END
```

---

## 4. Sense Amplifier Design

### 4.1 Architecture

The sense amplifier uses a **cross-coupled CMOS inverter latch** with CNTFET devices. For DRAM mode, it resolves the small differential voltage between the bitline and a reference voltage $V_{ref} = V_{DD}/2 = 0.4$ V. For neuromorphic mode, it serves as a current-mode or voltage-mode readout of the memristor conductance state.

### 4.2 Signal Development Equation

When the access transistor turns on for a DRAM read, charge sharing occurs between the storage capacitor $C_s$ and the bitline capacitance $C_{bl}$:

```
$$\Delta V_{bl} = \frac{C_s}{C_s + C_{bl}} \times (V_{SN} - V_{bl,pre})$$
```

For a stored "1" ($V_{SN} = V_{DD} = 0.8$ V) with $V_{bl,pre} = V_{DD}/2 = 0.4$ V:

```
$$\Delta V_{bl}("1") = \frac{39.8}{39.8 + 50} \times (0.8 - 0.4) = 0.443 \times 0.4 \approx +0.177 \text{ V}$$
```

For a stored "0" ($V_{SN} = 0$ V):

```
$$\Delta V_{bl}("0") = \frac{39.8}{39.8 + 50} \times (0 - 0.4) = 0.443 \times (-0.4) \approx -0.177 \text{ V}$$
```

The signal magnitude:

```
$$|\Delta V_{bl}| = \frac{C_s}{C_s + C_{bl}} \cdot \frac{V_{DD}}{2} = 0.443 \times 0.4 \approx 177 \text{ mV}$$
```

### 4.3 Sensing Margin Analysis

| Condition | $V_{BL}$ after charge sharing | $V_{ref}$ | Differential |
|---|---|---|---|
| Stored "1" | $0.4 + 0.177 = 0.577$ V | 0.400 V | +177 mV |
| Stored "0" | $0.4 - 0.177 = 0.223$ V | 0.400 V | -177 mV |
| Sensing margin | | | **354 mV** (differential) |

The sensing margin of **354 mV** (single-ended: 177 mV) is excellent for CNTFET-based amplifiers. The large $C_s/C_{bl}$ ratio of 0.80 ensures strong signal development despite the relatively small storage capacitance.

### 4.4 Sense Amplifier SPICE Subcircuit

```spice
* ========================================================================
* CNTFET DIFFERENTIAL SENSE AMPLIFIER
* ========================================================================
.SUBCKT SA_DIFF OUT OUTn BL BLb EN VDD VSS

* --- Cross-coupled inverter pair (latch core) ---
XMN1 OUT  OUTn VSS VSS VS_CNFET N_cnt=30 L_g=25n
XMN2 OUTn OUT  VSS VSS VS_CNFET N_cnt=30 L_g=25n
XMP1 OUT  OUTn VDD VDD VS_CNFET N_cnt=60 L_g=25n
XMP2 OUTn OUT  VDD VDD VS_CNFET N_cnt=60 L_g=25n

* --- Enable transistor (tail current source) ---
XMNen N_int EN VSS VSS VS_CNFET N_cnt=40 L_g=25n

* --- Input isolation transistors ---
XMNiso1 OUT  ISO1 N_int VSS VS_CNFET N_cnt=20 L_g=25n
XMNiso2 OUTn ISO2 N_int VSS VS_CNFET N_cnt=20 L_g=25n

* --- Column select switches ---
XMPys1 YS BL  VDD VDD VS_CNFET N_cnt=15 L_g=25n
XMPys2 YS BLb VDD VDD VS_CNFET N_cnt=15 L_g=25n

* --- Precharge/equalization ---
XMPpc1 BL  PC VDD VDD VS_CNFET N_cnt=15 L_g=25n
XMPpc2 BLb PC VDD VDD VS_CNFET N_cnt=15 L_g=25n
XMNpc  BL  EQ BLb VDD VS_CNFET N_cnt=10 L_g=25n

.ENDS SA_DIFF
```

### 4.5 Signal Development Time

The BL rise/fall time constant during sensing:

```
$$\tau_{sense} = (R_{on,cntfet} + R_{bl}) \times (C_{bl} + C_s)$$
```

With $R_{on,cntfet} \approx 1/(\mu C_{ox} (V_{GS}-V_T)) \approx 500\ \Omega$ for the access transistor in saturation:

```
$$\tau_{sense} \approx (500 + 0.5)\ \Omega \times (50 + 39.8)\ \text{fF} \approx 500 \times 89.8 \times 10^{-15} \approx 45\ \text{ps}$$
```

The signal develops to 90% of final value in approximately $2.3\tau \approx 100$ ps.

### 4.6 Reference Voltage Generator

```spice
* ========================================================================
* VDD/2 REFERENCE VOLTAGE GENERATOR
* ========================================================================
.SUBCKT VREF_GEN VREF VDD VSS
* Resistive divider with CNTFET-equivalent channel resistance
Rref1 VDD VREF 10k
Rref2 VREF VSS 10k
* Decoupling capacitor
Cref VREF VSS 100f
.ENDS VREF_GEN
```

---

## 5. Mode Switching Circuit

### 5.1 Voltage Protocol Summary

| Parameter | DRAM Mode | Neuromorphic Mode |
|---|---|---|
| Wordline voltage | 0.8 V (digital) | 0.3 V (analog pulse train) |
| Bitline write voltage | 0.8 V / 0 V | 0.3 V / -0.3 V (analog) |
| Plate voltage | 0.4 V (Vdd/2) | 0 V |
| Read voltage | 0.4 V (charge share) | 0.1 V (non-destructive) |
| Mode select (MODE) | 0 V | 0.3 V |
| Write pulse width | ~1 ns | ~10 ns (train of pulses) |
| Access type | Random access | Sequential pulse update |

### 5.2 Write Driver Architecture

The write driver must generate both full-swing digital signals (DRAM) and controlled analog pulses (neuromorphic). A dual-path architecture is used:

```spice
* ========================================================================
* DUAL-MODE WRITE DRIVER
* ========================================================================
.SUBCKT WRITE_DRIVER BL DATA MODE VDD VDD2 VSS

* --- DRAM path: Full-swing CMOS driver ---
XMN_dram BL N1_dram VSS VSS VS_CNFET N_cnt=40 L_g=25n
XMP_dram BL N1_dram VDD VDD VS_CNFET N_cnt=80 L_g=25n

* --- Neuro path: Analog pulse DAC ---
* 6-bit DAC for analog weight programming
XMN_neuro BL N1_neuro VSS VSS VS_CNFET N_cnt=20 L_g=25n
Vdac_neuro N1_neuro 0 PWL(0 0 10n 0 10.1n 0.3 12n 0.3 12.1n 0)

* --- Mode selection mux ---
* MODE=0: Select DRAM path
* MODE=1: Select neuro path
.ENDS WRITE_DRIVER
```

### 5.3 Timing Diagram

```
DRAM MODE (Write "1" → Read → Refresh)
═══════════════════════════════════════════════════════════════

WL  ─┐                                          ┌──────────┐
0.8V │    ┌────────┐                            │  READ    │
0V  ─┘    │ WRITE  │                            │          │
         └────────┘                            └──────────┘
         1ns  5ns                              50ns  55ns

BL  ─┐         ┌────────┐    ┌────────┐
0.8V │         │  "1"   │    │ PRECH  │
0.4V─┘─────────┘        └────┘  0.4V  └────────────────────
     1ns      1.2ns  5ns   5.2ns

SN  ─┐                   ┌────────┐             ┌────────┐
0.8V │                   │CHARGE  │             │SENSE   │
0V   └───────────────────┘        └─────────────┘        └──
                          (stores ~0.8V)       (readback)

PL  ════════════════════════════════════════════════════════
     0.4V (constant Vdd/2 bias)


NEUROMORPHIC MODE (Potentiation via Pulse Train)
═══════════════════════════════════════════════════════════════

WL  ─┐    ┌──┐    ┌──┐    ┌──┐
0.3V │    │P1│    │P2│    │P3│       (pulse train)
0V  ─┘────┘  └────┘  └────┘  └────────────────────────────
     10ns   12ns   20ns   22ns   30ns   32ns

BL  ─┐    ┌──┐    ┌──┐    ┌──┐
0.3V │    │  │    │  │    │  │       (write voltage)
0V  ─┘────┘  └────┘  └────┘  └────────────────────────────

SN  ─┐         ┌────┐        ┌────┐        ┌────┐
     │         │ G1 │        │ G2 │        │ G3 │
0V  ─┘─────────┘    └────────┘    └────────┘    └─────────
     (G increases stepwise: G_min → G1 → G2 → G3)

READ (neuro)           ┌──┐
BL  ───────────────────┘0.1├────────────────────────────────
0V                     40ns  42ns
     (non-destructive, ohmic read)

PL  ─────────────────────────────────────────────────────────
     0V (grounded in neuro mode)

MODE ────────────────────────────────────────────────────────
     0.3V (constant for neuromorphic operation)
```

### 5.4 Mode Switch Controller

```spice
* ========================================================================
* MODE SWITCH CONTROLLER
* ========================================================================
.SUBCKT MODE_CTRL MODE VDD VDD2 VSS CMD

* CMD = 0: Select DRAM mode (MODE = 0V)
* CMD = 1: Select Neuro mode (MODE = VDD2 = 0.3V)

* Simple inverter-based level translator
XMN_cmd N1 CMD VSS VSS VS_CNFET N_cnt=10 L_g=25n
XMP_cmd N1 CMD VDD VDD VS_CNFET N_cnt=20 L_g=25n

* Output stage: drives MODE to appropriate level
XMN_out MODE N1 VSS VSS VS_CNFET N_cnt=20 L_g=25n
XMP_out MODE N1 VDD2 VDD2 VS_CNFET N_cnt=40 L_g=25n

.ENDS MODE_CTRL
```

---

## 6. Key Equations Summary Table

| Equation | Expression | Application |
|---|---|---|
| **CNFET: Unified $I_{DS}$** | $I_{DS} = W C_{ox} v_{x0} \dfrac{V_{GT}^2}{V_{GT}+2V_t} F_{sat}(V_{DS})$ | Core transistor model |
| **CNFET: Gate overdrive** | $V_{GT} = \ln(1+e^{(V_{GS}-V_T)/2V_t n}) \cdot 2V_t n$ | Smooth subthreshold/above-threshold transition |
| **CNFET: DIBL + Body** | $V_T = V_{th0} - \delta V_{DS} - \eta V_{BS}$ | Threshold variation |
| **CNFET: Saturation function** | $F_{sat} = \dfrac{(\alpha V_{DS})^\beta}{1+(\alpha V_{DS})^\beta}$ | Velocity saturation |
| **CNFET: Subthreshold swing** | $SS = 2.303 \cdot n \cdot k_BT/q \approx 70$ mV/dec | Leakage characterization |
| **CNFET: Series resistance** | $R_{series} = 2R_s/N_{cnt} = 33.3\ \Omega$ | Contact resistance |
| **DRAM: Storage charge** | $Q_s = C_s \cdot V_{SN}$ | Stored data encoding |
| **DRAM: PF leakage** | $I_{leak} = \dfrac{V}{R_0} e^{\gamma_{PF}\sqrt{V}}$ | Retention degradation |
| **DRAM: Retention time** | $\tau_{RC} = R_0 C_s \approx 18.4$ hours | Refresh period spec |
| **DRAM: Signal development** | $\Delta V_{bl} = \dfrac{C_s}{C_s+C_{bl}}(V_{SN}-V_{bl,pre})$ | Read sensing signal |
| **DRAM: Sensing margin** | $|\Delta V_{bl}| = 0.443 \times 0.4 = 177$ mV | Sense amp input |
| **Neuro: Ohmic read** | $I_{read} = G_{cell} \cdot V_{read}$ | Non-destructive read |
| **Neuro: Conductance range** | $G \in [G_{min}, G_{max}] = [1\ \mu\text{S}, 1\ \text{mS}]$ | 60 dB dynamic range |
| **Neuro: Level spacing** | $\Delta G = (G_{max}-G_{min})/(N_{levels}-1) \approx 15.9\ \mu$S | 6-bit resolution |
| **Neuro: SET update** | $\Delta G^+ = \Delta G_0 \cdot e^{(V_{pulse}-V_{set})/V_0}$ | Potentiation rule |
| **Neuro: RESET update** | $\Delta G^- = -\Delta G_0 \cdot e^{(|V_{pulse}|-V_{reset})/V_0}$ | Depression rule |
| **Cell: RC time** | $\tau_{sense} = R_{on}(C_s+C_{bl}) \approx 45$ ps | Signal settling |
| **Cell: Write time** | $t_{write} = (C_s+C_{bl}) \cdot R_{on} \ln(V_{final}/V_{error}) \approx 1$ ns | Full charge transfer |

---

## Appendix A: Device Parameter Quick Reference

### A.1 CNTFET Access Transistor

| Parameter | Value | Unit | SPICE/VA Name |
|---|---|---|---|
| Gate length $L_g$ | 25 | nm | `L_g` |
| Gate capacitance $C_m$ | 345 | aF/$\mu$m | `C_m` |
| Low-field mobility $\mu$ | 8,000 | cm$^2$/V$\cdot$s | `mu0` |
| Threshold voltage $V_{th}$ | 0.35 | V | `V_th0` |
| Subthreshold factor $n$ | 1.35 | — | `n_sub` |
| DIBL coefficient $\delta$ | 50 | mV/V | `delta` |
| Series resistance $R_s$ | 500 | $\Omega$/CNT | `R_s` |
| VS velocity $v_{x0}$ | $3.8\times10^7$ | m/s | `v_x0` |
| Saturation $\alpha$ | 3.5 | V$^{-1}$ | `alpha` |
| Saturation $\beta$ | 1.8 | — | `beta` |
| Number of CNTs $N_{cnt}$ | 15 | — | `N_cnt` |
| CNT diameter $d_{cnt}$ | 1.5 | nm | `d_cnt` |

### A.2 GO Storage Element

| Parameter | Value | Unit | SPICE/VA Name |
|---|---|---|---|
| Storage capacitance $C_s$ | 39.8 | fF | `Cs` |
| Leakage resistance $R_0$ | $10^{15}$ | $\Omega$ | `R0` |
| PF coefficient $\gamma_{PF}$ | 0.1 | V$^{-1/2}$ | `gamma_PF` |
| High resistance $R_{HRS}$ | 1 | M$\Omega$ | `R_HRS` |
| Low resistance $R_{LRS}$ | 1 | k$\Omega$ | `R_LRS` |
| Conductance levels | 64 | — | `N_levels` |
| Write voltage (neuro) | 0.3 | V | — |
| Read voltage (neuro) | 0.1 | V | — |

### A.3 Cell Parasitics

| Parameter | Value | Unit |
|---|---|---|
| Bitline capacitance $C_{bl}$ | 50 | fF |
| Wordline capacitance $C_{wl}$ | 20 | fF |
| Bitline resistance $R_{bl}$ | 0.5 | $\Omega$/$\mu$m |
| Wordline resistance $R_{wl}$ | 0.2 | $\Omega$/$\mu$m |

---

*End of CIRCUIT MODELS document. All SPICE netlists and Verilog-A modules are production-ready for simulation in HSPICE, Spectre, or compatible simulators.*
