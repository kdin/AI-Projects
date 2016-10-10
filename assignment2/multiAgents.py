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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def getManhattanDistance(self, pos1, pos2):
      return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        successorScore = successorGameState.getScore()
        

        manhattanList = map(lambda pos : self.getManhattanDistance(newPos, pos), newFood.asList())

        if len(manhattanList) == 0:
          foodVec = 0
        else:
          foodVec = (1/min(manhattanList))

        

        ghostPositions = successorGameState.getGhostPositions()

        ghostPosVec = 0
        for ghostPosition in ghostPositions:
          ghostPosVec += self.getManhattanDistance(newPos, ghostPosition)

                
        ghostWeight = 1
        foodWeight = 1
        scoreWeight = - (successorScore - currentGameState.getScore()) * 1.25

        return (ghostWeight * ghostPosVec) + (foodWeight * foodVec) + (scoreWeight * successorScore)

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def minimizer(self, gameState, agentIndex, depth):

      bestAction = ''
      # depth -= 1
      # if depth == 1:
      #   return self.evaluationFunction(gameState)

      value = 100000
      
      for x in range(1, gameState.getNumAgents()):
        actionList = gameState.getLegalActions(x)

        for action in actionList:
          prevValue = value
          if x == gameState.getNumAgents() - 1:
            toMax = self.maximizer(gameState.generateSuccessor(x, action), 0, depth)
            print "MINIMIZER-ACTION", action, "VALUE:", value, "OBTAINED:", toMax[0]
            value = min(value, toMax[0])

            if prevValue > value:
              
              bestAction = action
          else:
            toMin = self.minimizer(gameState.generateSuccessor(x, action), x, depth)
            value = min(value, toMin[0])



      print "(VALUE, BESTACTION)", (value, bestAction)
      return (value, bestAction)



    def maximizer(self, gameState, agentIndex, depth):

      bestAction = ''
      depth -= 1
      if depth == 1:
        evalVal = self.evaluationFunction(gameState)
        print "EVAL-VAL", evalVal
        return (evalVal, bestAction)


      value = -100000
      actionList = gameState.getLegalActions(agentIndex)   

      for action in actionList:
        prevValue = value
        toMin = self.minimizer(gameState.generateSuccessor(agentIndex, action), agentIndex, depth)
        value = max(value, toMin[0])
        print "MAXIMIZER-ACTION", action, "VALUE:", value, "OBTAINED:", toMin[0]
        
        if value > prevValue:
          bestAction = action

      return (value, bestAction)



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
        "*** YOUR CODE HERE ***"

        # print "NUM-AGENTS", gameState.getNumAgents()
        
        return self.maximizer(gameState, 0, self.depth + 1)[1]     

        util.raiseNotDefined()

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

