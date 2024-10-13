import os

import numpy as np


NUM_POINTS = 16384
FS = 10e3
dt = 1/FS

TESTDATA_DIR = "../testdata/"

def gen_cw_and_burst():
    t = np.arange(0.0, NUM_POINTS * dt, dt)
    #s1 = np.sin(2 * np.pi * 100 * t)
    s1 = np.exp(1j * 2*np.pi * t * 1000)
    #s2 = 2 * np.sin(2 * np.pi * 4000 * t)
    s2 = 2*np.exp(1j * 2*np.pi * t * 4000)

    # create a transient "chirp"
    s2[t <= 1.0] = s2[1.2 <= t] = 0

    # add some noise into the mix
    nse = 0.01 * np.random.random(size=len(t))
    # make a new figure
    samples = s1 + s2 + nse
    np.save(TESTDATA_DIR+'sine_and_burst_double_10e3hz.npy', samples.real)
    np.save(TESTDATA_DIR+'sine_and_burst_complex_10e3hz.npy', samples)


if __name__ == '__main__':
    os.makedirs(TESTDATA_DIR, exist_ok=True)
    gen_cw_and_burst()