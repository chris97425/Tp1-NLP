import re , os

def get_wfb_info(pays,attribut):
    """
    Travaille TP1 Langage Naturel 
    :param pays: pays commençant par une majuscule 
    :param attribut: attribut correspondant à la liste suivante ["NATIONAL_ANTHEM","LITERACY","EXPORTS","GDP_REAL_GROWTH_RATE","GDP_PER_CAPITA","EXECUTIVE_BRANCH","DIPLOMATIC_REPRESENTATION_FROM_US", "NATURAL_HAZARDS"]
    :return: la valeur (String) qui match avec la regex de l'attribut pour un pays donné
    """

    dataDico = {"trillion": 10**12, "billion": 10**9, "million": 10**6, "quadrillion":10**15}
    attributDico = {"NATIONAL_ANTHEM" : "National anthem","LITERACY" : "Literacy","EXPORTS" : "Exports","GDP_REAL_GROWTH_RATE" : "GDP - real growth rate","GDP_PER_CAPITA" : "GDP - per capita \(PPP\)","EXECUTIVE_BRANCH" : "Executive branch:","DIPLOMATIC_REPRESENTATION_FROM_US" : "Diplomatic representation from the US:" , "NATURAL_HAZARDS":"Natural hazards:"}
    listetitre = ["Prince","King","Queen","President"]
    repcour = os.getcwd()
    os.chdir("factbook/geos")
    corel = open("aa.html", "r")
    allcorel = corel.read()


    sortie = True
    while sortie == True :

        filetoOpen = re.search('(..\.html)"> '+pays, allcorel)

        if (filetoOpen==None) or (pays == ""):

            pays = input("Je suis désolé mais le pays entré en paramètre n'ait pas dans ma base, verifier l'orthographe et rééssayer: ")


        else:

            sortie=False
    corel.close()
    fichWork = open(filetoOpen.group(1), "r")
    textAnalyse = fichWork.read()
    os.chdir(repcour)

    if attribut=='NATIONAL_ANTHEM':


        essai = re.search(attributDico[attribut]+":</a>[\n\t\w\W]*;\">\".*\((.*)\)</s",textAnalyse)

        if (essai == None):

            essai = re.search(attributDico[attribut] + ":</a>[\n\t\w\W]*;\">\"?(.*)\"</s", textAnalyse)

        print(essai.group(1))
        return essai.group(1)

    if attribut == 'LITERACY':

        essai = re.search(attributDico[attribut]+":[\W\w\t]*?male:[\W\w\t]*?\">([\d\W]*%)", textAnalyse)
        print(essai.group(1))
        return essai.group(1)

    if attribut == 'EXPORTS':

        essai = re.search(attributDico[attribut]+":[\W\w]*?(\$)([\d]*)(.?)([\d]*)? (.*ion)?", textAnalyse)

        if (essai.group(3) == "."):

            valeur = essai.group(2) + essai.group(3) + essai.group(4)

        else:

            valeur = essai.group(2)

        valeurF=float(valeur)
        valeurFi=essai.group(1)+str(int(valeurF*dataDico[essai.group(5)]))
        print(valeurFi)
        return valeurFi

    if (attribut == "GDP_REAL_GROWTH_RATE"):

        essai = re.search(attributDico[attribut] +":[\w\W]+?\">(-?[\d.]+%?)", textAnalyse)
        print(essai.group(1))
        return essai.group(1)

    if (attribut =="GDP_PER_CAPITA"):

        result = re.findall("\$([\d]+,[\d?]*)", textAnalyse)
        valeurfi2 = 0

        for i in range(0,len(result)):

            wiVir = re.search("([\d]+)(,)([\d]*)", result[i])

            if (valeurfi2 < int(wiVir.group(1)+wiVir.group(3)) ):

                valeurfi2=int(wiVir.group(1)+wiVir.group(3))

        valeurfi3="$"+str(valeurfi2)
        print(valeurfi3)
        return valeurfi3

    if (attribut == "NATURAL_HAZARDS"):

        natural = re.search(attributDico[attribut]+"[\w\W]*(typhoon|cyclon|storm|windstorm)[\w\W]*?<", textAnalyse)

        if (natural):

            print("YES")
            return "YES"

        else:

            print("NO")
            return "NO"

    if (attribut == "EXECUTIVE_BRANCH"):

        branch = re.search(attributDico[attribut]+"[\w\W]*?m;\">([A-Za-z]*).([a-zA-Z\W]*)? \(", textAnalyse)

        if (branch.group(1) in listetitre):

            finalvalue = branch.group(2) + ", " + branch.group(1)
            print(finalvalue)
            return finalvalue

        else:

            finalvalue = branch.group(1) + " " + branch.group(2)+", "+"Unknown"
            print(finalvalue)
            return finalvalue




    if (attribut == "DIPLOMATIC_REPRESENTATION_FROM_US"):

        diplomatic = re.search(attributDico[attribut]+"[\w\W]*(mailing address:)[\t\n]*<", textAnalyse)

        if (diplomatic):

            diplomatic = re.search(attributDico[attribut] + "[\w\W]*mailing address:[\w\W]*?>([\w\W]*?)([ADF]PO)", textAnalyse)

            if not(diplomatic == None):

                print(diplomatic.group(1)+diplomatic.group(2))
                return diplomatic.group(1)+diplomatic.group(2)

            diplomatic = re.search(attributDico[attribut] + "[\w\W]*mailing address:[\w\W]*?>(?:US Department of State, )?(B?[GPO .]*[\w\W]*?,[\w\W]*?) ?[,<]", textAnalyse)

            if not(diplomatic == None):

                print(diplomatic.group(1))
                return diplomatic.group(1)

        else:

            print("No_diplomatic_rep")
            return "No_diplomatic_rep"

    fichWork.close()

##############Faire une fonction menu qui permet de lancer le test ou bien un attribut pour un pays choisie