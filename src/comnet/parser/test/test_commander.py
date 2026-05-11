import mwparserfromhell as mwp

from comnet.parser.commander_parser import parse_commander
from comnet.parser.models import ParseBattle, ParseCommander, ParseCountry

def test_ubl():
    com_ubl = mwp.parse("""{{ubl|Bernd Wegener{{KIA}}|Klaus Hansen{{KIA}}}}""")
    assert parse_commander(com_ubl) == [ParseCommander("Bernd Wegener", []),
                                        ParseCommander("Klaus Hansen", [])]
    
    fra = ParseCountry("French Third Republic")
    gbr = ParseCountry("UKGBI")
    
    com_ubl_one_flag = mwp.parse("{{flagicon|French Third Republic}} {{ubl|[[Joseph Joffre]]|[[Ferdinand Foch]]|[[Émile Fayolle]]}} "
                                 "{{Flagicon|UKGBI}} {{ubl|[[Douglas Haig]]|[[Henry Rawlinson, 1st Baron Rawlinson|Henry Rawlinson]]|[[Hubert Gough]]| [[Edmund Allenby]]}}")
    assert parse_commander(com_ubl_one_flag) == [ParseCommander("Joseph Joffre", [fra]),
                                                 ParseCommander("Ferdinand Foch", [fra]),
                                                 ParseCommander("Émile Fayolle", [fra]),
                                                 ParseCommander("Douglas Haig", [gbr]),
                                                 ParseCommander("Henry Rawlinson, 1st Baron Rawlinson", [gbr]),
                                                 ParseCommander("Hubert Gough", [gbr]),
                                                 ParseCommander("Edmund Allenby", [gbr])]

    com_ubl_many_flags = mwp.parse("{{ubl|{{flagicon|UKGBI}} [[Douglas Haig, 1st Earl Haig|Douglas Haig]]|"
                                   "{{flagicon|French Third Republic}} [[Ferdinand Foch]]|{{flagicon|French Third Republic}} [[Émile Fayolle]]|"
                                   "{{flagicon|UKGBI}} [[Henry Rawlinson, 1st Baron Rawlinson|Henry Rawlinson]]|{{flagicon|UKGBI}} [[Hubert Gough]]}}")
    assert parse_commander(com_ubl_many_flags) == [ParseCommander("Douglas Haig, 1st Earl Haig", [ParseCountry("UKGBI")]),
                                                   ParseCommander("Ferdinand Foch", [ParseCountry("French Third Republic")]),
                                                   ParseCommander("Émile Fayolle", [ParseCountry("French Third Republic")]),
                                                   ParseCommander("Henry Rawlinson, 1st Baron Rawlinson", [ParseCountry("UKGBI")]),
                                                   ParseCommander("Hubert Gough", [ParseCountry("UKGBI")])]





