"""Settings"""
# pylint: disable=C0103

window_title = 'Missile countdown'
start_fullscreen = False

countdown_time = 5 * 60 + 5  # Time on the clock in seconds
code_linger_time = 5  # Time code stays on screen after end in seconds
correct_code = "80085"  # The correct code
tries = 3  # Amount of code input attempts allowed
color_change_on = 5 * 60  # Time in seconds to start changing the screen color

rocket_count = 15  # Total amount of rockets being launched
rocket_stagger = 500  # Maximum time between rockets

font_number = ('Fira Mono', 50)  # Font family and size for numbers
font_text = ('Fira Sans', 16)  # Font family and size for text


keys = {
    'fullscreen': '<Escape>',
    'start': '*',  # Numpad star or <shift + 8>
    'validateCode': ('<KP_Enter>', '<Return>')  # Numpad- and regular enter
}

# Text shown on screen in different situations.
# Please note that regular enters do not work. Use \n to add a line break.
text = {
    "aborted": "Launch aborted.\nThank you for using Classy Reconnaissance " +
               "Air Projectiles for your launching needs. We at CRAP are " +
               "very proud to be the worlds leading launching software.",
    "launched": "Missiles successfully launched.\nThank you for using Classy" +
                "Reconnaissance Air Projectiles for your launching needs. " +
                "We at CRAP are very proud to be the worlds leading " +
                "launching software.",
    "tampered": "Tampering attemt discovered, missiles have been launched " +
                "prematurely.\nThank you for using Classy Reconnaissance Air" +
                " Projectiles for your launching needs. We at CRAP are very " +
                "proud to be the worlds leading launching software.",
    "default": "Enter code to abort",
    "warn": ("Interface will lock after", "more attempts")
}

base_colors = {
    "background": '#333333',
    "foreground": '#ffffff'
}


# Status colors in hex (#rrggbb)
color_status = {
    "wrong": {"background": "#aa0000"},
    "undefined": {"background": "#0000aa"},
    "correct": {"background": "#00aa00"},
    "launched": {"background": "#aaaaaa"},
    "aborted": {"background": "#aaaaaa"},
}

labels = {
    'font': font_text,
    'wraplength': 500,
    **base_colors
}

entry = {
    'font': font_number,
    'bd': 0,
    'highlightthickness': 0,
    'border': 20
}

# Timebased color gradient in hex (#rrggbb)
gradient = ['#DD3333', '#D83333', '#D43333', '#CF3333', '#CB3333',
            '#C73333', '#C23333', '#BE3333', '#BA3333', '#B53333',
            '#B13333', '#AD3333', '#A83333', '#A43333', '#9F3333',
            '#9B3333', '#973333', '#923333', '#8E3333', '#8A3333',
            '#853333', '#813333', '#7D3333', '#783333', '#743333',
            '#703333', '#6B3333', '#673333', '#623333', '#5E3333',
            '#5A3333', '#553333', '#513333', '#4D3333', '#483333',
            '#443333', '#403333', '#3B3333', '#373333', '#333333']
color_time = {
    0: base_colors
}
# Build the color_time dict based on gradient
step = color_change_on / len(gradient)
for i in range(len(gradient)):
    key = round((i + 1) * step)
    color_time[key] = {'background': gradient[i]}


tries_total = tries
colors = {**color_status, **color_time}
