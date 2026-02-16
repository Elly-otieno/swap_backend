import re

class InvalidMSISDN(Exception):
    pass


def normalize_msisdn(msisdn: str) -> str:
    """
    Converts Kenyan phone numbers to E.164 format without '+'.
    Example:
        07XXXXXXXX -> 2547XXXXXXXX
        01XXXXXXXX -> 2541XXXXXXXX
        +2547XXXXXXX -> 2547XXXXXXX
    """

    if not msisdn:
        raise InvalidMSISDN("MSISDN is required")

    # Remove spaces and +
    msisdn = msisdn.strip().replace(" ", "")
    msisdn = re.sub(r"[^\d]", "", msisdn)

    # Handle starting with 0
    if msisdn.startswith("0") and len(msisdn) == 10:
        msisdn = "254" + msisdn[1:]

    # Handle +254 already removed to 254
    if msisdn.startswith("254") and len(msisdn) == 12:
        pass
    else:
        raise InvalidMSISDN("Invalid Kenyan phone number format")

    # Validate prefix
    if not (msisdn.startswith("2547") or msisdn.startswith("2541")):
        raise InvalidMSISDN("Invalid Kenyan mobile prefix")

    if len(msisdn) != 12:
        raise InvalidMSISDN("MSISDN must be 12 digits")

    return msisdn