def test_flags():
    # Actions of St Eloi Craters
    com_ubl_flag_no_flag = mwp.parse("{{ubl|{{flagicon|UKGBI}} [[Douglas Haig]]|[[Edwin Alderson]]}}")
    assert parse_commander(com_ubl_flag_no_flag) == [ParseCommander("Douglas Haig", [ParseCountry("UKGBI")]),
                                                     ParseCommander("Edwin Alderson", [])]

    # Battles of the Isonzo
    ita = ParseCountry("Kingdom of Italy")
    com_ubli = mwp.parse("{{ubli| [[Luigi Cadorna]]|{{flagdeco|Kingdom of Italy}} [[Pietro Frugoni]]|{{flagdeco|Kingdom of Italy}} [[Settimio Piacentini]]|{{flagdeco|Kingdom of Italy}} [[Luigi Capello]]|{{flagdeco|Kingdom of Italy}} [[Prince Emanuele Filiberto, Duke of Aosta|Prince Emanuele Filiberto]]}}")
    assert parse_commander(com_ubli) == [ParseCommander("Luigi Cadorna", []),
                                         ParseCommander("Pietro Frugoni", [ita]),
                                         ParseCommander("Settimio Piacentini", [ita]),
                                         ParseCommander("Luigi Capello", [ita]),
                                         ParseCommander("Prince Emanuele Filiberto, Duke of Aosta", [ita])]

    ger = ParseCountry("German Empire")
    bav = ParseCountry("Kingdom of Bavaria")
    # Battle of Flers–Courcelette
    com_multi_flag_person = mwp.parse("{{ubl|{{flagicon|German Empire}} {{flagicon|Kingdom of Bavaria}} [[Rupprecht, Crown Prince of Bavaria|Crown Prince Rupprecht]]|{{flagicon|German Empire}} [[Fritz von Below]]}}")
    assert parse_commander(com_multi_flag_person) == [ParseCommander("Rupprecht, Crown Prince of Bavaria", [ger, bav]),
                                                      ParseCommander("Fritz von Below", [ger])]

    aus = ParseCountry("Austria-Hungary")
    # Battle of Vittorio Veneto
    com_flagdeco = mwp.parse("{{flagdeco|Austria-Hungary}} [[Svetozar Boroević]]<br />"
                            "{{flagdeco|Austria-Hungary}} [[Archduke Joseph August of Austria|AD. Joseph August]]<br />"
                            "{{nowrap|{{flagdeco|Austria-Hungary}} [[Alexander von Krobatin]]}}")
    assert parse_commander(com_flagdeco) == [ParseCommander("Svetozar Boroević", [aus]),
                                            ParseCommander("Archduke Joseph August of Austria", [aus]),
                                            ParseCommander("Alexander von Krobatin", [aus])]

    ott = ParseCountry("Ottoman Empire")
    # Brusilov offensive
    com_flagdeco2 = mwp.parse("{{flagdeco|Austria-Hungary}} [[Franz Graf Conrad von Hötzendorf|Conrad von Hötzendorf]]<br />"
                            "{{flagdeco|Austria-Hungary}} [[Archduke Joseph Ferdinand of Austria|Joseph Ferdinand]]<br />"
                            "{{flagdeco|Austria-Hungary}} [[Eduard von Böhm-Ermolli|Eduard von Böhm]]<br />"
                            "{{nowrap|{{flagdeco|German Empire}} [[Alexander von Linsingen]]}}<br />"
                            "{{Flagicon|German Empire}} [[Paul von Hindenburg]]<br />"
                            "{{flagdeco|German Empire}} [[Felix von Bothmer]]<br />"
                            "{{flagdeco|Ottoman Empire}} [[Cevat Pasha]]")
    assert parse_commander(com_flagdeco2) == [ParseCommander("Franz Graf Conrad von Hötzendorf", [aus]),
                                             ParseCommander("Archduke Joseph Ferdinand of Austria", [aus]),
                                             ParseCommander("Eduard von Böhm-Ermolli", [aus]),
                                             ParseCommander("Alexander von Linsingen", [ger]),
                                             ParseCommander("Paul von Hindenburg", [ger]),
                                             ParseCommander("Felix von Bothmer", [ger]),
                                             ParseCommander("Cevat Pasha", [ott])]
    
    fin = ParseCountry("Flag of Finland 1918 (state).svg")
    # Battle of Antrea
    com_flagicon_image = mwp.parse("{{flagicon image|Flag of Finland 1918 (state).svg}} [[Herman Wärnhjelm]] <br>"
                                   "{{flagicon image|Flag of Finland 1918 (state).svg}} [[Aarne Sihvo]]")
    assert parse_commander(com_flagicon_image) == [ParseCommander("Herman Wärnhjelm", [fin]),
                                                  ParseCommander("Aarne Sihvo", [fin])]

    ara = ParseCountry("Arab Revolt")
    # Battle of Taif (1916)
    com_flag_icon = mwp.parse("{{Flag icon|Arab Revolt}} [[Abdullah I of Jordan|Abdullah bin Hussein]]<br/>{{Flag icon|Arab Revolt}} [[Faajir bin Sheliweh al-'Atawi]]")
    assert parse_commander(com_flag_icon) == [ParseCommander("Abdullah I of Jordan", [ara]),
                                             ParseCommander("Faajir bin Sheliweh al-'Atawi", [ara])]

    rom = ParseCountry("Kingdom of Romania")
    rus = ParseCountry("Flag_of_Russia_(1914-1917).svg")
    # Second Battle of Cobadin
    com_flagicon = mwp.parse("{{flagicon|Kingdom of Romania}} [[Alexandru Averescu]]<br/>" \
    "{{flagicon|Kingdom of Romania}} {{ill|Alexandru Socec|ro}}<br/>" \
    "{{flagicon|Kingdom of Romania}} {{ill|Alexandru Hartel|ro}}<br/>" \
    "{{flagicon|Kingdom of Romania}} {{ill|Constantin Scărișoreanu|ro}}<br />" \
    "{{flagicon|Kingdom of Romania}} {{ill|Traian Găiseanu|ro}}<br/>" \
    "{{flagicon|Kingdom of Romania}} [[Eremia Grigorescu]]<br/>" \
    "{{flagicon image|Flag_of_Russia_(1914-1917).svg}} [[Andrei Zayonchkovski]]")

    assert parse_commander(com_flagicon) == [ParseCommander("Alexandru Averescu", [rom]),
                                            ParseCommander("Alexandru Socec", [rom]),
                                            ParseCommander("Alexandru Hartel", [rom]),
                                            ParseCommander("Constantin Scărișoreanu", [rom]),
                                            ParseCommander("Traian Găiseanu", [rom]),
                                            ParseCommander("Eremia Grigorescu", [rom]),
                                            ParseCommander("Andrei Zayonchkovski", [rus])]

    
    # Battle of Choloki
    com_weird_flag_format = mwp.parse("""{{flagicon|Transcaucasian Democratic Federative Republic
}} [[Giorgi Mazniashvili]]""")
    assert parse_commander(com_weird_flag_format) == [ParseCommander("Giorgi Mazniashvili", [ParseCountry("Transcaucasian Democratic Federative Republic")])]





