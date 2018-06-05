"""Class simplifies GUI building using tkinter"""

import tkinter as tk
import time


class GUI:
    """Simplifies GUI building using tkinter
    """
    def __init__(self, fps=10, fullscreen=False, name=None):
        """Create a new GUI

        Args:
            fps (int, 10): Maximum frames per second

        Returns:
            Doesn't return anything.
        """
        self.name = name
        self.fullscreen = None
        self.loop_delay = round(fps / 1000, 2)

        # window setup
        self.window = tk.Tk()
        if self.name is not None:
            self.window.title(self.name)
        self.set_fullscreen(fullscreen)

    def key(self, sequence=None, func=None, add=None):
        """Bind one or more key sequeces to a function.

        Args:
            sequence:
                (str, None): A sequence of keys to be pressed.
                (tuple, None): Multiple string sequences of keys to be pressed.
            func (function, None): A function to be called on keypress.
            add (str, None): Allows multiple functions to be called.

        Returns:
            Doesn't return anything.
        """
        if isinstance(sequence, tuple):
            for seq in sequence:
                self.window.bind(seq, func, add,)
        else:
            self.window.bind(sequence, func, add)

    def toggle_fullscreen(self, _=None):
        """Toggle fullscreen on or off

        Args:
            _ (event, None): Object passed by key()

        Returns:
            Doesn't return anything.
        """
        self.set_fullscreen(not self.fullscreen)

    def set_fullscreen(self, val, size="1000x1000"):
        """Toggle fullscreen on or off

        Args:
            val (bool): Whether or not the window should go fullscreen
            size (str, 700x700): Size of windowed screen

        Returns:
            Doesn't return anything.
        """
        self.fullscreen = val
        self.window.attributes("-fullscreen", self.fullscreen)
        if self.fullscreen is False:
            self.window.geometry("%s+0+0" % size)

    def make_label(self, parent=None, text=None, config=None, pack=None):
        """Make a new label element onscreen.

        Args:
            parent (tkinter.elem, window): Enables element hierachy.
            text (str, ' '): The text shown on screen.
            config (dict, None): Configure tkinter element.
            pack (str, None): Configure tkinter element packing.

        Returns:
            (tkinter.StringVar, tkinter.Label)
        """
        if parent is None:
            parent = self.window
        if text is None:
            text = ' '

        content = tk.StringVar()
        content.set(text)
        elem = tk.Label(parent, textvariable=content)
        elem.config(config)
        self._pack(elem, pack)
        return content, elem

    def make_entry(self, parent=None, text=None, config=None, pack=None):
        """Make a new entry element onscreen.

        Args:
            parent (tkinter.elem, window): Enables element hierachy.
            text (str, ' '): The default text inside the entry.
            config (dict, None): Configure tkinter element.
            pack (str, None): Configure tkinter element packing.

        Returns:
            (tkinter.Entry, tkinter.Frame)
        """
        if parent is None:
            parent = self.window
        if text is None:
            text = ' '

        if 'border' in config.keys():
            padding = config['border']
            del config['border']
        else:
            padding = 0

        border = tk.Frame(parent, {
            'padx': padding,
            'pady': padding
        })
        elem = tk.Entry(border, config)
        self._pack(elem)
        self._pack(border, pack)
        return elem, border

    def update(self, delay=None):
        """Update everything on screen.

        Limits fps.

        Args:
            delay (float, None): Wait for some seconds while
                                 keeping the GUI active.

        Returns:
            Doesn't return anything.
        """
        def execute():
            """Actually execute update"""
            self.window.update_idletasks()
            self.window.update()
            time.sleep(self.loop_delay)

        if delay is None:
            execute()
        else:
            for _ in range(round(delay / self.loop_delay)):
                execute()

    @staticmethod
    def _pack(elem, pack=None):
        """ pack() a tkinter.elem """
        if pack is None:
            elem.pack()
        else:
            elem.pack(pack)
