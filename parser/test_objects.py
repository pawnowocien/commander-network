import mwparserfromhell as mwp

com_ubl = mwp.parse("""{{ubl|Bernd Wegener{{KIA}}|Klaus Hansen{{KIA}}}}""")
com_ubl_one_flag = mwp.parse(
    "{{flagicon|French Third Republic}} {{ubl|[[Joseph Joffre]]|[[Ferdinand Foch]]|[[Émile Fayolle]]}} "
    "{{Flagicon|UKGBI}} {{ubl|[[Douglas Haig]]|[[Henry Rawlinson, 1st Baron Rawlinson|Henry Rawlinson]]|[[Hubert Gough]]| [[Edmund Allenby]]}}")
com_ubl_many_flags = mwp.parse("{{ubl|{{flagicon|UKGBI}} [[Douglas Haig, 1st Earl Haig|Douglas Haig]]|{{flagicon|French Third Republic}} [[Ferdinand Foch]]|{{flagicon|French Third Republic}} [[Émile Fayolle]]|{{flagicon|UKGBI}} [[Henry Rawlinson, 1st Baron Rawlinson|Henry Rawlinson]]|{{flagicon|UKGBI}} [[Hubert Gough]]}}")

# Actions of St Eloi Craters
com_ubl_flag_no_flag = mwp.parse("{{ubl|{{flagicon|UKGBI}} [[Douglas Haig]]|[[Edwin Alderson]]}}")

# Battles of the Isonzo
com_ubli = mwp.parse("{{ubli| [[Luigi Cadorna]]|{{flagdeco|Kingdom of Italy}} [[Pietro Frugoni]]|{{flagdeco|Kingdom of Italy}} [[Settimio Piacentini]]|{{flagdeco|Kingdom of Italy}} [[Luigi Capello]]|{{flagdeco|Kingdom of Italy}} [[Prince Emanuele Filiberto, Duke of Aosta|Prince Emanuele Filiberto]]}}")

# Battle of Flers–Courcelette
com_multi_flag_person = mwp.parse("{{ubl|{{flagicon|German Empire}} {{flagicon|Kingdom of Bavaria}} [[Rupprecht, Crown Prince of Bavaria|Crown Prince Rupprecht]]|{{flagicon|German Empire}} [[Fritz von Below]]}}")

com_br = mwp.parse("{{flagicon|German Empire}} [[Friedrich Freiherr Kress von Kressenstein]]<br />"
                   "{{flagicon|Ottoman Empire}} [[Fevzi Çakmak|Fevzi Pasha]]<br />"
                   "{{flagicon|Ottoman Empire}} [[İsmet İnönü|İsmet Bey]]")

# Attack of the Dead Men
com_br2 = mwp.parse("{{flagicon|German Empire}} [[Paul von Hindenburg]]<br/>{{flagicon|German Empire}} [[Rudolf von Freudenberg]]")

# Battle of Ardahan
com_br3 = mwp.parse("{{flagicon image|Flag_of_Russia_(1914-1917).svg}} [[Nikolai Istomin]]<br>{{flagicon image|Flag_of_Russia_(1914-1917).svg}} [[Illarion Vorontsov-Dashkov]]<br>")

com_single = mwp.parse("{{flagicon|UKGBI}} [[Charles Levenax Haldane]]")

com_plainlist = mwp.parse("""{{plainlist|
* {{flagicon|French Third Republic}} [[Ferdinand Foch]]
* {{flagicon|UKGBI}} [[Douglas Haig, 1st Earl Haig|Douglas Haig]]
* {{flagicon|UKGBI}} [[Henry Rawlinson, 1st Baron Rawlinson|Henry Rawlinson]]
* {{flagicon|Canada|1907}} [[Sir Arthur William Currie]]
* {{flagicon|Australia}} [[Sir John Monash]]
* {{flagicon|French Third Republic}} [[Marie-Eugène Debeney]]
* {{flagicon|French Third Republic}} [[Georges Louis Humbert|Georges Humbert]]
}}""")

com_none = mwp.parse("")

com_upper_plainlist = mwp.parse("""{{Plainlist}}
* {{flagicon|French Third Republic}} [[Joseph Joffre]]
* {{flagicon|French Third Republic}} [[Ferdinand Foch]]
* {{flagicon|Belgium}} [[Albert I of Belgium|Albert I]]
* {{flagicon|UKGBI}} [[John French, 1st Earl of Ypres|John French]]
{{Endplainlist}}""")

