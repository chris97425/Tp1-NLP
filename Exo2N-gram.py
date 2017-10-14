import os , copy, codecs, math, re
os.chdir("detect_langue/")

#Ici je créer un dictionnaire vide contenant l'ensemble des lettres du corpus étudié sans doublon
def empty_dico(fich_txt):

    corpus={}

    with codecs.open(fich_txt, 'r', 'utf-8') as fileobj:

        for line in fileobj:

            for ch in line:

                corpus[ch] = 0

    return corpus

#print(empty_dico("corpus_entrainement/english-training.txt"))
#print(len(empty_dico("corpus_entrainement/english-training.txt")))
##################################################################unigramme####################

#Ici je vais créer une fonction qui vas permettre de construire mon unigramme, boolres en fonction de sa valeur va renvoyer le compte des lettres
#ou alors leurs probabilités, fich_txt sera le fichier texte d'entraînenemnt
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

#print(len(uni_gr("corpus_entrainement/portuguese-training.txt",False,True)))
#print(uni_gr("english-training.txt",True))


#Ici je vais créer une fonction qui vas me permettre de construire un bigramme, fich_txt est notre fichier txt d'entraînement,
#boolret est un booléen qui nous renvoie le bigramme sous forme de probabilité si False ou alors nous renvoie le bigramme sous forme de compte
#test et fich_txt_test sont dans l'ordre un booléen pour préciser que l'on est dans la construction d'un bigramme en ajoutant
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

#print(bi_grmo("corpus_entrainement/english-training.txt",False,True))
#################################################################trigramme ##################################

#Ici je vais créer une fonction qui vas me permettre de construire un trigramme, fich_txt est notre fichier txt d'entraînement,
#boolret est un booléen qui nous renvoie le trigramme sous forme de probabilité si False ou alors nous renvoie le trigramme sous forme de compte
#test et fich_txt_test sont dans l'ordre un booléen pour préciser que l'on est dans la construction d'un bigramme en ajoutant
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
        for key in dico_tri_count:

            dico_tri_count[key]["<UNK>"] = 0


    if (boolre==True):

        return dico_tri_count

    else:

        return dico_tri_gr


#print(tri_grmo("corpus_entrainement/english-training.txt",True,True))
#lissage de Laplace qui prend en entrée un n-gram un fichier text d'entraînement, boolres nous permet de renvoyer les nouvelles probabilités si True ou alors les nouveaux
#compte si False, delta et le coefficient multiplicateur du lissage de Laplace
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
# text_file = open("Output.txt", "w", encoding="utf8")
# text_file.write(str(lissage_laplace(tri_grmo("corpus_entrainement/english-training.txt", True, True),"corpus_entrainement/english-training.txt", True, 1)))
# text_file.close()
# print(lissage_laplace(tri_grmo("corpus_entrainement/english-training.txt",True,True),"corpus_entrainement/english-training.txt",True,1))

#print(lissage_laplace(bi_grmo("corpus_entrainement/english-training.txt",True,True),"corpus_entrainement/english-training.txt",True,1))

#print(lissage_laplace(uni_gr("corpus_entrainement/english-training.txt",False,True),"corpus_entrainement/english-training.txt",True,1))

#Fonction d'interpolation linaire qui vas prendre en entré un n-Gram et un fichier test et nous renvoie un nouvelle unigramme lisser par interpolation linaire
def interpola_linear(gram,fich_txt):

    uni=uni_gr(fich_txt,True,True)
    print(uni)
    usegram=copy.deepcopy(gram)

    for key in usegram:

        break

    if (len(key) == 1):

        for key in usegram:

            for key2 in usegram[key]:

                usegram[key][key2] = (1/2)*usegram[key][key2] + (1/2)*uni[key2]

    if (len(key) == 2):

        bi_gram = bi_grmo(fich_txt,False)

        for key in usegram:


            for key2 in usegram[key]:

                if (key == "<UNK>"):

                    usegram[key] = (1 / 3) * bi_gram[key[1]][key2] + (1 / 3) * uni[key2]

                else:

                    usegram[key][key2] =  (1 / 3) * usegram[key][key2] + (1 / 3) * bi_gram[key[1]][key2] + (1 / 3) * uni[key2]

    return usegram


