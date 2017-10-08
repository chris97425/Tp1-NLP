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

def uni_gr(fich_txt):

    corpus_empty = empty_dico(fich_txt)

    with open(fich_txt, "r") as fileobj:
        for line in fileobj:
           for ch in line:
            corpus_empty[ch]+=1
    return corpus_empty

####################################################bigrammamammammammmammmammmammmammma##################
def bi_grmo(fich_txt,boolret):

    uni=uni_gr(fich_txt)
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

#################################################################trigramme ##################################

def tri_grmo(fich_txt,boolre):
    c=0
    textdoc = open(fich_txt, "r").read()
    pro_bi_count = bi_grmo(fich_txt,False)
    dico_tri_gr = {}
    dico_tri_count={}

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

    return dico_tri_gr

#print(tri_grmo("english-training.txt",True)["A "]["c"])

def lissage_laplace(gram,fich_txt,boolres):

    v_corpus=len(empty_dico(fich_txt))
    for key in gram:
        break

    if (len(key)==1):

        count_char = uni_gr(fich_txt)

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
print(lissage_laplace(bi_grmo("english-training.txt",True),"english-training.txt",True))