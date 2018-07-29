'''
    File name: MechSim.py
    Author: Dave DeAngelis
'''
import sys
import User
import random
import numpy
import ConfigParser

def main():
    
    # Retrieve globals from config file
    if (len(sys.argv) != 3):
        print 'Error: Must specify configuration file and number of rounds to average'
        return
    else:
        cfgfilename = sys.argv[1]
        numRounds = int(sys.argv[2])
    
    config = ConfigParser.ConfigParser()
    config.read(cfgfilename)
    
    global NumUsers, PowerlawExponent, UniformExpertiseStdev, DifficultyExponent, QuestionAskConstant, QuestionSeenConstant, QuestionSeenDenomExp, MaxAnswers, Testwithrecommender, Strategy, DecayPercentage, IDCounter, RecipWeight, NumCycles    
    
    NumUsers = int(config.get("Sim Constants", "NumUsers"))
    PowerlawExponent = float(config.get("Sim Constants", "PowerlawExponent"))
    UniformExpertiseStdev = float(config.get("Sim Constants", "UniformExpertiseStdev"))
    DifficultyExponent = float(config.get("Sim Constants", "DifficultyExponent"))
    QuestionAskConstant = float(config.get("Sim Constants", "QuestionAskConstant"))
    QuestionSeenConstant = float(config.get("Sim Constants", "QuestionSeenConstant"))
    QuestionSeenDenomExp = float(config.get("Sim Constants", "QuestionSeenDenomExp"))
    MaxAnswers = int(config.get("Sim Constants", "MaxAnswers"))
    DecayPercentage = int(config.get("Sim Constants", "DecayPercentage"))
    RecipWeight = float(config.get("Sim Constants", "RecipWeight"))
    Testwithrecommender = config.get("Sim Constants", "Testwithrecommender")
    Strategy = config.get("Sim Constants", "Strategy")
    NumCycles = int(config.get("Sim Constants", "NumCycles"))

        
    # Instrumentation code
    avgexpertisel = []
    avgquestionsaskedl = []
    avgcorrectanswersreceivedl = []
    avgwronganswersreceivedl = []
    avgquestionsattemptedl = []
    avganswersrightl = []
    avganswerswrongl = []
    avgbestanswersgivenl = []
    
    stdexpertisel = []
    stdquestionsaskedl = []
    stdcorrectanswersreceivedl = []
    stdwronganswersreceivedl = []
    stdquestionsattemptedl = []
    stdanswersrightl = []
    stdanswerswrongl = []
    stdbestanswersgivenl = []
    
    printSettings()
    
    for singleround in range(numRounds):
                
        print 'Executing Round #' + str(singleround+1) + ' of ' + str(numRounds)
      
        IDCounter = 1      
        Users = {}
        ###########################
        # CREATE USERS
        ###########################
        # Power law expertise initialization  
        for i in range(NumUsers):
            if Strategy == 'Yahoo':
                TempUser = User.User(IDCounter, random.random() ** PowerlawExponent, random.random() * UniformExpertiseStdev, 100)
            else:
                TempUser = User.User(IDCounter, random.random() ** PowerlawExponent, random.random() * UniformExpertiseStdev, 100)
            if IDCounter in Users:
                print 'Duplicate User ID keys! Error'
                break
            Users[IDCounter] = TempUser
            IDCounter += 1
              
        for i in range(NumCycles):
            singleCycle(Users)
            if Strategy == 'Reciprocal':
                pointDecay(Users, DecayPercentage)
            userTurnover(Users)
            NumberofUsers = len(Users)
        #####################################################################################
        # Instrumentation Code
        #####################################################################################
        
        # Get top X percentage
        percenttoget = 10
         
        finalusernum = NumberofUsers
        
        topuserslist = Users.values()       
        topuserslist.sort(key = lambda element: element.expertiseMean)
        topuserslist.reverse()
        
        lastindex = int(round(len(topuserslist) * percenttoget / 100))
        topuserslist = topuserslist[0:lastindex]
        
        expertisel = []
        questionsaskedl = []
        correctanswersreceivedl = []
        wronganswersreceivedl = []
        questionsattemptedl = []
        answersrightl = []
        answerswrongl = []
        bestanswersgivenl = []
        finalusernuml = []
        
        for person in topuserslist:
            expertisel.append(person.expertiseMean)
            questionsaskedl.append(person.questionsasked)
            correctanswersreceivedl.append(person.correctanswersreceived)
            wronganswersreceivedl.append(person.wronganswersreceived)
            questionsattemptedl.append(person.questionsattempted)
            answersrightl.append(person.answersright)
            answerswrongl.append(person.answerswrong)
            bestanswersgivenl.append(person.bestanswersgiven)
        
        finalusernuml.append(finalusernum)
            
        avgexpertisel.append(numpy.mean(expertisel))
        avgquestionsaskedl.append(numpy.mean(questionsaskedl))
        avgcorrectanswersreceivedl.append(numpy.mean(correctanswersreceivedl))
        avgwronganswersreceivedl.append(numpy.mean(wronganswersreceivedl))
        avgquestionsattemptedl.append(numpy.mean(questionsattemptedl))
        avganswersrightl.append(numpy.mean(answersrightl))
        avganswerswrongl.append(numpy.mean(answerswrongl))
        avgbestanswersgivenl.append(numpy.mean(bestanswersgivenl))
        
        stdexpertisel.append(numpy.std(expertisel))
        stdquestionsaskedl.append(numpy.std(questionsaskedl))
        stdcorrectanswersreceivedl.append(numpy.std(correctanswersreceivedl))
        stdwronganswersreceivedl.append(numpy.std(wronganswersreceivedl))
        stdquestionsattemptedl.append(numpy.std(questionsattemptedl))
        stdanswersrightl.append(numpy.std(answersrightl))
        stdanswerswrongl.append(numpy.std(answerswrongl))
        stdbestanswersgivenl.append(numpy.std(bestanswersgivenl))
    
    print 'Final number of users: ' + str(numpy.mean(finalusernuml))         
    print 'avgexpertise: ' + str(numpy.mean(avgexpertisel)) + ' stdexpertise: ' + str(numpy.mean(stdexpertisel))
    print 'avgquestionsasked: ' + str(numpy.mean(avgquestionsaskedl)) + ' stdquestionsasked: ' + str(numpy.mean(stdquestionsaskedl))
    print 'avgcorrectanswersreceived: ' + str(numpy.mean(avgcorrectanswersreceivedl)) + ' stdcorrectanswersreceived: ' + str(numpy.mean(stdcorrectanswersreceivedl))
    print 'avgwronganswersreceived: ' + str(numpy.mean(avgwronganswersreceivedl)) + ' stdwronganswersreceived: ' + str(numpy.mean(stdwronganswersreceivedl))
    print 'avgquestionsattempted: ' + str(numpy.mean(avgquestionsattemptedl)) + ' stdquestionsattempted: ' + str(numpy.mean(stdquestionsattemptedl))
    print 'avganswersright: ' + str(numpy.mean(avganswersrightl)) + ' stdanswersright: ' + str(numpy.mean(stdanswersrightl))
    print 'avganswerswrong: ' + str(numpy.mean(avganswerswrongl)) + ' stdanswerswrong: ' + str(numpy.mean(stdanswerswrongl))
    print 'avgbestanswersgiven: ' + str(numpy.mean(avgbestanswersgivenl)) + ' stdbestanswersgiven: ' + str(numpy.mean(stdbestanswersgivenl))
  
    print 'end of program'
  
    return

    