def test_br():
    ger = ParseCountry("German Empire")
    ott = ParseCountry("Ottoman Empire")
    com_br = mwp.parse("{{flagicon|German Empire}} [[Friedrich Freiherr Kress von Kressenstein]]<br />"
                    "{{flagicon|Ottoman Empire}} [[Fevzi Çakmak|Fevzi Pasha]]<br />"
                    "{{flagicon|Ottoman Empire}} [[İsmet İnönü|İsmet Bey]]")
    assert parse_commander(com_br) == [ParseCommander("Friedrich Freiherr Kress von Kressenstein", [ger]),
                                       ParseCommander("Fevzi Çakmak", [ott]),
                                       ParseCommander("İsmet İnönü", [ott])]

    # Attack of the Dead Men
    com_br2 = mwp.parse("{{flagicon|German Empire}} [[Paul von Hindenburg]]<br/>{{flagicon|German Empire}} [[Rudolf von Freudenberg]]")
    assert parse_commander(com_br2) == [ParseCommander("Paul von Hindenburg", [ger]),
                                       ParseCommander("Rudolf von Freudenberg", [ger])]

    rus = ParseCountry("Flag_of_Russia_(1914-1917).svg")
    # Battle of Ardahan
    com_br3 = mwp.parse("{{flagicon image|Flag_of_Russia_(1914-1917).svg}} [[Nikolai Istomin]]<br>{{flagicon image|Flag_of_Russia_(1914-1917).svg}} [[Illarion Vorontsov-Dashkov]]<br>")
    assert parse_commander(com_br3) == [ParseCommander("Nikolai Istomin", [rus]),
                                       ParseCommander("Illarion Vorontsov-Dashkov", [rus])]
    




