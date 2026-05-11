WIKI_PREFIX = "https://en.wikipedia.org/wiki/"

FILES_NO_INFOBOXES = [
    "Battle_of_Albert_(1918).txt",
    "Battle_of_Broken_Hill.txt",                    # not really a ww1 battle
    "Battle_of_El_Burj.txt",
    "Battle_of_Eski_Hissarlik.txt",
    "Battle_of_Jaroslawice.txt",
    "Battle_of_Krithia.txt",
    "Battle_of_Lagarde_(1914).txt",
    "Battle_of_Saint_Hilaire-le-Grand.txt",
    "Mines_in_the_Battle_of_Messines_(1917).txt",   # not a battle
    "SMS_Cap_Trafalgar.txt",                        # not a battle
    ]

EXCEPTIONS = [
    "Action_of_8_June_1915.txt",        # Unique battle format, not parseable with current code
    "Battle_of_Nagyszeben_(1916).txt",  # Unique battle format, not parseable with current code
    "Campaigns_of_the_Arab_Revolt.txt", # Wrong formatting?
    "Stalemate_in_Southern_Palestine.txt",
    "Monastir_offensive.txt",           # Wrong formatting?
    "Battle_of_Sardarabad.txt",         # Wrong formatting (flags as commander names)
    "Battle_of_the_Yser.txt",           # Wrong formatting (flags as commander names)
    "Raid_on_Jifjafa.txt",              # Wrong formatting (flags as commander names)
    "Battle_of_the_Scarpe_(1918).txt",  # Weird formatting (has <!-- don't know {{flagicon|German Empire}} ???--> in commander2)
    "Battle_of_Kolubara.txt",           # ubl with "*"
    ]

FILES_NOT_BATTLES = [
    "Naval_warfare_of_World_War_I.txt",
    "Balkan_Front_(World_War_I).txt",
    "Battles_of_the_Isonzo.txt",
    "Northern_front_of_the_Battle_of_Transylvania.txt",
    "Western_Front_tactics,_1917.txt",
    "Winter_operations_1914–1915.txt",

    # Campaigns
    "Adriatic_Campaign_of_World_War_I.txt",
    "Atlantic_U-boat_campaign_of_World_War_I.txt",
    "British_campaign_in_the_Baltic_(1918–1919).txt",
    "Campaigns_of_the_Arab_Revolt.txt",
    "Dobruja_Campaign.txt",
    "East_African_campaign_(World_War_I).txt",
    "Gallipoli_campaign.txt",
    "German_campaign_in_Angola.txt",
    "Kamerun_campaign.txt",
    "Mediterranean_U-boat_campaign_of_World_War_I.txt",
    "Mesopotamian_campaign.txt",
    "Montenegrin_campaign.txt",
    "Naval_operations_in_the_Dardanelles_campaign.txt",
    "Naval_operations_of_the_Kamerun_campaign.txt",
    "Persian_campaign_(World_War_I).txt",
    "Portuguese_campaign_in_Mozambique_(World_War_I).txt",
    "Romanian_campaign_(1916).txt",
    "Romanian_campaign_(1917).txt",
    "Second_Romanian_campaign_of_World_War_I.txt",
    "Sinai_and_Palestine_campaign.txt",
    "South_West_Africa_campaign.txt",
    "Togoland_campaign.txt",
    "Trebizond_Campaign.txt",
    "U-boat_campaign.txt",

    # Orders of battle
    "Battle_of_the_Somme_order_of_battle.txt",
    "Delville_Wood_order_of_battle.txt",
    "German_attack_on_Vimy_Ridge_order_of_battle.txt",
    "Spring_Offensive_order_of_battle.txt",

    # Occupations
    "Australian_occupation_of_German_New_Guinea.txt",
    "British_occupation_of_the_Jordan_Valley.txt",
    "Occupation_of_German_Samoa.txt",
    "Occupation_of_Istanbul.txt",

    # Offensives are ~ok~
]

STATIC_FILES_TO_SKIP = FILES_NO_INFOBOXES + EXCEPTIONS + FILES_NOT_BATTLES