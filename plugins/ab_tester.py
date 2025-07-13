
import random

def ab_test(variants):
    return random.choice(variants)

def record_result(variant_id, result):
    with open("logs/ab_results.csv", "a") as f:
        f.write(f"{variant_id},{result}\n")
