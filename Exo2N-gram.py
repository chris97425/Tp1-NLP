import os , copy, codecs
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

    if ("<UNK>" in gram):
        v_corpus+=1

    for key in gram:
        break
        
    if (isinstance(gram[key], int)):

        for key in gram:

            gram[key] = (gram[key] + (1 * delta)) / ( (v_corpus * delta))


    elif (len(key)==1):

        count_char = uni_gr(fich_txt,False,True)

        for key in gram:

            for key2 in gram[key]:

                if (boolres==True):

                    gram[key][key2] = (gram[key][key2]+(1*delta))/(count_char[key]+(v_corpus*delta))

                else:

                    gram[key][key2] = ((gram[key][key2]+(1*delta)) * count_char[key]) / (count_char[key] + (v_corpus*delta))

    if (len(key)==2):

        count_char2 = bi_grmo(fich_txt,True,True)
        for key in gram:

            for key2 in gram[key]:
                if(key == "<UNK>"):

                    gram[key][key2] = (0 + (1 * delta)) / (0 + (v_corpus * delta))


                else:

                    if (boolres==True):

                        gram[key][key2] = (gram[key][key2]+(1*delta))/(count_char2[key[0]][key[1]]+(v_corpus*delta))

                    else:

                        gram[key][key2] = ((gram[key][key2]+(1*delta)) * count_char2[key[0]][key[1]]) / (count_char2[key[0]][key[1]] + (v_corpus*delta))


    return gram
#print(lissage_laplace(tri_grmo("corpus_entrainement/english-training.txt",True,True),"corpus_entrainement/english-training.txt",True,2))
print(lissage_laplace(uni_gr("corpus_entrainement/english-training.txt",False,True),"corpus_entrainement/english-training.txt",True,2))

#Fonction d'interpolation linaire qui vas prendre en entré un n-Gram et un fichier test et nous renvoie un nouvelle unigramme lisser par interpolation linaire
def interpola_linear(gram,fich_txt):

    uni=uni_gr(fich_txt,True)
    usegram=copy.deepcopy(gram)
   # print(usegram["A "]["c"])

    for key in usegram:

        break

    if (len(key) == 1): #je suis dans le cas d'une interpolation lineaire de Bi-Gram

        for key in usegram:

            for key2 in usegram[key]:

                usegram[key][key2] = (1/2)*usegram[key][key2] + (1/2)*uni[key2]

    if (len(key) == 2):  # je suis dans le cas d'une interpolation lineaire de tri-Gram

        bi_gram = bi_grmo(fich_txt,False)

        for key in usegram:

            for key2 in usegram[key]:


                usegram[key][key2] =  (1 / 3) * usegram[key][key2] + (1 / 3) * bi_gram[key[1]][key2] + (1 / 3) * uni[key2]

    return usegram
#print(interpola_linear(bi_grmo("english-training.txt",False),"english-training.txt"))
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


def perplexity(laporint,fich_txt_test,gram_ent):

    textdoc = codecs.open(fich_txt_test, "r","utf-8").read()
    laporintf=laporint
    if (laporintf== "interpolation"):

        dico_prob=copy.deepcopy(interpola_linear(gram,fich_txt))

    else:

        dico_prob=copy.deepcopy(lissage_laplace(gram,fich_txt,False))

    return dico_prob
    for key in laporintf:

        break

    if (len(key)==1):

        for key in interpola_linear(laporintf,"english-training.txt"):

            pass
#print(perplexity("interpolation","english-training.txt",bi_grmo("english-training.txt",False)))

















