def is_swap_allowed(line):
    customer = line.customer

    if line.is_golden_number:
        return False, "Golden number"

    if line.is_whitelisted:
        return False, "Whitelisted"

    if line.status != "ACTIVE":
        return False, "Line not active"

    if customer.fraud_location in ["PRISON_SITE", "DETACHED"]:
        return False, "Fraud location flagged"

    if not customer.iprs_verified:
        return False, "IPRS not verified"

    if not customer.iprs_approved:
        return False, "IPRS not approved"

    if line.is_roaming:
        return False, "Line roaming"

    if not line.on_in_data:
        return False, "Not on IN data"

    return True, None
