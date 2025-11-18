import random


def get_simulated_data() -> dict:
    hrv_val = random.uniform(20.0, 100.0)
    gsr_val = random.uniform(0.1, 5.0)

    return {
        "hrv_raw": hrv_val,
        "gsr_raw": gsr_val
    }
