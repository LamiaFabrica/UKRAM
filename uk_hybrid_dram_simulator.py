"""
UK-Hybrid DRAM Behavioral Simulator
====================================
Unified volatile DRAM + neuromorphic in-memory compute.
Supports: mode switching, STDP, GEMM, temperature sweep, DDR5 comparison.

Device: Hybrid 1T1C/1T1M memory array with carbon-nanotube (CNT) access transistor
Technology: IMEC 2024 UK Sovereign Semiconductor Programme
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict


@dataclass
class TimingParams:
    """DRAM timing parameters (all in nanoseconds unless noted)."""
    t_RCD: float = 12.0
    t_CAS: float = 10.0
    t_RP: float = 12.0
    t_RAS: float = 24.0
    t_RC: float = 36.0
    t_CCD: float = 2.5
    t_BURST: float = 2.5
    t_REF_27C_ms: float = 191.0
    t_REF_87C_ms: float = 22.5
    t_RFC: float = 260.0


@dataclass
class CellParams:
    """Physical cell parameters."""
    C_s_fF: float = 39.8
    V_dd_dram: float = 0.8
    V_dd_neuro_w: float = 0.3
    V_dd_neuro_r: float = 0.1
    I_off_fA: float = 75.0
    E_a_eV: float = 0.275
    I_on_mA: float = 1.5
    SS_mV_dec: float = 70.0
    R_HRS_MOhm: float = 1.0
    R_LRS_kOhm: float = 1.0
    n_levels: int = 64
    A_plus: float = 0.15
    A_minus: float = 0.15
    tau_plus_ms: float = 25.0
    tau_minus_ms: float = 25.0


@dataclass
class ArrayParams:
    """Array architecture parameters."""
    capacity_Gb: int = 1
    n_banks: int = 7
    n_rows_per_bank: int = 16384
    n_cols_per_bank: int = 8192
    n_subarrays: int = 32
    subarray_rows: int = 512
    subarray_cols: int = 256
    row_size_B: int = 1024
    col_IO_width: int = 64
    burst_length: int = 16
    clock_GHz: float = 6.4
    data_rate_GT_s: float = 12.8
    peak_BW_GB_s: float = 102.4
    die_area_mm2: float = 84.0


# Physical constants
k_B = 1.380649e-23
q_e = 1.602176634e-19
T_ref_K = 300.0


class UK_Hybrid_DRAM:
    """Complete simulator for the hybrid 1T1C/1T1M memory array."""

    def __init__(self):
        self.timing = TimingParams()
        self.cell = CellParams()
        self.array = ArrayParams()
        self.mode = "DRAM"
        self.T_kelvin = 300.0
        self.C_s = self.cell.C_s_fF * 1e-15
        self.V_dd = self.cell.V_dd_dram
        self.I_off = self.cell.I_off_fA * 1e-15
        self.Q_max = self.C_s * self.V_dd
        self.G_min = 1.0 / (self.cell.R_HRS_MOhm * 1e6)
        self.G_max = 1.0 / (self.cell.R_LRS_kOhm * 1e3)
        self.G_levels = np.linspace(self.G_min, self.G_max, self.cell.n_levels)
        self.total_rows = self.array.n_banks * self.array.n_rows_per_bank
        self.total_cells = self.total_rows * self.array.n_cols_per_bank
        self.row_buffer_bits = self.array.n_cols_per_bank
        self.E_refresh_per_cell_fJ = self.cell.C_s_fF * (self.V_dd ** 2) * 2

    def retention_time(self, T_kelvin: float) -> float:
        """DRAM retention with Arrhenius: t_ret = t_ref * exp[(Ea/kB)*(1/T - 1/Tref)]."""
        T = T_kelvin
        T_ref = T_ref_K
        E_a_J = self.cell.E_a_eV * q_e
        exponent = (E_a_J / k_B) * (1.0 / T - 1.0 / T_ref)
        return self.timing.t_REF_27C_ms * np.exp(exponent)

    def refresh_power(self, T_kelvin: float) -> float:
        """Refresh power in microwatts. P_refresh = N_cells * E_cell / t_ret."""
        t_ret_ms = self.retention_time(T_kelvin)
        t_ret_s = t_ret_ms * 1e-3
        E_per_cell_J = self.E_refresh_per_cell_fJ * 1e-15
        P_refresh_W = (self.total_cells * E_per_cell_J) / t_ret_s
        return P_refresh_W * 1e6

    def refresh_overhead_fraction(self, T_kelvin: float) -> float:
        """Fraction of time consumed by refresh operations."""
        t_ret_ms = self.retention_time(T_kelvin)
        t_ret_ns = t_ret_ms * 1e6
        n_rows = self.array.n_rows_per_bank
        t_refresh_period_ns = t_ret_ns / n_rows
        t_refresh_ns = self.timing.t_RFC
        overhead = t_refresh_ns / t_refresh_period_ns
        return min(overhead, 1.0)

    def stdp(self, delta_t_ms: float) -> float:
        """STDP: dw = A+ * exp(-dt/tau+) for dt>0; -A- * exp(dt/tau-) for dt<0."""
        if delta_t_ms > 0:
            dw = self.cell.A_plus * np.exp(-delta_t_ms / self.cell.tau_plus_ms)
        elif delta_t_ms < 0:
            dw = -self.cell.A_minus * np.exp(delta_t_ms / self.cell.tau_minus_ms)
        else:
            dw = 0.0
        return dw

    def gemm_dram(self, N: int = 1024) -> Dict:
        """GEMM in DRAM mode (von Neumann, memory-bound)."""
        n_ops = 2 * (N ** 3)
        bytes_per_elem = 2
        data_moved_B = 3 * (N ** 2) * bytes_per_elem
        bw_B_ns = self.array.peak_BW_GB_s
        time_ns = data_moved_B / bw_B_ns
        n_row_activates = N * 3
        row_activate_time_ns = n_row_activates * (self.timing.t_RCD + self.timing.t_RP)
        time_ns += row_activate_time_ns
        refresh_frac = self.refresh_overhead_fraction(self.T_kelvin)
        time_ns *= (1.0 + refresh_frac)
        time_s = time_ns * 1e-9
        tops = (n_ops / time_s) / 1e12
        P_active_W = 0.2 * self.array.n_banks
        P_refresh_W = self.refresh_power(self.T_kelvin) * 1e-6
        P_total_W = P_active_W + P_refresh_W
        energy_J = P_total_W * time_s
        tops_per_W = tops / P_total_W if P_total_W > 0 else 0
        return {
            'mode': 'DRAM', 'N': N, 'time_ms': time_s * 1e3, 'time_s': time_s,
            'TOPS': tops, 'TOPS_per_W': tops_per_W,
            'energy_mJ': energy_J * 1e3, 'energy_J': energy_J,
            'P_total_W': P_total_W, 'P_refresh_uW': P_refresh_W * 1e6,
            'refresh_overhead_frac': refresh_frac, 'n_ops': n_ops,
            'data_moved_MB': data_moved_B / (1024 * 1024)
        }

    def gemm_neuro(self, N: int = 1024) -> Dict:
        """GEMM in neuromorphic mode (analog in-memory compute with parallel ADCs)."""
        n_ops = 2 * (N ** 3)
        cols_per_array = self.array.subarray_cols
        rows_per_array = self.array.subarray_rows
        n_subarrays = self.array.n_subarrays
        n_banks = self.array.n_banks
        total_parallel_arrays = n_subarrays * n_banks
        tile_rows = min(N, rows_per_array)
        tiles_row_dim = int(np.ceil(N / tile_rows))
        tiles_col_dim = int(np.ceil(N / cols_per_array))
        total_tiles = tiles_row_dim * tiles_col_dim
        tiles_per_pass = min(total_tiles, total_parallel_arrays)
        passes_needed = int(np.ceil(total_tiles / tiles_per_pass))
        t_input_set_ns = 10.0
        t_compute_ns = 50.0
        t_adc_parallel_ns = 100.0
        t_per_row_tile_ns = t_input_set_ns + t_compute_ns + t_adc_parallel_ns
        row_iterations = int(np.ceil(N / tile_rows))
        time_per_pass_ns = t_per_row_tile_ns * row_iterations * tiles_row_dim
        time_ns = time_per_pass_ns * passes_needed
        time_s = time_ns * 1e-9
        tops = (n_ops / time_s) / 1e12 if time_s > 0 else 0
        E_compute_fJ = n_ops * 1.0
        E_compute_J = E_compute_fJ * 1e-15
        n_active_subarrays = min(total_tiles, total_parallel_arrays)
        P_ADC_W = 1e-3 * cols_per_array * n_active_subarrays
        E_adc_J = P_ADC_W * time_s
        P_input_W = 1e-4 * N * n_active_subarrays
        E_input_J = P_input_W * time_s
        energy_J = E_compute_J + E_adc_J + E_input_J
        P_total_W = energy_J / time_s if time_s > 0 else 0
        tops_per_W = tops / P_total_W if P_total_W > 0 else 0
        dram_result = self.gemm_dram(N)
        speedup = dram_result['time_s'] / time_s if time_s > 0 else 0
        return {
            'mode': 'NEURO', 'N': N, 'time_ms': time_s * 1e3, 'time_s': time_s,
            'TOPS': tops, 'TOPS_per_W': tops_per_W,
            'energy_mJ': energy_J * 1e3, 'energy_J': energy_J,
            'P_total_W': P_total_W, 'P_ADC_mW': P_ADC_W * 1e3,
            'speedup_vs_dram': speedup, 'n_ops': n_ops,
            'E_compute_fJ_total': E_compute_fJ,
            'total_tiles': total_tiles, 'tiles_per_pass': tiles_per_pass,
            'passes': passes_needed, 'parallel_arrays_used': n_active_subarrays
        }

    def temperature_sweep(self, T_range_K: np.ndarray) -> Dict:
        """Sweep temperature, return retention/power data."""
        results = {'T_K': [], 'T_C': [], 't_ret_ms': [], 'P_refresh_uW': [],
                   'refresh_overhead_frac': [], 'ddr5_compliant': []}
        ddr5_min_ret_ms = 32.0
        for T in T_range_K:
            t_ret = self.retention_time(T)
            P_ref = self.refresh_power(T)
            ref_overhead = self.refresh_overhead_fraction(T)
            ddr5_ok = "Y" if t_ret >= ddr5_min_ret_ms else "N"
            results['T_K'].append(T)
            results['T_C'].append(T - 273.15)
            results['t_ret_ms'].append(t_ret)
            results['P_refresh_uW'].append(P_ref)
            results['refresh_overhead_frac'].append(ref_overhead)
            results['ddr5_compliant'].append(ddr5_ok)
        return results

    def mode_switch(self, new_mode: str) -> str:
        """Switch between DRAM and NEURO modes."""
        if new_mode.upper() not in ["DRAM", "NEURO"]:
            return f"Error: Invalid mode '{new_mode}'. Use 'DRAM' or 'NEURO'."
        self.mode = new_mode.upper()
        if self.mode == "DRAM":
            self.V_dd = self.cell.V_dd_dram
            return f"Switched to DRAM mode. V_dd = {self.V_dd} V."
        else:
            self.V_dd = self.cell.V_dd_neuro_r
            return f"Switched to NEURO mode. V_dd_read = {self.V_dd} V. Analog MAC enabled."

    def ddr5_comparison(self) -> Dict:
        """Side-by-side comparison with DDR5-6400."""
        ddr5 = {'name': 'DDR5-6400', 'data_rate_GT_s': 6.4, 'bw_GB_s': 51.2,
                't_RCD_ns': 14.16, 't_RP_ns': 14.16, 't_RAS_ns': 32.0,
                't_CAS_ns': 22.5, 'refresh_ms': 32.0, 'retention_85C_ms': 32.0,
                'power_active_W': 3.5, 'power_idle_W': 1.0}
        uk_hybrid = {'name': 'UK-Hybrid 1T1C/1T1M', 'data_rate_GT_s': 12.8,
                     'bw_GB_s': 102.4, 't_RCD_ns': 12.0, 't_RP_ns': 12.0,
                     't_RAS_ns': 24.0, 't_CAS_ns': 10.0,
                     'refresh_ms': self.retention_time(358.15),
                     'retention_85C_ms': self.retention_time(358.15),
                     'power_active_W': 1.4, 'power_idle_W': 0.05}
        ratios = {'bw_ratio': uk_hybrid['bw_GB_s'] / ddr5['bw_GB_s'],
                  'latency_ratio': ddr5['t_CAS_ns'] / uk_hybrid['t_CAS_ns'],
                  'retention_ratio': uk_hybrid['retention_85C_ms'] / ddr5['retention_85C_ms'],
                  'power_ratio': ddr5['power_active_W'] / uk_hybrid['power_active_W']}
        return {'ddr5': ddr5, 'uk_hybrid': uk_hybrid, 'ratios': ratios}

    def mnist_inference_sim(self, batch_size: int = 1) -> Dict:
        """Simulate MNIST inference (784 -> 128 -> 10) in both modes."""
        input_dim = 784
        hidden_dim = 128
        output_dim = 10
        ops_layer1 = 2 * input_dim * hidden_dim
        ops_layer2 = 2 * hidden_dim * output_dim
        total_ops = ops_layer1 + ops_layer2

        # --- DRAM Mode ---
        weight_bytes = (input_dim * hidden_dim + hidden_dim * output_dim) * 2
        data_bytes = (input_dim + hidden_dim + output_dim) * 2
        total_data_B = weight_bytes + data_bytes
        bw_B_ns = self.array.peak_BW_GB_s
        dram_time_ns = total_data_B / bw_B_ns
        mac_per_clock = 64
        clock_rate_GHz = self.array.clock_GHz
        compute_time_ns = total_ops / (mac_per_clock * clock_rate_GHz)
        dram_time_ns = max(dram_time_ns, compute_time_ns)
        dram_time_ns += 20 * (self.timing.t_RCD + self.timing.t_RP)
        refresh_frac = self.refresh_overhead_fraction(self.T_kelvin)
        dram_time_ns *= (1.0 + refresh_frac)
        dram_time_s = dram_time_ns * 1e-9 * batch_size
        P_dram_W = 0.2 * self.array.n_banks
        P_refresh_W = self.refresh_power(self.T_kelvin) * 1e-6
        E_dram_J = (P_dram_W + P_refresh_W) * dram_time_s

        # --- NEURO Mode ---
        cols_per_array = self.array.subarray_cols
        rows_per_array = self.array.subarray_rows
        l1_row_tiles = int(np.ceil(input_dim / rows_per_array))
        l1_col_tiles = int(np.ceil(hidden_dim / cols_per_array))
        l1_tiles = l1_row_tiles * l1_col_tiles
        l2_row_tiles = int(np.ceil(hidden_dim / rows_per_array))
        l2_col_tiles = int(np.ceil(output_dim / cols_per_array))
        l2_tiles = l2_row_tiles * l2_col_tiles
        total_tiles = l1_tiles + l2_tiles
        t_input_set_ns = 10.0
        t_compute_ns = 50.0
        t_adc_parallel_ns = 100.0
        t_per_row_ns = t_input_set_ns + t_compute_ns + t_adc_parallel_ns
        l1_time_ns = l1_row_tiles * t_per_row_ns
        l2_time_ns = l2_row_tiles * t_per_row_ns
        neuro_time_ns = l1_time_ns + l2_time_ns + 50.0
        neuro_time_s = neuro_time_ns * 1e-9 * batch_size
        E_compute_J = total_ops * 1e-15 * batch_size
        n_active_adc_cols = cols_per_array * total_tiles
        P_ADC_W = 1e-3 * n_active_adc_cols
        E_adc_J = P_ADC_W * neuro_time_s
        P_input_W = 1e-4 * (input_dim + hidden_dim)
        E_input_J = P_input_W * neuro_time_s
        E_neuro_J = E_compute_J + E_adc_J + E_input_J
        speedup = dram_time_s / neuro_time_s if neuro_time_s > 0 else 0
        energy_ratio = E_dram_J / E_neuro_J if E_neuro_J > 0 else 0

        return {
            'batch_size': batch_size, 'network': f'{input_dim}x{hidden_dim}x{output_dim}',
            'total_ops': total_ops,
            'dram_time_us': dram_time_s * 1e6,
            'dram_energy_nJ': E_dram_J * 1e9,
            'dram_energy_per_inf_nJ': (E_dram_J / batch_size) * 1e9,
            'neuro_time_us': neuro_time_s * 1e6,
            'neuro_energy_nJ': E_neuro_J * 1e9,
            'neuro_energy_per_inf_nJ': (E_neuro_J / batch_size) * 1e9,
            'E_compute_nJ': E_compute_J * 1e9,
            'E_adc_nJ': E_adc_J * 1e9,
            'E_input_nJ': E_input_J * 1e9,
            'speedup': speedup, 'energy_ratio': energy_ratio,
            'meets_target_uJ': (E_neuro_J / batch_size) < 1e-6,
            'subarrays_used': total_tiles
        }

    def stdp_ascii_plot(self, dt_min: float = -100.0, dt_max: float = 100.0,
                        n_points: int = 41, height: int = 15) -> str:
        """Generate ASCII plot of STDP learning window."""
        dt_vals = np.linspace(dt_min, dt_max, n_points)
        dw_vals = np.array([self.stdp(dt) for dt in dt_vals])
        lines = []
        lines.append("=" * 70)
        lines.append("STDP Learning Window")
        lines.append(f"A_+ = {self.cell.A_plus}, A_- = {self.cell.A_minus}")
        lines.append(f"tau_+ = {self.cell.tau_plus_ms} ms, tau_- = {self.cell.tau_minus_ms} ms")
        lines.append("=" * 70)
        max_dw = max(abs(dw_vals)) if max(abs(dw_vals)) > 1e-10 else 1.0
        zero_line = height // 2
        for row in range(height):
            line_chars = []
            y_val = max_dw * (zero_line - row) / zero_line
            for i, dt in enumerate(dt_vals):
                dw = dw_vals[i]
                if abs(dw - y_val) < max_dw / height * 0.8:
                    line_chars.append('*')
                elif row == zero_line:
                    line_chars.append('-')
                else:
                    line_chars.append(' ')
            y_label = f"{y_val:+.3f}"
            lines.append(f"{y_label:>7s} |" + ''.join(line_chars))
        lines.append("        +" + "-" * n_points)
        x_label = f"     dt: {dt_min:+.0f} ms"
        x_label_end = f"{dt_max:+.0f} ms"
        lines.append(f"{x_label:>20s}{'':>{n_points-20}s}{x_label_end}")
        return '\n'.join(lines)

    def print_summary(self):
        """Print device configuration summary."""
        print("=" * 70)
        print("UK Hybrid 1T1C/1T1M Memory Array Simulator")
        print("=" * 70)
        print(f"\n--- Array Configuration ---")
        print(f"  Capacity:          {self.array.capacity_Gb} Gb")
        print(f"  Banks:             {self.array.n_banks}")
        print(f"  Rows/Bank:         {self.array.n_rows_per_bank:,}")
        print(f"  Cols/Bank:         {self.array.n_cols_per_bank:,}")
        print(f"  Subarrays:         {self.array.n_subarrays}")
        print(f"  Row Size:          {self.array.row_size_B} B")
        print(f"  Column I/O:        {self.array.col_IO_width} bits")
        print(f"  Burst Length:      {self.array.burst_length}")
        print(f"  Clock:             {self.array.clock_GHz} GHz")
        print(f"  Data Rate:         {self.array.data_rate_GT_s} GT/s")
        print(f"  Peak BW:           {self.array.peak_BW_GB_s} GB/s")
        print(f"  Die Area:          {self.array.die_area_mm2} mm\u00b2")
        print(f"\n--- Cell Parameters ---")
        print(f"  C_s:               {self.cell.C_s_fF} fF")
        print(f"  V_dd (DRAM):       {self.cell.V_dd_dram} V")
        print(f"  V_dd (neuro W):    {self.cell.V_dd_neuro_w} V")
        print(f"  V_dd (neuro R):    {self.cell.V_dd_neuro_r} V")
        print(f"  I_off:             {self.cell.I_off_fA} fA @ 300K")
        print(f"  E_a:               {self.cell.E_a_eV} eV")
        print(f"  I_on (CNT):        {self.cell.I_on_mA} mA")
        print(f"  Subthreshold Swing:{self.cell.SS_mV_dec} mV/dec")
        print(f"\n--- Timing ---")
        print(f"  t_RCD:             {self.timing.t_RCD} ns")
        print(f"  t_CAS:             {self.timing.t_CAS} ns")
        print(f"  t_RP:              {self.timing.t_RP} ns")
        print(f"  t_RAS:             {self.timing.t_RAS} ns")
        print(f"  t_REF (27C):       {self.timing.t_REF_27C_ms} ms")
        print(f"  t_REF (87C):       {self.timing.t_REF_87C_ms} ms")
        print(f"\n--- Neuromorphic ---")
        print(f"  R_HRS:             {self.cell.R_HRS_MOhm} MOhm")
        print(f"  R_LRS:             {self.cell.R_LRS_kOhm} kOhm")
        print(f"  Levels:            {self.cell.n_levels} (6-bit)")
        print(f"  STDP A_+/-:        {self.cell.A_plus}/{self.cell.A_minus}")
        print(f"  STDP tau_+/-:      {self.cell.tau_plus_ms}/{self.cell.tau_minus_ms} ms")
        print(f"  Analog MAC energy: ~1 fJ/op")
        print(f"  ADC readout:       100 ns/col (parallel)")
        print(f"  Current mode:      {self.mode}")
        print("=" * 70)


def run_all_simulations():
    """Execute all simulations and print results."""
    sim = UK_Hybrid_DRAM()
    sim.print_summary()
    print("\n")

    # 1. TEMPERATURE SWEEP
    print("=" * 70)
    print("SIMULATION 1: Temperature Sweep (300 K - 400 K)")
    print("=" * 70)
    T_range = np.arange(300, 401, 10)
    sweep = sim.temperature_sweep(T_range)
    print(f"\n{'T (K)':>6s} | {'T (C)':>6s} | {'t_ret (ms)':>12s} | {'P_refresh (uW)':>16s} | {'Overhead':>8s} | {'DDR5':>6s}")
    print("-" * 70)
    for i in range(len(sweep['T_K'])):
        print(f"{sweep['T_K'][i]:6.0f} | {sweep['T_C'][i]:6.1f} | "
              f"{sweep['t_ret_ms'][i]:12.2f} | {sweep['P_refresh_uW'][i]:16.2f} | "
              f"{sweep['refresh_overhead_frac'][i]:8.4f} | {sweep['ddr5_compliant'][i]:>6s}")

    # 2. GEMM COMPARISON
    print("\n")
    print("=" * 70)
    print("SIMULATION 2: GEMM Comparison (N = 1024)")
    print("=" * 70)
    gemm_dram_r = sim.gemm_dram(N=1024)
    gemm_neuro_r = sim.gemm_neuro(N=1024)
    print(f"\n--- DRAM Mode ---")
    print(f"  Matrix size:       {gemm_dram_r['N']} x {gemm_dram_r['N']}")
    print(f"  Total ops:         {gemm_dram_r['n_ops']:.3e}")
    print(f"  Data moved:        {gemm_dram_r['data_moved_MB']:.1f} MB")
    print(f"  Time:              {gemm_dram_r['time_ms']:.3f} ms")
    print(f"  TOPS:              {gemm_dram_r['TOPS']:.4f}")
    print(f"  TOPS/W:            {gemm_dram_r['TOPS_per_W']:.4f}")
    print(f"  Energy:            {gemm_dram_r['energy_mJ']:.4f} mJ")
    print(f"  Refresh overhead:  {gemm_dram_r['refresh_overhead_frac']*100:.2f}%")
    print(f"\n--- NEURO Mode ---")
    print(f"  Matrix size:       {gemm_neuro_r['N']} x {gemm_neuro_r['N']}")
    print(f"  Total ops:         {gemm_neuro_r['n_ops']:.3e}")
    print(f"  Subarrays used:    {gemm_neuro_r['parallel_arrays_used']}")
    print(f"  Tiles total:       {gemm_neuro_r['total_tiles']}")
    print(f"  Passes:            {gemm_neuro_r['passes']}")
    print(f"  Time:              {gemm_neuro_r['time_ms']:.4f} ms")
    print(f"  TOPS:              {gemm_neuro_r['TOPS']:.4f}")
    print(f"  TOPS/W:            {gemm_neuro_r['TOPS_per_W']:.4f}")
    print(f"  Energy:            {gemm_neuro_r['energy_mJ']:.6f} mJ")
    print(f"\n--- Comparison ---")
    spd = gemm_neuro_r['speedup_vs_dram']
    e_ratio = gemm_dram_r['energy_mJ'] / gemm_neuro_r['energy_mJ'] if gemm_neuro_r['energy_mJ'] > 0 else 0
    print(f"  Speedup (NEURO vs DRAM): {spd:.1f}x")
    print(f"  Energy ratio (DRAM/NEURO): {e_ratio:.1f}x")

    # 3. DDR5 COMPARISON
    print("\n")
    print("=" * 70)
    print("SIMULATION 3: DDR5-6400 Comparison")
    print("=" * 70)
    comp = sim.ddr5_comparison()
    ddr5 = comp['ddr5']
    uk = comp['uk_hybrid']
    ratios = comp['ratios']
    print(f"\n{'Parameter':<25s} | {'DDR5-6400':>12s} | {'UK-Hybrid':>12s} | {'Ratio':>8s}")
    print("-" * 65)
    print(f"{'Data Rate (GT/s)':<25s} | {ddr5['data_rate_GT_s']:>12.1f} | {uk['data_rate_GT_s']:>12.1f} | {ratios['bw_ratio']:>8.2f}x")
    print(f"{'Bandwidth (GB/s)':<25s} | {ddr5['bw_GB_s']:>12.1f} | {uk['bw_GB_s']:>12.1f} | {ratios['bw_ratio']:>8.2f}x")
    print(f"{'t_RCD (ns)':<25s} | {ddr5['t_RCD_ns']:>12.2f} | {uk['t_RCD_ns']:>12.2f} | {uk['t_RCD_ns']/ddr5['t_RCD_ns']:>8.2f}x")
    print(f"{'t_CAS (ns)':<25s} | {ddr5['t_CAS_ns']:>12.2f} | {uk['t_CAS_ns']:>12.2f} | {ratios['latency_ratio']:>8.2f}x")
    print(f"{'Retention @85C (ms)':<25s} | {ddr5['retention_85C_ms']:>12.1f} | {uk['retention_85C_ms']:>12.1f} | {ratios['retention_ratio']:>8.2f}x")
    print(f"{'Active Power (W)':<25s} | {ddr5['power_active_W']:>12.2f} | {uk['power_active_W']:>12.2f} | {ratios['power_ratio']:>8.2f}x")
    print(f"\n--- Improvement Summary ---")
    print(f"  Bandwidth:          {ratios['bw_ratio']:.2f}x higher")
    print(f"  Access latency:     {ratios['latency_ratio']:.2f}x lower (CAS)")
    print(f"  Retention @85C:     {ratios['retention_ratio']:.2f}x longer")
    print(f"  Active power:       {ratios['power_ratio']:.2f}x lower")

    # 4. MNIST INFERENCE
    print("\n")
    print("=" * 70)
    print("SIMULATION 4: MNIST Inference Simulation")
    print("=" * 70)
    mnist = sim.mnist_inference_sim(batch_size=1)
    print(f"\n--- Network Configuration ---")
    print(f"  Topology:          {mnist['network']}")
    print(f"  Total MAC ops:     {mnist['total_ops']:,}")
    print(f"  Batch size:        {mnist['batch_size']}")
    print(f"  Subarrays used:    {mnist['subarrays_used']}")
    print(f"\n--- DRAM Mode ---")
    print(f"  Inference time:    {mnist['dram_time_us']:.2f} us")
    print(f"  Energy:            {mnist['dram_energy_per_inf_nJ']:.2f} nJ")
    print(f"\n--- NEURO Mode ---")
    print(f"  Inference time:    {mnist['neuro_time_us']:.2f} us")
    print(f"  Energy breakdown:")
    print(f"    Compute (1 fJ/op):  {mnist['E_compute_nJ']:.4f} nJ")
    print(f"    ADC readout:        {mnist['E_adc_nJ']:.4f} nJ")
    print(f"    Input drivers:      {mnist['E_input_nJ']:.4f} nJ")
    print(f"  Total energy:      {mnist['neuro_energy_per_inf_nJ']:.2f} nJ")
    print(f"  Meets <1 uJ target: {'YES' if mnist['meets_target_uJ'] else 'NO'}")
    print(f"\n--- Comparison ---")
    print(f"  Speedup:           {mnist['speedup']:.1f}x")
    print(f"  Energy savings:    {mnist['energy_ratio']:.1f}x")
    print(f"\n--- Theoretical Accuracy ---")
    print(f"  Expected accuracy: >90% (2-layer MLP on MNIST)")
    print(f"  6-bit weights provide sufficient precision for MNIST")

    # 5. STDP
    print("\n")
    print("=" * 70)
    print("SIMULATION 5: STDP Learning Window")
    print("=" * 70)
    print("\n" + sim.stdp_ascii_plot())
    print(f"\n--- STDP Numeric Values ---")
    dt_samples = [-100, -50, -25, -10, 0, 10, 25, 50, 100]
    print(f"{'dt (ms)':>8s} | {'dw':>10s}")
    print("-" * 25)
    for dt in dt_samples:
        print(f"{dt:8d} | {sim.stdp(dt):10.4f}")

    # EXECUTIVE SUMMARY
    print("\n")
    print("=" * 70)
    print("EXECUTIVE SUMMARY")
    print("=" * 70)
    print(f"""