# Battle of Vittorio Veneto
com_flagdeco = mwp.parse("{{flagdeco|Austria-Hungary}} [[Svetozar Boroević]]<br />"
                         "{{flagdeco|Austria-Hungary}} [[Archduke Joseph August of Austria|AD. Joseph August]]<br />"
                         "{{nowrap|{{flagdeco|Austria-Hungary}} [[Alexander von Krobatin]]}}")

# Brusilov offensive
com_flagdeco2 = mwp.parse("{{flagdeco|Austria-Hungary}} [[Franz Graf Conrad von Hötzendorf|Conrad von Hötzendorf]]<br />"
                          "{{flagdeco|Austria-Hungary}} [[Archduke Joseph Ferdinand of Austria|Joseph Ferdinand]]<br />"
                          "{{flagdeco|Austria-Hungary}} [[Eduard von Böhm-Ermolli|Eduard von Böhm]]<br />"
                          "{{nowrap|{{flagdeco|German Empire}} [[Alexander von Linsingen]]}}<br />"
                          "{{Flagicon|German Empire}} [[Paul von Hindenburg]]<br />"
                          "{{flagdeco|German Empire}} [[Felix von Bothmer]]<br />"
                          "{{flagdeco|Ottoman Empire}} [[Cevat Pasha]]")

# First Battle of Ypres
com_multiple_plainlist = mwp.parse("""{{Plainlist}}
* {{flagicon|German Empire}} [[Erich von Falkenhayn]]
* {{flagicon|German Empire}} [[Albrecht, Duke of Württemberg|Albrecht of Württemberg]]
* {{flagicon|German Empire}} [[Rupprecht of Bavaria]]
* {{flagicon|German Empire}} [[Max von Fabeck]]
* {{flagicon|German Empire}} [[Alexander von Linsingen]]
{{Endplainlist}}""")

# Ice Cruise of the Batlic Fleet
com_almost_empty = mwp.parse("|")

# Battle of the Ancre Heights
com_unbulleted_list = mwp.parse("{{unbulleted list | [[Erich Ludendorff]] | "
                                "[[Rupprecht, Crown Prince of Bavaria|Kronprinz Rupprecht]] | "
                                "[[Max von Gallwitz]] | [[Fritz von Below]]}}")

# Third Battle of Krithia
com_no_list_multi = mwp.parse("""{{flagicon|British Empire}} [[Aylmer Hunter-Weston]]
 
 {{flagicon|British Empire}} [[Joseph Trumpeldor]]""")

# First Battle of Gaza
# has (tr), /, a commander without link and a commander with a red link
com_weird_format = mwp.parse(
    "{{flagicon|Ottoman Empire}} [[Djemal Pasha|Ahmed Djemal]] Paşa<br />"
    "{{flagicon|German Empire}} [[Friedrich Freiherr Kress von Kressenstein]] {{small|(actual)}}<br />"
    "{{flagicon|Ottoman Empire}} Colonel [[Rüştü Sakarya|Mehmet Rüştü]]<br/ > "
    "{{flagicon|Ottoman Empire}} Lieutenant Colonel [[Edip Servet Tör|Edip Servet]] ([[:tr:Edip_Servet_Tör|tr]])<br />"
    "{{flagicon|German Empire}} Major Tiller<br />"
    "{{flagicon|Venezuela|1905}}/{{flagicon|Ottoman Empire}} [[Rafael de Nogales Méndez|Rafael de Nogales]]")

com_single_ill = mwp.parse("{{ill|Heinrich von Kummer (General, 1874)|lt=Heinrich von Kummer|de}}")

# Battle of Doss Alto
com_question_mark = mwp.parse("{{flagicon|Austria-Hungary}} ?")

# Persian campaign (World War I) TODO - this campaign is 3-way
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

all_com_test_cases = [
    com_ubl,
    com_ubl_one_flag,
    com_ubl_many_flags,
    com_br,
    com_br2,
    com_single,
    com_plainlist,
    com_none,
    com_upper_plainlist,
    com_flagdeco,
    com_flagdeco2,
    com_multiple_plainlist,
    com_almost_empty,
    com_unbulleted_list,
    com_no_list_multi,
    com_question_mark,
    com_tree_list,
    com_collapsible_list,
]