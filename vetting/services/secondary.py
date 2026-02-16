from decimal import Decimal

def validate_balance(actual, provided):
    actual = Decimal(actual)
    provided = Decimal(provided)

    diff = abs(actual - provided)

    if actual <= 100:
        return diff <= 10
    elif actual <= 1000:
        return diff <= 50
    elif actual <= 10000:
        return diff <= 100
    else:
        return diff <= actual * Decimal("0.1")


def evaluate_secondary(customer, wallet, answers):
    correct = 0

    if "mpesa_balance" in answers:
        if validate_balance(wallet.mpesa_balance, answers["mpesa_balance"]):
            correct += 1

    if "airtime_balance" in answers:
        if validate_balance(wallet.airtime_balance, answers["airtime_balance"]):
            correct += 1

    if "fuliza_limit" in answers and wallet.fuliza_opted_in:
        if wallet.fuliza_limit == answers["fuliza_limit"]:
            correct += 1

    if correct >= 3:
        return True

    return False
