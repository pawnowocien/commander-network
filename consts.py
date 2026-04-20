from utils import get_redirects


SKIP_INCLUDING = ["battleship", "Battleship", "Battlefield", "List_of", "order_of_battle", "(film)"]
EXTRACT_INCLUDING = ["battle", "Battle"]

USER_AGENT = "WikiBattlesDownloader/1.0"

WAIT_REQUEST_SEC = 1.0

INFOBOX_NAMES = ["infobox military conflict", "warbox", "battle", "infobox battle", "Mines_in_the_Battle_of_Messines_(1917)", ]

FLAG_ICON_TEMPLATE_NAMES = ["flagicon", "flagdeco"]
BR_NAMES = ["<br />", "<br/>", "{{br}}", "<br>", "<Br>", "<BR />", "<br/ >", "<BR>"]

MULTI_ALLEGIANCE_COMMANDER_NAMES = [
    "Crown Prince Rupprecht", "Rupprecht, Crown Prince of Bavaria",
    "Crown Prince Rupprecht of Bavaria", "Crown Prince Rupprecht", "Rupprecht of Bavaria",
    "Rupprecht, Crown Prince of Bavaria",   # {{flagicon|German Empire}} {{flagicon|Kingdom of Bavaria}}
    "Richard Ackermann",                    # {{flagicon|Ottoman Empire|naval}} {{flagicon|German Empire|naval}}
    "Rafael de Nogales Méndez",             # {{flagicon|Venezuela|1905}}/{{flagicon|Ottoman Empire}}
    "Lt. Col. August Stange Bey",           # {{flagicon|Ottoman Empire}}{{flagicon|German Empire}},
    "Wilhelm Souchon",                      # {{flagicon|Ottoman Empire|naval}}{{flagicon|German Empire|naval}}
    "Hermann von Stein (1854–1927)",        # {{flagicon|German Empire}} {{flagicon|Kingdom of Prussia}}
    "Albrecht, Duke of Württemberg"        # {{Flagicon|German Empire}}{{Flagicon|Kingdom of Württemberg}}
    ]

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
FILES_REDIRECTS = get_redirects()

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

FILES_TO_SKIP = FILES_NO_INFOBOXES + FILES_REDIRECTS + EXCEPTIONS
RANK_WIKILINKS_TO_REMOVE = [
    'colonel', 'lieutenant colonel', 'major general', 'general', 'captain', 'lieutenant',
    'field marshal', 'admiral', 'major', 'commander', 'brigadier', 'brigadier general',
    'rear admiral', 'vice admiral', 'commodore', 'air marshal', 'air commodore',
    'marshal', 'lieutenant-colonel', 'major-general', 'lieutenant general', 'lieutenant-general'
]
