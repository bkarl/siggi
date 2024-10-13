import time
from unittest.mock import MagicMock,patch
import numpy as np
import pytest
from siggi.sample_selector import SampleSelector, UPDATE_TIME_S
from siggi.structs.file_parameters import FileParameters


@pytest.fixture(scope='function')
def setup(request):
    canvas = MagicMock()
    selector = MagicMock()
    selector.figure = 5
    selector.get_y.return_value = 0x55
    canvas.figure = 5
    calculator = MagicMock()
    param = FileParameters.create(fs=10e3, path='', n_samples=8192, fft_size=1024)
    request.cls.sample_selector = SampleSelector(canvas, selector, calculator, param)
    request.cls.sample_selector.update = MagicMock()
    request.cls.calculator = calculator
    request.cls.selector = selector
    yield


@pytest.mark.usefixtures("setup")
class TestSpectrumCalculator():
    def test_on_mouse_update_time(self):
        time.sleep(UPDATE_TIME_S)
        event = MagicMock()
        event.xdata = 0.5
        event.ydata = 100
        self.sample_selector.on_mouse_move(event)
        self.sample_selector.on_mouse_move(event)
        self.sample_selector.update.assert_called_once()

    def test_on_mouse_wrong_event(self):
        time.sleep(UPDATE_TIME_S)
        event = MagicMock()
        self.sample_selector.on_mouse_move(event)
        self.sample_selector.update.assert_not_called()

    @pytest.mark.parametrize("x", [0.01, 0.99])
    def test_on_mouse_update_out_of_bounds(self, x):
        time.sleep(UPDATE_TIME_S)
        event = MagicMock()
        event.xdata = x
        event.ydata = 100
        self.sample_selector.on_mouse_move(event)
        self.sample_selector.update.assert_not_called()

    def test_on_mouse_update(self):
        time.sleep(UPDATE_TIME_S)
        event = MagicMock()
        event.xdata = 0.3
        event.ydata = 100
        new_center = 0.3*10e3 - 512
        self.sample_selector.on_mouse_move(event)
        self.sample_selector.update.assert_called_once()
        self.sample_selector.sample_selector.set_xy.assert_called_once_with((new_center/10e3, 0x55))

