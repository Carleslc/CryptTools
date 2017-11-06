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
        print(f'i: {i}\ta: {bin(a)}\tb: {bin(b)}\tr: {bin(r)} ({hex(r)})')
        if least_bit(b):
            r = add(r, a)
        overflow = highest_bit(a)
        a <<= 1
        if overflow:
            a = fit(add(a, x8))
        b >>= 1
        print(f'i: {i}\ta: {bin(a)}\tb: {bin(b)}\tr: {bin(r)} ({hex(r)})')
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

def test():
    def test_product(i):
        for j in range(256):
            tij = GF_product_t(i, j)
            tji = GF_product_t(j, i)
            pij = GF_product_p(i, j)
            pji = GF_product_p(j, i)
            assert tij == tji
            assert pij == pji
            assert tij == pij

    def test_invers(i):
        inv = GF_invers(i)
        assert (i == 0 and inv == 0) or GF_product_t(i, inv) == 1

    GF_tables()
    for i in range(256):
        test_product(i)
        test_invers(i)

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
    return 0 if a == 0 or b == 0 else exp_t[(log_t[a] + log_t[b]) % 255]

def GF_tables(generator=0x03):
    """Generates exponential (exp[i] == `generator`**i) and logarithm (log[`generator`**i] == i) tables"""
    global exp_t, log_t
    exp_t = [1] * 256
    log_t = [None] * 256

    for i in range(1, 256):
        exp_t[i] = GF_product_p(generator, exp_t[i - 1])
        log_t[exp_t[i]] = i % 255

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

def GF_invers(a):
    return 0 if a == 0 else exp_t[255 - log_t[a]]

## TIMING TESTS

def measure(f, repetitions=1000):
    """Measures CPU mean time consumed by f method call repeated `repetitions` times (in fractional seconds)"""
    elapsed = 0
    for _ in range(repetitions):
        start = time.process_time()
        f()
        end = time.process_time()
        elapsed += end - start
    return elapsed / repetitions

def measure_ms(f, repetitions=500):
    """Returns CPU mean time consumed by f method call (in fractional milliseconds)"""
    return measure(f, repetitions) * 1000

def print_ms(name, ms):
    print(f'{name}:\t{"{:.4f}".format(ms)} ms per call')

def measure_and_print(f, repetitions=500):
    """Prints CPU mean time consumed by f method call (in fractional milliseconds)"""
    print_ms(f.__name__, measure_ms(f, repetitions))

def wrap(f, **kwargs):
    """Returns a function that, when called, executes `f` with `kwargs` parameters"""
    @wraps(f)
    def wrapper():
        return f(**kwargs)
    return wrapper

def compare_p_t():
    print("Compare GF_product_p(a, b) vs GF_product_t(a, b) [10 repetitions for each a and b from 0 to 255]")
    total_ms_p = 0
    total_ms_t = 0
    for i in range(256):
        print("a: " + str(i) + ", Testing all b...")
        for j in range(256):
            total_ms_p += measure_ms(wrap(GF_product_p, a=i, b=j), repetitions=10)
            total_ms_t += measure_ms(wrap(GF_product_t, a=i, b=j), repetitions=10)
    print_ms("GF_product_p(a, b)", total_ms_p / (256 * 256))
    print_ms("GF_product_t(a, b)", total_ms_t / (256 * 256))
    print()

def compare(second):
    print("Compare GF_product_p(a, " + hex(second) + ") vs GF_product_t(a, " + hex(second) + ") [500 repetitions for each a from 0 to 255]")
    def measure_compare(first):
        ms_p = measure_ms(wrap(GF_product_p, a=first, b=second))
        ms_t = measure_ms(wrap(GF_product_t, a=first, b=second))
        return ms_p, ms_t
    total_ms_p = 0
    total_ms_t = 0
    for i in range(256):
        ms_p, ms_t = measure_compare(i)
        total_ms_p += ms_p
        total_ms_t += ms_t
    print_ms("GF_product_p(a, " + hex(second) + ")", total_ms_p / 256)
    print_ms("GF_product_t(a, " + hex(second) + ")", total_ms_t / 256)
    print()

if __name__ == "__main__":
    test()
    print(f'exp_t: {exp_t}')
    print(f'log_t: {log_t}')
    print(bin(GF_product_p_verbose(0b10000011, 0b01010111)));
    measure_and_print(wrap(GF_tables), repetitions=100)
    measure_and_print(wrap(GF_invers, a=0b110))
    measure_and_print(GF_generador, repetitions=50)
    compare_p_t()
    compare(0x02)
    compare(0x03)
    compare(0x09)
    compare(0x0B)
    compare(0x0D)
    compare(0x0E)