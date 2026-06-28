"""
UK-DRAM Behavioral Simulator
============================
A cycle-accurate Python model for a 1Gb CNT+GO DRAM array.
Simulates: timing, power, refresh, retention physics, and AI GEMM workloads.

Usage:
    from uk_dram_behavioral_model import UK_DRAM_Simulator
    dram = UK_DRAM_Simulator()
    results = dram.simulate_gemm(N=1024)
    print(f"GEMM time: {results['time_ms']:.1f} ms")

Author: Generated for UK-DRAM Technical Analysis
Date: 2026-06-28
"""

import numpy as np


class UK_DRAM_Simulator:
    """
    Behavioral simulator for 1Gb UK-DRAM (CNT access transistor + GO storage capacitor).
    
    Models:
    - Array organization (banks, rows, columns, subarrays)
    - Timing parameters (t_RCD, t_CAS, t_RP, t_RAS)
    - Power consumption (active, refresh, standby)
    - Temperature-dependent retention physics
    - AI GEMM workload performance
    - DDR5 baseline comparison
    """
    
    def __init__(self, capacity_gb=1, n_banks=7, n_rows=16384, n_cols=8192,
                 n_subarrays=32, f_clock=6.4e9, V_dd=0.8,
                 C_s=39.8e-15, I_leak_300K=75e-15, cell_area_um2=0.06):
        """
        Initialize UK-DRAM simulator with device and array parameters.
        
        Parameters:
        -----------
        capacity_gb : int
            Total memory capacity in gigabits (default: 1 Gb)
        n_banks : int
            Number of independent banks (default: 7)
        n_rows : int
            Rows per bank (default: 16384 = 16K)
        n_cols : int
            Columns (bits) per row (default: 8192 = 8K)
        n_subarrays : int
            Subarrays per bank (default: 32)
        f_clock : float
            Clock frequency in Hz (default: 6.4e9 = 6.4 GHz)
        V_dd : float
            Supply voltage in V (default: 0.8)
        C_s : float
            Storage capacitance per cell in F (default: 39.8e-15 = 39.8 fF)
        I_leak_300K : float
            Cell leakage current at 300K in A (default: 75e-15 = 75 fA)
        cell_area_um2 : float
            Cell area in square microns (default: 0.06)
        """
        self.capacity_gb = capacity_gb
        self.capacity = capacity_gb * 1e9  # bits
        self.n_banks = n_banks
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_subarrays = n_subarrays
        self.f_clock = f_clock
        self.V_dd = V_dd
        self.C_s = C_s
        self.I_leak_0 = I_leak_300K
        self.cell_area = cell_area_um2
        
        # Physical constants
        self.kB = 1.381e-23      # Boltzmann constant (J/K)
        self.q = 1.602e-19       # Elementary charge (C)
        self.eps_0 = 8.854e-12   # Vacuum permittivity (F/m)
        self.V_T_300 = self.kB * 300 / self.q  # Thermal voltage at 300K (~25.9 mV)
        
        # Timing parameters (in seconds)
        self.t_RCD = 12e-9       # Row to column delay
        self.t_CAS = 10e-9       # Column access strobe
        self.t_RP = 12e-9        # Row precharge
        self.t_RAS = 24e-9       # Row active time
        self.t_BURST = 4e-9      # Burst transfer (8 beats)
        
        # Timing in clock cycles
        self.t_RCD_cyc = max(1, int(self.t_RCD * f_clock))
        self.t_CAS_cyc = max(1, int(self.t_CAS * f_clock))
        self.t_RP_cyc = max(1, int(self.t_RP * f_clock))
        self.t_RAS_cyc = max(1, int(self.t_RAS * f_clock))
        self.t_BURST_cyc = 16    # DDR burst length
        
        # DDR5 baseline for comparison
        self.ddr5_bw_GBps = 51.2
        self.ddr5_V = 1.1
        self.ddr5_refresh_ms = 32
        self.ddr5_refresh_power_mW_Gb = 80
        
    # -------------------------------------------------------------------------
    # Retention Physics
    # -------------------------------------------------------------------------
    
    def retention_time(self, T_kelvin):
        """
        Calculate cell retention time at temperature T (K).
        
        Uses Arrhenius temperature dependence for CNT subthreshold leakage:
        I_leak(T) = I_0 * (T/T_0)^2 * exp(-E_a/kT) / exp(-E_a/kT_0)
        
        Then: t_ret = C_s * deltaV / I_leak(T)
        
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
        
        I_leak = self.I_leak_0 * (T_kelvin / T0)**2 * \
                 np.exp(-E_a * self.q / (self.kB * T_kelvin)) / \
                 np.exp(-E_a * self.q / (self.kB * T0))
        
        delta_V = self.V_dd - 0.35  # V_sense_min = 0.35 V
        return self.C_s * delta_V / I_leak
    
    def refresh_interval(self, T_kelvin, margin=0.8):
        """
        Calculate refresh interval with safety margin.
        
        Parameters:
        -----------
        T_kelvin : float
            Temperature in Kelvin
        margin : float
            Safety margin factor (default: 0.8 = 80% of retention time)
            
        Returns:
        --------
        float : Refresh interval in seconds
        """
        return margin * self.retention_time(T_kelvin)
    
    # -------------------------------------------------------------------------
    # Power Analysis
    # -------------------------------------------------------------------------
    
    def refresh_power(self, T_kelvin):
        """
        Calculate refresh power consumption in Watts.
        
        Refresh energy = C_s * V_dd^2 per cell per refresh cycle.
        All rows must be refreshed within t_refresh interval.
        
        Parameters:
        -----------
        T_kelvin : float
            Temperature in Kelvin
            
        Returns:
        --------
        float : Refresh power in Watts
        """
        t_ret = self.retention_time(T_kelvin)
        t_refresh = 0.8 * t_ret  # 80% margin
        
        # Energy to refresh one row = all cells in that row
        E_per_row = self.n_cols * self.C_s * (self.V_dd ** 2)
        
        # Power = Energy per row * number of rows / refresh interval
        P_refresh = E_per_row * self.n_rows / t_refresh
        return P_refresh
    
    def active_power(self, activity_factor=0.5):
        """
        Calculate active (read/write) power consumption.
        
        P_dynamic = alpha * C_total * V_dd^2 * f
        
        Parameters:
        -----------
        activity_factor : float
            Fraction of cycles with memory access (default: 0.5)
            
        Returns:
        --------
        tuple : (P_dynamic_W, P_leakage_W)
        """
        # Total bitline capacitance (differential)
        C_bitline = self.n_rows * self.C_s * 2
        
        # Wordline capacitance
        C_wordline = self.n_cols * 2e-15  # ~2 fF per cell loading
        
        # Sense amplifier + decoder capacitance
        C_overhead = 20e-15
        
        C_total = C_bitline + C_wordline + C_overhead
        
        P_dynamic = activity_factor * C_total * (self.V_dd ** 2) * self.f_clock
        
        # Standby leakage (all cells)
        P_leakage = self.capacity * self.I_leak_0 * self.V_dd
        
        return P_dynamic, P_leakage
    
    def total_power(self, T_kelvin=300, activity_factor=0.5):
        """
        Calculate total power (active + refresh + leakage).
        
        Parameters:
        -----------
        T_kelvin : float
            Operating temperature (default: 300K = 27C)
        activity_factor : float
            Activity factor (default: 0.5)
            
        Returns:
        --------
        dict : Power breakdown in Watts
        """
        P_dynamic, P_leak = self.active_power(activity_factor)
        P_refresh = self.refresh_power(T_kelvin)
        
        return {
            'P_dynamic_W': P_dynamic,
            'P_refresh_W': P_refresh,
            'P_leakage_W': P_leak,
            'P_total_W': P_dynamic + P_refresh + P_leak,
            'refresh_overhead_pct': 100 * P_refresh / (P_dynamic + P_refresh + P_leak)
        }
    
    # -------------------------------------------------------------------------
    # Performance Metrics
    # -------------------------------------------------------------------------
    
    def bandwidth(self):
        """
        Calculate peak memory bandwidth.
        
        Returns:
        --------
        float : Bandwidth in GB/s
        """
        bits_per_transfer = 64  # 64-bit data bus
        transfers_per_sec = self.f_clock * 2  # DDR = 2 transfers/cycle
        bandwidth_bps = bits_per_transfer * transfers_per_sec
        return bandwidth_bps / (8 * 1e9)  # Convert to GB/s
    
    def die_area(self):
        """
        Calculate total die area including overhead.
        
        Returns:
        --------
        float : Die area in mm^2
        """
        cell_area_total = self.capacity * self.cell_area  # um^2
        overhead = 1.4  # 40% overhead for decoders, sense amps, I/O
        return cell_area_total * overhead / 1e6  # mm^2
    
    def read_latency(self):
        """
        Calculate read latency in nanoseconds.
        
        Returns:
        --------
        float : Read latency in ns
        """
        return (self.t_RCD_cyc + self.t_CAS_cyc + self.t_BURST_cyc) / (self.f_clock / 1e9)
    
    # -------------------------------------------------------------------------
    # AI GEMM Workload Simulation
    # -------------------------------------------------------------------------
    
    def simulate_gemm(self, N=1024):
        """
        Simulate N x N matrix multiply (C = A x B).
        
        Total MACs = 2 * N^3
        Each MAC requires 4 memory accesses (read A, B, partial C; write C)
        
        Parameters:
        -----------
        N : int
            Matrix dimension (default: 1024)
            
        Returns:
        --------
        dict : GEMM performance metrics
        """
        total_macs = 2 * N ** 3
        mem_ops_per_mac = 4
        total_mem_ops = total_macs * mem_ops_per_mac
        
        bytes_per_access = 8  # 64-bit float
        bandwidth_Bps = self.bandwidth() * 1e9
        
        # Memory-bound time
        total_bytes = total_mem_ops * bytes_per_access
        t_memory = total_bytes / bandwidth_Bps
        
        # Energy
        E_per_mac = self.C_s * (self.V_dd ** 2)
        E_total = total_macs * E_per_mac * 2  # Factor of 2 for overhead
        P_avg = E_total / t_memory if t_memory > 0 else 0
        
        # Refresh during GEMM
        P_refresh = self.refresh_power(300)
        refresh_overhead = P_refresh / (P_avg + P_refresh) if (P_avg + P_refresh) > 0 else 0
        
        tops = (total_macs / t_memory) / 1e12 if t_memory > 0 else 0
        tops_per_w = tops / (P_avg + P_refresh) if (P_avg + P_refresh) > 0 else 0
        
        return {
            'matrix_size': N,
            'total_macs': total_macs,
            'total_mem_ops': total_mem_ops,
            'time_ms': t_memory * 1000,
            'bandwidth_GBps': self.bandwidth(),
            'energy_per_mac_pJ': E_per_mac * 1e12,
            'total_energy_mJ': E_total * 1000,
            'P_avg_W': P_avg,
            'P_refresh_W': P_refresh,
            'refresh_overhead_pct': refresh_overhead * 100,
            'TOPS': tops,
            'TOPS_per_W': tops_per_w,
        }
    
    # -------------------------------------------------------------------------
    # DDR5 Comparison
    # -------------------------------------------------------------------------
    
    def compare_ddr5(self, N=1024):
        """
        Compare UK-DRAM performance against DDR5-6400 baseline.
        
        Parameters:
        -----------
        N : int
            Matrix dimension for GEMM (default: 1024)
            
        Returns:
        --------
        dict : Side-by-side comparison metrics
        """
        uk_gemm = self.simulate_gemm(N)
        
        # DDR5 GEMM (memory bound)
        ddr5_bw = self.ddr5_bw_GBps * 1e9  # B/s
        total_bytes = uk_gemm['total_mem_ops'] * 8
        t_ddr5 = total_bytes / ddr5_bw
        
        # DDR5 power (approximate)
        P_ddr5_active = 0.4  # W per Gb
        P_ddr5_refresh = self.ddr5_refresh_power_mW_Gb * 1e-3  # W per Gb
        
        total_macs = uk_gemm['total_macs']
        E_ddr5 = total_macs * 25e-15 * (self.ddr5_V ** 2) * 2
        P_ddr5_avg = E_ddr5 / t_ddr5 if t_ddr5 > 0 else 0
        
        ddr5_refresh_overhead = P_ddr5_refresh / (P_ddr5_avg + P_ddr5_refresh)
        ddr5_tops = (total_macs / t_ddr5) / 1e12 if t_ddr5 > 0 else 0
        ddr5_tops_per_w = ddr5_tops / (P_ddr5_avg + P_ddr5_refresh)
        
        ddr5_time_ms = t_ddr5 * 1000
        uk_time_ms = uk_gemm['time_ms']
        
        return {
            'uk_dram': uk_gemm,
            'ddr5': {
                'time_ms': ddr5_time_ms,
                'bandwidth_GBps': self.ddr5_bw_GBps,
                'P_active_W': P_ddr5_active,
                'P_refresh_W': P_ddr5_refresh,
                'refresh_overhead_pct': ddr5_refresh_overhead * 100,
                'TOPS': ddr5_tops,
                'TOPS_per_W': ddr5_tops_per_w,
            },
            'speedup': ddr5_time_ms / uk_time_ms if uk_time_ms > 0 else 0,
            'efficiency_ratio': uk_gemm['TOPS_per_W'] / ddr5_tops_per_w if ddr5_tops_per_w > 0 else 0,
        }
    
    # -------------------------------------------------------------------------
    # Reporting
    # -------------------------------------------------------------------------
    
    def report(self, T_kelvin=300):
        """
        Generate a comprehensive performance report.
        
        Parameters:
        -----------
        T_kelvin : float
            Operating temperature (default: 300K)
        """
        print("=" * 72)
        print("UK-DRAM SIMULATION REPORT")
        print("=" * 72)
        print(f"\nArray Configuration:")
        print(f"  Capacity:              {self.capacity_gb:.0f} Gb")
        print(f"  Banks:                 {self.n_banks}")
        print(f"  Rows per bank:         {self.n_rows:,} ({self.n_rows//1024}K)")
        print(f"  Columns per row:       {self.n_cols:,} ({self.n_cols//1024}K)")
        print(f"  Die area:              {self.die_area():.1f} mm^2")
        print(f"  Clock:                 {self.f_clock/1e9:.1f} GHz")
        print(f"  Bandwidth:             {self.bandwidth():.1f} GB/s")
        
        print(f"\nCell Parameters:")
        print(f"  Storage capacitance:   {self.C_s*1e15:.1f} fF")
        print(f"  Supply voltage:        {self.V_dd:.1f} V")
        print(f"  Leakage (300K):        {self.I_leak_0*1e15:.1f} fA")
        
        t_ret = self.retention_time(T_kelvin)
        t_ref = self.refresh_interval(T_kelvin)
        print(f"\nRetention (T = {T_kelvin-273:.0f}C):")
        print(f"  Retention time:        {t_ret*1e3:.1f} ms")
        print(f"  Refresh interval:      {t_ref*1e3:.1f} ms")
        
        power = self.total_power(T_kelvin)
        print(f"\nPower Breakdown:")
        print(f"  Dynamic:               {power['P_dynamic_W']*1e3:.2f} mW")
        print(f"  Refresh:               {power['P_refresh_W']*1e6:.2f} uW")
        print(f"  Leakage:               {power['P_leakage_W']*1e6:.2f} uW")
        print(f"  Total:                 {power['P_total_W']*1e3:.2f} mW")
        print(f"  Refresh overhead:      {power['refresh_overhead_pct']:.1f}%")
        
        gemm = self.simulate_gemm(1024)
        print(f"\nAI GEMM (1024x1024):")
        print(f"  Time:                  {gemm['time_ms']:.1f} ms")
        print(f"  TOPS:                  {gemm['TOPS']:.1f}")
        print(f"  TOPS/W:                {gemm['TOPS_per_W']:.1f}")
        print(f"  Refresh overhead:      {gemm['refresh_overhead_pct']:.1f}%")
        
        comp = self.compare_ddr5(1024)
        print(f"\nvs DDR5-6400:")
        print(f"  Speedup:               {comp['speedup']:.1f}x")
        print(f"  Efficiency ratio:      {comp['efficiency_ratio']:.1f}x")
        print("=" * 72)


# =============================================================================
# Example Usage and Self-Test
# =============================================================================

if __name__ == "__main__":
    print("UK-DRAM Behavioral Model - Self-Test\n")
    
    # Create simulator instance
    dram = UK_DRAM_Simulator()
    
    # Generate full report
    dram.report(T_kelvin=300)
    
    # Temperature sweep
    print("\n--- Temperature Sweep ---")
    print(f"{'Temp (C)':<10} {'Retention (ms)':<16} {'Refresh P (uW)':<16}")
    for T in [300, 330, 360, 390, 400]:
        t_ret = dram.retention_time(T)
        P_ref = dram.refresh_power(T)
        print(f"{T-273:<10} {t_ret*1e3:<16.1f} {P_ref*1e6:<16.2f}")
    
    # GEMM at different matrix sizes
    print("\n--- GEMM Scaling ---")
    print(f"{'Matrix':<10} {'Time (ms)':<12} {'TOPS':<10} {'TOPS/W':<10}")
    for N in [512, 1024, 2048]:
        result = dram.simulate_gemm(N)
        print(f"{N}x{N:<3} {result['time_ms']:<12.1f} {result['TOPS']:<10.1f} {result['TOPS_per_W']:<10.1f}")
