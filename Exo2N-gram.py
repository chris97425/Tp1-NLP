import os , copy

os.chdir("detect_langue/corpus_entrainement")

def empty_dico(fich_txt):

    corpus={}

    with open(fich_txt, "r") as fileobj:

        for line in fileobj:
            for ch in line:
                corpus[ch] = 0
    return corpus

##################################################################unigramme####################

def uni_gr(fich_txt,boolres):

    corpus_empty_count = empty_dico(fich_txt)

    i=0

    with open(fich_txt, "r") as fileobj:

        for line in fileobj:

           for ch in line:

            i+=1
            corpus_empty_count[ch]+=1

    #print(i)
    corpus_empty_prob=copy.deepcopy(corpus_empty_count)

    for key in corpus_empty_prob:

        corpus_empty_prob[key]=corpus_empty_prob[key]/i

    if (boolres == False):

        return corpus_empty_count

    else:

        return corpus_empty_prob

#print(uni_gr("english-training.txt",True)["c"])
#print(uni_gr("english-training.txt",True))


####################################################bigrammamammammammmammmammmammmammma##################
def bi_grmo(fich_txt,boolret):

    uni=uni_gr(fich_txt,False)
    textdoc = open(fich_txt, "r").read()
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

    if(boolret==False):

        return bigr_prob

    else:

        return bigr_count
print(bi_grmo("english-training.txt",True))
#################################################################trigramme ##################################

def tri_grmo(fich_txt,boolre):


    textdoc = open(fich_txt, "r").read()
    pro_bi_count = bi_grmo(fich_txt,True)
    dico_tri_gr = {}

    for i in range(0, len(textdoc)-2):

        dico_tri_gr[textdoc[i]+textdoc[i+1]]={}

    for key in dico_tri_gr:

        dico_tri_gr[key]=empty_dico(fich_txt)

    dico_tri_count=copy.deepcopy(dico_tri_gr)


    for i in range(0, len(textdoc) - 2):

        dico_tri_gr[textdoc[i]+textdoc[i+1]][textdoc[i+2]] += 1/pro_bi_count[textdoc[i]][textdoc[i+1]]
        dico_tri_count[textdoc[i] + textdoc[i + 1]][textdoc[i + 2]] += 1

    if (boolre==True):

        return dico_tri_count

    else:

        return dico_tri_gr



#print(tri_grmo("english-training.txt",False)["A "]["c"])

def lissage_laplace(gram,fich_txt,boolres):

    v_corpus=len(empty_dico(fich_txt))
    for key in gram:
        break

    if (len(key)==1):

        count_char = uni_gr(fich_txt,False)

        for key in gram:

            for key2 in gram[key]:

                if (boolres==True):

                    gram[key][key2] = (gram[key][key2]+1)/(count_char[key]+v_corpus)

                else:

                    gram[key][key2] = ((gram[key][key2]+1) * count_char[key]) / (count_char[key] + v_corpus)

    if (len(key)==2):

        count_char2 = bi_grmo(fich_txt,True)

        for key in gram:

            for key2 in gram[key]:

                if (boolres==True):

                    gram[key][key2] = (gram[key][key2]+1)/(count_char2[key[0]][key[1]]+v_corpus)

                else:

                    gram[key][key2] = ((gram[key][key2]+1) * count_char2[key[0]][key[1]]) / (count_char2[key[0]][key[1]] + v_corpus)

    return gram
#print(lissage_laplace(bi_grmo("english-training.txt",True),"english-training.txt",True))


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


#print(interpola_linear(tri_grmo("english-training.txt",False),"english-training.txt"))

