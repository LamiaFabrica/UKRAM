"""
UK-Hybrid DRAM Behavioral Simulator
====================================
Unified volatile DRAM + neuromorphic in-memory compute model.
Supports: mode switching, STDP, GEMM workloads, temperature sweep.

Usage:
    from uk_hybrid_dram import UK_Hybrid_DRAM
    dram = UK_Hybrid_DRAM()
    
    # DRAM mode GEMM
    result_dram = dram.gemm_dram(N=1024)
    print(f"DRAM: {result_dram['time_ms']:.1f} ms, {result_dram['TOPS_per_W']:.1f} TOPS/W")
    
    # Neuromorphic mode GEMM  
    result_neuro = dram.gemm_neuro(N=1024)
    print(f"Neuro: {result_neuro['time_ms']:.1f} ms, {result_neuro['TOPS_per_W']:.1f} TOPS/W")
    
    # Temperature sweep
    temps = dram.temperature_sweep(np.arange(300, 401, 20))
    for t in temps:
        print(f"{t['T_C']}C: {t['t_ret_ms']:.1f} ms retention")

Author: Generated for UK-Hybrid DRAM Technical Analysis
Date: 2026-06-28
"""

import numpy as np

# Physical constants
q = 1.602e-19       # Elementary charge (C)
k_B = 1.381e-23     # Boltzmann constant (J/K)
eps_0 = 8.854e-12   # Vacuum permittivity (F/m)


