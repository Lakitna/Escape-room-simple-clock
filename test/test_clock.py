import threading
import time
import pytest
from . import before
import clock

@pytest.fixture
def cd():
    return clock.Countdown(3600)

def test_is_thread(cd):
    assert isinstance(cd, threading.Thread)

def test_make_countdown(cd):
    assert cd.duration == 3600
    assert cd.remaining == 3600
    assert cd.elapsed == 0
    assert cd.active is False
    assert cd.done is False

    assert cd.is_alive()
    assert cd.daemon

def test_call_self(cd):
    assert cd() == "01:00:00"

def test_format(cd):
    assert cd._format(60) == "00:01:00"
    assert cd._format(0) == "00:00:00"
    assert cd._format(-1) == "23:59:59"
    assert cd._format(3661) == "01:01:01"

def test_countdown_start_stop(cd):
    cd.resume()
    assert cd.active
    time.sleep(1.1)
    assert cd.remaining == 3599
    assert cd.elapsed == 1
    assert cd.duration == 3600
    assert cd.done is False

    cd.pause()
    assert cd.active is False

def test_countdown_set_done(cd):
    cd.set(1)
    assert cd.remaining == 1
    assert cd.duration == 1
    assert cd.elapsed == 0
    assert cd.active is False

    cd.resume()
    started_on = cd._started_on

    time.sleep(1.1)
    cd.resume()
    assert started_on == cd._started_on

    assert cd.done is True
    assert cd.active is False
    assert cd.remaining == 0
