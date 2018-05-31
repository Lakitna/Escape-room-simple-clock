import os
import threading
import pytest
from . import before
import sound


@pytest.yield_fixture(autouse=True)
def run_around_tests():
    # Code that will run before your test
    sound.player = sound.SoundPlayer(path="_test")

    yield
    # Code that will run after your test
    sound.player.unload()


def test_initialization():
    p = os.path.dirname(os.path.realpath(__file__))
    sound.player = sound.SoundPlayer(path=p)
    assert sound.player.sound_filepath == p

    p = "someSubDir"
    sound.player = sound.SoundPlayer(path=p)
    assert sound.player.sound_filepath.endswith('/%s' % p)


def test_is_thread():
    assert isinstance(sound.player, threading.Thread)


def test_play_sound():
    sound.load("beep")
    sound.queue("beep", .01)
    sound.queue("beep")
    assert sound.player.queue_length == 2
    sound.wait_done()


load_sound_test_cases = (
    ("comment", "input_", "expected"),
    [
        ["Bare minimum", {
            'file': 'beep'
        }, 'beep'],
        ["With extention", {
            'file': 'beep.wav'
        }, 'beep'],
        ["Unsupported extention", {
            'file': 'beep.unsupported'
        }, sound.SoundPlayerException],
        ["Name changed", {
            'file': 'beep',
            'name': 'someName',
        }, 'someName'],
        ["Unavailable file", {
            'file': 'someObscureFilename.wav',
        }, sound.SoundPlayerException],
    ]
)

@pytest.mark.parametrize(*load_sound_test_cases)
def test_load_sound(comment, input_, expected):
    if type(expected) is type:
        if issubclass(expected, Exception):
            with pytest.raises(expected) as e_info:
                sound.load(**input_)
    else:
        sound.load(**input_)
        assert expected in sound.player.sounds
        assert isinstance(sound.player.sounds[expected], sound.sa.WaveObject)


def test_load_all_test_folder():
    sound.load_all()
    assert len(sound.player.sounds) == 2
    assert 'beep' in sound.player.sounds
    assert 'mario-boo' in sound.player.sounds


queue_sound_test_cases = (
    ("comment", "load", "input_", "expected"),
    [
        ["Bare minimum", "beep", {
            'name': 'beep'
        }, ('beep', 0)],
        ["Unloaded, unkown file", None, {
            'name': 'someObscureSoundName'
        }, sound.SoundPlayerException],
        ["Unloaded, kown file", None, {
            'name': 'beep'
        }, ('beep', 0)],
        ["Happy with duration", 'beep', {
            'name': 'beep',
            'duration': 0.1
        }, ('beep', 0.1)],
        ["Name with valid extention", 'beep', {
            'name': 'beep.wav'
        }, ('beep', 0)],
        ["Name with invalid extention", 'beep', {
            'name': 'beep.unsupported'
        }, ('beep', 0)],
    ]
)

@pytest.mark.parametrize(*queue_sound_test_cases)
def test_queue_sound(comment, load, input_, expected):
    if load is not None:
        sound.load(load)

    if type(expected) is type:
        if issubclass(expected, Exception):
            with pytest.raises(expected) as e_info:
                sound.queue(**input_)
    else:
        sound.queue(**input_)
        assert sound.player.queue_length == 1
        queued = sound.player.queue.get_nowait()
        assert expected[0] == queued[0]
        assert isinstance(queued[1], sound.sa.WaveObject)
        assert expected[1] == queued[2]


def test_wait_done():
    def func(val):
        assert val == "SomeString"

    sound.load('beep')
    sound.queue('beep')
    sound.wait_done(func, {'val': 'SomeString'})
