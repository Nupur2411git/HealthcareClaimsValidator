import json
import csv
import os
from validation_rules import (
    validate_required_fields,
    validate_dates,
    validate_amounts,
    validate_unique_ids  # Import updated uniqueness checker
)

# Function to load claims from CSV
def load_claims(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Function to load client config from JSON
def load_client_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

# Load data
claims = load_claims('input_data/claims_sample.csv')
config = load_client_config('configs/client1.json')

# Output folder setup
os.makedirs('output_reports', exist_ok=True)
output_file = 'output_reports/client1_report.csv'

print("Claim Validation Report:\n")

# 🔍 Step 1: Check for duplicate ClaimIDs (returns set)
duplicate_ids = validate_unique_ids(claims)
if duplicate_ids:
    print("🚨 Duplicate ClaimIDs found:")
    for dup in duplicate_ids:
        print(f" - {dup}")
    print()

# 🔍 Step 2: Validate each claim and write to report
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ClaimID', 'Status', 'Errors'])

    for claim in claims:
        errors = []
        claim_id = claim.get('ClaimID', '').strip()

        # Add duplicate ID error if found
        if claim_id in duplicate_ids:
            errors.append(f"Duplicate ClaimID: {claim_id}")

        # Apply validation rules from config
        if config.get("validate_required_fields", True):
            errors += validate_required_fields(claim)

        if config.get("validate_dates", True):
            errors += validate_dates(claim)

        if config.get("validate_amounts", True):
            errors += validate_amounts(claim)

        # Terminal and CSV Output
        if errors:
            status = 'Invalid ❌'
            error_str = '; '.join(errors)
            print(f"Claim {claim_id} has errors:")
            for e in errors:
                print(f" - {e}")
            print()
        else:
            status = 'Valid ✅'
            error_str = ''
            print(f"Claim {claim_id} is valid ✅\n")

        writer.writerow([claim_id, status, error_str])
