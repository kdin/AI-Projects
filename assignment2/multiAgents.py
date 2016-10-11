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



      # if depth == self.depth or len(gameState.getLegalActions(agentIndex)) == 0:
      #   print "DEPTH =", depth
      #   if depth == self.depth:
      #     print "DEPTH REACHED"
      #   if len(gameState.getLegalActions(agentIndex)) == 0:
      #     print "TERMINAL STATE"
      #   return (self.evaluationFunction(gameState), bestAction)

      if gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState), bestAction)


      value = 100000

      actionList = gameState.getLegalActions(agentIndex)

      for action in actionList:
        prevValue = value
        if agentIndex == gameState.getNumAgents() - 1:
          toMax = self.maximizer(gameState.generateSuccessor(agentIndex, action), 0, depth)
          value = min(value, toMax[0])
        else:
          toMin = self.minimizer(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth)
          value = min(value, toMin[0])

        if prevValue > value:
          bestAction = action





      # print "(VALUE, BESTACTION)", (value, bestAction)
      return (value, bestAction)



    def maximizer(self, gameState, agentIndex, depth):

      bestAction = ''
      # depth -= 1
      # print "DEPTH-", depth
      if depth == self.depth or gameState.isWin() or gameState.isLose():

        evalVal = self.evaluationFunction(gameState)
        # print "EVAL-VAL", evalVal
        return (evalVal, bestAction)


      value = -100000
      actionList = gameState.getLegalActions(agentIndex)   

      for action in actionList:
        prevValue = value
        toMin = self.minimizer(gameState.generateSuccessor(agentIndex, action), 1, depth + 1)
        value = max(value, toMin[0])
        # print "MAXIMIZER-ACTION", action, "VALUE:", value, "OBTAINED:", toMin[0]
        
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

        # print "NUM-AGENTS:", gameState.getNumAgents(), "DEPTH:", self.depth
        # return gameState.getLegalActions(0)[0]
        return self.maximizer(gameState, 0, 0)[1]     

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def minimizer(self, gameState, agentIndex, depth, alpha, beta):

      bestAction = ''

      if gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState), bestAction)


      value = 100000

      actionList = gameState.getLegalActions(agentIndex)

      for action in actionList:
        prevValue = value
        if agentIndex == gameState.getNumAgents() - 1:
          toMax = self.maximizer(gameState.generateSuccessor(agentIndex, action), 0, depth, alpha, beta)
          value = min(value, toMax[0])
        else:
          toMin = self.minimizer(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth, alpha, beta)
          value = min(value, toMin[0])

        if prevValue > value:
          bestAction = action

        if value < alpha:
          return (value, bestAction)

        beta = min (beta, value)

      return (value, bestAction)



    def maximizer(self, gameState, agentIndex, depth, alpha, beta):

      bestAction = ''
      # depth -= 1
      # print "DEPTH-", depth
      if depth == self.depth or gameState.isWin() or gameState.isLose():

        evalVal = self.evaluationFunction(gameState)
        # print "EVAL-VAL", evalVal
        return (evalVal, bestAction)


      value = -100000
      actionList = gameState.getLegalActions(agentIndex)   

      for action in actionList:
        prevValue = value
        toMin = self.minimizer(gameState.generateSuccessor(agentIndex, action), 1, depth + 1, alpha, beta)
        value = max(value, toMin[0])
        # print "MAXIMIZER-ACTION", action, "VALUE:", value, "OBTAINED:", toMin[0]
        
        if value > prevValue:
          bestAction = action

        if value > beta:
          return (value, bestAction)

        alpha = max(alpha, value)


      return (value, bestAction)
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -1000000
        beta = 1000000
        return self.maximizer(gameState, 0, 0, alpha, beta)[1] 
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def minimizer(self, gameState, agentIndex, depth):

      bestAction = ''

      if gameState.isWin() or gameState.isLose():
        return (float(self.evaluationFunction(gameState)), bestAction)


      # value = 100000

      actionList = gameState.getLegalActions(agentIndex)

      if len(actionList) != 0:
        weight = float (1)/ float(len(actionList))
      expectimax_value = float(0)


      for action in actionList:

        if agentIndex == gameState.getNumAgents() - 1:
          toMax = self.maximizer(gameState.generateSuccessor(agentIndex, action), 0, depth)
          expectimax_value += (float(toMax[0])* weight)
        else:
          toMin = self.minimizer(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth)
          expectimax_value += (float(toMin[0])* weight)

      expectimax_value = (expectimax_value) / float(len(actionList))
      return (expectimax_value, " ")



    def maximizer(self, gameState, agentIndex, depth):

      bestAction = ''

      if depth == self.depth or gameState.isWin() or gameState.isLose():

        evalVal = float(self.evaluationFunction(gameState))
        return (evalVal, bestAction)


      value = float(-999999999)
      actionList = gameState.getLegalActions(agentIndex)   
      debugList = []
      for action in actionList:
        prevValue = value
        toMin = self.minimizer(gameState.generateSuccessor(agentIndex, action), 1, depth + 1)
        value = max(value, toMin[0])
        debugList.append((value,action))
        if value > prevValue:
          bestAction = action


      if bestAction == 'Stop':
        equalityList = filter(lambda pair: pair[0] != value,debugList)

        if len(equalityList) != 0:
          pairsList = filter(lambda pair:pair[1] != 'Stop',debugList)
          bestAction = filter(lambda pair:pair[0]==value,pairsList)[-1][1]
          
        if bestAction == 'East':
          print "DEBUG-LIST", debugList
      # print "DEBUG-LIST", debugList, "BEST-ACTION", bestAction

      return (value, bestAction)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        return self.maximizer(gameState, 0, 0)[1] 
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

