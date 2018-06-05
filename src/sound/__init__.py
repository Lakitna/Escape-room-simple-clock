"""Simplaudio module wrapper"""

import os
import time
import threading
import logging
from queue import Queue
import simpleaudio as sa


class SoundPlayerException(Exception):
    """Module specific exception"""
    pass


class SoundPlayer(threading.Thread):
    """
    Provides audio player in new thread.
    """
    def __init__(self, path=None, runner=None):
        """Create a new thread and start it."""
        threading.Thread.__init__(self)
        self.name = "Sound-T%s" % self.name.split("-")[-1]
        self.daemon = True
        self.queue = Queue()
        self.sounds = {}
        self.playing = False
        self.runner = runner

        self.sound_filepath = os.path.dirname(os.path.realpath(__file__))
        if path is not None:
            if os.path.isabs(path):
                self.sound_filepath = path
            else:
                self.sound_filepath = os.path.join(self.sound_filepath, path)

        self.start()

    def __repr__(self):
        return "<SoundPlayer @ %s | %d sounds queued>" % (
            self.name,
            self.queue_length
        )

    def run(self):
        """The body of the thread.

        Plays sounds from the queue if available.
        """
        while True:
            item = self.queue.get(block=True)  # Wait for new item in queue
            name = item[0]
            wave_object = item[1]
            duration = item[2]

            self.playing = True

            try:
                if self.runner != "ci":
                    player_obj = wave_object.play()
                if duration > 0:  # If custom duration
                    logging.info("Playing sound: '%s' (%.2fs)",
                                 name, duration)
                    time.sleep(duration)
                else:  # If file duration
                    logging.info("Playing sound: '%s'", name)
                    player_obj.wait_done()
            finally:
                self.playing = False

    @property
    def queue_length(self):
        """ Get the current length of the queue. """
        return self.queue.qsize()

    def queue_clear(self):
        """ Empty the queue """
        self.queue.empty()

    def unload(self):
        """ Unload everything """
        self.queue_clear()
        self.sounds.clear()


# pylint: disable=C0103
# Expose the class to the ouside of the module
player = SoundPlayer()


def load_all(directory=None, depth=0):
    """Load all sound.wav files from module folder and its subfolders.

    Args:
        directory (str, None): Current working directory, used for recursion.
                               Defaults to module directory.
        top_level (bool, True): Tracks recursion depth.

    Returns:
        True on succes
        False on fail
    """
    if directory is None:
        directory = ''
    else:
        directory += '/'

    path = os.path.join(player.sound_filepath, directory)
    files = [f for f in os.listdir(path)
             if os.path.isfile(os.path.join(path, f))
             and f.endswith(".wav")]
    dirs = [d for d in os.listdir(path)
            if os.path.isdir(os.path.join(path, d))
            and not d.startswith("_")]

    for f in files:
        load("%s%s" % (directory, f))
    logging.debug("Loaded %d sounds @ depth %d", len(files), depth)
    for d in dirs:
        load_all("%s%s" % (directory, d), depth=(depth + 1))

    if depth == 0:
        logging.info(
            "A total of %d sound files have been loaded",
            len(player.sounds)
        )


def load(file, name=None):
    """Load a sound file

    Args:
        file (str): Filename to be loaded.
                    When no extention is specified .wav will be used.
        name (str, None): Identifier of the sound used in queue()
                          Defaults to file name without extention.

    Returns:
        True on succes
        False on fail
    """
    split = file.rsplit(".", 1)
    if len(split) == 1:
        file = "%s.wav" % file
        split = file.rsplit(".", 1)

    if split[1] != 'wav':
        raise SoundPlayerException(
            "File has unsupported extention '.%s'" % split[-1])

    if name is None:
        name = split[0].replace("/", "-")

    if is_loaded(name):
        logging.warning("Sound '%s' has already been loaded", name)
        return False

    filepath = "%s/%s" % (player.sound_filepath, file)
    if os.path.isfile(filepath):
        player.sounds[name] = sa.WaveObject.from_wave_file(filepath)
        logging.debug("%s has been loaded as '%s'", file, name)
        return True
    else:
        raise SoundPlayerException(
            "File '%s' could not be loaded" % file)


def is_loaded(name):
    """Return True if sound has been loaded"""
    return name in player.sounds


def queue(name, duration=0):
    """Queue a loaded sound to be played asap.

    If the file has not been loaded there will be an attempt to do so
    by invoking load(name).

    Args:
        name (str): Identifier of a loaded file as specified in load()
        duration (int, 0): Duration in seconds after which the next sound
                           can be played. Defaults to duration of file.

    Returns:
        True on succes
        False on fail
    """
    split = name.rsplit(".", 1)
    if len(split) > 1:
        logging.debug("Don't provide extention .%s when queing sound %s.",
                      split[1], split[0])
        name = split[0]

    if is_loaded(name):
        player.queue.put((name, player.sounds[name], duration))
        logging.debug("Queued sound '%s'", name)
        return True
    else:
        logging.info("%s has not been loaded, attempting to so:", name)
        load(name)
        queue(name)
    return False


def wait_done(function=None, kwargs=None):
    """Wait until the whole queue has been played.

    When a function is provided its executed continiously while waiting
    for the queue to finish playing.

    Args:
        function (function): A function to excecute continiously
        kwargs (dict, {}): Kwargs for function argument

    Returns:
        Doesn't return anything
    """
    if kwargs is None:
        kwargs = {}

    while player.queue_length > 0 or player.playing:
        if function is not None:
            function(**kwargs)
