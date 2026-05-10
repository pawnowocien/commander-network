INFOBOX_NAMES = ["infobox military conflict", "warbox", "battle", "infobox battle", "Mines_in_the_Battle_of_Messines_(1917)", ]

FLAG_ICON_TEMPLATE_NAMES = ["flagicon", "flagdeco", "flagicon image", "flag icon"]

BR_NAMES = ["<br />", "<br/>", "{{br}}", "<br>", "<Br>", "<BR />", "<br/ >", "<BR>", 
            "{{clear}}"]    # {{clear}} is only used German bombing of Monrovia, it's not really a <br> but it serves the same purpose


RANK_WIKILINKS_TO_REMOVE = [
    'colonel', 'lieutenant colonel', 'major general', 'general', 'captain', 'lieutenant',
    'field marshal', 'admiral', 'major', 'commander', 'brigadier', 'brigadier general',
    'rear admiral', 'vice admiral', 'commodore', 'air marshal', 'air commodore',
    'marshal', 'lieutenant-colonel', 'major-general', 'lieutenant general', 'lieutenant-general'
]




# Legacy, this is handled by normalizer now
# MULTI_ALLEGIANCE_COMMANDER_NAMES = [
#     "Crown Prince Rupprecht", "Rupprecht, Crown Prince of Bavaria",
#     "Crown Prince Rupprecht of Bavaria", "Crown Prince Rupprecht", "Rupprecht of Bavaria",
#     "Rupprecht, Crown Prince of Bavaria",   # {{flagicon|German Empire}} {{flagicon|Kingdom of Bavaria}}
#     "Richard Ackermann",                    # {{flagicon|Ottoman Empire|naval}} {{flagicon|German Empire|naval}}
#     "Rafael de Nogales Méndez",             # {{flagicon|Venezuela|1905}}/{{flagicon|Ottoman Empire}}
#     "Lt. Col. August Stange Bey",           # {{flagicon|Ottoman Empire}}{{flagicon|German Empire}},
#     "Wilhelm Souchon",                      # {{flagicon|Ottoman Empire|naval}}{{flagicon|German Empire|naval}}
#     "Hermann von Stein (1854–1927)",        # {{flagicon|German Empire}} {{flagicon|Kingdom of Prussia}}
#     "Albrecht, Duke of Württemberg"        # {{Flagicon|German Empire}}{{Flagicon|Kingdom of Württemberg}}
#     ]