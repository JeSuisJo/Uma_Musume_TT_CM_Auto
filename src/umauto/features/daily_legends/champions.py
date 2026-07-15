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
    ("Curren Chan", "legend_curren_chan"),
    ("Maruzensky", "legend_maruzensky"),
    ("Fuji Kiseki", "legend_fuji_kiseki"),
    ("Mihono Bourbon", "legend_mihono_bourbon"),
    ("Matikane Fukukitaru", "legend_matikane_fukukitaru"),
    ("Seiun Sky", "legend_seiun_sky"),
    ("Biwa Hayahide", "legend_biwa_hayahide"),
    ("Air Groove", "legend_air_groove"),
    ("Eishin Flash", "legend_eishin_flash"),
    ("Agnes Digital", "legend_agnes_digital"),
    ("Nice Nature", "legend_nice_nature"),
    ("Grass Wonder", "legend_grass_wonder"),
    ("Oguri Cap", "legend_oguri_cap"),
]

NAMES = [name for name, _ in CHAMPIONS]
COORD_BY_NAME = {name: coord for name, coord in CHAMPIONS}
DEFAULT = "Special Week"
