import os
import random
import numpy as np
from commpy import rrcosfilter, PSKModem
import matplotlib.pyplot as plt

FS = 10e3
dt = 1/FS
N_BURSTS = 5
TESTDATA_DIR = "../testdata/"
BITS_PER_SYMBOL = 2
OS = 8

def gen_cw_and_burst(filename, num_samples):
    modem = PSKModem(4)
    t = np.arange(0.0, num_samples * dt, dt)
    cw = np.exp(1j * 2*np.pi * t * 1000)
    #bursts = 2 * np.sin(2 * np.pi * 4000 * t)
    bursts = np.zeros(num_samples, dtype=complex)
    #bursts = 2*np.exp(1j * 2*np.pi * t * 4000)
    #plt.plot(np.arange(h_rrcos.size), h_rrcos)
    #plt.show()
    # create bursts
    h_rrcos = rrcosfilter(100, 0.35, 1, OS)[1]
    for i in range(N_BURSTS):
        n_samples_burst = random.randint(0, num_samples//2)
        n_samples_burst -= n_samples_burst % 2
        n_bits = (n_samples_burst // OS) * BITS_PER_SYMBOL
        bits = np.random.randint(2, size=n_bits)
        symbols = modem.modulate(bits)
        filtered = np.zeros(symbols.size * OS, dtype=complex)
        filtered[::OS] = symbols
        filtered = np.convolve(filtered, h_rrcos, mode='valid')
        start = random.randint(0, num_samples - filtered.size)
        shift = random.randint(-int(FS//4), int(FS/4))
        t_shift = np.arange(0.0, filtered.size * dt, dt)[:filtered.size]

        bursts[start:start + filtered.size] = filtered * np.exp(1j * 2*np.pi * t_shift * shift)

    # add some noise into the mix
    nse = 0.01 * np.random.random(size=len(t))
    # make a new figure
    samples = bursts + nse + cw
    np.save(TESTDATA_DIR+f'{filename}_real_10e3hz.npy', samples.real)
    np.save(TESTDATA_DIR+f'{filename}_complex_10e3hz.npy', samples)


if __name__ == '__main__':
    os.makedirs(TESTDATA_DIR, exist_ok=True)
    large_file_size_byte = 1e9
    n_samples_large_files = int(large_file_size_byte)//16
    gen_cw_and_burst("testdata_small", num_samples=16384)
    gen_cw_and_burst("testdata_large", num_samples=n_samples_large_files)