# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from Queue import Queue

from util import manhattanDistance
from game import Directions
import random, util
time_taken = 0
from game import Agent
import globalVariables
#evaluation function for sparse boards: gives a specific direction
def getClosestFoodTrial(successorGameState,posX,posY):
    currMin = 9999

    food = successorGameState.getFood()

    # print food[0][0]
    # print food[0]
    rows = len(list(food))
    cols = len(food[0])
    if food[posX][posY] == True:
        return 1
    for i in range(rows):
        for j in range(cols):
            if food[i][j] == True:
                currMin = min(currMin,manhattanDistance((posX,posY),(i,j)))

    return 1/currMin
#eval function for food for dense board. expands slower. but terminates faster
def getClosestFood(currentGameState, successorGameState,posX,posY):
    dict = {(posX,posY):1}
    posList = Queue()
    posList._put(((posX,posY),0))
    walls = successorGameState.getWalls()
    food = currentGameState.getFood()
    if food[posX][posY] == True:
        return 1
    check = False
    closestFood = 99999
    max = 20
    current = 0
    #from the position of pacman, expands on all sides with a valid path. efficient for dense food positions
    while not posList.empty():
        ((currX, currY),x) = posList._get()
        current = x+1
        if(food[currX][currY] == True):
            check = True
            closestFood = min(closestFood,current)
        if check == False and (currX-1,currY) not in dict.keys() and walls[currX-1][currY] != True:
            posList._put(((currX-1,currY),current))
            dict[(currX-1,currY)] = 1
        if check == False and (currX,currY-1) not in dict.keys()and walls[currX][currY-1] != True:
            posList._put(((currX,currY-1),current))
            dict[(currX,currY-1)] = 1
        if check == False and (currX+1,currY) not in dict.keys() and walls[currX+1][currY] != True:
            posList._put(((currX+1,currY),current))
            dict[(currX+1,currY)] = 1
        if check == False and(currX,currY+1) not in dict.keys() and walls[currX][currY+1] != True:
            posList._put(((currX,currY+1),current))
            dict[(currX,currY+1)] = 1
    return 1.0/closestFood
