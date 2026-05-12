from comnet.parser.models import ParseBattle, ParseCommander, ParseCountry, ParseSide


INFOBOX_NAMES = ["infobox military conflict", "warbox", "battle", "infobox battle", "Mines_in_the_Battle_of_Messines_(1917)", ]

FLAG_ICON_TEMPLATE_NAMES = ["flagicon", "flagdeco", "flagicon image", "flag icon", "flagd"]

BR_NAMES = ["<br />", "<br/>", "{{br}}", "<br>", "<Br>", "<BR />", "<br/ >", "<BR>", 
            "{{clear}}"]    # {{clear}} is only used German bombing of Monrovia, it's not really a <br> but it serves the same purpose


RANK_WIKILINKS_TO_REMOVE = [
    'colonel', 'lieutenant colonel', 'major general', 'general', 'captain', 'lieutenant',
    'field marshal', 'admiral', 'major', 'commander', 'brigadier', 'brigadier general',
    'rear admiral', 'vice admiral', 'commodore', 'air marshal', 'air commodore',
    'marshal', 'lieutenant-colonel', 'major-general', 'lieutenant general', 'lieutenant-general'
]

_AU = ParseCountry("Austria-Hungary")
_IT = ParseCountry("Italy")
_UK = ParseCountry("UKGBI")
_FR = ParseCountry("France")
_DE = ParseCountry("Germany")
_OT = ParseCountry("Ottoman Empire")
_AS = ParseCountry("Australia")
_SR = ParseCountry("Serbia")
HANDLED_EXCEPTION_BATTLES = {
    "Action_of_8_June_1915": ParseBattle(
        "Action_of_8_June_1915",
        "Action of 8 June 1915",
        [
            ParseSide(
                [_AU],
                [
                    ParseCommander("Gustav Klasing", [_AU]),
                    ParseCommander("Hans Fritsche von Crouenwald", [_AU])
                ]
            ),
            ParseSide(
                [_IT],
                [
                    ParseCommander("Castruccio Castracane degli Antelminelli", [_IT])
                ]
            )
        ]
    ),
    "Stalemate_in_Southern_Palestine": ParseBattle(
        "Stalemate_in_Southern_Palestine",
        "Stalemate in Southern Palestine",
        [
            ParseSide(
                [_UK, _FR, _IT],
                [
                    ParseCommander("Archibald Murray", [_UK]),
                    ParseCommander("Edmund Allenby, 1st Viscount Allenby", [_UK]),
                    ParseCommander("Edward Bulfin", [_UK]),
                    ParseCommander("Harry Chauvel", [_AS]),
                    ParseCommander("Philip Chetwode", [_UK]),
                ]
            ),
            ParseSide(
                [_OT, _DE],
                [
                    ParseCommander("Mustafa Kemal Pasha", [_OT]),
                    ParseCommander("Fevzi Pasha", [_OT]),
                    ParseCommander("Erich von Falkenhayn", [_DE]),
                    ParseCommander("Friedrich Freiherr Kress von Kressenstein", [_DE])
                ]
            )
        ]
    ),
    "Battle_of_Kolubara": ParseBattle(
        "Battle_of_Kolubara",
        "Battle of Kolubara",
        [
            ParseSide(
                [_SR],
                [
                    ParseCommander("Radomir Putnik", [_SR]),
                    ParseCommander("Živojin Mišić", [_SR]),
                    ParseCommander("Stepa Stepanović", [_SR]),
                    ParseCommander("Pavle Jurišić Šturm", [_SR]),
                    ParseCommander("Miloš Božanović", [_SR]),
                ]
            ),
            ParseSide(
                [_AU],
                [
                    ParseCommander("Oskar Potiorek", [_AU]),
                    ParseCommander("Liborius Ritter von Frank", [_AU]),
                ]
            )
        ]
    ),
    "Battle_of_Monte_Corno": ParseBattle(
        "Battle_of_Monte_Corno",
        "Battle of Monte Corno",
        [
            ParseSide(
                [_IT],
                [
                    ParseCommander("Luigi Cadorna", [_IT]),
                    ParseCommander("Armando Diaz", [_IT]),
                    ParseCommander("Pietro Badoglio", [_IT]),
                    ParseCommander("Luigi Casonato", [_IT]),
                    ParseCommander("Cesare Battisti (politician)", [_IT]),
                    ParseCommander("Fabio Filzi", [_IT]),
                    ParseCommander("Nazario Sauro", [_IT]),
                ]
            ),
            ParseSide(
                [_AU],
                [
                    ParseCommander("Bruno Franceschini", [_AU]),
                ]
            )
        ]
    )
}

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
