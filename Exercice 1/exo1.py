#Version de python utilisé 3.5.0

import re , os, codecs

#La fonction indexPays permet de creer le dossier index pays
##################################### Partie 0
def indexPays(chemin):
    newpath = r""+chemin+'indexpays'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

def get_wfb_info():
##################################### Partie 1
    os.chdir("factbook/geos")

    corel = codecs.open("aa.html", "r",'utf-8')
    allcorel = corel.read()
    corel.close()
    os.chdir("../../")

    listePays = re.findall("geos/(...html)", allcorel)
    del listePays[0]
##################################### Partie 2
    for i in range(0,len(listePays)):

        os.chdir("factbook/geos")

        paysread = codecs.open(listePays[i], "r", 'utf-8')
        pays = paysread.read()
        paysread.close()

        nompays = re.search("[\w\W]*?xx[\w\W]*?" + listePays[i] + "\"> ?([\w\W]*?) </", pays)

        indexPays("../../")
        os.chdir("../../indexpays/")


        text_file = open(nompays.group(1) + ".json", "w", encoding="utf8")
        text_file.write("{\"name\":\"" + nompays.group(1) + "\",\n ")
##################################### Partie 3
        try:

            introduction = re.search("Introduction[\w\W]*?middle[\w\W]*?a\">(.*?)</", pays)

            text_file.write("\"Background\":\""+introduction.group(1).replace('"','\\"')+"\",\n")

        except AttributeError:

            text_file.write("\"Background\":\"""\",\n")

        try:

            geonote = re.search("hy - note[\W\w]*?<d.*?\">(.*?)</", pays)

            text_file.write("\"Geography-note\":\""+geonote.group(1).replace('"','\\"')+"\",\n")

        except AttributeError:

            text_file.write("\"Geography-note\":\"""\",\n")

        try:

            ecomoni = re.search("my - ov[\w\W]*?<di.*\">(.*)</", pays)

            text_file.write("\"Economy-overview\":\""+ecomoni.group(1).replace('"','\\"')+"\"\n""}")

        except AttributeError:

            text_file.write("\"Economy-overview\":\"""\",\n")

        os.chdir("../")
        text_file.close()


get_wfb_info()
