from __future__ import division
from data_parser import parse_training_data


def main():
    learnedData = parse_training_data('data/train')
    f = open('data/test')
    m = 100
    p  = 0.002
    correct =0
    incorrect = 0
    for line in f:
        wordList = line.split()

        #spam probability
        probSpam = learnedData['spamCount']/learnedData['mailCount']
        probHam = learnedData['hamCount']/learnedData['mailCount']

        #probability that this email is a spam
        emailSpamProb = 1
        emailHamProb =1
        emailId = wordList[0]
        type = wordList[1]
        # for each word find the probability it is spam and prob it is ham
        max_diff_s = 0
        max_diff_h = 0
        for word in wordList[2::2]:
            if word in learnedData.keys():
                wordSpamProb = (learnedData[word]['spam']+p*m)/(learnedData[word]['ham']+learnedData[word]['spam']+m)
                wordHamProb = (learnedData[word]['ham']+p*m)/(learnedData[word]['ham']+learnedData[word]['spam']+m)
            else:
                wordSpamProb = 0.5
                wordHamProb = 0.5
            emailSpamProb = emailSpamProb*wordSpamProb
            emailHamProb = emailHamProb*wordHamProb

        naiveBayesSpamProb = emailSpamProb*probSpam
        naiveBayesHamProb = emailHamProb*probHam
        found = 'spam'
        # print(" naive spam "+str(naiveBayesSpamProb)+" naive Ham "+str(naiveBayesHamProb))
        if(naiveBayesHamProb > naiveBayesSpamProb):
            #print("mail "+emailId+" is Ham"+" given is "+ type)
            found = 'ham'
        else:
            #print("mail "+emailId+" is Spam"+" given is "+ type)
            found = 'spam'
        if type == found:
            correct +=1
        else:
            incorrect +=1
    print("correct "+str(correct)+" incorrect "+str(incorrect))
    total = correct+incorrect
    correctPer = (correct/total)*100
    incorrectPer = (incorrect/total)*100
    print("correct "+str(correctPer)+" incorrect "+str(incorrectPer))

if __name__ == "__main__":
    main()