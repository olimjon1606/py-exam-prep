import math

def identity(x=1):
    z = complex(0, 1)
    return math.atan2(z.imag, z.real) / (2 * 3.141592) * 4 * x
