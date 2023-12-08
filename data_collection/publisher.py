import time
import os
import csv
from typing import Dict, List


def write_results(records: List[Dict], result: Dict, target_dir: str) -> None:
    """
    generates two files, final result, and sequence of records (e.g., turns)
    """
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    os.mkdir(f"{target_dir}/{timestamp}")

    with open(f"{target_dir}/{timestamp}/final_result.csv", "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=result.keys())
        writer.writeheader()
        writer.writerow(result)
    f.close()

    with open(f"{target_dir}/{timestamp}/steps.csv", "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
