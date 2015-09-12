from __future__ import division
import math
def bestInfoGainAttr(cptTable, attributes):
    #cptTable is a list of dictionaries. Each dictionary is a row in CPT table.
    #for each key (attribute) calculate information Gain and the one with highest
    #calculate hx
    print("______________________________________________")
    print(" Choosing an attribute to branch")
    hx = calculate_hx(cptTable)
    bestAttribute=None
    bestIGain = 0
    #check Infogain for each contribute
    for attribute in attributes:
        #for each attribute find gain
        attriValues = []
        for row in cptTable:
            if row[attribute] not in attriValues:
                attriValues.append(row[attribute])
        if len(attriValues) == 1:
            continue
        attr_value_count ={}
        total_rows = 0
        for value in attriValues:
            attr_value_count[value] =0
        for row in cptTable:
            total_rows +=1
            attr_value_count[row[attribute]] +=1
        gain =0
        for value in attriValues:
            hxy = calculate_hxy(cptTable, attribute, value)
            phxy = (attr_value_count[value]/total_rows)*hxy
            gain +=phxy
        #print(attribute+" "+str(attriValues))
        ig = hx - gain
        #print("gain "+str(ig))
        if ig > bestIGain:
            bestIGain = ig
            bestAttribute = attribute

        #now for each attribute value, find the info gain
    #print(" The best attribute "+ str(bestAttribute)+ " info gain "+ str(bestIGain))
    #if bestIGain == 0:
    #    print("next Page "+ str(cptTable[0]['nextPage']))
    return bestAttribute
def calculate_hx(cptTable):
    #we will calculate Hx value
    #values is list of unique values.
    values = []
    for row in cptTable:
        #print(row['nextPage'])
        if row['nextPage'] not in values:
            values.append(row['nextPage'])
    #we will calculate number of rows with value from 'values'
    value_dict = {}
    for value in values:
        value_dict[value] =0
    for row in cptTable:
        value_dict[row['nextPage']] +=1
    #print(value_dict)
    total_count = 0
    for value in values:
        total_count +=value_dict[value]
    gainValue =0
    for value in values:
        f1 = value_dict[value]/total_count
        log_f1 = math.log(f1, 2)
        gainValue += f1*log_f1
    #print(gainValue)
    return -1*gainValue
def calculate_hxy(cptTable, attribute, value):
    #calculate gain for an attribute passed as argument
    total_count_rows = 0
    pos_count = 0
    neg_count = 0
    hxy = 0
    for row in cptTable:
        if row[attribute] == value:
            total_count_rows +=1
            if row['nextPage'] =='0':
                neg_count +=1
            elif row['nextPage'] =='1':
                pos_count +=1
    if pos_count!=0:
        hxy += (pos_count/total_count_rows)*math.log(pos_count/total_count_rows,2)
    if neg_count != 0:
        hxy += (neg_count/total_count_rows)*math.log(neg_count/total_count_rows,2)
    #print(hxy)
    return -1*hxy
def calculate_chisquare(cptTable, attribute, p_value, totalRows):
    if  p_value == '1':
        return True

    chi_square_table= {}
    for i in range(1,6):
        chi_square_table[i] ={}
    #referred to http://www.ndsu.edu/pubweb/~mcclean/plsc431/mendel/mendel4.htm for probability, degree of freedom table
    chi_square_table[1]['0.01'] = 6.64
    chi_square_table[1]['0.05'] = 3.84

    chi_square_table[2]['0.01'] = 9.21
    chi_square_table[2]['0.05'] = 5.99


    chi_square_table[3]['0.01'] = 11.35
    chi_square_table[3]['0.05'] = 7.82

    chi_square_table[4]['0.01'] = 13.28
    chi_square_table[4]['0.05'] = 9.49

    chi_square_table[5]['0.01'] = 15.09
    chi_square_table[5]['0.05'] = 11.07


    d_freedom=0;
    total_pos= 0
    total_neg = 0
    values = []
    for row in cptTable:
        if row[attribute] not in values:
            values.append(row[attribute])
        if row['nextPage'] == '0':
            total_neg +=1
        elif row['nextPage'] == '1':
            total_pos +=1
    d_freedom = len(values) -1
    if d_freedom <1:
        return False
    if d_freedom >  5:
        d_freedom =5
    #print("calculate chi-suqare p value "+str(p_value)+" dfreedo "+str(d_freedom))
    chi_value_threshold = chi_square_table[d_freedom][p_value]

    pi  = total_pos*(len(cptTable)/totalRows)
    ni = total_neg*(len(cptTable)/totalRows)
    #calculate chi value from the cpt tables
    chi_value =0
    for value in values:
        poses = 0
        negs =0
        if row[attribute] == value:
            if row['nextPage'] == '1':
                poses +=1
            elif row['nextPage'] == '0':
                negs +=1
        chi_value += (pi - poses)**2/pi + (ni -negs)**2/ni
    #print("Chi_value "+str(chi_value))
    if chi_value > chi_value_threshold:
        #We should branch
        return True
    else:
        #we should not branch
        return False

def IsCompliant(row, rootNode):
    #here row is a cpt Row and root node is the root of the ID3 tree.
    if rootNode.decision is not None:
        print("Decision We got "+ str(rootNode.decision) + " actual decision " +str(row['nextPage']))
        if rootNode.decision == int(row['nextPage']):
            #print("Hurray")
            return True
        else:
            return False
    else:
        #this is not a leaf node in decision tree, check for values
        keys = rootNode.branches.keys()
        if row[rootNode.attribute] in keys:
            #print("Thank goodness")
            return IsCompliant(row, rootNode.branches[row[rootNode.attribute]], )
        else:
            #print("Existing keys")
            #print(keys)
            #print("Given key")
            #print(row[rootNode.attribute])
            #print("There was a problem with test data")
            return True
