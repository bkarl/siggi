from siggi.blit_manager import BlitManager

class SpectrumUpdater(BlitManager):
    def __init__(self, canvas, spectrum_line):

        super().__init__(canvas)
        self.spectrum_line = spectrum_line
        self.add_artist(spectrum_line)

    def update_spectrum(self, new_spectrum):
        xf, yf = new_spectrum
        self.spectrum_line.set_xdata(xf)
        self.spectrum_line.set_ydata(yf)
        self.update()

