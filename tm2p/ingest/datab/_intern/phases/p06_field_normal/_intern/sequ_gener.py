import itertools
import string

_counter = itertools.count()


def sequ_gener():
    digits = string.digits + string.ascii_uppercase
    n, result = next(_counter), []
    if n == 0:
        result = ["0"]
    while n > 0:
        result.append(digits[n % 36])
        n //= 36
    return "/" + "".join(reversed(result)).zfill(4)
