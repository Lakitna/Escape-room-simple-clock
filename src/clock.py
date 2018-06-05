"""Countdown clock"""

import time
import logging
import threading
import sound


class Countdown(threading.Thread):
    """
    Provides countdown in new thread
    """

    def __init__(self, duration):
        """Create a new thread and start it."""
        threading.Thread.__init__(self)
        self.name = "Clock-T%s" % self.name.split("-")[-1]
        self.daemon = True

        self.duration = None
        self.remaining = None
        self.elapsed = None
        self.active = None
        self.done = None
        self._started_on = None

        self.set(duration)

        self._sound_name = "beep"
        sound.load(self._sound_name)
        self.beep_times = [
            *range(1, 10),  # every second last 10sec
            *range(10, 60, 5),  # between 10sec and 60sec every 5 seconds
            *range(60, 300, 10),  # between 1min and 5min every 10 seconds
            *range(300, self.duration, 60)  # every minute for the rest
        ]

        self.start()

    def __call__(self):
        """Return remaining time in seconds."""
        return self._format(self.remaining)

    def __repr__(self):
        return "<%s, active: %s, remaining: %s, elapsed: %s>" % (
            self.name,
            self.active,
            self._format(self.remaining),
            self._format(self.elapsed)
        )

    def run(self):
        """The body of the thread.

        Keeps the time and manages the countdown.
        """
        while True:
            if self.active:
                elapsed = round(time.time()) - self._started_on
                if elapsed != self.elapsed:
                    self.elapsed = elapsed
                    self.remaining = self.duration - self.elapsed

                    if self.remaining in self.beep_times:
                        sound.queue(self._sound_name)

                    if self.remaining <= 0:
                        self.active = False
                        self.done = True
                        logging.debug("Countdown done")
            # Let's not get carried away with system resources
            time.sleep(.1)

    def pause(self):
        """Pause the countdown"""
        logging.info("Countdown paused")
        self.active = False

    def set(self, duration):
        """Set the countdown

        Args:
            duration (int): Time in seconds the countdown should be set to.
        """
        logging.info("Countdown set to %s", self._format(duration))
        self.duration = duration
        self.remaining = duration
        self.elapsed = 0
        self.active = False
        self.done = False
        self._started_on = round(time.time())

    def resume(self):
        """Resume the countdown"""
        if not self.active and self.remaining > 0:
            logging.info("Countdown resumed")
            self._started_on = round(time.time()) - self.elapsed
            self.active = True

    @staticmethod
    def _format(sec):
        return time.strftime("%H:%M:%S", time.gmtime(sec))
