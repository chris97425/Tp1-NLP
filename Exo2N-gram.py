#Version de python utilisé 3.6.1

import os , copy, codecs, math, re

os.chdir("detect_langue/")

def empty_dico(fich_txt):

    corpus={}

    with codecs.open(fich_txt, 'r', 'utf-8') as fileobj:

        for line in fileobj:

            for ch in line:

                corpus[ch] = 0

    return corpus
#Ici je crée un dictionnaire vide contenant l'ensemble des lettres du corpus étudié sans doublon
#Exemple
#print(empty_dico("corpus_entrainement/english-training.txt"))

##################################################################Construction d'un unigramme####################


def uni_gr(fich_txt,boolres,test):

    corpus_empty_count = empty_dico(fich_txt)

    i=0

    with codecs.open(fich_txt, 'r', 'utf-8') as fileobj:

        for line in fileobj:

           for ch in line:

            i+=1
            corpus_empty_count[ch]+=1

    corpus_empty_prob=copy.deepcopy(corpus_empty_count)

    for key in corpus_empty_prob:

        corpus_empty_prob[key]=corpus_empty_prob[key]/i
    if (test == True):
        corpus_empty_count["<UNK>"]=0
        corpus_empty_prob["<UNK>"] = 0
    if (boolres == False):

        return corpus_empty_count

    else:

        return corpus_empty_prob
# Ici je vais créer une fonction qui vas permettre de construire mon unigramme.
# Si boolres vaut False je renvoie l'unigram avec les compte sinon avec les probabilités
#Si test vaut true cela veut dire que j'inclue <unk> pour le lissage

#print(len(uni_gr("corpus_entrainement/portuguese-training.txt",False,True)))

##################################################################Construction d'un bigramme####################


def bi_grmo(fich_txt,boolret,test):

    uni=uni_gr(fich_txt,False,False)
    textdoc = codecs.open(fich_txt, 'r', 'utf-8').read()
    emptyd=empty_dico(fich_txt)
    bigr_prob=copy.deepcopy(emptyd)
    bigr_count= copy.deepcopy(emptyd)
    for key in bigr_prob:
        bigr_prob[key]={}
        bigr_count[key]={}


    for key in bigr_prob:

        bigr_prob[key] = empty_dico(fich_txt)
        bigr_count[key] = empty_dico(fich_txt)

    for i in range(0,len(textdoc)-1):

        bigr_prob[textdoc[i]][textdoc[i+1]]+=1/uni[textdoc[i]]
        bigr_count[textdoc[i]][textdoc[i+1]]+=1

    if (test == True):

        for key in bigr_prob:
            bigr_prob[key]["<UNK>"] = 0
            bigr_count[key]["<UNK>"] = 0

        bigr_prob["<UNK>"] = empty_dico(fich_txt)
        bigr_prob["<UNK>"]["<UNK>"]=0

        bigr_count["<UNK>"] = empty_dico(fich_txt)
        bigr_count["<UNK>"]["<UNK>"] = 0



    if(boolret==False):

        return bigr_prob

    else:

        return bigr_count
# Ici je vais créer une fonction qui vas me permettre de construire un bigramme
# fich_txt est notre fichier txt d'entraînement
# boolret est un booléen qui nous renvoie le bigramme sous forme de probabilité si False ou alors nous renvoie le bigramme sous forme de compte
# test  est la pour préciser que l'on est dans la construction d'un bigramme pour le test en ajoutant <unk>

#print(bi_grmo("corpus_entrainement/english-training.txt",False,True))
#print(bi_grmo("corpus_entrainement/english-training.txt",False,False))

#################################################################trigramme ##################################


