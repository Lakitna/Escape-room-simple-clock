import os
from subprocess import call
import pytest
from . import before
import gui as module

@pytest.yield_fixture(autouse=True)
def run_around_tests():
    # Code that will run before your test
    os.environ["DISPLAY"] = ":0.0"

    yield
    # Code that will run after your test


@pytest.fixture
def gui():
    return module.GUI()


def test_init():
    g = module.GUI(fps=10, fullscreen=True)
    assert g.loop_delay == 0.01
    assert g.fullscreen is True
