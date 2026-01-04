#!/usr/bin/env python3
"""Debug import issue."""

try:
    from parallel_transmission_path import (
        ParallelTransmissionPath,
        TransmissionStatus,
        ObservationPriority
    )
    print("SUCCESS: Import worked")
    print(f"  ParallelTransmissionPath: {ParallelTransmissionPath}")
    print(f"  TransmissionStatus: {TransmissionStatus}")
    print(f"  ObservationPriority: {ObservationPriority}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