class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        i = 0
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]

        bestScore = max(scores)
        #globalVariables.nodesExpanded +=len(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]

        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        oldPos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print successorGameState
        #base score is that of the board
        baseScore = successorGameState.getScore()
        (posX,posY) = newPos
        closestGhost = 999999999999
        if action == "Stop":
            baseScore -= 2
        #if ghosts are not scared, then evaluate ghost positon by manhatan distance
        if newScaredTimes <[20,20]:
            for ghost in newGhostStates:
              closestGhost = min(closestGhost,manhattanDistance(newPos, ghost.configuration.pos))
            if closestGhost != 0 and closestGhost < 3:
               baseScore = baseScore-10/closestGhost
            elif closestGhost != 0 and closestGhost <5:
                baseScore = baseScore -10/closestGhost-1
        count = currentGameState.getNumFood()
        #if the board is sparse/dense choose the right food position eval function
        if count < 5:
            closestCost = getClosestFood(currentGameState,successorGameState,posX,posY)
        else:
            closestCost = getClosestFood(currentGameState,successorGameState,posX,posY)

        baseScore +=closestCost
        return baseScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    (posX, posY) = currentGameState.getPacmanPosition()
    foodCloseness = getClosestFoodTrial(currentGameState, posX, posY)
    return currentGameState.getScore() + foodCloseness
    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    #def __init__(self, evalFn = 'better', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.minList = [[] for i in range(self.depth)]
        # self.maxList = []

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    #max level
    def MaxAction(self, gameState, depth):
        #if the depth is more than max depth, just return the cost of the board
        if self.depth ==depth:
            return self.evaluationFunction(gameState)
        actionAgent = gameState.getLegalActions(0)
        if actionAgent == []:
            return self.evaluationFunction(gameState)
        maxList = []
        maximum = -99999
        maximumIndex = -1
        for action in actionAgent:
            #for each action generate successor, keep track of minimum cost at that level, call minaction for the same depth
            nextSuccessor = gameState.generateSuccessor(0,action)
            ghostId = 1
            minimumC = 9999
            # globalVariables.nodesExpanded +=1
            maximum = max(maximum,self.MinAction(nextSuccessor, ghostId, depth, minimumC))
        # print maxList

        return maximum
        # pass
    def MinAction(self, gameState, ghost, depth,minimumC):
        if self.depth == depth:
            return self.evaluationFunction(gameState)
        #if we have more ghosts to set positon for..
        if ghost <gameState.getNumAgents():
            actionGhost = gameState.getLegalActions(ghost)
            #if no legal path return the cost
            if actionGhost == []:
                return self.evaluationFunction(gameState)
            for action in actionGhost:
                nextSuccessor = gameState.generateSuccessor(ghost, action)
                ghostId = ghost + 1
                # globalVariables.nodesExpanded +=1
                #keep track of minimum.. not update, that happens only if all the ghosts are set.
                minimumC = self.MinAction(nextSuccessor, ghostId, depth, minimumC)
        #no more ghosts to set position for... go to max level of next depth
        else:
            #update the minlevel minimum value
            # globalVariables.nodesExpanded +=1
            minimumC = min(minimumC,self.MaxAction(gameState, depth+1))
            # print self.minList

        return minimumC
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        #root level (max) eval function (same as MaxAgent)
        depth = 0
        actionAgent = gameState.getLegalActions(0)
        maxList = []
        maximum = -99999
        maximumIndex = -1
        # print gameState
        index = 0
        for action in actionAgent:
            nextSuccessor = gameState.generateSuccessor(0, action)
            # print nextSuccessor
            # print nextSuccessor
            ghostId = 1
            minimumC = 9999
            priorMax = maximum
            # globalVariables.nodesExpanded +=1
            maximum = max(maximum, self.MinAction(nextSuccessor, ghostId, depth, minimumC))
            if priorMax != maximum:
                #print action
                #print maximum
                maximumIndex = index
            index = index + 1
            #print "index" + str(index)
        # print "get action depth:"+ str(depth)

        #print maxList
        # print actionAgent[chosenIndex]
        return actionAgent[maximumIndex]
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    #similar to MaxAction in Minimax but we also keep track fo alpha and beta
    def MaxAction(self, gameState, depth, alphaParent, betaParent):
        if self.depth ==depth:
            return self.evaluationFunction(gameState)
        actionAgent = gameState.getLegalActions(0)
        if actionAgent == []:
            return self.evaluationFunction(gameState)
        maximum = -99999
        alphaCurr =alphaParent
        betaCurr = betaParent
        maximumIndex = -1
        for action in actionAgent:
            nextSuccessor = gameState.generateSuccessor(0,action)
            ghostId = 1
            minimumC = 9999
            # globalVariables.nodesExpanded +=1
            #get the cost from childen adn update the node value
            maximumTemp = self.MinAction(nextSuccessor, ghostId, depth, minimumC, alphaCurr, betaCurr)
            #maximum has no funciton just scared to remove
            maximum = max(maximum, maximumTemp)
            #update the alpa value based on its childen, beta not affected
            alphaCurr = max(maximumTemp, alphaCurr)
            if alphaCurr > betaCurr:
                #print "pruned at maximum"
                return minimumC
        # print maxList

        return maximum
    #same as MinAction in Minimax. but with alpha nd beta
    def MinAction(self, gameState, ghost, depth,minimumC, alphaParent, betaParent):
        if self.depth == depth:
            return self.evaluationFunction(gameState)
        alphaCurr =alphaParent
        betaCurr = betaParent
        if ghost <gameState.getNumAgents():
            actionGhost = gameState.getLegalActions(ghost)
            if actionGhost == []:
                return self.evaluationFunction(gameState)
            for action in actionGhost:
                nextSuccessor = gameState.generateSuccessor(ghost, action)
                ghostId = ghost + 1
                # globalVariables.nodesExpanded +=1

                minimumTemp = self.MinAction(nextSuccessor, ghostId, depth, minimumC, alphaCurr, betaCurr)
                minimumC = min(minimumTemp, minimumC)
                #at min level update the beta value, not aplha
                betaCurr = min(betaCurr, minimumTemp)
                if minimumC < alphaParent:
                    #print "pruned at minimum"
                    return minimumC

        else:
            # globalVariables.nodesExpanded +=1
            #update the minvalue at the level from the cost we get from previous level
            minimumC = min(minimumC,self.MaxAction(gameState, depth+1, alphaCurr, betaCurr))

        return minimumC
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        #acts as the root (same function as the MaxAgent but returns index instead of cost
        depth = 0
        actionAgent = gameState.getLegalActions(0)
        maxList = []
        maximum = -99999  #value V
        alphaParent = -99999 #alpha from parent (root has no parent)
        betaParent  =  99999 #beta from parent (root has no parent )
        alphaCurr = -99999
        betaCurr  =  99999
        maximumIndex = -1
        # print gameState
        index = 0
        for action in actionAgent:
            nextSuccessor = gameState.generateSuccessor(0, action)
            # print nextSuccessor
            # print nextSuccessor
            ghostId = 1
            maximumC = 9999
            priorMax = maximum
            # globalVariables.nodesExpanded +=1
            # print "getaction"
            # print "alphacurr", alphaCurr
            # print "betacurr", betaCurr
            maximumTemp = self.MinAction(nextSuccessor, ghostId, depth, maximumC,alphaCurr,betaCurr)
            maximum  = max(maximum, maximumTemp)
            alphaCurr = max(alphaCurr, maximumTemp)
            if priorMax != maximum:
                #print action
                #print maximum
                maximumIndex = index
            index = index + 1
            if maximum>betaParent:
                #print "pruned at root"
                break
            #print "index" + str(index)
        # print "get action depth:"+ str(depth)

        #print maxList
        # print actionAgent[chosenIndex]
        return actionAgent[maximumIndex]
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()



class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