UK Hybrid 1T1C/1T1M Memory Array -- Key Performance Metrics:

+---------------------------------------------------------------+
| Parameter                | Value                              |
+---------------------------------------------------------------+
| Die Area                 | 84.0 mm^2                          |
| Peak Bandwidth           | 102.4 GB/s                         |
| Data Rate                | 12.8 GT/s                          |
| Access Latency (t_CAS)   | 10 ns                              |
| Retention @ 27C          | {sim.retention_time(300):.1f} ms                          |
| Retention @ 87C          | {sim.retention_time(360):.1f} ms                           |
| Refresh Power @ 300K     | {sim.refresh_power(300):.2f} uW                        |
| Refresh Power @ 400K     | {sim.refresh_power(400):.2f} uW                      |
| Analog MAC Energy        | ~1 fJ/op                           |
| GEMM Speedup (vs DRAM)   | {spd:.1f}x                             |
| MNIST Inf. Energy (NEURO)| {mnist['neuro_energy_per_inf_nJ']:.1f} nJ                        |
| DDR5 BW Advantage        | {ratios['bw_ratio']:.2f}x                             |
+---------------------------------------------------------------+

Key achievements:
  - {ratios['bw_ratio']:.2f}x bandwidth vs DDR5-6400
  - {ratios['latency_ratio']:.2f}x lower latency
  - {spd:.0f}x speedup for GEMM via analog in-memory compute
  - Sub-uJ MNIST inference (target <1 uJ): {'MET' if mnist['meets_target_uJ'] else 'NOT MET'}
  - STDP-compatible learning with {sim.cell.n_levels}-level memristive weights
""")

    return {
        'temperature_sweep': sweep,
        'gemm_dram': gemm_dram_r,
        'gemm_neuro': gemm_neuro_r,
        'ddr5_comparison': comp,
        'mnist': mnist,
        'simulator': sim
    }


if __name__ == "__main__":
    results = run_all_simulations()