#print(interpola_linear(bi_grmo("corpus_entrainement/english-training.txt",False,True),"corpus_entrainement/english-training.txt"))
#print("\n\n\n\n\n\n <>----------------------------<> \n\n\n\n\n\n")

#Fonction qui vas me permettre de savoir quelle sont le nombre de lettre differente entre les deux fichier
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


def perplexity(laplace,fich_test):


    uselaplace=copy.deepcopy(laplace)
    # print(uselaplace)
    log=0

    test = codecs.open(fich_test, 'r', 'utf-8').read()
    v_corpus = len(test)
    # print(v_corpus)

    for key in uselaplace:
        break

    if (isinstance(uselaplace[key], float)):

        for line in test:

            for ch in line:

                if not(ch in uselaplace):

                    #print(ch)
                    log += math.log(uselaplace["<UNK>"])

                else:

                    log += math.log(uselaplace[ch])

                    #print(uselaplace[ch])
                    #print(log)
                    #print(uselaplace[ch],"est",ch)

        # print("la valeur de log",log)
        valeur1 = (-1/v_corpus)*log
        pp =  math.exp(valeur1)
        # print("La perp",pp)

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

        print("la valeur de log", log)
        valeur1 = (-1 / v_corpus) * log
        pp = math.exp(valeur1)
        print(pp)

    if (len(key) == 2):

        for i in range(0, len(test) - 2):
            A=""
            B=""
            key1 = test[i]+test[i+1]

            key2 = test[i + 2]

            if not(key1 in uselaplace):
                print(key1)
                A = key1
                key1 = "<UNK>"

            if not(key2 in uselaplace[key]):
                print(key2)
                B = key2
                key2 = "<UNK>"

            log += math.log(uselaplace[key1][key2])

            print(key1, key2, uselaplace[key1][key2])

        valeur1 = (-1 / v_corpus) * log
        pp = math.exp(valeur1)
        print("la perp",pp)

    return pp

def detect_language(n,langue,fich_txt,fich_test):



    # if(n == "UNI"):
    #
    #     for i in langue:
    #         print("---------", i)
    #         lot[i] = lissage_laplace(uni_gr("corpus_entrainement/" + i, False, True), "corpus_entrainement/" + i, True,
    #                                  1)
    #     UNI=copy.deepcopy(uni_gr("corpus_entrainement" + fich_txt, False, True))
    #
    # #BI=perplexity(lissage_laplace(bi_grmo("corpus_entrainement"+fich_txt, True, True),"corpus_entrainement"+fich_txt, True, 1), "corpus_test/"+fich_test)
    #
    # #TRI=perplexity(lissage_laplace(tri_grmo("corpus_entrainement"+fich_txt, True, True),"corpus_entrainement"+fich_txt, True, 1), "corpus_test/"+fich_test)


    listtest = os.listdir('corpus_test/')
    listent = os.listdir('corpus_entrainement/')
    #print(listent)
    langue = {}

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
                    # print("la valeur de A",A)
    #

    # lot={}
    #
    #
    # for i in langue:
    #
    # n=perplexity(lissage_laplace(uni_gr("corpus_entrainement" + fich_txt, False, True), "corpus_entrainement" + fich_txt, True,1), "corpus_test/" + fich_test)


    return langue


#print(detect_language("UNI",None,None,None))



def prédiction(langue,n):
    i=0
    listkey= []
    listkeyKey=[]

    for key in langue:

        listkey+=[key]


    for key in langue[key]:

        listkeyKey+=[key]


    for key in listkeyKey:

        b=1000000000.0

        for key2 in listkey:


            a=langue[key2][key]
            print("voila",float(a[n]))

            if(float(a[n])<=b):

                b=float(a[n])
                print("------<>")
                c=key2

        i+=1

        a=re.search("([\w\W]*)-", c)

        print("Pour un",n,"-gram la langue prédite du fichier: ",key,"\n Est le\la:",a.group(1))

prédiction(detect_language("UNI",None,None,None),"UNI")

























