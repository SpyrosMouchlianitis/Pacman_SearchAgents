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
from collections import defaultdict

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getInitialState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isFinalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getNextStates(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getActionCost(self, actions):
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
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of steps that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """

    graph = util.Stack()
    visited = []
    startState = problem.getInitialState()
    startNode = (startState, [], 0)

    graph.enqueue(startNode)

    while not graph.isEmpty():
        currentState, steps, cost = graph.dequeue()

        if problem.isFinalState(currentState):
            return steps

        if currentState not in visited:
            visited.append(currentState)

            nextStates = problem.getNextStates(currentState)

            for nextState, nextStep, nextCost in nextStates:
                newCost = cost + nextCost
                newStep = steps + [nextStep]
                newNode = (nextState, newStep, newCost)
                graph.enqueue(newNode)

    return steps


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    graph = util.Queue()
    visitedNodes = []
    startState = problem.getInitialState()
    startNode = (startState, [], 0)

    graph.enqueue(startNode)

    while not graph.isEmpty():
        currentState, actions, cost = graph.dequeue()

        if currentState not in visitedNodes:
            visitedNodes.append(currentState)

            if problem.isFinalState(currentState):
                return actions
            else:
                successors = problem.getNextStates(currentState)

                for nextState, nextAction, nextCost in successors:
                    newAction = actions + [nextAction]
                    newCost = cost + nextCost
                    newNode = (nextState, newAction, newCost)

                    graph.enqueue(newNode)

    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    graph = util.PriorityQueue()
    visited = {}
    startState = problem.getInitialState()
    startNode = (startState, [], 0)

    graph.enqueue(startNode, 0)

    while not graph.isEmpty():
        currentState, actions, cost = graph.dequeue()

        if (currentState not in visited) or (cost < visited[currentState]):
            visited[currentState] = cost

            if problem.isFinalState(currentState):
                return actions
            else:
                nextStates = problem.getNextStates(currentState)

                for nextState, nextAction, nextCost in nextStates:
                    newAction = actions + [nextAction]
                    newCost = cost + nextCost
                    newNode = (nextState, newAction, newCost)

                    graph.enqueue(newNode, newCost)

    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    graph = util.PriorityQueue()
    visitedNodes = []

    startState = problem.getInitialState()
    startNode = (startState, [], 0)

    graph.enqueue(startNode, 0)

    while not graph.isEmpty():
        currentState, actions, currentCost = graph.dequeue()

        currentNode = (currentState, actions, currentCost)

        if problem.isFinalState(currentState):
            return actions
        else:
            nextStates = problem.getNextStates(currentState)

            for nextState, nextAction, nextCost in nextStates:
                newAction = actions + [nextAction]
                newCost = currentCost + nextCost
                newNode = (nextState, newAction, newCost)

                alreadyVisited = False
                for visited in visitedNodes:
                    visitedState, visitedAction, visitedCost = visited

                    if (nextState == visitedState) and (newCost >= visitedCost):
                        alreadyVisited = True

                if not alreadyVisited:
                    graph.enqueue(newNode, newCost + heuristic(nextState, problem))
                    visitedNodes.append(newNode)

    return actions





# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
