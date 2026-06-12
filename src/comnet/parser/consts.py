from comnet.parser.models import ParseBattle, ParseCommander, ParseCountry, ParseSide
from comnet.config import pipeline_type

PARSED_BATTLES_PATH = f"data/{pipeline_type}/parsed/battles.json"



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



BANNED_NAMES_WW2 = [
    "(12:00pm 25–26 April)",
    "(131st Division)",
    "(1st Division)",
    "(22 April–12:00pm 25 April)",
    "(23rd Division)",
    "(2nd Corps)",
    "(4th Division)",
    "(731 Battalion)",
    "(8th Infantry Division)",
    "(Avvocata)",
    "(Bari Division)",
    "(Capodimonte)",
    "(Corso Giuseppe Garibaldi)",
    "(Field Army)",
    "(II Corps)",
    "(Kalamas Sector)",
    "(Materdei)",
    "(Negrades Sector)",
    "(Norwegian Military Governor)",
    "(Piazza Carlo III)",
    "(Piazza Mazzini)",
    "(Puglie Division)",
    "(Siena Division)",
    "(Thesprotia Sector)",
    "(VIII Corps)",
    "(Vasto)",
    "(Via Duomo)",
    "(commander Netherlands)",
    "(foreign air support)",
    "(formation leader)",
    "12th Army Group",
    "14–17 April:",
    "15th Army Group",
    "15–20 April:",
    "17–19 April:",
    "20 April – 5 May:",
    "21st Army Group",
    "54th Rifle Division (Soviet Union)",
    "56th Division: (December)",
    "5th Panzer Army",
    "6th Army (Italy)",
    "7th Army (Wehrmacht)",
    "Air Forces:",
    "Air forces:",
    "Allied Air Forces:",
    "Allied Force Headquarters",
    "Allied naval forces:",
    "XIV Panzer Corps",
    "Eighth Army (United Kingdom)",
    "Lieutenant Colonel (United Kingdom)",
    "XXV Army Corps (Italy)",
    "Army Air Force:",
    "Army Group B",
    "Army Group Centre",
    "Army Group South",
    "Army:",
    "Bryansk Front",
    "Central Front (Soviet Union)",
    "Steppe Front:",
    "Voronezh Front",
    "Western Front (Soviet Union)",
    "Captain (British Army and Royal Marines)",
    "Captain (Royal Navy)",
    "Captain (land and air)",
    "Commonwealth of the Philippines",
    "Convoy Commodore: WB MacKenzie RNR",
    "Corps: (February–March)",
    "Chetniks:",
    "Chiaia",
    "Comando Supremo",
    "Combined Fleet",
    "Commander, U.S. Pacific Fleet",
    "Commander-in-Chief:",
    "Division:",
    "Eighth Area Army",
    "Fifth Panzer Army",
    "First Army (United States)",
    "First Australian Army",
    "First Lieutenant Kurilov",
    "First Phase:",
    "First United States Army",
    "Garrison in Rogatica:",
    "Guerrillas:",
    "I/IR12 (1st battalion of Infantry Regiment 12):",
    "Japanese Seventeenth Army",
    "Land:",
    "Naples",
    "National Archaeological Museum, Naples",
    "Naval forces:",
    "Naval:",
    "Navy:",
    "Montecalvario",
    "OB West",
    "Oberbefehlshaber Süd",
    "Overall:",
    "Partisans:",
    "Posillipo",
    "Relief forces from Sarajevo:",
    "Second Army (United Kingdom)",
    "Seventh United States Army",
    "Sixth Panzer Army",
    "Sixth United States Army",
    "Southwest Pacific Area",
    "Special Attack Force:",
    "Supreme Command:",
    "Supreme Headquarters Allied Expeditionary Force",
    "Tenth United States Army",
    "Third United States Army",
    "Thirty-Second Army (Japan)",
    "U.S. Army:",
    "U.S. Marine Corps:",
    "U.S. Navy:",
    "United States Fifth Fleet",
    "United States Seventh Fleet",
    "United States Third Fleet",
    "Unteroffizier",
    "Vomero",
    "from 6 December:",
    "7th Air Division (Japan):",
    "Japanese Eighteenth Army:"
]