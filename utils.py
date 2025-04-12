# utils.py
def short_address(address):
    if len(address) > 10:
        return address[:4] + "..." + address[-4:]
    return address
