import csv
def parse_training_data(featfile, trainfile, decfile):
    featureList=[]
    f_feature = open(featfile,'rt')
    try:
        featureReader = csv.reader(f_feature)
        for feature in featureReader:
            featureList.append(feature)
    except:
        print("error reading featnames file")
    featureValueDict = {}
    f_attributes = open(trainfile,'rt')
    cptTable=[]
    try:
        attriValReader = csv.reader(f_attributes)
        for row in attriValReader:
            cptRow={}
            attrString = " ".join(row)
            attriValList = attrString.split()
            #print(attriValList)
            for i in range(0, len(featureList)):
                #print(featureList[i])
                #print(attriValList[i])
                if attriValList[i] == ' ':
                    print("danger")
                cptRow[featureList[i][0]] = attriValList[i]
            cptTable.append(cptRow)
        #for dictRow in cptTable:
        #   print(dictRow)
    except:
        print("error reading train feature file")
    f_anotherPage = open(decfile,"rt")
    nextPageRows = f_anotherPage.readlines();
    for i in range(0, len(cptTable)):
        cptTable[i]['nextPage'] = nextPageRows[i].strip('\n')
    return cptTable