def tri_grmo(fich_txt,boolre,test):


    textdoc = codecs.open(fich_txt, 'r', 'utf-8').read()
    pro_bi_count = bi_grmo(fich_txt,True,True)
    dico_tri_gr = {}


    for i in range(0, len(textdoc)-2):

        dico_tri_gr[textdoc[i]+textdoc[i+1]]={}

    for key in dico_tri_gr:

        dico_tri_gr[key]=empty_dico(fich_txt)

    dico_tri_count=copy.deepcopy(dico_tri_gr)

    for i in range(0, len(textdoc) - 2):

        dico_tri_gr[textdoc[i]+textdoc[i+1]][textdoc[i+2]] += 1/pro_bi_count[textdoc[i]][textdoc[i+1]]
        dico_tri_count[textdoc[i] + textdoc[i + 1]][textdoc[i + 2]] += 1

    if (test == True):

        dico_tri_count["<UNK>"] = empty_dico(fich_txt)
        dico_tri_gr["<UNK>"] = empty_dico(fich_txt)
        for key in dico_tri_count:

            dico_tri_count[key]["<UNK>"] = 0
            dico_tri_gr[key]["<UNK>"] = 0

    if (boolre==True):

        return dico_tri_count

    else:

        return dico_tri_gr

# Ici je vais créer une fonction qui vas me permettre de construire un trigramme
# fich_txt est notre fichier txt d'entraînement
# boolret est un booléen qui nous renvoie le trigramme sous forme de probabilité si False ou alors nous renvoie le trigramme sous forme de compte
# test  est la pour préciser que l'on est dans la construction d'un bigramme pour le test en ajoutant <unk>

#print(tri_grmo("corpus_entrainement/english-training.txt",True,True))


#################################################################Laplace ##################################

def lissage_laplace(gram,fich_txt,boolres,delta):

    v_corpus=len(empty_dico(fich_txt))
    usegram=copy.deepcopy(gram)
    if ("<UNK>" in usegram):
        v_corpus+=1
    # print(v_corpus)
    for key in usegram:
        break

    if (isinstance(usegram[key], int)):
        nbValue=0
        nbProb=0
        for key in usegram:
            nbValue+=usegram[key]
        # print(nbValue)
        for key in usegram:

            usegram[key] = (usegram[key] + (1 * delta)) / (nbValue +(v_corpus * delta))
        for key in usegram:
            nbProb+= usegram[key]
        #(nbProb)
        #(usegram)

    elif (len(key)==1):

        count_char = uni_gr(fich_txt,False,True)

        for key in usegram:
            #(count_char[key])
            for key2 in usegram[key]:

                if (boolres==True):

                    usegram[key][key2] = (usegram[key][key2]+(1*delta))/(count_char[key]+(v_corpus*delta))

                else:

                    usegram[key][key2] = ((usegram[key][key2]+(1*delta)) * count_char[key]) / (count_char[key] + (v_corpus*delta))

    if (len(key)==2):

        count_char2 = bi_grmo(fich_txt,True,True)
        for key in usegram:

            for key2 in usegram[key]:
                if(key == "<UNK>"):

                    usegram[key][key2] = (0 + (1 * delta)) / (0 + (v_corpus * delta))


                else:

                    if (boolres==True):

                        usegram[key][key2] = (usegram[key][key2]+(1*delta))/(count_char2[key[0]][key[1]]+(v_corpus*delta))

                    else:

                        usegram[key][key2] = ((usegram[key][key2]+(1*delta)) * count_char2[key[0]][key[1]]) / (count_char2[key[0]][key[1]] + (v_corpus*delta))


    return usegram


#lissage de Laplace qui prend en entrée un n-gram sur fichier text d'entraînement
# boolres nous permet de renvoyer les nouvelles probabilités si True ou alors les nouveaux comptes
#Delta et le coefficient multiplicateur du lissage de Laplace

#Lissage de Laplacce pour mes modèles trigram, bigram et unigram

#print(lissage_laplace(tri_grmo("corpus_entrainement/english-training.txt",True,True),"corpus_entrainement/english-training.txt",True,1))

# print(lissage_laplace(bi_grmo("corpus_entrainement/english-training.txt",True,True),"corpus_entrainement/english-training.txt",True,1))

#print(lissage_laplace(uni_gr("corpus_entrainement/english-training.txt",False,True),"corpus_entrainement/english-training.txt",True,1))


#################################################################Interpolation linear##################################

