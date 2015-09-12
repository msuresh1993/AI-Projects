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

from game import Agent
def getClosestFoodTrial(successorGameState,posX,posY):
    currMin = 9999
    food = successorGameState.getFood()
    if food[posX][posY] == True:
        return 1
    for i in range(20):
        for j in range(10):
            if food[i][j] == True:
                currMin = min(currMin,manhattanDistance((posX,posY),(i,j)))

    return 1/currMin
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
    while not posList.empty():
        #print "entered"
        ((currX, currY),x) = posList._get()
        current = x+1
        # if current >10:
        #     break
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
    # if closestFood <3:
    #     closestFood = 7-closestFood
    # elif closestFood < 10:
    #     closestFood = 5-closestFood/2
    #
    # elif closestFood >10:
    #     closestFood = 5-closestFood/4
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

        baseScore = 0
        (posX,posY) = newPos
        closestGhost = 999999999999
        if action == "Stop":
            baseScore -= 2
        if newScaredTimes <[20,20]:
            for ghost in newGhostStates:
              closestGhost = min(closestGhost,manhattanDistance(newPos, ghost.configuration.pos))
            if closestGhost != 0 and closestGhost < 3:
               baseScore = baseScore-10/closestGhost
            elif closestGhost != 0 and closestGhost <5:
                baseScore = baseScore -10/closestGhost-1
        count = currentGameState.getNumFood()
        if count >5:
            closestCost = getClosestFood(currentGameState,successorGameState,posX,posY)
        else:
            closestCost = getClosestFood(currentGameState,successorGameState,posX,posY)

        baseScore +=closestCost
        # print closestGhost
        # baseScore = baseScore + closestGhost
        # successorGameState.data.score = baseScore
        return baseScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

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
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.minList = [[] for i in range(self.depth)]
        # self.maxList = []

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def MaxAction(self, gameState, depth):
        if self.depth ==depth:
            return self.evaluationFunction(gameState)
        actionAgent = gameState.getLegalActions(0)
        if actionAgent == []:
            return self.evaluationFunction(gameState)
        maxList = []
        for action in actionAgent:
            nextSuccessor = gameState.generateSuccessor(0,action)
            ghostId = 1
            maxList.append(self.MinAction(nextSuccessor, ghostId, depth))
        # print maxList
        if len(maxList):
            maxScore = max(maxList)
        else:
            print "max"
            return self.evaluationFunction(gameState)
        # print "max depth:" + str(depth)
        # print maxList
        # self.maxList = []
        return maxScore
        # pass
    def MinAction(self, gameState, ghost, depth):
        if self.depth == depth:
            return self.evaluationFunction(gameState)
        if ghost <gameState.getNumAgents():
            actionGhost = gameState.getLegalActions(ghost)
            if actionGhost == []:
                return self.evaluationFunction(gameState)
            for action in actionGhost:
                nextSuccessor = gameState.generateSuccessor(ghost, action)
                # if nextSuccessor.isLose():
                #     # print "wtf"
                ghostId = ghost + 1
                self.MinAction(nextSuccessor, ghostId, depth)
        else:
            self.minList[depth].append(self.MaxAction(gameState, depth+1))
            # print self.minList

        if ghost == 1:
            # print "min depth:" + str(depth)
            # print self.minList[depth]
            if len(self.minList[depth]):
                # print "not here" + str(depth)+str(ghostId)
                minScore = min(self.minList[depth])
            else:
                print "hmm"
                return self.evaluationFunction(gameState)
            self.minList[depth] = []
            return minScore
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
        # MaxAction(gameState,)
        depth = 0
        actionAgent = gameState.getLegalActions(0)
        maxList = []
        # print gameState
        for action in actionAgent:
            nextSuccessor = gameState.generateSuccessor(0, action)
            # print nextSuccessor
            # print nextSuccessor
            ghostId = 1
            maxList.append(self.MinAction(nextSuccessor, ghostId, depth))
        maxScore = max(maxList)
        maxIndex = [index for index in range(len(maxList)) if maxList[index] == maxScore]
        chosenIndex = random.choice(maxIndex)
        # print "get action depth:"+ str(depth)

        print maxList
        # print actionAgent[chosenIndex]
        return actionAgent[chosenIndex]
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
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

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

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


