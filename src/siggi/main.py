import numpy as np
import matplotlib
#matplotlib.use('TkAgg')
#matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from blit_manager import BlitManager
from scipy.fft import fft, fftfreq
from scipy import signal
from sample_selector import SampleSelector
from siggi.structs.file_parameters import FileParameters
from spectrum_calculator import SpectrumCalculator
from spectrum_updater import SpectrumUpdater
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

NUM_POINTS = 16384
FFT_SIZE = 1024
FS = 10e3
dt = 1/FS
t = np.arange(0.0, NUM_POINTS * dt, dt)
s1 = np.sin(2 * np.pi * 100 * t)
s2 = 2 * np.sin(2 * np.pi * 4000 * t)

# create a transient "chirp"
s2[t <= 1.0] = s2[1.2 <= t] = 0

# add some noise into the mix
nse = 0.01 * np.random.random(size=len(t))
# make a new figure

samples = s1 + s2 + nse  # the signal
fig_spec, ax_spec = plt.subplots()

fig_samples, ax_samples = plt.subplots()
ax_samples.specgram(samples, NFFT=FFT_SIZE, Fs=FS)

N = samples[:samples.size//4].size
yf = fft(samples[:samples.size//4])
xf = fftfreq(FFT_SIZE, dt)[:FFT_SIZE//2]
spec_line, = ax_spec.plot(xf, 2.0/FFT_SIZE * np.abs(yf[0:FFT_SIZE//2]), animated=True)
y_size = ax_samples.get_ylim()
# add a line
fftwidth_sec = FFT_SIZE/FS
rect = Rectangle((0, y_size[0]), fftwidth_sec, y_size[1], animated=True, linestyle='-', alpha=0.3, linewidth=1)
ax_samples.add_patch(rect)

param = FileParameters.create(FS, '', samples.size, FFT_SIZE)

su = SpectrumUpdater(fig_spec.canvas, spec_line)
sc = SpectrumCalculator(samples, su, param)
sss = SampleSelector(fig_samples.canvas, sample_selector=rect, spectrum_calculator=sc, file_params=param)

plt.show()

