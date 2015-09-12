# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""
import time

import util
from spade import pyxf
from game import Directions
class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"

  myXsb=  pyxf.xsb("/Users/muthukumarsuresh/Downloads/XSB/bin/xsb")
  myXsb.load('mazeeee.P')
  myXsb.load('dfs2.P')
  time.sleep(5)
  result = myXsb.query('planPath(X)')

  while(result == False):
      result = myXsb.query('planPath(X)')
  returnstr = result[0]['X']
  returnstr = returnstr[1:len(returnstr)-1]
  returnList = returnstr.split(',')
  s =Directions.SOUTH
  w = Directions.WEST
  e = Directions.EAST
  n = Directions.NORTH
  retList = []
  for element in returnList:
      if element == 's':
          retList.append(s)
      if element == 'e':
          retList.append(e)
      if element == 'w':
          retList.append(w)
      if element == 'n':
          retList.append(n)
  # returnList = returnList.reverse()
  return retList
  # util.raiseNotDefined()

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  myXsb=  pyxf.xsb("/Users/muthukumarsuresh/Downloads/XSB/bin/xsb")
  myXsb.load('mazeeee.P')
  myXsb.load('bfs2.P')
  time.sleep(5)
  result = myXsb.query('planPathbfs(X)')
  while(result == False):
      result = myXsb.query('planPathbfs(X)')
  returnstr = result[0]['X']
  returnstr = returnstr[1:len(returnstr)-1]
  returnList = returnstr.split(',')
  s =Directions.SOUTH
  w = Directions.WEST
  e = Directions.EAST
  n = Directions.NORTH
  retList = []
  for element in returnList:
      if element == 's':
          retList.append(s)
      if element == 'e':
          retList.append(e)
      if element == 'w':
          retList.append(w)
      if element == 'n':
          retList.append(n)
  # returnList = returnList.reverse()
  return retList
  # util.raiseNotDefined()
  # util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"

  myXsb=  pyxf.xsb("/Users/muthukumarsuresh/Downloads/XSB/bin/xsb")
  myXsb.load('mazeeee.P')

  myXsb.load('heuristic.P')

  myXsb.load('astar.P')
  time.sleep(5)
  result = myXsb.query('planPathbfs(X)')

  if result is False:
      print(result)
      result = myXsb.query('planPathbfs(X)')
  print("hello", result)
  returnstr = result[0]['X']
  returnstr = returnstr[1:len(returnstr)-1]
  returnList = returnstr.split(',')
  s =Directions.SOUTH
  w = Directions.WEST
  e = Directions.EAST
  n = Directions.NORTH
  retList = []
  for element in returnList:
      if element == 's':
          retList.append(s)
      if element == 'e':
          retList.append(e)
      if element == 'w':
          retList.append(w)
      if element == 'n':
          retList.append(n)
  print retList
  # returnList = returnList.reverse()
  return retList
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch