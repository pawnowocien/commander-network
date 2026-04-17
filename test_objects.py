import mwparserfromhell as mwp

com_ubl = mwp.parse("""{{ubl|Bernd Wegener{{KIA}}|Klaus Hansen{{KIA}}}}""")

com_br = mwp.parse("{{flagicon|German Empire}} [[Friedrich Freiherr Kress von Kressenstein]]<br />"
                   "{{flagicon|Ottoman Empire}} [[Fevzi Çakmak|Fevzi Pasha]]<br />"
                   "{{flagicon|Ottoman Empire}} [[İsmet İnönü|İsmet Bey]]")

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