from unittest.mock import MagicMock

import pytest
from siggi.spectrum_updater import SpectrumUpdater

@pytest.fixture(scope='function')
def setup(request):
    canvas = MagicMock()
    spec_line = MagicMock()
    spec_line.figure = 5
    canvas.figure = 5
    request.cls.spectrum_updater = SpectrumUpdater(canvas, spec_line)
    request.cls.spec_line = spec_line
    yield


@pytest.mark.usefixtures("setup")
class TestSpectrumUpdater():
    def test_update_spectrum(self):
        new_spectrum = 44, 55
        self.spectrum_updater.update = MagicMock()
        self.spectrum_updater.update_spectrum(new_spectrum)
        self.spec_line.set_xdata.assert_called_once_with(44)
        self.spec_line.set_ydata.assert_called_once_with(55)
        self.spectrum_updater.update.assert_called_once()
