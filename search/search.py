# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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

def depthFirstSearch(problem):
    return genericSearch(problem, util.Stack())

def genericSearch(problem, fringe):
    fringe.push((problem.getStartState(), []))
    expandedNodes = []
    while not fringe.isEmpty():
        leafNode = fringe.pop()
        current_state = leafNode[0]
        path_to_current_state = leafNode[1]
        if problem.isGoalState(current_state):
            return path_to_current_state
        else:
            if current_state not in expandedNodes:
                for node in expand_node(problem, leafNode):
                    fringe.push(node)
                expandedNodes.append(current_state)
    return []

def genericCostSearch(problem, fringe):
    fringe.push((problem.getStartState(), [], 0), 0)
    expandedNodes = []
    while not fringe.isEmpty():
        leafNode = fringe.pop()
        current_state = leafNode[0]
        path_to_current_state = leafNode[1]
        aggregate_cost = leafNode[2]
        if problem.isGoalState(current_state):
            return path_to_current_state
        else:
            if current_state not in expandedNodes:
                for node in expand_node(problem, leafNode, aggregate_cost):
                    fringe.push(node, node[2])
                expandedNodes.append(current_state)
    return []

def expand_node(problem, leafNode, aggregate_cost):
    current_state = leafNode[0]
    path_to_current_state = leafNode[1]
    result = []
    successors = problem.getSuccessors(current_state)
    for successor in successors:
        next_state = successor[0]
        direction = successor[1]
        step_cost= successor[2]
        result += [(next_state, path_to_current_state+ [direction], aggregate_cost + step_cost)]
    return result

def breadthFirstSearch(problem):
    return genericSearch(problem, util.Queue())

def uniformCostSearch(problem):
    return genericCostSearch(problem, util.PriorityQueue())

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    fringe = util.PriorityQueue();
    fringe.push((problem.getStartState(), [], 0), 0)
    expandedNodes = []
    while not fringe.isEmpty():
        leafNode = fringe.pop()
        current_state = leafNode[0]
        path_to_current_state = leafNode[1]
        aggregate_cost = leafNode[2]
        if problem.isGoalState(current_state):
            return path_to_current_state
        else:
            if current_state not in expandedNodes:
                for node in expand_node(problem, leafNode, aggregate_cost):
                    next_state = node[0]
                    h_cost = heuristic(next_state, problem)
                    fringe.push(node, node[2] + h_cost)
                expandedNodes.append(current_state)
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
