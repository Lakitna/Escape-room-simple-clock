import pytest
from . import before
import sound
import settings as sett
import clock

@pytest.fixture()
def main():
    return before.main

@pytest.fixture()
def cd():
    return clock.Countdown(3600)


def test_launch_rockets(main):
    main.launch_rockets()
    assert sound.player.queue_length == sett.rocket_count

    sound.player.unload()

