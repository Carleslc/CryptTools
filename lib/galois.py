#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import time
from functools import partial, wraps

# All arithmetic is done with polynomials within GF(2^8)

## METHOD UTILS

x8 = 0b11011 # x^8 = x^4 + x^3 + x + 1 -> 0x1B
range8 = range(8)

def add(x, y):
    """
    Performs x + y
    Substraction is equivalent
    """
    return x ^ y

def GF_product_p_verbose(a, b):
    """Performs a * b where a and b are polinomials in its binary representation. Verbose version"""
    print(f'{bin(a)} * {bin(b)}')
    r = 0
    for i in range8:
        if least_bit(b):
            r = add(r, a)
        overflow = highest_bit(a)
        a <<= 1
        if overflow:
            a = fit(add(a, x8))
        b >>= 1
        print(f'i: {i}\tb: {hex(b)}\tr: {hex(r)} ({bin(r)})')
    return r

def bit_at(b, i):
    """Returns bit at position i of b (where least_bit is position 0)"""
    return b & (1 << i)

def least_bit(b):
    """Returns b least significant bit"""
    return b & 1

def highest_bit(b):
    """Returns b most significant bit"""
    return b & 0x80

def fit(b):
    """Keeps 8 least significant bits"""
    return b & 0xFF

def measure(f, repetitions=1000):
    """Measures CPU mean time consumed by f method call repeated `repetitions` times (in fractional seconds)"""
    elapsed = 0
    for _ in range(repetitions):
        start = time.process_time()
        f()
        end = time.process_time()
        elapsed += end - start
    return elapsed / repetitions

def measure_ms(f, repetitions=1000):
    """Prints CPU mean time consumed by f method call (in fractional milliseconds)"""
    return print(f'{f.__name__}:\t{"{:.4f}".format(measure(f, repetitions) * 1000)} ms per call')

def wrap(f, **kwargs):
    """Returns a function that, when called, executes `f` with `kwargs` parameters"""
    @wraps(f)
    def wrapper():
        return f(**kwargs)
    return wrapper

def test_product():
    for i in range(256):
        for j in range(256):
            tij = GF_product_t(i, j)
            tji = GF_product_t(j, i)
            pij = GF_product_p(i, j)
            pji = GF_product_p(j, i)
            assert tij == tji
            assert pij == pji
            assert tij == pij

## OPTIMIZED METHODS

def GF_product_p(a, b):
    """Performs a * b where a and b are polinomials in its binary representation. Inline version (more efficient)"""
    r = 0
    for _ in range8:
        if b & 1:
            r ^= a
        overflow = a & 0x80
        a <<= 1
        if overflow:
            a = (a ^ x8) & 0xFF
        b >>= 1
    return r

def GF_product_t(a, b):
    """Performs a * b where a and b are polinomials in its binary representation. Tables version"""
    return 0 if a == 0 or b == 0 else exp_t[(log_t[a] + log_t[b] + 1) % 255]

def GF_tables(generator=0x03):
    """Generates exponential (exp[i] == `generator`**i) and logarithm (log[`generator`**i] == i) tables"""
    global exp_t, log_t
    exp_t = [generator] * 256
    log_t = [0] * 256

    for i in range(1, 256):
        exp_t[i] = GF_product_p(generator, exp_t[i - 1])
        log_t[exp_t[i]] = i

    return (exp_t, log_t)

def GF_generador():
    gen_list = []
    for gen in range(2, 256):
        i = 1
        g_i = gen
        while g_i != 1:
            g_i = GF_product_t(g_i, gen)
            i += 1
        if i == 255:
            gen_list.append(gen)
    return gen_list

# FIXME
def GF_invers(a):
    return 0 if a == 0 else exp_t[254 - log_t[a]]

## TIMING TESTS

if __name__ == "__main__":
    measure_ms(wrap(GF_tables), repetitions=100)
    measure_ms(wrap(GF_product_p, a=0b110, b=0b11))
    measure_ms(wrap(GF_product_t, a=0b110, b=0b11))
    measure_ms(wrap(GF_invers, a=0b110))
    measure_ms(GF_generador, repetitions=50)
    test_product()
    print(GF_generador())
    assert GF_invers(1) == 1