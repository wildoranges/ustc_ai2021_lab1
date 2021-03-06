import util

"""
Data sturctures we will use are stack, queue and priority queue.

Stack: first in last out
Queue: first in first out
    collection.push(element): insert element
    element = collection.pop() get and remove element from collection

Priority queue:
    pq.update('eat', 2)
    pq.update('study', 1)
    pq.update('sleep', 3)
pq.pop() will return 'study' because it has highest priority 1.

"""

"""
problem is a object has 3 methods related to search state:

problem.getStartState()
Returns the start state for the search problem.

problem.isGoalState(state)
Returns True if and only if the state is a valid goal state.

problem.getChildren(state)
For a given state, this should return a list of tuples, (next_state,
step_cost), where 'next_state' is a child to the current state, 
and 'step_cost' is the incremental cost of expanding to that child.

"""
def myDepthFirstSearch(problem):
    visited = {}
    frontier = util.Stack()

    frontier.push((problem.getStartState(), None))

    while not frontier.isEmpty():
        state, prev_state = frontier.pop()

        if problem.isGoalState(state):
            solution = [state]
            while prev_state != None:
                solution.append(prev_state)
                prev_state = visited[prev_state]
            return solution[::-1]                
        
        if state not in visited:
            visited[state] = prev_state

            for next_state, step_cost in problem.getChildren(state):
                frontier.push((next_state, state))

    return []

def myBreadthFirstSearch(problem):
    visited = {}
    queue = util.Queue()

    queue.push((problem.getStartState(), None))

    while not queue.isEmpty():
        state, prev_state = queue.pop()

        if problem.isGoalState(state):
            solution = [state]
            while prev_state != None:
                solution.append(prev_state)
                prev_state = visited[prev_state]
            return solution[::-1]

        if state not in visited:
            visited[state] = prev_state

            for next_state, step_cost in problem.getChildren(state):
                queue.push((next_state, state))

    return []

def myAStarSearch(problem, heuristic):
    visited = {}
    cost = {}
    pq = util.PriorityQueue()
    st = problem.getStartState()
    cost[st] = 0.0
    pq.push((st,None),heuristic(st))
    
    while not pq.isEmpty():
        state,prev_state = pq.pop()

        if problem.isGoalState(state):
            solution = [state]
            while prev_state != None:
                solution.append(prev_state)
                prev_state = visited[prev_state]
            return solution[::-1]

        if state not in visited:
            visited[state] = prev_state

            for next_state,step_cost in problem.getChildren(state):
                cost[next_state] = cost[state] + step_cost
                pq.push((next_state, state),heuristic(next_state)+cost[next_state])
    
    return []

"""
Game state has 4 methods we can use.

state.isTerminated()
Return True if the state is terminated. We should not continue to search if the state is terminated.

state.isMe()
Return True if it's time for the desired agent to take action. We should check this function to determine whether an agent should maximum or minimum the score.

state.getChildren()
Returns a list of legal state after an agent takes an action.

state.evaluateScore()
Return the score of the state. We should maximum the score for the desired agent.

"""
class MyMinimaxAgent():

    def __init__(self, depth):
        self.depth = depth

    def minimax(self, state, depth):
        if state.isTerminated():
            return None, state.evaluateScore()        
        if state.isMe():
            best_state,best_score = self.maxval(state,0)
            return best_state,best_score
        else:
            best_state,best_score = self.minval(state,0)
            return best_state,best_score

    def maxval(self,state,depth):
        if state.isTerminated():
            return None,state.evaluateScore() 
        
        if depth >= self.depth:
            return state,state.evaluateScore() 

        best_state,best_score = None,-float('inf')

        for child in state.getChildren():
            if child.isMe():
                _,score = self.maxval(child,depth+1)
                if score > best_score:
                    best_state = child
                    best_score = score
            else:
                _,score = self.minval(child,depth)
                if score > best_score:
                    best_state = child
                    best_score = score
        
        return best_state,best_score


    def minval(self,state,depth):
        if state.isTerminated():
            return None,state.evaluateScore()

        best_state,best_score = None,float('inf')

        for child in state.getChildren():
            if child.isMe():
                _,score = self.maxval(child,depth+1)
                if score < best_score:
                    best_state = child
                    best_score = score
            else:
                _,score = self.minval(child,depth)
                if score < best_score:
                    best_state = child
                    best_score = score
        
        return best_state,best_score

    def getNextState(self, state):
        best_state, _ = self.minimax(state, self.depth)
        return best_state

class MyAlphaBetaAgent():

    def __init__(self, depth):
        self.depth = depth

    def alphabeta(self,state,depth):
        if state.isTerminated():
            return None, state.evaluateScore() 

        if state.isMe():
            best_state,best_score = self.maxval(state,0,-float('inf'),float('inf'))
            return best_state,best_score
        else:
            best_state,best_score = self.minval(state,0,-float('inf'),float('inf'))
            return best_state,best_score
        

    def maxval(self,state,depth,a,b):
        if state.isTerminated():
            return None,state.evaluateScore() 
        
        if depth >= self.depth:
            return state,state.evaluateScore()

        best_state,best_score = None,-float('inf')
        for child in state.getChildren():
            if child.isMe():
                _,score = self.maxval(child,depth+1,a,b)
                if score > best_score:
                    best_score = score
                    best_state = child
                if best_score > b:
                    return best_state,best_score
                a = max(a,best_score)
            else:
                _,score = self.minval(child,depth,a,b)
                if score > best_score:
                    best_score = score
                    best_state = child
                if best_score > b:
                    return best_state,best_score
                a = max(a,best_score)
        
        return best_state,best_score

    def minval(self,state,depth,a,b):
        if state.isTerminated():
            return None,state.evaluateScore()

        best_state,best_score = None,float('inf')
        for child in state.getChildren():
            if child.isMe():
                _,score = self.maxval(child,depth+1,a,b)
                if score < best_score:
                    best_score = score
                    best_state = child
                if best_score < a:
                    return best_state,best_score
                b = min(b,best_score)
            else:
                _,score = self.minval(child,depth,a,b)
                if score < best_score:
                    best_score = score
                    best_state = child
                if best_score < a:
                    return best_state,best_score
                b = min(b,best_score)

        return best_state,best_score

    def getNextState(self, state):
        best_state, _ = self.alphabeta(state,self.depth)
        return best_state
