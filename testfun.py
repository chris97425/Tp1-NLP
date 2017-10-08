import csv, t1

listatt=["PREC_NATIONAL_ANTHEM","PREC_LITERACY","PREC_EXPORTS","PREC_GDP_REAL_GROWTH_RATE","PREC_GDP_PER_CAPITA","PREC_NATURAL_HAZARDS","PREC_EXECUTIVE_BRANCH","PREC_DIPLOMATIC_REPRESENTATION_FROM_US"  ]
nbpays = 9
with open('wfb_test2.1.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    motsc,reperb,compteurliste,gene=0,0,0,0

    for row in spamreader:
        print(row[0],row[1])
        a = t1.get_wfb_info(row[0], row[1])
        reperb = reperb+1
        reperb = reperb % nbpays

        if(a == row[2]):
            motsc+=1
            gene+=1

        else:

            print("ERROR 404: --------------------------------------------->" + a + " ||devrait être:|| " + row[2])

        if(reperb == 0):

            motsc=(motsc/nbpays)*100
            print("-------------------------------------------------------->"+listatt[compteurliste]+": "+str(motsc)+"%")
            compteurliste+=1
            motsc = 0

    print("La précision total est:"+str((gene/80)*100))



