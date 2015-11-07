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
        #chosenIndex = max (bestIndices)
        #print bestIndices
        #print scores
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
        newGhostPos = successorGameState.getGhostPosition(1)
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #print newPos
        #print newFood
        #print newScaredTimes
        #print newGhostStates

        nearFood = 1
        farFood = 1

        s = successorGameState.getScore()
        if newFood.asList():
            nearFood = min([util.manhattanDistance(newPos, food) for food in newFood.asList()])
            farFood = max([util.manhattanDistance(newPos, food) for food in newFood.asList()])
        ghostPos = successorGameState.getGhostPositions()

        nearGhost = min ([util.manhattanDistance(newPos, g) for g in ghostPos])
        farGhost = max([util.manhattanDistance(newPos, g) for g in ghostPos])

        scaredTime = min(newScaredTimes)

        if nearGhost < 2 and scaredTime == 0:
            s -= 7000
        # elif nearGhost < 5:
        #     s -= 10
        else:
            if nearFood < nearGhost:
                s = s + 5000
                if farFood < nearGhost:
                    s+= 7000
                if nearFood + farFood < nearGhost:
                    s += 8000
                else:
                    s -= 1000
            else:
                s -= nearGhost * 1000



        if nearFood == farFood and ghostPos > 5:
            s += 7000

        if nearFood == farFood:
            s+= 2000

        # if powerpellet location is closer than ghost, higher point.
        # if in scaredtimes nearghost higher point


        if successorGameState.isLose():
            s -= 10000

        if successorGameState.isWin():
            s = s + 10000


        if scaredTime > 0 and scaredTime < 40:
            s += 5000
            if farFood < scaredTime:
                s += 3000
            elif nearFood < scaredTime:
                s += 2000
            else:
                s+= nearGhost * 100
            if nearFood == farFood and scaredTime >= nearFood:
                s += 7000
            if nearFood == farFood:
                s += 2000

        if action == Directions.STOP and ghostPos > 5:
            s -= 3000

        return s

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


        self.nextAgent = 0
        self.count = 1
        self.iter = 1

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

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
        states = []
        actions = []
        v = []

        def maxvalue(state, agent, depth):
            v = -99999
            #print "agent:" + str(agent)
            for action in state.getLegalActions(0):
                val = minimax(state.generateSuccessor(0,action), 1, depth)
                v = max(v, val)
            return v


        def minvalue(state, agent, depth):
            v = 99999
            #print "agent:" + str(agent)
            for action in state.getLegalActions(agent):
                if agent < state.getNumAgents() - 1:
                    #val = minimax(state.generateSuccessor(agent,action), agent + 1, depth)
                    v = min (v, minimax(state.generateSuccessor(agent,action), agent + 1, depth))
                else:
                    #val = minimax(state.generateSuccessor(agent,action), 0, depth + 1)
                    v = min (v, minimax(state.generateSuccessor(agent,action), 0, depth + 1))
            return v


        def minimax (state, agent, depth):
            #print "depth: " + str(depth)
            if self.depth == depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agent > state.getNumAgents() - 1 and depth > 0:
                agent = 0
            if agent == 0: return maxvalue(state, agent, depth)
            if agent in range (1, state.getNumAgents()): return minvalue(state, agent, depth)


        for action in gameState.getLegalActions(0):
            actions.append(action)
            states.append(gameState.generateSuccessor(0, action))

        for state in states:
            v.append(minimax(state, 1, 0))

        #print actions
        #print v
        return actions[v.index(max(v))]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        states = []
        actions = []
        v = []
        alpha = -99999
        beta = 99999

        def alphabetaprune (state, agent, depth, alpha, beta):
            #print "depth: " + str(depth)
            #print alpha, beta
            if self.depth == depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agent > state.getNumAgents() - 1 and depth > 0:
                agent = 0
            if agent == 0:
                t = -99999.0
                #print "agent:" + str(agent)
                for action in state.getLegalActions(0):
                    val = alphabetaprune(state.generateSuccessor(0, action), 1, depth, alpha, beta)
                    t = max(t, val)
                    if t > beta:
                        return t
                    alpha = max(t, alpha)
                return t

            if agent in range (1, state.getNumAgents()):
                t = 99999.0
                #print "agent:" + str(agent)
                for action in state.getLegalActions(agent):
                    if agent < state.getNumAgents() - 1:
                        #val = minimax(state.generateSuccessor(agent,action), agent + 1, depth)
                        t = min (t, alphabetaprune(state.generateSuccessor(agent,action), agent + 1, depth, alpha, beta))
                        if t < alpha:
                            return t
                        beta = min (beta, t)
                    else:
                        #val = minimax(state.generateSuccessor(agent,action), 0, depth + 1)
                        t = min (t, alphabetaprune(state.generateSuccessor(agent,action), 0, depth + 1, alpha, beta))
                        if t < alpha:
                            return t
                        beta = min (beta, t)
                return t



        r = -99999
        for action in gameState.getLegalActions(0):
            actions.append(action)
            states.append(gameState.generateSuccessor(0, action))
            r = alphabetaprune(gameState.generateSuccessor(0, action), 1, 0, alpha, beta)
            if r > beta:
                break
            alpha = max(r, alpha)
            v.append(r)





        #print actions
        #print v
        return actions[v.index(max(v))]

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

        states = []
        actions = []
        v = []

        def maxvalue(state, agent, depth):
            v = -99999
            #print "agent:" + str(agent)
            for action in state.getLegalActions(0):
                val = expectimax(state.generateSuccessor(0, action), 1, depth)
                v = max(v, val)
            return v


        def expectvalue(state, agent, depth):
            v = 0.0
            c = 0.0
            #print "agent:" + str(agent)
            for action in state.getLegalActions(agent):
                c += 1.0
                if agent < state.getNumAgents() - 1:
                    #val = minimax(state.generateSuccessor(agent,action), agent + 1, depth)
                    v += expectimax(state.generateSuccessor(agent,action), agent + 1, depth)
                else:
                    #val = minimax(state.generateSuccessor(agent,action), 0, depth + 1)
                    v += expectimax(state.generateSuccessor(agent,action), 0, depth + 1)
            #print v, c
            return v/c


        def expectimax (state, agent, depth):
            #print "depth: " + str(depth)
            if self.depth == depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agent > state.getNumAgents() - 1 and depth > 0:
                agent = 0
            if agent == 0: return maxvalue(state, agent, depth)
            if agent in range (1, state.getNumAgents()): return expectvalue(state, agent, depth)


        for action in gameState.getLegalActions(0):
            actions.append(action)
            states.append(gameState.generateSuccessor(0, action))

        for state in states:
            v.append(expectimax(state, 1, 0))

        #print actions
        #print v
        return actions[v.index(max(v))]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """

    newPos = currentGameState.getPacmanPosition()
    newGhostPos = currentGameState.getGhostPosition(1)
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


    "*** YOUR CODE HERE ***"
    nearFood = 1
    farFood = 1

    s = currentGameState.getScore()
    if newFood.asList():
        nearFood = min([util.manhattanDistance(newPos, food) for food in newFood.asList()])
        farFood = max([util.manhattanDistance(newPos, food) for food in newFood.asList()])

    ghostPos = currentGameState.getGhostPositions()

    nearGhost = min ([util.manhattanDistance(newPos, g) for g in ghostPos])
    farGhost = max([util.manhattanDistance(newPos, g) for g in ghostPos])
    scaredTime = min(newScaredTimes)


    if nearGhost < 1 and scaredTime == 0:
        s -= 1000
    # elif nearGhost < 5:
    #     s -= 10
    else:
        if nearFood < nearGhost:
            s = s + 1000
            if farFood < nearGhost:
                s += 1000
        else:
            s -= nearGhost * 100

    if farFood + nearFood <= nearGhost and scaredTime == 0:
        s+= 2000

    if nearFood == farFood and nearGhost >= nearFood and scaredTime == 0:
        s+= 1500
    elif nearFood == farFood and nearGhost > 3 and scaredTime == 0:
        s+= 1000
    elif nearFood == farFood and scaredTime == 0:
        s+= 300 * nearFood


    if currentGameState.isLose():
        s -= 2000

    if currentGameState.isWin():
        s = s + 3000

    if currentGameState.getLegalActions() > 2:
        s += 1000
    else:
        s -= 1000


    if scaredTime > 0 and scaredTime <= 40:
            s += 2000 * scaredTime
            if farFood <= scaredTime:
                s += 500
            if nearFood <= scaredTime:
                s += 500

            if nearFood + farFood <= scaredTime:
                s += 500

            if nearFood == farFood and scaredTime >= nearFood:
                s += 500
            if nearFood == farFood:
                s += 200
            if nearGhost < scaredTime:
                s+= 1000

    return s


# Abbreviation
better = betterEvaluationFunction

