import csv
import json
import os

# ---------------------------
# Step 1: Load data
# ---------------------------
def load_claims(data_folder):
    claims = []
    auto_id = 1

    # Load CSV (alpha)
    alpha_path = os.path.join(data_folder, "emr_alpha.csv")
    if os.path.exists(alpha_path):
        with open(alpha_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not any(row.values()):
                    continue
                row["source_system"] = "alpha"
                # Give auto claim_id if missing
                if not row.get("claim_id"):
                    row["claim_id"] = f"AUTO_{auto_id}"
                    auto_id += 1
                claims.append(row)

    # Load JSON (beta)
    beta_path = os.path.join(data_folder, "emr_beta.json")
    if os.path.exists(beta_path):
        with open(beta_path, encoding="utf-8") as f:
            data = json.load(f)
            for row in data:
                if not any(row.values()):
                    continue
                row["source_system"] = "beta"
                if not row.get("claim_id"):
                    row["claim_id"] = f"AUTO_{auto_id}"
                    auto_id += 1
                claims.append(row)

    return claims

# ---------------------------
# Step 2: Process claims
# ---------------------------
def process_claims(claims):
    resubmission_candidates = []
    excluded = []

    for claim in claims:
        claim_id = claim.get("claim_id", "UNKNOWN")
        denial_reason = claim.get("denial_reason", "")
        status = claim.get("status", "")

        # Exclude malformed claims
        if not claim.get("patient_id"):
            excluded.append((claim_id, "Missing patient_id"))
            continue

        if status.lower() != "denied":
            excluded.append((claim_id, "Not denied"))
            continue

        # Hardcoded simple classifier
        recommended = None
        if "npi" in denial_reason.lower():
            recommended = "Review NPI number and resubmit"
        elif "modifier" in denial_reason.lower():
            recommended = "Add correct modifier and resubmit"
        elif "prior auth" in denial_reason.lower():
            recommended = "Obtain prior authorization and resubmit"

        if recommended:
            resubmission_candidates.append({
                "claim_id": claim_id,
                "resubmission_reason": denial_reason,
                "source_system": claim.get("source_system", "unknown"),
                "recommended_changes": recommended
            })
        else:
            excluded.append((claim_id, "Denial reason not auto-classifiable"))

    return resubmission_candidates, excluded

# ---------------------------
# Step 3: Save output
# ---------------------------
def save_output(resubmission_candidates, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resubmission_candidates, f, indent=2)

# ---------------------------
# Step 4: Pipeline runner
# ---------------------------
def run_pipeline():
    data_folder = "data"
    output_file = "resubmission_candidates.json"

    claims = load_claims(data_folder)
    resubmission_candidates, excluded = process_claims(claims)
    save_output(resubmission_candidates, output_file)

    # ---------------------------
    # Logging / Metrics
    # ---------------------------
    print("\n--- Pipeline Summary ---")
    print(f"Total claims processed: {len(claims)}")

    # Source breakdown
    sources = {}
    for c in claims:
        src = c.get("source_system", "unknown")
        sources[src] = sources.get(src, 0) + 1
    print(f"From sources: {sources}")

    print(f"Flagged for resubmission: {len(resubmission_candidates)}")
    print(f"Excluded: {len(excluded)}")

    if excluded:
        print("\nExcluded claims with reasons:")
        for cid, reason in excluded:
            print(f"  - {cid}: {reason}")

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    run_pipeline()

