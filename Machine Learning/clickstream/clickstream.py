from __future__ import division
from parse_data import parse_training_data
from decision_tree_class import TreeNode
from utility_funcs import bestInfoGainAttr
from utility_funcs import calculate_chisquare
from utility_funcs import IsCompliant
import sys
p_value = 0
total_num_rows = 0
total_size = 0
def main():

    print(" Please choose if you want to use chi-square:")
    print(" 1. Do not use Chi-Square")
    print(" 2. Use Chi-Square")
    userInput = input(" Enter your choice:")
    global p_value
    useChiSq = False
    if userInput == 1:
        useChiSq = False
    elif userInput == 2:
        userPvalue = input(" Enter p value, Valid values (0.01|0.05|1):")
        if (userPvalue != 0.01) and (userPvalue != 0.05) and (userPvalue != 1):
            print(" Please enter a valid P value, exiting")
            return
        p_value = str(userPvalue)
        useChiSq = True
    else:
        print(" Please make a valid choice, exiting ")
        return
    global total_size
    total_size =0
    print(" Given p value "+str(p_value))
    #CPT table is a list of rows with attributes and values, approximately of 40k size
    print(" Parsing Training Data")
    cptTable = parse_training_data('data/featnames.csv','data/trainfeat.csv','data/trainlabs.csv')
    global total_num_rows
    total_num_rows = len(cptTable)
    attributes = cptTable[0].keys()
    attributes.remove('nextPage')
    print(" Building decision tree")
    root_node  = build_id3(cptTable, attributes, useChiSq)
    #bestInfoGainAttr(cptTable)
    #print_id3(root_node)
    test_accuracy(root_node)
    calculatespace(root_node)
    print("Total Size (Nodes in decision tree)="+str(total_size))

def build_id3(cptTable, attributes, useChiSq):
    #print(" ID3  p_value "+str(p_value))
    bestAttribute = bestInfoGainAttr(cptTable, attributes)
    print("Branching on attribute "+ str(bestAttribute))
    if bestAttribute is None:
        decision = get_decision(cptTable)
        treenode = TreeNode()
        treenode.decision = decision
        return treenode
    treenode = TreeNode()
    treenode.attribute = bestAttribute
    #should i make branches on this best attribute ? Lets decide by chi-square values
    if useChiSq:
        print(" Calculating Chi-square and deciding to branch or not")
        if not calculate_chisquare(cptTable, bestAttribute,p_value, total_num_rows ):
            decision = get_decision(cptTable)
            treenode.decision = decision
            return treenode
    #make branches
    values = []
    for row in cptTable:
        if row[bestAttribute] not in values:
            values.append(row[bestAttribute])
    tempCptTable =[]
    #print(" values count = "+str(len(values)))
    attributes.remove(bestAttribute)
    if len(attributes) == 0:
        decision = get_decision(cptTable)
        treenode.decision = decision
        return treenode
    for value in values:
        print(value)
        tempCptTable = []

        for row in cptTable:
            if row[bestAttribute] == value:
                tempCptTable.append(row)

        childNode = build_id3(tempCptTable, attributes, useChiSq)
        treenode.branches[value] = childNode
    print(treenode.branches)
    return treenode
def print_id3(rootNode):
    if rootNode.attribute is None:
        return
    print "------------------------------"
    print(rootNode.attribute)
    print "_______________________________"
    print("number of subnodes "+str(len(rootNode.branches)))
    for key in rootNode.branches.keys():
        print_id3(rootNode.branches[key])
def get_decision(cptTables):
    #make a decision
    pos_dec = 0
    neg_dec = 0
    decision =0
    for row in cptTables:
        if row['nextPage'] == '0':
            neg_dec +=1
        elif row['nextPage'] =='1':
            pos_dec +=1
    if pos_dec == 0:
        decision =0
    elif neg_dec ==0:
        decision = 1
    elif pos_dec/neg_dec >= 1.0:
        #print(" positive decision")
        decision = 1
    elif neg_dec/pos_dec >=1.0:
        #print("negative decision")
        decision = 0
    else:
        #print("uncertain")
        decision = -1
    return  decision

def test_accuracy(rootNode):
    print("Testing Accuracy of the Algorithm")
    testCptTable = parse_training_data('data/featnames.csv','data/testfeat.csv','data/testlabs.csv')
    num_corrects = 0
    num_wrongs =   0
    for row in testCptTable:
        #for each row test the accuracy
        if not IsCompliant(row, rootNode):
            num_wrongs+=1
        else:
            num_corrects+=1
    total_count = num_corrects+num_wrongs
    accuracy = (num_corrects/total_count)*100
    print("          Accuracy Percentage ="+str(accuracy))

def calculatespace(rootNode):
    global total_size
    if rootNode.decision is not None:
        total_size +=1
        #this is a leaf node
        return
    else:
        #it is a decision node
        total_size +=1
        for key in rootNode.branches.keys():
            calculatespace(rootNode.branches[key])


if __name__ == "__main__":
    main()