def test_corner_cases():
    com_single = mwp.parse("{{flagicon|UKGBI}} [[Charles Levenax Haldane]]")
    assert parse_commander(com_single) == [ParseCommander("Charles Levenax Haldane", [ParseCountry("UKGBI")])]

    com_none = mwp.parse("")
    assert parse_commander(com_none) == []

    # Ice Cruise of the Batlic Fleet
    com_almost_empty = mwp.parse("|")
    assert parse_commander(com_almost_empty) == []

    bri = ParseCountry("British Empire")
    # Third Battle of Krithia
    com_no_list_multi = mwp.parse("""{{flagicon|British Empire}} [[Aylmer Hunter-Weston]]
 
 {{flagicon|British Empire}} [[Joseph Trumpeldor]]""")
    assert parse_commander(com_no_list_multi) == [ParseCommander("Aylmer Hunter-Weston", [bri]),
                                                 ParseCommander("Joseph Trumpeldor", [bri])]
    
    # Battle of Doss Alto
    com_question_mark = mwp.parse("{{flagicon|Austria-Hungary}} ?")
    assert parse_commander(com_question_mark) == []

    ger = ParseCountry("German Empire")
    ott = ParseCountry("Ottoman Empire")
    # First Battle of Gaza
    # has (tr), /, a commander without link and a commander with a red link
    com_weird_format = mwp.parse(
        "{{flagicon|Ottoman Empire}} [[Djemal Pasha|Ahmed Djemal]] Paşa<br />"
        "{{flagicon|German Empire}} [[Friedrich Freiherr Kress von Kressenstein]] {{small|(actual)}}<br />"
        "{{flagicon|Ottoman Empire}} Colonel [[Rüştü Sakarya|Mehmet Rüştü]]<br/ > "
        "{{flagicon|Ottoman Empire}} Lieutenant Colonel [[Edip Servet Tör|Edip Servet]] ([[:tr:Edip_Servet_Tör|tr]])<br />"
        "{{flagicon|German Empire}} Major Tiller<br />"
        "{{flagicon|Venezuela|1905}}/{{flagicon|Ottoman Empire}} [[Rafael de Nogales Méndez|Rafael de Nogales]]")
    assert parse_commander(com_weird_format) == [ParseCommander("Djemal Pasha", [ott]),
                                                 ParseCommander("Friedrich Freiherr Kress von Kressenstein", [ger]),
                                                 ParseCommander("Rüştü Sakarya", [ott]),
                                                 ParseCommander("Lieutenant Colonel Edip Servet (tr)", [ott]), # TODO doesnt sound good
                                                 ParseCommander("Major Tiller", [ger]),
                                                 ParseCommander("Rafael de Nogales Méndez", [ParseCountry("Venezuela"), ott])]
    
    
    fra = ParseCountry("French Third Republic")
    # Siege of Mora
    com_ref = mwp.parse("{{flagicon|British Empire}} [[Frederick Hugh Cunliffe]]<br>{{flagicon|British Empire}} R. W. Fox<br>"
                        "{{flagicon|French Third Republic}} Brisett<br>{{flagicon|French Third Republic}} Ferrandi<ref name=\"TSB\">Fecitte.</ref>")
    assert parse_commander(com_ref) == [ParseCommander("Frederick Hugh Cunliffe", [bri]),
                                        ParseCommander("R. W. Fox", [bri]),
                                        ParseCommander("Brisett", [fra]),
                                        ParseCommander("Ferrandi", [fra])]

    ukg = ParseCountry("United Kingdom")
    # Petsamo expeditions
    com_wia = mwp.parse("{{flagicon|United Kingdom}} Captain Vincent Brown ([[Wounded in action|WIA]])<br>{{flagicon|United Kingdom|naval}} Captain James Farie")
    assert parse_commander(com_wia) == [ParseCommander("Captain Vincent Brown", [ukg]),
                                        ParseCommander("Captain James Farie", [ukg])]




