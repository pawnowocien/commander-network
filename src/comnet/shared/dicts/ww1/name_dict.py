# For normalizing letters in names
LETTER_DICT = {
    "ß": "ss"
}

# For common (first) names that are often spelt differently, but refer to the same person.
# Sorry if the names are not in the correct language!
SIMPLE_NAME_DICT = {
    "Aleksei": "Aleksei",
    "Alexei": "Aleksei",
    "Alexey": "Aleksei",
}

# For names with extra info in parentheses, or other weird cases
CLEAN_NAME_DICT = {
    "(possibly Kpt. Karsten von Heydebreck)": "Karsten von Heydebreck",
    "(Vali of Baghdad) Javi Pasha": "Javi Pasha",
}

# For duplicates
COMPLEX_NAME_DICT = {
    "Albrecht of Württemberg": "Albrecht of Württemberg",
    "Albrecht, Duke of Württemberg": "Albrecht of Württemberg",

    "Archduke Joseph Ferdinand": "Archduke Joseph Ferdinand",
    "Archduke Joseph Ferdinand of Austria": "Archduke Joseph Ferdinand",

    "Arthur Currie": "Arthur Currie",
    "Sir Arthur William Currie": "Arthur Currie",

    "Arthur Hoskins": "Arthur Hoskins",
    "Reginald Hoskins": "Arthur Hoskins",

    "Asim": "Asim Pasha",
    "Asim Pasha": "Asim Pasha",
    
    "Auguste Dubail": "Auguste Dubail",
    "Augustin Dubail": "Auguste Dubail",

    "Augustin Édouard Michel du Faing d'Aigremont": "Augustin Édouard Michel du Faing d'Aigremont",
    "Édouard Michel du Faing d'Aigremont": "Augustin Édouard Michel du Faing d'Aigremont",

    "Brigadier General Frederick Hugh Cunliffe": "Frederick Hugh Cunliffe",
    "Frederick Hugh Cunliffe": "Frederick Hugh Cunliffe",

    "Brigadier J. M. Stewart": "Brigadier J. M. Stewart",
    "Gen. Stewart": "Brigadier J. M. Stewart",

    "C. V. F. Townshend": "C. V. F. Townshend",
    "Charles Townshend (British Army officer)": "C. V. F. Townshend",
    "Charles Vere Ferrers Townshend": "C. V. F. Townshend",

    "Charles Dobell": "Charles Dobell",
    "Charles Macpherson Dobell": "Charles Dobell",

    "Adolf Schipper": "Adolf Schipper",
    "Cap. Schipper": "Adolf Schipper",

    "Captain von Crailsheim": "Captain von Crailsheim",
    "von Crailsheim": "Captain von Crailsheim",

    "Colonel Subhi Bey": "Mehmed Subhi Bey",
    "Mehmed Subhi Bey": "Mehmed Subhi Bey",

    "Crown Prince Rupprecht": "Crown Prince Rupprecht of Bavaria",
    "Crown Prince Rupprecht of Bavaria": "Crown Prince Rupprecht of Bavaria",
    "Kronprinz Rupprecht von Bayern": "Crown Prince Rupprecht of Bavaria",
    "Prince Rupprecht": "Crown Prince Rupprecht of Bavaria",
    "Rupprecht of Bavaria": "Crown Prince Rupprecht of Bavaria",
    "Rupprecht, Crown Prince of Bavaria": "Crown Prince Rupprecht of Bavaria",

    "Crown Prince Wilhelm": "Crown Prince Wilhelm of Germany",
    "Crown Prince Wilhelm of Germany": "Crown Prince Wilhelm of Germany",
    "Wilhelm, German Crown Prince": "Crown Prince Wilhelm of Germany",
    "William, German Crown Prince": "Crown Prince Wilhelm of Germany",

    "David Beatty, 1st Earl Beatty": "David Beatty",
    "Sir David Beatty": "David Beatty",

    "Ahmed Djemal": "Ahmed Djemal",
    "Djemal Pasha": "Ahmed Djemal",

    "Douglas Haig": "Douglas Haig",
    "Douglas Haig, 1st Earl Haig": "Douglas Haig",

    "Edmund Allenby": "Edmund Allenby",
    "Edmund Allenby(Egyptian Expeditionary Force)": "Edmund Allenby",
    "Edmund Allenby, 1st Viscount Allenby": "Edmund Allenby",

    "Edward Bulfin": "Edward Bulfin",
    "Edward Bulfin(XX Corps)": "Edward Bulfin",

    "Ehrhard Schmidt": "Ehrhard Schmidt",
    "Ehrhard Schmidt (admiral)": "Ehrhard Schmidt",

    "Emanuele Filiberto, 2nd Duke of Aosta": "Emanuele Filiberto, 2nd Duke of Aosta",
    "Prince Emanuele Filiberto, Duke of Aosta": "Emanuele Filiberto, 2nd Duke of Aosta",
    "Prince Emanuele Filiberto, Duke of Aosta (1869–1931)": "Emanuele Filiberto, 2nd Duke of Aosta",

    "Emir Faisal": "Emir Faisal",
    "Faisal I of Iraq": "Emir Faisal",
    "Faisal bin Hussein(Sharifian Army)": "Emir Faisal",
    "Feisal I of Iraq": "Emir Faisal",   

    "Émile Guépratte": "Émile Guépratte",
    "Émile Paul Amable Guépratte": "Émile Guépratte",

    "Enver Pasha": "İsmail Enver Pasha",
    "İsmail Enver": "İsmail Enver Pasha",

    "Erich Falkenhayn": "Erich von Falkenhayn",
    "Erich von Falkenhayn": "Erich von Falkenhayn",

    "Erich Müller": "Erich Müller",
    "Hptm. Erich Müller": "Erich Müller",

    "Felix Graf von Bothmer": "Felix Graf von Bothmer",
    "Felix von Bothmer": "Felix Graf von Bothmer",

    "Fevzi Pasha": "Fevzi Çakmak",
    "Fevzi Çakmak": "Fevzi Çakmak",

    "Franchet d'Espèrey": "Franchet d'Espèrey",
    "Louis Franchet d'Espèrey": "Franchet d'Espèrey",

    "Conrad von Hötzendorf": "Conrad von Hötzendorf",
    "Count Franz Conrad von Hötzendorf": "Conrad von Hötzendorf",
    "Franz Conrad von Hötzendorf": "Conrad von Hötzendorf",
    "Franz Graf Conrad von Hötzendorf": "Conrad von Hötzendorf",

    "Franz Hipper": "Franz von Hipper",
    "Franz von Hipper": "Franz von Hipper",

    "Frederick Bryant": "Frederick Bryant",
    "Frederick Bryant (officer)": "Frederick Bryant",

    "Frederick Stanley Maude": "Frederick Stanley Maude",
    "Stanley Maude": "Frederick Stanley Maude",

    "Friedrich Freiherr Kress von Kressenstein": "Friedrich Kress von Kressenstein",
    "Friedrich Kressenstein": "Friedrich Kress von Kressenstein",

    "Friedrich Sixt von Armin": "Friedrich Sixt von Armin",
    "Sixt von Armin": "Friedrich Sixt von Armin",

    "George Milne": "George Milne",
    "George Milne, 1st Baron Milne": "George Milne",

    "Grand Duke Nicholas": "Grand Duke Nicholas",
    "Grand Duke Nicholas Nikolaevich of Russia (1856–1929)": "Grand Duke Nicholas",
    
    "Tsar Nicholas II": "Tsar Nicholas II",
    "Nicholas II": "Tsar Nicholas II",

    "Grigore C. Crăiniceanu": "Grigore C. Crăiniceanu",
    "Grigore Crăiniceanu": "Grigore C. Crăiniceanu",

    "Gustav von Oppen": "Gustav von Oppen",
    "Oberst Gustav von Oppen": "Gustav von Oppen",

    "Hans Hartwig von Beseler": "Hans Hartwig von Beseler",
    "Hans von Beseler": "Hans Hartwig von Beseler",

    "Harry Chauvel": "Harry Chauvel",
    "Harry Chauvel(Desert Mounted Corps)": "Harry Chauvel",
    "Henry George Chauvel": "Harry Chauvel",

    "Henri Berthelot": "Henri Berthelot",
    "Henri Mathias Berthelot": "Henri Berthelot",

    "Henri Gouraud": "Henri Gouraud",
    "Henri Gouraud (French Army officer)": "Henri Gouraud",
    "Henri Gouraud (general)": "Henri Gouraud",

    "Henry Hodgson (British Army officer)": "Henry Hodgson",
    "Henry Hodgson (general)": "Henry Hodgson",
    "Henry West Hodgson": "Henry Hodgson",
    
    "Henry John Macandrew": "Henry John Macandrew",
    "Henry John Milnes MacAndrew": "Henry John Macandrew",

    "General C.O'Grady": "Henry de Courcy O'Grady",
    "Henry de Courcy O'Grady": "Henry de Courcy O'Grady",

    "Herbert Plumer": "Herbert Plumer",
    "Herbert Plumer, 1st Viscount Plumer": "Herbert Plumer",
    
    "Hermann Kövess von Kövesshaza": "Hermann Kövess von Kövesshaza",
    "Hermann Kövess von Kövessháza": "Hermann Kövess von Kövesshaza",

    "Horace Smith-Dorrien": "Horace Smith-Dorrien",
    "Sir Horace Smith-Dorrien": "Horace Smith-Dorrien",

    "Hubert Gough": "Hubert Gough",
    "Hubert de la Poer Gough": "Hubert Gough",

    "Hussein bin Ali, King of Hejaz": "Hussein bin Ali",
    "Hussein bin Ali, Sharif of Mecca": "Hussein bin Ali",
    "Nasir ibn Ali ibn Hussein": "Hussein bin Ali",

    "Ian Hamilton": "Ian Hamilton",
    "Ian Hamilton (British Army officer)": "Ian Hamilton",

    "Illarion Ivanovich Vorontsov-Dashkov": "Illarion Ivanovich Vorontsov-Dashkov",
    "Illarion Vorontsov-Dashkov": "Illarion Ivanovich Vorontsov-Dashkov",

    "Col. J. van Deventer": "Jacob van Deventer",
    "Jacob van Deventer (general)": "Jacob van Deventer",

    "James G. Harbord": "James G. Harbord",
    "James Harbord": "James G. Harbord",
    
    "Jan Christiaan Smuts": "Jan Smuts",
    "Jan Smuts": "Jan Smuts",

    "John Eccles Nixon": "John Nixon",
    "John Nixon (Indian Army officer)": "John Nixon",

    "John Jellicoe": "John Jellicoe",
    "John Jellicoe, 1st Earl Jellicoe": "John Jellicoe",
    "Sir John Jellicoe": "John Jellicoe",

    "John Maxwell (general)": "John Maxwell",
    "John Maxwell (British Army officer)": "John Maxwell",

    "John Monash": "John Monash",
    "Sir John Monash": "John Monash",

    "John Shea": "John Shea",
    "John Shea (Indian Army officer)": "John Shea",

    "Alves Roçadas": "Alves Roçadas",
    "José Augusto Alves Roçadas": "Alves Roçadas",

    "Julian Byng": "Julian Byng",
    "Julian Byng, 1st Viscount Byng of Vimy": "Julian Byng",
    "Julian H.G. Byng, Viscount Byng of Vimy": "Julian Byng",

    "Józef Haller": "Józef Haller",
    "Józef Haller de Hallenburg": "Józef Haller",

    "Józef Piłsudski": "Józef Piłsudski",
    "Jozef Pilsudski": "Józef Piłsudski",

    "Kaiser Wilhelm II": "Kaiser Wilhelm II",
    "Wilhelm II": "Kaiser Wilhelm II",

    "Karl Müller": "Karl von Müller",
    "Karl von Müller": "Karl von Müller",

    "Albert I of Belgium": "King Albert I",
    "King Albert I": "King Albert I",

    "Konrad Wolf": "Konrad Wolf",
    "Konrad Wolf (commander)": "Konrad Wolf",

    "Liman von Sanders": "Liman von Sanders",
    "Liman von Sanders(Yıldırım Army Group)": "Liman von Sanders",
    "Otto Liman von Sanders": "Liman von Sanders",

    "Paul André Marie Maistre": "Paul Maistre",
    "Paul Maistre": "Paul Maistre",

    "Paul Emil von Lettow-Vorbeck": "Paul von Lettow-Vorbeck",
    "Paul von Lettow-Vorbeck": "Paul von Lettow-Vorbeck",

    "António Júlio da Costa Pereira de Eça": "Pereira d'Eça",
    "Pereira d'Eça": "Pereira d'Eça",

    "Philip Chetwode": "Philip Chetwode",
    "Philip Chetwode(XXI Corps)": "Philip Chetwode",
    "Philip Chetwode, 1st Baron Chetwode": "Philip Chetwode",

    "Reginald Bacon": "Reginald Bacon",
    "Sir Reginald Bacon": "Reginald Bacon",

    "Robert L. Bullard": "Robert L. Bullard",
    "Robert Lee Bullard": "Robert L. Bullard",

    "Roger Keyes": "Roger Keyes",
    "Roger Keyes, 1st Baron Keyes": "Roger Keyes",

    "Stepa Stepanovic": "Stepa Stepanović",
    "Stepa Stepanović": "Stepa Stepanović",

    "Suleyman Izzet Bey": "Suleyman Izzet Bey",
    "Süleyman Izzet Bey": "Suleyman Izzet Bey",

    "Svetozar Boroević": "Svetozar Boroević",
    "Svetozar Boroevic": "Svetozar Boroević",
    "Svetozar Boroević von Bojna": "Svetozar Boroević",
    "Svetozar Borojević": "Svetozar Boroević",

    "Viktor Dankl": "Viktor Dankl von Krasnik",
    "Viktor Dankl von Krasnik": "Viktor Dankl von Krasnik",

    "Vladimir Sakharov (general)": "Vladimir Sakharov",
    "Vladimir Viktorovich Sakharov": "Vladimir Sakharov",

    "W. Grant": "William Grant",
    "William Grant (general)": "William Grant",

    "William M. Marshall": "William M. Marshall",
    "William Marshall (British Army officer)": "William M. Marshall",

    "Wiliam Meldrum": "William Meldrum",
    "William Meldrum (lawyer)": "William Meldrum",

    "William Birdwood": "William Birdwood",
    "William Birdwood, 1st Baron Birdwood": "William Birdwood",

    "Émile Guépratte": "Émile Guépratte",
    "Émile Paul Amable Guépratte": "Émile Guépratte",

    "Ismet Pasha": "İsmet İnönü",
    "İsmet İnönü": "İsmet İnönü",

    "Mustafa Kemal Atatürk": "Mustafa Kemal Atatürk",
    "Mustafa Kemal Pasha": "Mustafa Kemal Atatürk",

    "Frederick Campbell (British Army officer, born 1860)": "Frederick Campbell",
    "Frederick Campbell": "Frederick Campbell",
}