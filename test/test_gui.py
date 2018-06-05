import os
import pytest
from . import before
import gui as module

@pytest.fixture
def gui():
    os.system("export DISPLAY=:0.0")
    return module.GUI()


def test_init():
    g = module.GUI(fps=10, fullscreen=True)
    assert g.loop_delay == 0.01
    assert g.fullscreen is True
