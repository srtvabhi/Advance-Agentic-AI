class TemporaryVendorError(Exception):
    pass


def verify_vendor(retry_count: int) -> str:
    # Simulate a recoverable external API failure on the first attempt.
    if retry_count == 0:
        raise TemporaryVendorError("Vendor API timeout. Retry required.")

    return "Vendor verified successfully on retry."