def test_plainlist():
    fra = ParseCountry("French Third Republic")
    gbr = ParseCountry("UKGBI")
    com_plainlist = mwp.parse("""{{plainlist|
* {{flagicon|French Third Republic}} [[Ferdinand Foch]]
* {{flagicon|UKGBI}} [[Douglas Haig, 1st Earl Haig|Douglas Haig]]
* {{flagicon|UKGBI}} [[Henry Rawlinson, 1st Baron Rawlinson|Henry Rawlinson]]
* {{flagicon|Canada|1907}} [[Sir Arthur William Currie]]
* {{flagicon|Australia}} [[Sir John Monash]]
* {{flagicon|French Third Republic}} [[Marie-Eugène Debeney]]
* {{flagicon|French Third Republic}} [[Georges Louis Humbert|Georges Humbert]]
}}""")
    assert parse_commander(com_plainlist) == [ParseCommander("Ferdinand Foch", [fra]),
                                              ParseCommander("Douglas Haig, 1st Earl Haig", [gbr]),
                                              ParseCommander("Henry Rawlinson, 1st Baron Rawlinson", [gbr]),
                                              ParseCommander("Sir Arthur William Currie", [ParseCountry("Canada")]),
                                              ParseCommander("Sir John Monash", [ParseCountry("Australia")]),
                                              ParseCommander("Marie-Eugène Debeney", [fra]),
                                              ParseCommander("Georges Louis Humbert", [fra])]


    com_upper_plainlist = mwp.parse("""{{Plainlist}}
* {{flagicon|French Third Republic}} [[Joseph Joffre]]
* {{flagicon|French Third Republic}} [[Ferdinand Foch]]
* {{flagicon|Belgium}} [[Albert I of Belgium|Albert I]]
* {{flagicon|UKGBI}} [[John French, 1st Earl of Ypres|John French]]
{{Endplainlist}}""")
    assert parse_commander(com_upper_plainlist) == [ParseCommander("Joseph Joffre", [fra]),
                                                    ParseCommander("Ferdinand Foch", [fra]),
                                                    ParseCommander("Albert I of Belgium", [ParseCountry("Belgium")]),
                                                    ParseCommander("John French, 1st Earl of Ypres", [gbr])]

    ger = ParseCountry("German Empire")
    # First Battle of Ypres
    com_multiple_plainlist = mwp.parse("""{{Plainlist}}
* {{flagicon|German Empire}} [[Erich von Falkenhayn]]
* {{flagicon|German Empire}} [[Albrecht, Duke of Württemberg|Albrecht of Württemberg]]
* {{flagicon|German Empire}} [[Rupprecht of Bavaria]]
* {{flagicon|German Empire}} [[Max von Fabeck]]
* {{flagicon|German Empire}} [[Alexander von Linsingen]]
{{Endplainlist}}""")
    assert parse_commander(com_multiple_plainlist) == [ParseCommander("Erich von Falkenhayn", [ger]),
                                                       ParseCommander("Albrecht, Duke of Württemberg", [ger]),
                                                       ParseCommander("Rupprecht of Bavaria", [ger]),
                                                       ParseCommander("Max von Fabeck", [ger]),
                                                       ParseCommander("Alexander von Linsingen", [ger])]

    bel = ParseCountry("Belgium")
    # Battle of Halen
    com_plainlist_other = mwp.parse("""{{Plain list|
* {{flagicon|Belgium}} [[Léon de Witte de Haelen|Léon De Witte]]
* {{flagicon|Belgium}} [[Adolf Proost]]
}}""")
    assert parse_commander(com_plainlist_other) == [ParseCommander("Léon de Witte de Haelen", [bel]),
                                                     ParseCommander("Adolf Proost", [bel])]




