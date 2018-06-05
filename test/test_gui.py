import pytest
from . import before
import gui as module

@pytest.fixture
def gui():
    return module.GUI()


def test_init():
    g = module.GUI(fps=10, fullscreen=True)
    assert g.loop_delay == 0.01
    assert g.fullscreen is True


# def test_keybind(gui):
#     gui.key("<Escape>")
#     print(gui.window.tk)
#     print(dict(gui.window.tk))
#     assert False