class UK_Hybrid_DRAM:
    """
    Unified UK-Hybrid DRAM simulator.
    
    Two mutually exclusive modes:
    - DRAM: 1T1C, volatile, refresh-based, DDR5-compatible
    - Neuromorphic: 1T1M, analog in-memory compute, STDP learning
    
    The cell shares a CNT access transistor and reconfigures the GO element
    between capacitor (DRAM) and memristor (neuro) via write voltage protocol.
    """
    
    def __init__(self):
        # --- Cell parameters ---
        self.C_s = 39.8e-15      # Storage capacitance (F)
        self.V_dd = 0.8          # Supply voltage (V)
        self.I_off = 75e-15      # Cell leakage at 300K (A)
        self.I_drive = 1.5e-3    # Drive current (A)
        
        # --- Neuro parameters ---
        self.R_hrs = 1e6         # High resistance state (Ω)
        self.R_lrs = 1e3         # Low resistance state (Ω)
        self.G_min = 1.0 / self.R_hrs
        self.G_max = 1.0 / self.R_lrs
        self.n_levels = 64       # Conductance levels
        self.V_set = 1.5         # SET voltage (V)
        self.V_reset = -1.5      # RESET voltage (V)
        self.V_read_neuro = 0.1  # Non-destructive read voltage (V)
        self.pulse_width_ns = 100  # Programming pulse width (ns)
        
        # --- Array parameters ---
        self.capacity_gb = 1
        self.n_banks = 7
        self.n_rows = 16384
        self.n_cols = 8192
        self.f_clock = 6.4e9     # 6.4 GHz
        
        # --- Timing ---
        self.t_RCD = 12e-9       # Row to column delay
        self.t_CAS = 10e-9       # Column access strobe
        self.t_RP = 12e-9        # Row precharge
        
        # --- DDR5 baseline for comparison ---
        self.ddr5_bw_GBps = 51.2
        self.ddr5_refresh_ms = 32
        
    # =====================================================================
    # DRAM Mode Methods
    # =====================================================================
    
    def retention_time(self, T_kelvin):
        """
        Calculate DRAM retention time at temperature T (K).
        
        Uses Arrhenius model for CNT subthreshold leakage:
        I_leak(T) = I_0 * (T/T_0)^2 * exp(-E_a/kT) / exp(-E_a/kT_0)
        
        Parameters:
        -----------
        T_kelvin : float
            Temperature in Kelvin
            
        Returns:
        --------
        float : Retention time in seconds
        """
        T0 = 300.0
        E_a = 0.275  # eV (CNT subthreshold activation energy = E_g/2)
        
        I_leak = self.I_off * (T_kelvin / T0)**2 * \
                 np.exp(-E_a * q / (k_B * T_kelvin)) / \
                 np.exp(-E_a * q / (k_B * T0))
        
        delta_V = self.V_dd - 0.35  # V_sense_min = 0.35 V
        return self.C_s * delta_V / I_leak
    
    def refresh_power(self, T_kelvin):
        """
        Calculate DRAM refresh power consumption in Watts.
        
        Parameters:
        -----------
        T_kelvin : float
            Temperature in Kelvin
            
        Returns:
        --------
        float : Refresh power in Watts
        """
        t_ret = self.retention_time(T_kelvin)
        t_refresh = 0.8 * t_ret  # 80% safety margin
        
        # Energy to refresh one row = all cells in that row
        E_per_row = self.n_cols * self.C_s * (self.V_dd ** 2)
        
        # Power = Energy per row * number of rows / refresh interval
        return E_per_row * self.n_rows / t_refresh
    
    def dram_active_power(self, activity_factor=0.5):
        """
        Calculate active (read/write) power consumption.
        
        Parameters:
        -----------
        activity_factor : float
            Fraction of cycles with memory access (default: 0.5)
            
        Returns:
        --------
        tuple : (P_dynamic_W, P_leakage_W)
        """
        # Bitline capacitance (differential)
        C_bitline = self.n_rows * self.C_s * 2
        
        # Wordline + sense amp capacitance
        C_wordline = self.n_cols * 2e-15
        C_sense_amp = 20e-15
        
        C_total = C_bitline + C_wordline + C_sense_amp
        
        P_dynamic = activity_factor * C_total * (self.V_dd ** 2) * self.f_clock
        P_leakage = self.capacity_gb * 1e9 * self.I_off * self.V_dd
        
        return P_dynamic, P_leakage
    
    # =====================================================================
    # Neuromorphic Mode Methods
    # =====================================================================
    
    def stdp(self, delta_t_ms, A_p=0.15, A_m=0.15, tau_p=25, tau_m=25):
        """
        Spike-Timing-Dependent Plasticity (STDP) for GO memristor.
        
        Asymmetric STDP window:
        - delta_t > 0 (pre before post): LTP (potentiation)
        - delta_t < 0 (post before pre): LTD (depression)
        
        Parameters:
        -----------
        delta_t_ms : float or ndarray
            Time difference t_post - t_pre in milliseconds
        A_p, A_m : float
            Maximum weight change amplitudes (default: 0.15)
        tau_p, tau_m : float
            Time constants in ms (default: 25)
            
        Returns:
        --------
        float or ndarray : Normalized weight change Δw/w
        """
        delta_w = np.zeros_like(delta_t_ms, dtype=float)
        
        # LTP: pre before post
        mask_ltp = delta_t_ms > 0
        delta_w[mask_ltp] = A_p * np.exp(-delta_t_ms[mask_ltp] / tau_p)
        
        # LTD: post before pre
        mask_ltd = delta_t_ms < 0
        delta_w[mask_ltd] = -A_m * np.exp(delta_t_ms[mask_ltd] / tau_m)
        
        return delta_w
    
    def neuro_read(self, G_cell, V_read=None):
        """
        Neuromorphic read: I = V_read * G_cell (Ohm's Law).
        
        In a crossbar array, this performs analog MAC:
        I_out = sum(V_in_j * G_ji) for all inputs j
        
        Parameters:
        -----------
        G_cell : float
            Cell conductance in Siemens
        V_read : float, optional
            Read voltage (default: self.V_read_neuro = 0.1 V)
            
        Returns:
        --------
        float : Read current in Amperes
        """
        if V_read is None:
            V_read = self.V_read_neuro
        return V_read * G_cell
    
    def neuro_program(self, G_target, G_current, V_pulse=0.3, pw_ns=100):
        """
        Program GO memristor to target conductance.
        
        Uses incremental pulse scheme:
        - G_target > G_current: SET pulses (positive)
        - G_target < G_current: RESET pulses (negative)
        
        Parameters:
        -----------
        G_target : float
            Target conductance in Siemens
        G_current : float
            Current conductance in Siemens
        V_pulse : float
            Pulse voltage amplitude (default: 0.3 V)
        pw_ns : float
            Pulse width in nanoseconds (default: 100)
            
        Returns:
        --------
        tuple : (n_pulses, E_total_J)
        """
        delta_G = (self.G_max - self.G_min) / self.n_levels
        delta_needed = G_target - G_current
        n_pulses = int(abs(delta_needed) / delta_G) + 1
        
        # Energy per pulse: E = V^2 * G * t
        E_pulse = V_pulse ** 2 * max(G_current, self.G_min) * pw_ns * 1e-9
        E_total = n_pulses * E_pulse
        
        return n_pulses, E_total
    
    def neuro_mac_array(self, V_inputs, G_matrix):
        """
        Perform analog MAC on neuromorphic crossbar array.
        
        I_out = G_matrix^T @ V_inputs
        
        Parameters:
        -----------
        V_inputs : ndarray (n_inputs,)
            Input voltages
        G_matrix : ndarray (n_inputs, n_outputs)
            Conductance matrix (synaptic weights)
            
        Returns:
        --------
        ndarray (n_outputs,) : Output currents (MAC results)
        """
        return G_matrix.T @ V_inputs
    
    # =====================================================================
    # GEMM Simulation
    # =====================================================================
    
    def gemm_dram(self, N=1024):
        """
        Simulate N x N matrix multiply using DRAM mode (memory-bound).
        
        Total MACs = 2 * N^3
        Each MAC requires 4 memory accesses.
        
        Parameters:
        -----------
        N : int
            Matrix dimension (default: 1024)
            
        Returns:
        --------
        dict : GEMM performance metrics
        """
        total_macs = 2 * N ** 3
        mem_ops = total_macs * 4
        bytes_per = 8
        bw = 64 * 2 * self.f_clock / 8  # bytes/s
        t_mem = mem_ops * bytes_per / bw
        
        E_per_mac = self.C_s * (self.V_dd ** 2)
        E_total = total_macs * E_per_mac * 2
        P_avg = E_total / t_mem if t_mem > 0 else 0
        P_refresh = self.refresh_power(300)
        
        tops = (total_macs / t_mem) / 1e12 if t_mem > 0 else 0
        tops_per_w = tops / (P_avg + P_refresh) if (P_avg + P_refresh) > 0 else 0
        
        return {
            'mode': 'DRAM',
            'matrix_size': N,
            'time_ms': t_mem * 1000,
            'TOPS': tops,
            'TOPS_per_W': tops_per_w,
            'energy_mJ': E_total * 1000,
            'refresh_overhead_pct': 100 * P_refresh / (P_avg + P_refresh) if (P_avg + P_refresh) > 0 else 0,
        }
    
    def gemm_neuro(self, N=1024):
        """
        Simulate N x N matrix multiply using neuromorphic mode (in-memory compute).
        
        Matrix A encoded as input voltages, Matrix B as conductance values.
        Analog VMM: I_out = G^T @ V_in
        
        Parameters:
        -----------
        N : int
            Matrix dimension (default: 1024)
            
        Returns:
        --------
        dict : GEMM performance metrics
        """
        total_macs = 2 * N ** 3
        
        # Analog compute + ADC readout
        t_analog = 1e-6  # 1 μs for full array
        t_adc = N * 100e-9  # Sequential ADC
        t_total = t_analog + t_adc
        
        # Energy per analog MAC
        G_avg = (self.G_max + self.G_min) / 2
        I_cell = self.V_read_neuro * G_avg
        P_cell = I_cell ** 2 / G_avg if G_avg > 0 else 0
        E_mac_analog = P_cell * t_analog / (N * N) if N > 0 else 0
        
        E_total = total_macs * E_mac_analog * 10  # 10x for ADC overhead
        P_avg = E_total / t_total if t_total > 0 else 0
        
        tops = (total_macs / t_total) / 1e12 if t_total > 0 else 0
        tops_per_w = tops / P_avg if P_avg > 0 else 0
        
        return {
            'mode': 'Neuromorphic',
            'matrix_size': N,
            'time_ms': t_total * 1000,
            'TOPS': tops,
            'TOPS_per_W': tops_per_w,
            'energy_mJ': E_total * 1000,
            'refresh_overhead_pct': 0,
            'analog_energy_fJ': E_mac_analog * 1e15,
        }
    
    # =====================================================================
    # Temperature Sweep
    # =====================================================================
    
    def temperature_sweep(self, T_range=np.arange(300, 401, 10)):
        """
        Sweep temperature and return retention/power data for DRAM mode.
        
        Parameters:
        -----------
        T_range : ndarray
            Temperature range in Kelvin (default: 300-400K in 10K steps)
            
        Returns:
        --------
        list : Dictionaries with T_C, t_ret_ms, P_refresh_uW
        """
        results = []
        for T in T_range:
            t_ret = self.retention_time(T)
            P_ref = self.refresh_power(T)
            results.append({
                'T_C': T - 273,
                'T_K': T,
                't_ret_ms': t_ret * 1000,
                'P_refresh_uW': P_ref * 1e6,
            })
        return results
    
    # =====================================================================
    # DDR5 Comparison
    # =====================================================================
    
    def compare_ddr5(self, N=1024):
        """
        Compare UK-Hybrid performance against DDR5-6400 baseline.
        
        Parameters:
        -----------
        N : int
            Matrix dimension for GEMM (default: 1024)
            
        Returns:
        --------
        dict : Side-by-side comparison
        """
        uk_dram = self.gemm_dram(N)
        uk_neuro = self.gemm_neuro(N)
        
        # DDR5 baseline
        ddr5_bw = self.ddr5_bw_GBps * 1e9
        total_bytes = 2 * N**3 * 4 * 8
        t_ddr5 = total_bytes / ddr5_bw
        
        return {
            'ddr5_time_ms': t_ddr5 * 1000,
            'uk_dram': uk_dram,
            'uk_neuro': uk_neuro,
            'speedup_dram_vs_ddr5': (t_ddr5 * 1000) / uk_dram['time_ms'] if uk_dram['time_ms'] > 0 else 0,
            'speedup_neuro_vs_ddr5': (t_ddr5 * 1000) / uk_neuro['time_ms'] if uk_neuro['time_ms'] > 0 else 0,
            'speedup_neuro_vs_dram': uk_dram['time_ms'] / uk_neuro['time_ms'] if uk_neuro['time_ms'] > 0 else 0,
        }
    
    # =====================================================================
    # Reporting
    # =====================================================================
    
    def report(self, T_kelvin=300):
        """
        Generate comprehensive performance report.
        
        Parameters:
        -----------
        T_kelvin : float
            Operating temperature (default: 300K = 27C)
        """
        print("=" * 72)
        print("UK-HYBRID DRAM SIMULATION REPORT")
        print("=" * 72)
        
        print(f"\nArray Configuration:")
        print(f"  Capacity:         {self.capacity_gb:.0f} Gb")
        print(f"  Banks:            {self.n_banks}")
        print(f"  Rows:             {self.n_rows:,} ({self.n_rows//1024}K)")
        print(f"  Columns:          {self.n_cols:,} ({self.n_cols//1024}K)")
        print(f"  Clock:            {self.f_clock/1e9:.1f} GHz")
        
        print(f"\nCell Parameters:")
        print(f"  C_s:              {self.C_s*1e15:.1f} fF")
        print(f"  V_dd:             {self.V_dd:.1f} V")
        print(f"  I_off (300K):     {self.I_off*1e15:.1f} fA")
        print(f"  I_drive:          {self.I_drive*1e6:.0f} μA")
        
        t_ret = self.retention_time(T_kelvin)
        print(f"\nRetention @ {T_kelvin-273:.0f}C:")
        print(f"  t_ret:            {t_ret*1e3:.1f} ms")
        
        print(f"\n--- DRAM Mode GEMM (1024x1024) ---")
        dram = self.gemm_dram(1024)
        for k, v in dram.items():
            if isinstance(v, float):
                print(f"  {k:<20} {v:.2f}")
            else:
                print(f"  {k:<20} {v}")
        
        print(f"\n--- Neuromorphic Mode GEMM (1024x1024) ---")
        neuro = self.gemm_neuro(1024)
        for k, v in neuro.items():
            if isinstance(v, float):
                print(f"  {k:<20} {v:.2f}")
            else:
                print(f"  {k:<20} {v}")
        
        comp = self.compare_ddr5(1024)
        print(f"\n--- vs DDR5-6400 ---")
        print(f"  DDR5 time:        {comp['ddr5_time_ms']:.1f} ms")
        print(f"  Speedup (DRAM):   {comp['speedup_dram_vs_ddr5']:.1f}x")
        print(f"  Speedup (Neuro):  {comp['speedup_neuro_vs_ddr5']:.0f}x")
        print(f"  Neuro vs DRAM:    {comp['speedup_neuro_vs_dram']:.0f}x")
        print("=" * 72)


# =============================================================================
# Self-Test
# =============================================================================

if __name__ == "__main__":
    print("UK-Hybrid DRAM Simulator - Self-Test\n")
    
    dram = UK_Hybrid_DRAM()
    dram.report(T_kelvin=300)
    
    print("\n--- STDP Curve Sample ---")
    delta_t = np.array([-50, -20, -10, 0, 10, 20, 50])
    dw = dram.stdp(delta_t)
    print(f"{'Δt (ms)':<10} {'Δw/w':<10}")
    for dt, w in zip(delta_t, dw):
        print(f"{dt:<10.0f} {w:<10.4f}")
    
    print("\n--- Temperature Sweep ---")
    temps = dram.temperature_sweep(np.arange(300, 381, 20))
    print(f"{'T(°C)':<8} {'t_ret(ms)':<12} {'P_refresh(μW)':<15} {'DDR5 Pass?'}")
    for t in temps:
        status = "PASS" if t['t_ret_ms'] > 32 else "FAIL"
        print(f"{t['T_C']:<8} {t['t_ret_ms']:<12.1f} {t['P_refresh_uW']:<15.2f} {status}")
