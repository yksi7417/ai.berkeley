# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
import sys
import itertools


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
        x,y = newPos

        import searchAgents, search
        problem = searchAgents.AnyFoodSearchProblem(successorGameState)
        closestFoodPath = search.bfs(problem)

        ## logic to run towards food
        foodScore = 0
        if currentGameState.getFood()[x][y]:
            foodScore = 10

        ## logic to run away from ghost
        ghostScore = 0
        radar = 3
        for gs in newGhostStates:
            g_x, g_y = gs.getPosition()
            distance = abs(x-g_x) + abs(y-g_y)
            if (distance < radar):
                ghostScore = ghostScore - (radar - distance)

        if (ghostScore != 0):
            return 100 * ghostScore
        elif (foodScore != 0):
            return foodScore
        else:
            return - len(closestFoodPath)

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

    def getMaxScore(self, currentGameState, currentDepth, pathSoFar):
        if currentDepth  == self.depth or currentGameState.isWin() or currentGameState.isLose():
            return self.evaluationFunction(currentGameState), pathSoFar
        maxScore = -sys.maxint
        finalPath = None
        for action in currentGameState.getLegalActions():
            successorState = currentGameState.generateSuccessor(0, action)
            scoreSoFar, thisPath= self.getMinScore(successorState, currentDepth, pathSoFar + [action])
            if (scoreSoFar > maxScore):
                maxScore = scoreSoFar
                finalPath = thisPath
        return maxScore, finalPath

    def expandGhostSuccessors(self, gameState, intermediateSuccessor, remainingIndex):
        if (len(remainingIndex) == 0):
            return []

        if (intermediateSuccessor.isWin() or intermediateSuccessor.isLose()):
            return [intermediateSuccessor]

        if (len(remainingIndex) == 1):
            successors = []
            idx = remainingIndex[0]
            for action in intermediateSuccessor.getLegalActions(idx):
                nextSuccessor = intermediateSuccessor.generateSuccessor(idx, action)
                successors = successors + [ nextSuccessor ]
            return successors

        successors = []
        idx = remainingIndex[0]
        whatsLeft = remainingIndex[1:]
        legalActions = intermediateSuccessor.getLegalActions(idx)
        for action in legalActions:
            nextSuccessor = intermediateSuccessor.generateSuccessor(idx, action)
            successors += self.expandGhostSuccessors(gameState, nextSuccessor, whatsLeft )
        return successors

    def getMinScore(self, currentGameState, currentDepth, pathSoFar):
        if currentGameState.isWin() or currentGameState.isLose():
            return self.evaluationFunction(currentGameState), pathSoFar
        minScore = sys.maxint
        finalPath = None

        listOfGhosts = list(xrange(1, currentGameState.getNumAgents() ))
        ghostSuccessors = self.expandGhostSuccessors(currentGameState, currentGameState, listOfGhosts)
        for ghostSuccessor in ghostSuccessors:
            scoreSoFar, thisPath  = self.getMaxScore(ghostSuccessor, currentDepth+1, pathSoFar)
            if scoreSoFar < minScore:
                minScore = scoreSoFar
                finalPath = thisPath
        return minScore, finalPath

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
        """
        score, path = self.getMaxScore(gameState, 0, [])
        return path[0]

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

