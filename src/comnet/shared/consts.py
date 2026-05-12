WIKI_PREFIX = "https://en.wikipedia.org/wiki/"

BATTLES_NO_INFOBOXES = [
    "Battle_of_Albert_(1918)",
    "Battle_of_Broken_Hill",                    # not really a ww1 battle
    "Battle_of_El_Burj",
    "Battle_of_Eski_Hissarlik",
    "Battle_of_Jaroslawice",
    "Battle_of_Krithia",
    "Battle_of_Lagarde_(1914)",
    "Battle_of_Saint_Hilaire-le-Grand",
    "Mines_in_the_Battle_of_Messines_(1917)",   # not a battle
    "SMS_Cap_Trafalgar",                        # not a battle
    ]

BATTLES_EXCEPTIONS = [
    "Action_of_8_June_1915",           # Unique battle format, not parseable with current code
    "Stalemate_in_Southern_Palestine", # Inconsisntent with <br>s
    "Battle_of_Kolubara",              # ubl with "*"
    "Battle_of_Monte_Corno",           # Very wrong flag format
    ]

BATTLES_NOT_BATTLES = [
    "Naval_warfare_of_World_War_I",
    "Balkan_Front_(World_War_I)",
    "Battles_of_the_Isonzo",
    "Northern_front_of_the_Battle_of_Transylvania",
    "Western_Front_tactics,_1917",
    "Winter_operations_1914–1915",

    # Campaigns
    "Adriatic_Campaign_of_World_War_I",
    "Atlantic_U-boat_campaign_of_World_War_I",
    "British_campaign_in_the_Baltic_(1918–1919)",
    "Campaigns_of_the_Arab_Revolt",
    "Dobruja_Campaign",
    "East_African_campaign_(World_War_I)",
    "Gallipoli_campaign",
    "German_campaign_in_Angola",
    "Kamerun_campaign",
    "Mediterranean_U-boat_campaign_of_World_War_I",
    "Mesopotamian_campaign",
    "Montenegrin_campaign",
    "Naval_operations_in_the_Dardanelles_campaign",
    "Naval_operations_of_the_Kamerun_campaign",
    "Persian_campaign_(World_War_I)",
    "Portuguese_campaign_in_Mozambique_(World_War_I)",
    "Romanian_campaign_(1916)",
    "Romanian_campaign_(1917)",
    "Second_Romanian_campaign_of_World_War_I",
    "Sinai_and_Palestine_campaign",
    "South_West_Africa_campaign",
    "Togoland_campaign",
    "Trebizond_Campaign",
    "U-boat_campaign",

    # Orders of battle
    "Battle_of_the_Somme_order_of_battle",
    "Delville_Wood_order_of_battle",
    "German_attack_on_Vimy_Ridge_order_of_battle",
    "Spring_Offensive_order_of_battle",

    # Occupations
    "Australian_occupation_of_German_New_Guinea",
    "British_occupation_of_the_Jordan_Valley",
    "Occupation_of_German_Samoa",
    "Occupation_of_Istanbul",

    # Offensives are ~ok~
]

STATIC_BATTLES_TO_SKIP = BATTLES_NO_INFOBOXES + BATTLES_NOT_BATTLES