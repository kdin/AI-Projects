# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]





def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def genericSearch(problem, fringe, heuristic=nullHeuristic):
    """ Implementation of a generic search
            - starts from a state
            - Expands nodes and puts into fringe
            - picks up from the fringe and does goal test
            - If goal, stop. If not, continue"""

    

    startState = problem.getStartState()
    # print "STARTSTATE::", startState
    # print "SUCCESSORS", problem.getSuccessors(startState)
    # print "SUCCESSORS", problem.getSuccessors(problem.getSuccessors(startState)[1][0])
    # print "igs", problem.isGoalState(problem.getSuccessors(startState)[0])
    pathFringe = fringe.__class__()
    path = ["START"]
    


    startState = [startState, "STOP", 0]
    if fringe.__class__ == util.PriorityQueue:
        fringe.push(startState, 0)   
        pathFringe.push((path, 0), 0)
    else:
        fringe.push(startState)
        pathFringe.push(path)
    
    exploredStates = []

    treeDict = {}
    treeDict[startState[0]] = []
    treeDict[startState[0]].append("STOP")

    expandedOrder = []
    inTheFringe = []
    inTheFringe.append(startState[0])

    
    
    while  (not fringe.isEmpty()):
        # print "INSIDE WHILE"
        nextState = fringe.pop()
        pathFringeState = pathFringe.pop()
        # print type(pathFringeState)
        # print pathFringeState
        expandedOrder.append(nextState[0])
        # print "NEXT STATE::", nextState

        if (nextState[0]) not in exploredStates:
            if problem.isGoalState(nextState[0]):
                if fringe.__class__ == util.PriorityQueue:
                    return pathFringeState[0][1:]
                else:
                    return pathFringeState[1:]
                # print "THIS HAS REACHED HERE"
                break
            # print "Now here"
            # successors = filter(lambda successor:successor[0] not in inTheFringe, problem.getSuccessors(nextState[0]))
            successors = problem.getSuccessors(nextState[0])
            
            
            exploredStates.append(nextState[0])
            
            for successor in successors:

                

                if fringe.__class__ == util.PriorityQueue:
                    toPath = []
                    toPath += pathFringeState[0]
                    toPath.append(successor[1])
                    pathCost = pathFringeState[1] + successor[2]
                    fringe.push(successor, pathCost+heuristic(successor[0], problem))    
                    pathFringe.push((toPath, pathCost), pathCost+heuristic(successor[0], problem))
                else:
                    toPath = []
                    toPath += pathFringeState
                    toPath.append(successor[1])
                    fringe.push(successor)
                    pathFringe.push(toPath)

                if successor[0] not in treeDict:
                    treeDict[successor[0]] = []
                    treeDict[successor[0]] += treeDict[nextState[0]]
                    treeDict[successor[0]].append(successor[1])




                # print treeDict[successor[0]]
        
    
    # print "PATH 2::", treeDict[nextState[0]][1:]
    # print "INCLUDED ORDER", includedOrder
    # print "EXPANDED ORDER", expandedOrder
    return treeDict[nextState[0]][1:]#["South","South","South","West","West","North","West","West"]   



        


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
    
    return genericSearch(problem, util.Stack())
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    return genericSearch(problem, util.Queue())
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    return genericSearch(problem, util.PriorityQueue())
    util.raiseNotDefined()


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    return genericSearch(problem, util.PriorityQueue(), heuristic)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
