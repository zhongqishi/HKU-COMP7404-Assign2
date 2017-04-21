#Edit by SHI Zhongqi

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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()

        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        baseScore = successorGameState.getScore()
        foods = currentGameState.getFood().asList()

        minDistance=-float("inf")
        for food in foods:
            if minDistance<-manhattanDistance(food,newPos):
              minDistance=-manhattanDistance(food,newPos)

        baseScore+=minDistance

        if newPos == currentGameState.getPacmanPosition():
            baseScore=-float("inf")

        for ghostState in newGhostStates:
            if ghostState.getPosition() == newPos and ghostState.scaredTimer is 0:
                baseScore=-float("inf")
  
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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #print("targetDepth",targetDepth)
        #print("numberOfAgents",numberOfAgents)
        result=self.minMax(0,gameState,0)
        
        return result[1]
        util.raiseNotDefined()

    def minMax(self,agentID,gameState,depth):
       
        resultAction=""

        if agentID==gameState.getNumAgents():
            agentID=0
            depth+=1

        if depth==self.depth:
            return (self.evaluationFunction(gameState),0)

        if not gameState.getLegalActions(agentID):
            return (self.evaluationFunction(gameState),0)
        
        if agentID==0:
          maxValue=-float('inf')

          for action in gameState.getLegalActions(agentID):
            if action == "Stop":
                continue
            successor=gameState.generateSuccessor(agentID, action)
            tmpValue=self.minMax(agentID+1,successor,depth)
           
            if tmpValue[0]>maxValue:
              maxValue=tmpValue[0]
              resultAction=action
            
          return (maxValue,resultAction)

        else:
          minValue=float('inf')
         
          for action in gameState.getLegalActions(agentID):
            if action == "Stop":
                continue
            successor=gameState.generateSuccessor(agentID, action)
            tmpValue=self.minMax(agentID+1,successor,depth)
           
            if tmpValue[0]<minValue:
              minValue=tmpValue[0]
              resultAction=action
            
          return (minValue,resultAction)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        result=self.AlphaBeta(0,gameState,0,-float('inf'),float('inf'))
        
        return result[1]
        util.raiseNotDefined()

    def AlphaBeta(self,agentID,gameState,depth,alpha,beta):
       
        resultAction=""

        if agentID==gameState.getNumAgents():
            agentID=0
            depth+=1

        if depth==self.depth:
            return (self.evaluationFunction(gameState),0)

        if not gameState.getLegalActions(agentID):
            return (self.evaluationFunction(gameState),0)
        
        if agentID==0:
          "Max Value"
          maxValue=-float('inf')

          for action in gameState.getLegalActions(agentID):
            if action == "Stop":
                continue
            successor=gameState.generateSuccessor(agentID, action)

            tmpValue=self.AlphaBeta(agentID+1,successor,depth,alpha,beta)
                  
            if tmpValue[0]>maxValue:
              maxValue=tmpValue[0]
              resultAction=action

            if tmpValue[0]>beta:
              return (tmpValue[0],action)

            if alpha<tmpValue[0]:
              alpha=tmpValue[0]
            
          return (maxValue,resultAction)

        else:
          "Min Value"
          minValue=float('inf')
         
          for action in gameState.getLegalActions(agentID):
            if action == "Stop":
                continue
            successor=gameState.generateSuccessor(agentID, action)
            tmpValue=self.AlphaBeta(agentID+1,successor,depth,alpha,beta)
           
            if tmpValue[0]<alpha:
              return (tmpValue[0],action)

            if tmpValue[0]<minValue:
              minValue=tmpValue[0]
              resultAction=action

            if beta>tmpValue[0]:
              beta=tmpValue[0]
            
            
          return (minValue,resultAction)
        

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
        result=self.minMax(0,gameState,0)
        
        return result[1]
        util.raiseNotDefined()

    def minMax(self,agentID,gameState,depth):
       
        resultAction=""

        if agentID==gameState.getNumAgents():
            agentID=0
            depth+=1

        if depth==self.depth:
            return (self.evaluationFunction(gameState),0)

        if not gameState.getLegalActions(agentID):
            return (self.evaluationFunction(gameState),0)
        
        if agentID==0:
          maxValue=-float('inf')
          
          for action in gameState.getLegalActions(agentID):
            if action == "Stop":
                continue
            successor=gameState.generateSuccessor(agentID, action)
            tmpValue=self.minMax(agentID+1,successor,depth)
           
            if tmpValue[0]>maxValue:
              maxValue=tmpValue[0]
              resultAction=action

          return (maxValue,resultAction)

        else:
          #minValue=float('inf')
          avgValue=0
          indicator=0
          for action in gameState.getLegalActions(agentID):
            if action == "Stop":
                continue
            successor=gameState.generateSuccessor(agentID, action)
            tmpValue=self.minMax(agentID+1,successor,depth)
            indicator+=1
            avgValue+=tmpValue[0]
          
          avgValue=avgValue/indicator
          return (avgValue,0)
      

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
        The Score are consist of:
          1. BaseScore of the CurrentBoard
          2. Distance to nearest Food
          3. Distance to the ghost * 5
          4. Distance to the Scared Ghost

    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    "*** YOUR CODE HERE ***"
    baseScore = currentGameState.getScore()
    foods = currentGameState.getFood().asList()

    minDistance=-float("inf")
    for food in foods:
        if minDistance>manhattanDistance(food,pacmanPos):
          minDistance=manhattanDistance(food,pacmanPos)

    if minDistance==-float("inf"):
      minDistance=0
    baseScore+=-minDistance

    for ghostState in ghostStates:
        if ghostState.scaredTimer==0:
            baseScore+=-5*manhattanDistance(ghostState.getPosition(),pacmanPos)
        if ghostState.scaredTimer>0:
            baseScore+=-manhattanDistance(ghostState.getPosition(),pacmanPos)
      
    return baseScore

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

