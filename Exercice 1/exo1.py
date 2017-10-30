#Version de python utilisé 3.6.1

import re , os, codecs

def get_wfb_info():

    os.chdir("factbook/geos")

    corel = codecs.open("aa.html", "r",'utf-8')
    allcorel = corel.read()
    corel.close()
    os.chdir("../../")

    listePays = re.findall("geos/(...html)", allcorel)
    del listePays[0]

    for i in range(0,len(listePays)):

        os.chdir("factbook/geos")

        paysread = codecs.open(listePays[i], "r", 'utf-8')
        pays = paysread.read()
        paysread.close()

        nompays = re.search("[\w\W]*?xx[\w\W]*?" + listePays[i] + "\"> ?([\w\W]*?) </", pays)

        os.chdir("../../indexpays/")


        text_file = open(nompays.group(1) + ".json", "w", encoding="utf8")
        text_file.write("{\"name\":\"" + nompays.group(1) + "\",\n ")

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
