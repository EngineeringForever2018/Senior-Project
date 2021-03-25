import numpy as np
import math

RTOL = 1e-04
ATOL = 1e-07


def npclose(first, second):
    if isnumber(first) or isnumber(second):
        return math.isclose(first, second, rel_tol=RTOL, abs_tol=ATOL)

    return np.allclose(first, second, rtol=RTOL, atol=ATOL)


def isnumber(number):
    return isinstance(number, float) or isinstance(number, int)