def interpola_linear(gram,fich_txt):


    uni=uni_gr(fich_txt,True,True)
    # print(uni)
    usegram=copy.deepcopy(gram)

    for key in usegram:

        break

    if (len(key) == 1):

        for key in usegram:

            for key2 in usegram[key]:

                if (key == "<UNK>"):

                    usegram[key] = (1 / 2) * uni[key2]

                else:

                    usegram[key][key2] = (1/2)*usegram[key][key2] + (1/2)*uni[key2]

    if (len(key) == 2):

        bi_gram = bi_grmo(fich_txt,False,False)

        for key in usegram:

            for key2 in usegram[key]:

                if (key == "<UNK>"):

                    usegram[key] = (1 / 3) * bi_gram[key[1]][key2] + (1 / 3) * uni[key2]

                else:

                    usegram[key][key2] =  (1 / 3) * usegram[key][key2] + (1 / 3) * bi_gram[key[1]][key2] + (1 / 3) * uni[key2]

    return usegram

#lissage par interpolation qui prend en entrée un n-gram sur fichier text d'entraînement avec un delta constant
#Ne fonctionne que pour les vocabulaire fermé

# print(interpola_linear(bi_grmo("corpus_entrainement/english-training.txt",True,False),"corpus_entrainement/english-training.txt"))
# print(interpola_linear(tri_grmo("corpus_entrainement/english-training.txt",True,False),"corpus_entrainement/english-training.txt"))



#Fonction qui vas me permettre de savoir quel  est le nombre de lettres differentes entre les deux fichiers

def word_unknown(fich_tex_ent,fich_text_test):

    unigram_ent=copy.deepcopy(uni_gr(fich_tex_ent,False,False))
    unigram_test=copy.deepcopy(uni_gr(fich_text_test,False,False))
    unigram_ent["<UNK>"] = 0
    dico_unk={}

    for key in unigram_test:

        if (key in unigram_ent):

            pass

        else:

            dico_unk[key]= unigram_test[key]
            unigram_ent["<UNK>"] +=   unigram_test[key]

    return unigram_ent

#print(word_unknown("corpus_entrainement/english-training.txt","corpus_test/test20.txt"))

##################################Calcul de la PP##########

def perplexity(laplace,fich_test):


    uselaplace=copy.deepcopy(laplace)
    log=0

    test = codecs.open(fich_test, 'r', 'utf-8').read()
    v_corpus = len(test)


    for key in uselaplace:
        break

    if (isinstance(uselaplace[key], float)):

        for line in test:

            for ch in line:

                if not(ch in uselaplace):

                    log += math.log(uselaplace["<UNK>"])

                else:

                    log += math.log(uselaplace[ch])

        valeur1 = (-1/v_corpus)*log
        pp =  math.exp(valeur1)

    elif (len(key) == 1):

        for i in range(0,len(test)-1):

            key1=test[i]
            key2=test[i+1]

            if not(test[i] in uselaplace):
                key1="<UNK>"
                A=test[i]
            if not(test[i+1] in uselaplace):
                key2 = "<UNK>"
                B = test[i+1]

            log += math.log(uselaplace[key1][key2])

        valeur1 = (-1 / v_corpus) * log
        pp = math.exp(valeur1)

    if (len(key) == 2):

        for i in range(0, len(test) - 2):

            A=""
            B=""
            key1 = test[i]+test[i+1]
            key2 = test[i + 2]

            if not(key1 in uselaplace):

                A = key1
                key1 = "<UNK>"

            if not(key2 in uselaplace[key]):

                B = key2
                key2 = "<UNK>"

            log += math.log(uselaplace[key1][key2])


        valeur1 = (-1 / v_corpus) * log
        pp = math.exp(valeur1)

    return pp

#Calul de la PP
#Prend en entrée un fichier lisser par Laplace
#Un fichier test
#Renvoie la PP

#print(perplexity(lissage_laplace(bi_grmo("corpus_entrainement/espanol-training.txt",True,True),"corpus_entrainement/espanol-training.txt",True,1),"corpus_test/test2.txt"))
#print(perplexity(lissage_laplace(tri_grmo("corpus_entrainement/espanol-training.txt",True,True),"corpus_entrainement/espanol-training.txt",True,1),"corpus_test/test2.txt"))
#print(perplexity(lissage_laplace(uni_gr("corpus_entrainement/espanol-training.txt",False,True),"corpus_entrainement/espanol-training.txt",True,1),"corpus_test/test1.txt"))


