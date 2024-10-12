from siggi.blit_manager import BlitManager
import time

UPDATE_TIME_S = 0.01

class SampleSelector(BlitManager):
    def __init__(self, canvas, sample_selector, spectrum_calculator, n_samples, fs, fft_size):
        super().__init__(canvas)
        self.sample_selector = sample_selector
        self.spectrum_calculator = spectrum_calculator
        self.n_samples = n_samples
        self.fs = fs
        self.fft_size = fft_size
        self.last_update = time.time()
        connect = self.canvas.mpl_connect
        connect('motion_notify_event', self.on_mouse_move)

        self.add_artist(sample_selector)

    def on_mouse_move(self, event):
        if time.time() - self.last_update > UPDATE_TIME_S:
            self.last_update = time.time()

            if event.xdata and event.ydata:
                new_center = int(event.xdata * self.fs) - self.fft_size//2
                if new_center <= 0 or new_center > self.n_samples - self.fft_size:
                    return
                self.sample_selector.set_xy((new_center/self.fs, self.sample_selector.get_y()))
                self.spectrum_calculator.notifyUpdate(new_center)
                self.update()
