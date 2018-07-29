'''
    File name: User.py
    Author: Dave DeAngelis
'''
import random
from scipy.stats import norm

class User:
    def __init__(self, inID, inexpertiseMean, inexpertiseStdev, initPoints):
        self.userID = inID
        self.points = initPoints
        self.expertiseMean = inexpertiseMean
        self.expertiseStdev = inexpertiseStdev
        self.questionsasked = 0             #
        self.wronganswersreceived = 0       #
        self.correctanswersreceived = 0     #
        self.questionsattempted = 0         #
        self.answerswrong = 0               #
        self.answersright = 0               #
        self.bestanswersgiven = 0           #
 
    def generateAnswer(self):
        return random.normalvariate(self.expertiseMean, self.expertiseStdev) 
        
    def probabilityCorrect(self, questiondifficulty):
        return norm.cdf((self.expertiseMean - questiondifficulty) / self.expertiseStdev)
    
    def generateQuestion(self, difficultyExp):
        # Difficulty is random, with lower level questions more common
        # but number of questions is a function of the self.expertiseMean
        # Can consider question lifespan issues, pass another number along
        return random.random() ** difficultyExp
    
    # Probability that a question is considered for answering (seen on screen)
    # This is a function of the number of questions in the pool
    # This is a decreasing function from 1-> inf, never crosses X axis. At X=0, Y=1
    def isquestionconsidered(self, numQuestions, QuestionSeenConstant, QuestionSeenDenomExp):
        # y=K/x^J
        probseen = QuestionSeenConstant / (numQuestions ** QuestionSeenDenomExp)
        if random.random() < probseen:
            return True
        else:
            return False
    
    # Evaluating and answering questions
    # Sort list of considered questions by expected earnings (including probability correct and exclusivity)
    # Returns a list of (questiontuple, answertuple)
    # Yahoo Strategy: Giving an answer = +2, Best Answer = +10, +1 for correct answer 
    def YahooAnswer(self, consideredQuestions, MaxAnswers):
        if len(consideredQuestions) == 0:
            return []
        else:
            # EV = (Probcorrect * 1) + 2
            qalist = []
            outlist = []
            
            for question in consideredQuestions:
                # EV is just Prob. correct * 1 + 2
                EV = self.probabilityCorrect(question[0]) + 2
                qalist.append((EV, question, (self.userID, self.generateAnswer())))
            
            qalist.sort(reverse=True)
           
            if len(qalist) < MaxAnswers:
                maxoutputsize = len(qalist)
            else:
                maxoutputsize = MaxAnswers
                                   
            for z in range(maxoutputsize):
                if (qalist[z])[0] > 0:
                    outlist.append(((qalist[z])[1], (qalist[z])[2]))
            return outlist
        
        
    # Evaluating and answering questions
    # Sort list of considered questions by expected earnings (including probability correct and exclusivity)
    # Points must decay
    def ReciprocalAnswer(self, consideredQuestions, MaxAnswers, RecipWeight):
        # print 'evaluating, Reciprocal Style'
        if len(consideredQuestions) == 0:
            return []
        else:
            # Must fill in this function
            # EV = (Probcorrect * 1) + 2
            qalist = []
            outlist = []
            
            for question in consideredQuestions:
                # EV is a function of probcorrect, askerpoints
                EV = self.probabilityCorrect(question[0]) * question[2] * RecipWeight
                qalist.append((EV, question, (self.userID, self.generateAnswer())))
            
            qalist.sort(reverse=True)
                       
            if len(qalist) < MaxAnswers:
                maxoutputsize = len(qalist)
            else:
                maxoutputsize = MaxAnswers
                                   
            for z in range(maxoutputsize):
                if (qalist[z])[0] > 0:
                    outlist.append(((qalist[z])[1], (qalist[z])[2]))
            return outlist
