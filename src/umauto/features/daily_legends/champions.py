"""The Daily Legends champions and their coordinate names.

The config stores exactly one champion (its display name). ``COORD_BY_NAME``
maps that name to the coordinate entry the runner taps to select it.
"""

# (display name, coordinate name) in the order shown on screen.
CHAMPIONS = [
    ("El Condor Pasa", "legend_el_condor_pasa"),
    ("Special Week", "legend_special_week"),
    ("Symboli Rudolf", "legend_symboli_rudolf"),
    ("King Halo", "legend_king_halo"),
    ("Taiki Shuttle", "legend_taiki_shuttle"),
    ("Sakura Bakushin O", "legend_sakura_bakushin_o"),
    ("Winning Ticket", "legend_winning_ticket"),
    ("Vodka", "legend_vodka"),
    ("Tokai Teio", "legend_tokai_teio"),
    ("Mayano Top Gun", "legend_mayano_top_gun"),
    ("Mejiro McQueen", "legend_mejiro_mcqueen"),
    ("TM Opera O", "legend_tm_opera_o"),
    ("Super Creek", "legend_super_creek"),
    ("Mejiro Ryan", "legend_mejiro_ryan"),
    ("Silence Suzuka", "legend_silence_suzuka"),
    ("Gold Ship", "legend_gold_ship"),
]

NAMES = [name for name, _ in CHAMPIONS]
COORD_BY_NAME = {name: coord for name, coord in CHAMPIONS}
DEFAULT = "Special Week"