def test_other_lists():
    # Battle of the Ancre Heights
    com_unbulleted_list = mwp.parse("{{unbulleted list | [[Erich Ludendorff]] | "
                                    "[[Rupprecht, Crown Prince of Bavaria|Kronprinz Rupprecht]] | "
                                    "[[Max von Gallwitz]] | [[Fritz von Below]]}}")
    assert parse_commander(com_unbulleted_list) == [ParseCommander("Erich Ludendorff", []),
                                                    ParseCommander("Rupprecht, Crown Prince of Bavaria", []),
                                                    ParseCommander("Max von Gallwitz", []),
                                                    ParseCommander("Fritz von Below", [])]

    com_single_ill = mwp.parse("{{ill|Heinrich von Kummer (General, 1874)|lt=Heinrich von Kummer|de}}")
    assert parse_commander(com_single_ill) == [ParseCommander("Heinrich von Kummer (General, 1874)", [])]

    ott = ParseCountry("Ottoman Empire")
    ger = ParseCountry("German Empire")
    # Persian campaign (World War I) (although it is not really a battle)
    com_tree_list = mwp.parse("""{{tree list}}
* {{flagicon|Ottoman Empire}} '''[[Mehmed V]]'''
* {{flagicon|Ottoman Empire}} '''[[Enver Pasha]]'''
* {{flagicon|Ottoman Empire}} [[Halil Kut]]
* {{flagicon|Ottoman Empire}} [[Ali İhsan Pasha|Ali Ihsan Pasha]]
* {{flagicon|Ottoman Empire}} [[Kâzım Karabekir|Kâzım (Karabekir) Bey]]
* {{flagicon|Ottoman Empire}} [[Nazif Kayacık|Nazif (Kayacık) Bey]]
* {{flagicon|German Empire}} '''[[Kaiser Wilhelm II]]'''
* {{flagicon|German Empire}} [[Georg von Kaunitz]]
* {{flagicon|German Empire}} [[Wilhelm Wassmuss]]
* {{flagicon|German Empire}} {{ill|Arthur Bopp|de|Arthur Bopp}}
* {{flagicon|German Empire}} Captain Angman
* [[Simko Shikak]]<ref name="Bruinessen 2006 18–21">{{cite book|last=Bruinessen|first=Martin|author-link=Martin van Bruinessen|editor1-last=Atabaki|editor1-first=Touraj|editor1-link=Touraj Atabaki|chapter=Chapter 5: A Kurdish warlord on the Turkish-Persian frontier in the early Twentieth century: Isma'il Aqa Simko|title=Iran and the First World War: Battleground of the Great Powers|series=Library of modern Middle East studies, 43|publisher=[[I.B. Tauris]]|location=London; New York|pages=18–21|chapter-url=https://www.academia.edu/3555229|year=2006|isbn=9781860649646|oclc=56455579}}</ref>
{{tree list/end}}""")
    assert parse_commander(com_tree_list) == [ParseCommander("Mehmed V", [ott]),
                                             ParseCommander("Enver Pasha", [ott]),
                                             ParseCommander("Halil Kut", [ott]),
                                             ParseCommander("Ali İhsan Pasha", [ott]),
                                             ParseCommander("Kâzım Karabekir", [ott]),
                                             ParseCommander("Nazif Kayacık", [ott]),
                                             ParseCommander("Kaiser Wilhelm II", [ger]),
                                             ParseCommander("Georg von Kaunitz", [ger]),
                                             ParseCommander("Wilhelm Wassmuss", [ger]),
                                             ParseCommander("Arthur Bopp", [ger]),
                                             ParseCommander("Captain Angman", [ger]),
                                             ParseCommander("Simko Shikak", [])]

    aus = ParseCountry("Austria-Hungary")
    # Air Battle on Istrana
    com_collapsible_list = mwp.parse(""" {{Collapsible list
|bullets = yes
|title = '''Known List:'''
|{{flagdeco|German Empire}} [[Georg Est]]{{KIA}}
|{{flagdeco|German Empire}} [[Franz Hertling]]{{KIA}}
|{{flagicon|Austria-Hungary}} [[Lieutenant|Lt.]] Kessler{{POW}}
|{{flagdeco|German Empire}} [[Lieutenant|Lt.]] Edehbole{{KIA}}
|{{flagdeco|German Empire}} [[Karl Uecker]]{{KIA}}
|{{flagdeco|German Empire}} [[Heinrich Pfeiffer (aviator)|Heinrich Pfeiffer]]{{KIA}}
|{{flagicon|Austria-Hungary}} Pallasch{{POW}}
|{{flagicon|Austria-Hungary}} [[Pohlmann (aviator)|Pohlmann]]{{POW}}
|{{flagicon|Austria-Hungary}} [[Schlamm]]{{POW}}
}}""")
    assert parse_commander(com_collapsible_list) == [ParseCommander("Georg Est", [ger]),
                                                     ParseCommander("Franz Hertling", [ger]),
                                                     ParseCommander("Kessler", [aus]),
                                                     ParseCommander("Edehbole", [ger]),
                                                     ParseCommander("Karl Uecker", [ger]),
                                                     ParseCommander("Heinrich Pfeiffer (aviator)", [ger]),
                                                     ParseCommander("Pallasch", [aus]),
                                                     ParseCommander("Pohlmann (aviator)", [aus]),
                                                     ParseCommander("Schlamm", [aus])]
