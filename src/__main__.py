"""
Countdown system for escape room.
"""

import logging
import tkinter as tk
import random
import coloredlogs
from clock import Countdown
from gui import GUI
import settings as sett
import sound

coloredlogs.DEFAULT_LOG_FORMAT = '%(threadName)-10s | ' + \
                                 '%(levelname)-7s | ' + \
                                 '%(message)s'
coloredlogs.install(level=logging.INFO)


def gui_set(keyword, code_status=None):
    """Set a variety of gui elements to a state"""
    logging.debug("Set GUI to visual state '%s'", keyword)
    if keyword in sett.colors:
        gui_set_visual_state(sett.colors[keyword])
    if keyword in sett.text:
        status_text.set(sett.text[keyword])

    if code_status is not None and code_status in sett.color_status:
        logging.debug("Set code input to visual state '%s'", code_status)
        code_field_border.config(sett.color_status[code_status])


def gui_set_visual_state(kwargs):
    """Set visual state of multiple gui elements"""
    countdown_elem.config(**kwargs)
    status_elem.config(**kwargs)
    try:
        del kwargs['foreground']
    except KeyError:
        pass
    finally:
        gui.window.config(**kwargs)


def launch_rockets():
    """Play sound of multiple rockets launching"""
    for _ in range(sett.rocket_count):
        sound.queue("rocket", random.randrange(sett.rocket_stagger) / 1000)


def validate_code_caller(_):
    """Call validate_code and execute extras"""
    if cd.active:
        if validate_code(code_field.get()):
            sound.queue("finish", 4.9)
            sound.queue("yougotit")
            teardown()
        else:
            sound.queue("laugh", .3)


def validate_code(code, *, correct_code=None):
    """Validate the user inputed code"""
    if code == (correct_code or sett.correct_code):
        logging.info("Code %s is correct", code)
        cd.pause()
        gui_set('aborted', 'correct')
        return True
    else:
        logging.info("Code %s is wrong", code)
        sett.tries -= 1
        if sett.tries == 0:
            cd.pause()
            gui_set('launched')
        gui_set(None, 'wrong')
    return False


def teardown():
    """Perform end of program code"""
    logging.debug("teardown")
    code_field.config({"state": tk.DISABLED})
    gui.update(sett.code_linger_time)

    code_field_border.pack_forget()  # Delete code input.
    logging.warning("Program has now ended. Close GUI to terminate.")
    gui.window.mainloop()  # Stop the program, but keep the GUI active.


def start(_):
    """Start everything"""
    if not cd.active:
        sound.queue("start", 1)
        sound.queue("okiedokie", 2)
        sound.queue("letsgo", .7)
        sound.wait_done(gui.update)

        cd.resume()
        code_field.config({"state": tk.NORMAL})


if __name__ == '__main__':
    # pylint: disable=C0103
    sound.load_all()

    # Setting up Countdown and GUI classes
    cd = Countdown(sett.countdown_time)
    gui = GUI(fps=30, fullscreen=sett.start_fullscreen, name=sett.window_title)

    # Label for countdown
    countdown_text, countdown_elem = gui.make_label(text=cd(), config={
        **sett.labels,
        'height': 5,
        'font': sett.font_number
    })

    # Label above code input
    status_text, status_elem = gui.make_label(
        text=sett.text['default'],
        config=sett.labels
    )

    # Code input field
    code_field, code_field_border = gui.make_entry(config={
        'width': len(sett.correct_code) + 2,
        'justify': tk.CENTER,
        **sett.entry
    })
    code_field.insert(0, "-" * len(sett.correct_code))
    code_field.focus()
    code_field.config({"state": tk.DISABLED})

    # Set correct colors on everything
    gui_set(0, 'undefined')

    # Key bindings
    gui.key(sett.keys['start'], start)
    gui.key(sett.keys['validateCode'], validate_code_caller)
    gui.key(sett.keys['fullscreen'], gui.toggle_fullscreen)

    logging.info("Press * to start countdown.")
    # Program main loop
    while True:
        gui.update()
        countdown_text.set(cd())
        if sett.tries != sett.tries_total:  # if there has been a try
            if sett.tries > 0:  # if there are tries left
                if cd.active:
                    # TODO: use with gui_set
                    status_text.set("%s %d %s" % (
                        sett.text['warn'][0],
                        sett.tries,
                        sett.text['warn'][1]
                    ))
            else:
                gui_set('tampered')
                launch_rockets()
                teardown()
            sett.tries_total = sett.tries

        if cd.active:  # if countdown is active
            # Limit amount of chars in code_field
            if len(code_field.get()) > len(sett.correct_code):
                code_field.delete(-1)

            # Timebased color changes
            if cd.remaining in sett.color_time:
                gui_set(cd.remaining)
                del sett.color_time[cd.remaining]
        elif cd.done:  # if time has run out
            gui_set('launched')
            gui.update()
            sound.queue("laugh", .3)
            launch_rockets()
            teardown()
