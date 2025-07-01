from datetime import datetime

# Rule 1: Required fields check
def validate_required_fields(claim):
    required = ['ClaimID', 'PatientName', 'DateOfService', 'AmountCharged', 'AmountPaid']
    errors = []
    for field in required:
        if not claim[field]:  # empty string or missing
            errors.append(f"Missing {field}")
    return errors

# Rule 2: Date format check
def validate_dates(claim):
    try:
        datetime.strptime(claim['DateOfService'], '%Y-%m-%d')
        return []
    except:
        return ["Invalid DateOfService"]

# Rule 3: Amount logic check
def validate_amounts(claim):
    try:
        charged = float(claim['AmountCharged'])
        paid = float(claim['AmountPaid'])
        if paid > charged:
            return ["AmountPaid exceeds AmountCharged"]
        return []
    except:
        return ["Invalid amount format"]
    

def validate_unique_ids(claims):
    seen = set()
    duplicates = set()

    for claim in claims:
        claim_id = claim.get("ClaimID", "").strip()
        if not claim_id:
            continue
        if claim_id in seen:
            duplicates.add(claim_id)
        else:
            seen.add(claim_id)

    return duplicates
