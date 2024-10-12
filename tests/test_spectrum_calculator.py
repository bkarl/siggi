from unittest.mock import MagicMock,patch
import numpy as np
import pytest
from siggi.spectrum_calculator import SpectrumCalculator

@pytest.fixture(scope='function')
def setup(request):
    updater = MagicMock()
    raw_samples = np.arange(4096)
    request.cls.spectrum_calculator = SpectrumCalculator(raw_samples, updater)
    request.cls.updater = updater
    yield


@pytest.mark.usefixtures("setup")
class TestSpectrumCalculator():
    def test_calc_initial_sample_selection(self):
        self.spectrum_calculator.calc_initial_sample_selection()
        np.testing.assert_array_equal(self.spectrum_calculator.selected_samples, np.arange(1024))

    @patch("siggi.spectrum_calculator.fftfreq")
    def test_calc_frequency_axes(self, fftfreq):
        fftfreq.return_value = np.arange(4096)
        self.spectrum_calculator.calc_frequency_axes()
        np.testing.assert_array_equal(self.spectrum_calculator.xf, np.arange(512))

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