def detect_language(n):

    listtest = os.listdir('corpus_test/')
    listent = os.listdir('corpus_entrainement/')
    langue = {}
    if(n=="UNI"):

        for j in listent:
            if (j == ".DS_Store"):

                pass

            else:
                langue[j] = {}

                for i in listtest:

                    if (i==".DS_Store"):

                        pass

                    else:

                        langue[j][i]={n: perplexity(lissage_laplace(uni_gr("corpus_entrainement/" + j, False, True),"corpus_entrainement/" + j, True, 1),"corpus_test/" + i)}

    if (n == "BI"):

        for j in listent:


            if not(j == ".DS_Store"):

                lissabi = lissage_laplace(bi_grmo("corpus_entrainement/" + j, True, True), "corpus_entrainement/" + j,True, 10)
                langue[j] = {}

                for i in listtest:

                    if not(i == ".DS_Store"):

                        langue[j][i] = {n: perplexity(lissabi, "corpus_test/" + i)}

    if (n == "TRI"):

        for j in listent:

            if not (j == ".DS_Store"):
                lissabi = lissage_laplace(tri_grmo("corpus_entrainement/" + j, True, True), "corpus_entrainement/" + j,True, 1)

                langue[j] = {}

                for i in listtest:

                    if not (i == ".DS_Store"):

                        langue[j][i] = {n: perplexity(lissabi, "corpus_test/" + i)}

    return langue

#Renvoie la PP d'un modèle par rapport à tous les fichiers test dans un dictionnaire

# print(detect_language("UNI"))
# print(detect_language("TRI"))
# print(detect_language("BI"))


def prédiction(langue,n):

    i=0
    listkey= []
    listkeyKey=[]

    dicograph={"english":{"spp":0,"nb":0,"key":{}},"espanol":{"spp":0,"nb":0,"key":{}},"french":{"spp":0,"nb":0,"key":{}},"portuguese":{"spp":0,"nb":0,"key":{}}}


    for key in langue:

        listkey+=[key]


    for key in langue[key]:

        listkeyKey+=[key]
        #print(key)
    for key in listkeyKey:

        b=1000000000.0

        for key2 in listkey:


            a=langue[key2][key]

            if(float(a[n])<=b):

                b=float(a[n])
                c=key2

        i+=1

        a=re.search("([\w\W]*)-", c)
        dicograph[a.group(1)]["spp"]+=b
        dicograph[a.group(1)]["nb"]+=1
        dicograph[a.group(1)]["key"]["goodP"+str(i)]=key

        print("Pour un",n,"-gram la langue prédite du fichier: ",key,"\n Est le\la:",a.group(1))

    return dicograph

#Ici je teste et récupère pour tout les modèles d'entraînement la plus petite valeur de la perpléxité pour un fichier test
#Je précise ensuite la langue du fichier test

# print(prédiction(detect_language("BI"),"BI"))
# print(prédiction(detect_language("UNI"),"UNI"))
# print(prédiction(detect_language("TRI"),"TRI"))

#Fonction pour afficher les graphes
import matplotlib.pyplot as plt

def graphFile(langue):

    x = [1000, 2000, 3000]

    ALL_PP = perplexity(lissage_laplace(bi_grmo("corpus_entrainement/"+langue+"-training.txt",True,True),"corpus_entrainement/"+langue+"-training.txt",True,1),"nchar/1000.txt"),perplexity(lissage_laplace(bi_grmo("corpus_entrainement/english-training.txt",True,True),"corpus_entrainement/english-training.txt",True,1),"nchar/2000.txt") ,perplexity(lissage_laplace(bi_grmo("corpus_entrainement/english-training.txt",True,True),"corpus_entrainement/english-training.txt",True,1),"nchar/3000.txt")

    plt.plot(x, ALL_PP, label=langue)

    plt.title('PP de ' + 'test' + str(langue) + '.txt' + ' en fonction du modèle de langue')
    plt.ylabel('Perplexité')
    plt.xlabel('Modele bi-gram (1000, 2000, 3000)')
    plt.legend()
    plt.show()

#
# graphFile("french")
#
# graphFile("espanol")
# graphFile("english")
#
# graphFile("portuguese")





