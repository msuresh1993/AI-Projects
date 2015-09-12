
def parse_training_data(filename):
    # open the training file and parse it
    f= open(filename,'r')
    learnedData = {}
    learnedData['mailCount'] = 0
    learnedData['spamCount'] = 0
    learnedData['hamCount']  = 0
    for line in f:
        #parse the email
        wordList = line.split()
        mailId = wordList[0]
        type = wordList[1]
        learnedData['mailCount'] +=1
        if type == 'spam':
            learnedData['spamCount'] +=1
        elif type == 'ham':
            learnedData['hamCount'] +=1
        for word in wordList[2::2]:
            index = wordList.index(word)
            occurrences = wordList[index+1]
            if word not in learnedData.keys():
                #initialize the data structure for the word
                learnedData[word]={}
                learnedData[word]['spam']=0
                learnedData[word]['ham'] = 0
            learnedData[word][type] +=1

    print(learnedData)
    return learnedData

