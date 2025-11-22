def calculate_stress_index(hrv: float, gsr: float) -> float:
    if hrv == 0:
        return 100.0

    stress_index = (gsr * 10) / (hrv / 50)
    return round(stress_index, 2)


def analyze_session_statistics(records: list) -> dict:
    if not records:
        return {"average_hrv": 0, "max_stress_index": 0}

    total_hrv = sum(r['hrv_score'] for r in records)
    avg_hrv = total_hrv / len(records)

    stress_indices = [calculate_stress_index(r['hrv_score'], r['gsr_score']) for r in records]
    max_stress = max(stress_indices)

    return {
        "average_hrv": round(avg_hrv, 2),
        "max_stress_index": max_stress,
        "total_records": len(records)
    }