def singleCycle(Users):
    # Question bank
    currentQuestions = []
    questionswithAnswers = {}
          
    ###########################
    # CREATE QUESTIONS
    ###########################
    for singleUserkey in Users:
        # Calculate the probability of asking a question
        probAsk = ((-1 * Users[singleUserkey].expertiseMean) + 1) / QuestionAskConstant
        if(random.random() < probAsk):
            # Generate question (difficulty, questioner points)
            questiondifficulty = Users[singleUserkey].generateQuestion(DifficultyExponent)
            questionproperties = (questiondifficulty, Users[singleUserkey].userID, Users[singleUserkey].points)
            currentQuestions.append(questionproperties)
            questionswithAnswers[questionproperties] = []
            
            Users[singleUserkey].questionsasked += 1
            # Deduct 5 points when asking a question
            if Strategy == 'Yahoo':
                Users[singleUserkey].points -= 5
        
    ###########################
    # ANSWER QUESTIONS
    ###########################
    # For each User, send list of considered questions (tuples), When user generates ranking and returns a list of answer tuples 
    # Append each answer tuple to the values of a dictionary keyed by Question Tuple. Then walk through each key and distribute rewards
    # Tuple types:
    # Question Tuple: (Difficulty, QuestionerID, QuestionerPoints)
    # Answer Tuple: (AnswererID, AnswerVal)
    # Answer Tuples are always bound to a Question Tuple in another tuple. Multiple Answer Tuples 
    # bound to the same Question Tuple form a list in the second tuple field.
    numquestions = len(currentQuestions)
    for singleUserkey in Users:
        consideredQuestions = []    # list of questions considered for answering
        for question in currentQuestions:
            if Testwithrecommender=='True' or Users[singleUserkey].isquestionconsidered(numquestions, QuestionSeenConstant, QuestionSeenDenomExp):
                # add to question list, include expected reward, answer just 1 in list
                consideredQuestions.append(question)
        
        # Now use different strategies to decide to answer question
        # Build list of answer tuples 
        if Strategy == 'Yahoo':
            oneuserQandAlist = Users[singleUserkey].YahooAnswer(consideredQuestions, MaxAnswers)
        elif Strategy == 'Reciprocal':
            oneuserQandAlist = Users[singleUserkey].ReciprocalAnswer(consideredQuestions, MaxAnswers, RecipWeight)
        else:
            print 'Bad Strategy name. Choose \'Reciprocal\' or \'Yahoo\'' 
        
        # Append answer tuples into Dict, keyed with question tuple
        for response in oneuserQandAlist:
        #    print 'response 0: ' + str(response[0])
            questionswithAnswers[response[0]].append(response[1])
            Users[singleUserkey].questionsattempted += 1
    
    ###########################
    # DISTRIBUTE REWARDS
    ###########################                    
    # Evaluate and distribute rewards, depends on strategy
    # Have questionswithAnswers Dictionary, structure: Key: QuestionTuple, Value: List of AnswerTuples
    # Question Tuple: (Difficulty, QuestionerID, QuestionerPoints)
    # Answer Tuple: (AnswererID, AnswerVal)
    
    pointchangelist = []
    
    if Strategy == 'Yahoo':
        for qa in questionswithAnswers:
            pointchangelist = Yahoopoints(Users, qa, questionswithAnswers[qa])
            # print pointchangelist
            for item in pointchangelist:
                oldval = (Users[item[0]]).points
                Users[item[0]].points = oldval + item[1] 
    
    elif Strategy == 'Reciprocal':
        for qa in questionswithAnswers:
            pointchangelist = Recippoints(Users, qa, questionswithAnswers[qa])
            # print pointchangelist
            for item in pointchangelist:
                oldval = (Users[item[0]]).points
                Users[item[0]].points = oldval + item[1]         
    
    else:
        print 'Bad Strategy name. Choose \'Reciprocal\' or \'Yahoo\'' 
    
    
    numquestions = len(currentQuestions)        

