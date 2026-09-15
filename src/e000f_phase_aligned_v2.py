"""Corrected E000-F v2: common analytic-phase origin across cuts.

This wrapper intentionally reuses the full E000-F v1 data/model/evaluation code and
changes only the phase-boundary definition. The correction was pre-registered in
D000g before any v1 metrics were inspected.
"""
from pathlib import Path

import numpy as np
from scipy import signal

import e000f_fixed_vs_process_token as base


def common_phase_boundaries(force: np.ndarray):
    """Use absolute analytic-phase 2π crossings, not cut-relative phase[0]."""
    xp = base.robust_phase_signal(force[0])
    peak, err = base.spindle_peak(xp)
    low, high = peak * 0.82, peak * 1.18
    sos = signal.butter(4, [low, high], btype="bandpass", fs=base.FS, output="sos")
    xf = signal.sosfiltfilt(sos, xp)
    ph = np.unwrap(np.angle(signal.hilbert(xf)))

    # Critical v2 correction: crossings of a shared analytic-signal phase reference.
    # Do NOT subtract ph[0], which would create an arbitrary per-cut phase origin.
    turns = np.floor(ph / (2 * np.pi)).astype(np.int64)
    b = np.flatnonzero(np.diff(turns) > 0) + 1
    return b, peak, err


base.phase_boundaries = common_phase_boundaries
base.OUT = Path("results/e000f_v2")

if __name__ == "__main__":
    base.main()
