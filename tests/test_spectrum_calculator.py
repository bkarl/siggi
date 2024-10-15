from unittest.mock import MagicMock,patch
import numpy as np
import pytest

from siggi.file_handling.file_reader import FileReader
from siggi.spectrum_calculator import SpectrumCalculator
from siggi.structs.file_parameters import FileParameters


@pytest.fixture(scope='function')
def setup(request):
    updater = MagicMock()
    raw_samples = np.arange(4096)
    param = FileParameters.create(fs=10e3, path='', n_samples=raw_samples.size, fft_size=1024)
    fr = FileReader(param, raw_samples)
    request.cls.spectrum_calculator = SpectrumCalculator(param, updater, fr)
    request.cls.updater = updater
    yield


@pytest.mark.usefixtures("setup")
class TestSpectrumCalculator():

    @patch("siggi.spectrum_calculator.fftfreq")
    def test_calc_frequency_axes(self, fftfreq):
        fftfreq.return_value = np.arange(4096)
        xf = self.spectrum_calculator.calc_frequency_axes(FileParameters.create(fs=10e3, fft_size=1024, path='', n_samples=0))
        np.testing.assert_array_equal(xf, np.arange(512))

    @pytest.mark.parametrize("new_center, expected_start, expected_stop", [(0, 0, 1024), (1024, 512, 1024 + 512), (8192, 4096-1024, 4096)])
    def test_calc_new_samples_selection(self, new_center, expected_start, expected_stop):
        self.spectrum_calculator.calc_new_samples_selection(new_center)
        np.testing.assert_array_equal(self.spectrum_calculator.selected_samples, np.arange(expected_start, expected_stop))

    def test_notifyUpdate(self):
        self.spectrum_calculator.calc_new_samples_selection = MagicMock()
        self.spectrum_calculator.calc_new_spectrum = MagicMock()
        self.spectrum_calculator.notifyUpdate(0x55)
        self.spectrum_calculator.calc_new_samples_selection.assert_called_once_with(0x55)
        self.spectrum_calculator.calc_new_spectrum.assert_called_once()
        self.updater.update_spectrum.assert_called_once()