# Requires a single question, and a list of the answers
# Return list of tuples of the form: (UserID, change in points)
# +1 for correct answer, +10 for Best Answer, +2 for answering a question at all
def Yahoopoints(inUsers, inquestiontuple, inanswertuplelist):
    
    pointchange = 0
    currentuserID = -1
    questiondiff = inquestiontuple[0]
    questionerID = inquestiontuple[1]
    BestAnswerVal = -1000
    BestAnswerID = -1
    
    returnlist = []
    
    for singleanswer in inanswertuplelist:
        
        # Bonus for providing any answer
        pointchange = 2
        
        currentuserID = singleanswer[0]
        currentanswerval = singleanswer[1]
        
        if currentanswerval > BestAnswerVal:
            # New best answer
            BestAnswerVal = currentanswerval
            BestAnswerID = currentuserID
        
        # Correct Answer
        if currentanswerval > questiondiff:
            pointchange += 1
            inUsers[currentuserID].answersright += 1
            inUsers[questionerID].correctanswersreceived += 1
        else:
            inUsers[currentuserID].answerswrong += 1
            inUsers[questionerID].wronganswersreceived += 1
            
        # Create output Tuple
        returnlist.append((currentuserID, pointchange))
    
    if BestAnswerID != -1:
        inUsers[BestAnswerID].bestanswersgiven += 1
        for item in returnlist:
            if item[0] == BestAnswerID:
                item = (item[0], item[1] + 10)        
    
    return returnlist

# Requires a single question, and a list of the answers
# Return list of tuples of the form: (UserID, change in points)
# Question tuple has questioner points
# 0 for wrong answer, recipweight * Questionerpoints for right answer,  5 * recipWeight * Questionerpoints for BA
def Recippoints(inUsers, inquestiontuple, inanswertuplelist):
    
    pointchange = 0
    currentuserID = -1
    questiondiff = inquestiontuple[0]
    questionerpoints = inquestiontuple[2]
    questionerID = inquestiontuple[1]
    BestAnswerVal = -1000
    BestAnswerID = -1
    
    returnlist = []
    
    for singleanswer in inanswertuplelist:
        
        pointchange = 0
        
        currentuserID = singleanswer[0]
        currentanswerval = singleanswer[1]
        
        if currentanswerval > BestAnswerVal:
            # New best answer
            BestAnswerVal = currentanswerval
            BestAnswerID = currentuserID
        
        # Correct Answer
        if currentanswerval > questiondiff:
            pointchange += RecipWeight * questionerpoints
            inUsers[currentuserID].answersright += 1
            inUsers[questionerID].correctanswersreceived += 1
        else:
            inUsers[currentuserID].answerswrong += 1
            inUsers[questionerID].wronganswersreceived += 1
            
        # Create output Tuple
        returnlist.append((currentuserID, pointchange))

    if BestAnswerID != -1:
        inUsers[BestAnswerID].bestanswersgiven += 1
        for item in returnlist:
            if item[0] == BestAnswerID:
                item = (item[0], item[1] + RecipWeight * 5 * questionerpoints)        
    
    return returnlist

###########################
# USERS COME AND GO
###########################
def userTurnover(inUsers):
    # Remove some current users, function of users' points relative to everyone else's
    
    global IDCounter
    preturnoverusersize = len(inUsers)
    userslist = []
    for singleuserkeys in inUsers:
        userslist.append((singleuserkeys, inUsers[singleuserkeys]))
        
    # y=1/(5*x^(1/4)) - .2, yields 6.666667% turnover per cycle
    
    userslist.sort(key = lambda element: element[1].points)
        
    poplist = []
    
    # Calculate percentile for each user. Then calculate probability of defection
    # Use this probability to compare a random number and remove user
    for z in range(len(userslist)):
        # Generate percentile, then generate probability, then determine if pop
        percentile = float(z) / len(inUsers)
        probdefect = 1 / (5 * (percentile + .01) ** (.25)) - .2
        if(random.random() < probdefect):
            poplist.append(z)
    
    # Poplist is the list of indices to remove, must be translated to keys
    
    poplist.reverse()
       
    for elementindex in poplist:
        del inUsers[(userslist[elementindex])[0]]
        
    # Add some new users
    # Number of users to add: 7% stddev=1
    numtoadd = int(round(random.normalvariate(.07*preturnoverusersize, .01*preturnoverusersize)))
    if numtoadd < 0:
        numtoadd = 0
    for i in range(numtoadd):
        if IDCounter in inUsers:
            print 'ID already in the Users. Check IDCounter'
        inUsers[IDCounter] = (User.User(IDCounter, random.random() ** PowerlawExponent, random.random() * UniformExpertiseStdev, 100))
        IDCounter += 1 
    
    return

###########################
# POINTS DECAY OVER TIME
###########################
# Amount of point decay is a fixed percentage of total points accumulated. 
# This percentage must be tweaked.
# Alternate option: Decay is a function of percentile rank. Higher ranking people lose a larger percentage of points.
def pointDecay(inUsers, decaypercentage):
        
    for singleuserkey in inUsers:
        temppoints = inUsers[singleuserkey].points
        pointstodeduct = int(round(.01 * float(decaypercentage) * float(temppoints)))
        inUsers[singleuserkey].points -= pointstodeduct   
    
    return
    
def printSettings():
    print 'numUsers: ' + str(NumUsers)
    print 'PowerlawExponent: ' + str(PowerlawExponent)
    print 'UniformExpertiseStdev: ' + str(UniformExpertiseStdev)
    print 'DifficultyExponent: ' + str(DifficultyExponent)
    print 'QuestionAskConstant: ' + str(QuestionAskConstant)
    print 'QuestionSeenConstant: ' + str(QuestionSeenConstant)
    print 'QuestionSeenDenomExp: ' + str(QuestionSeenDenomExp)
    print 'MaxAnswers: ' + str(MaxAnswers)
    print 'Testwithrecommender: ' + Testwithrecommender
    print 'RecipWeight: ' + str(RecipWeight)
    print 'Decay percentage: ' + str(DecayPercentage)
    print 'Strategy: ' + Strategy
    print 'NumCycles: ' + str(NumCycles)
    

if __name__ == "__main__":
    main()
