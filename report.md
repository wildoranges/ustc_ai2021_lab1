# 人工智能LAB1实验报告

**PB18111757 陈金宝**

## 算法介绍

### BFS
BFS的思路与DFS类似。使用容器`Queue`来管理。使用`visited`字典记录访问到的节点和父节点。每次从队列中队首弹出节点，判断是否是目标节点。若是目标节点，则通过visited获取到目标节点的路径作为结果返回。如果该节点还未访问过，则将该节点和父节点加入visited字典中，该节点为key,父节点为value。并将该节点的孩子节点(以及作为父节点的该节点)放入队列。循环上述过程直至队列为空。

源代码:

```python
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
```

### A-star
A\*算法使用优先队列来排序。按照$f(n)=h(n)+g(n)$排序。其中$h$是启发式函数，预估到目标点的距离。$g$是到当前节点的cost。初始时初始节点$g=0，f=h$。在算法实现中，使用一个字典`cost`记录到每个节点的距离（即g(n)）。初始时字典中只有初始节点,value是0.0。在扩展节点时，使用`cost[next_state] = cost[state] + step_cost`记录该路径上下个子节点的cost。循环方式与BFS类型。每次从优先队列弹出第一个元素。判断是否是目标节点，若是则通过visited找到路径并返回。之后判断是否在visited中。若不在，则获取其所有子节点，并得到到子节点的cost，之后将子节点压入优先队列。循环上述过程，直至优先队列为空。

源代码:

```python
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
```

### Minimax
在类`MyMinimaxAgent`中增加两个函数:`maxval`,`minval`。分别负责处理max节点和min节点。对于max节点(isMe()==true)。获取其所有子节点。根据子节点是否是max节点来调用maxval或minval。并获取子节点的最大值并返回。对于minval，根据子节点是否是max节点来调用maxval或minval。并获取子节点的最小值并返回。minimax根据state是否是max来调用maxval或minval并返回结果给`getNextState`。

源代码:

```python
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
```

### Alpha-beta pruning
alpha-beta剪枝与Minimax类似，新增三个函数`maxval`、`minval`和`alphabeta`。参数$\alpha,\beta$代表已经找到的max节点最大值和min节点最小值。在遍历的过程中,`maxval`如果发现max节点当前找到的子节点的最大值大于$\beta$时，此时再遍历子节点是没有意义的，无法减少$\beta$的值。则停止遍历子节点并返回。`minval`如果发现min节点当前找到的子节点最小值小于$\alpha$,此时再遍历子节点是没有意义的,无法增大$\alpha$的值。则停止遍历子节点并返回。函数`alphabeta`负责调用`maxval`或`minval`获取结果并返回给`getNextState`

源代码:

```python
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
```

## 实验过程
实验环境:
```shell
操作系统: Linux arch 5.12.3-arch1-1 #1 SMP PREEMPT Wed, 12 May 2021 17:54:18 +0000 x86_64 GNU/Linux
工具: anaconda 4.10.1
python环境: Python 3.6.13
```
根据文档要求和要实现的算法填充要实现的四个函数。根据未PASS的case信息DEBUG。
实验过程中出现的bug：
1. A-star算法中cost初值要赋成0.0(float)，不能为0(int)。否则优先队列中可能出现乱序的情况，导致部分case fail
2. min(max)节点的子节点不一定是max(min)
3. alpha-beta剪枝中判断当前最大(小)值和$\beta(\alpha)$的关系时不能用>=(<=)要用>(<)。

## 结果分析

每次测试时将标准输出定向到文件`result.txt`，标准错误定向到文件`err.txt`中方便测试后查看
```shell
$ ./test.sh 2> err.txt 1>result.txt
```
最后`err.txt`为空，`result.txt`中所有case通过。

`result.txt`中的结果:
```
Starting on 5-24 at 15:00:17

Question q1
===========
*** PASS: test_cases/q1/graph_backtrack.test
*** 	solution:		['1:A->C', '0:C->G']
*** 	expanded_states:	['A', 'D', 'C']
*** PASS: test_cases/q1/graph_bfs_vs_dfs.test
*** 	solution:		['2:A->D', '0:D->G']
*** 	expanded_states:	['A', 'D']
*** PASS: test_cases/q1/graph_infinite.test
*** 	solution:		['0:A->B', '1:B->C', '1:C->G']
*** 	expanded_states:	['A', 'B', 'C']
*** PASS: test_cases/q1/graph_manypaths.test
*** 	solution:		['2:A->B2', '0:B2->C', '0:C->D', '2:D->E2', '0:E2->F', '0:F->G']
*** 	expanded_states:	['A', 'B2', 'C', 'D', 'E2', 'F']
*** PASS: test_cases/q1/pacman_1.test
*** 	pacman layout:		mediumMaze
*** 	solution length: 130
*** 	nodes expanded:		146

### Question q1: 4/4 ###


Finished at 15:00:17

Provisional grades
==================
Question q1: 4/4
------------------
Total: 4/4

Your grades are NOT yet registered.  To register your grades, make sure
to follow your instructor's guidelines to receive credit on your project.

[SearchAgent] using function depthFirstSearch
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 130 in 0.0 seconds
Search nodes expanded: 146
Pacman emerges victorious! Score: 380
Average Score: 380.0
Scores:        380.0
Win Rate:      1/1 (1.00)
Record:        Win
Starting on 5-24 at 15:00:19

Question q2
===========
*** PASS: test_cases/q2/graph_backtrack.test
*** 	solution:		['1:A->C', '0:C->G']
*** 	expanded_states:	['A', 'B', 'C', 'D']
*** PASS: test_cases/q2/graph_bfs_vs_dfs.test
*** 	solution:		['1:A->G']
*** 	expanded_states:	['A', 'B']
*** PASS: test_cases/q2/graph_infinite.test
*** 	solution:		['0:A->B', '1:B->C', '1:C->G']
*** 	expanded_states:	['A', 'B', 'C']
*** PASS: test_cases/q2/graph_manypaths.test
*** 	solution:		['1:A->C', '0:C->D', '1:D->F', '0:F->G']
*** 	expanded_states:	['A', 'B1', 'C', 'B2', 'D', 'E1', 'F', 'E2']
*** PASS: test_cases/q2/pacman_1.test
*** 	pacman layout:		mediumMaze
*** 	solution length: 68
*** 	nodes expanded:		269

### Question q2: 4/4 ###


Finished at 15:00:19

Provisional grades
==================
Question q2: 4/4
------------------
Total: 4/4

Your grades are NOT yet registered.  To register your grades, make sure
to follow your instructor's guidelines to receive credit on your project.

[SearchAgent] using function bfs
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 68 in 0.0 seconds
Search nodes expanded: 269
Pacman emerges victorious! Score: 442
Average Score: 442.0
Scores:        442.0
Win Rate:      1/1 (1.00)
Record:        Win
Starting on 5-24 at 15:00:21

Question q3
===========
*** PASS: test_cases/q3/astar_0.test
*** 	solution:		['Right', 'Down', 'Down']
*** 	expanded_states:	['A', 'B', 'D', 'C', 'G']
*** PASS: test_cases/q3/astar_1_graph_heuristic.test
*** 	solution:		['0', '0', '2']
*** 	expanded_states:	['S', 'A', 'D', 'C']
*** PASS: test_cases/q3/astar_2_manhattan.test
*** 	pacman layout:		mediumMaze
*** 	solution length: 68
*** 	nodes expanded:		221
*** PASS: test_cases/q3/astar_3_goalAtDequeue.test
*** 	solution:		['1:A->B', '0:B->C', '0:C->G']
*** 	expanded_states:	['A', 'B', 'C']
*** PASS: test_cases/q3/graph_backtrack.test
*** 	solution:		['1:A->C', '0:C->G']
*** 	expanded_states:	['A', 'B', 'C', 'D']
*** PASS: test_cases/q3/graph_manypaths.test
*** 	solution:		['1:A->C', '0:C->D', '1:D->F', '0:F->G']
*** 	expanded_states:	['A', 'B1', 'C', 'B2', 'D', 'E1', 'F', 'E2']

### Question q3: 4/4 ###


Finished at 15:00:21

Provisional grades
==================
Question q3: 4/4
------------------
Total: 4/4

Your grades are NOT yet registered.  To register your grades, make sure
to follow your instructor's guidelines to receive credit on your project.

[SearchAgent] using function astar and heuristic manhattanHeuristic
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 68 in 0.0 seconds
Search nodes expanded: 221
Pacman emerges victorious! Score: 442
Average Score: 442.0
Scores:        442.0
Win Rate:      1/1 (1.00)
Record:        Win
Starting on 5-24 at 15:00:22

Question q2
===========

*** PASS: test_cases/q2/0-eval-function-lose-states-1.test
*** PASS: test_cases/q2/0-eval-function-lose-states-2.test
*** PASS: test_cases/q2/0-eval-function-win-states-1.test
*** PASS: test_cases/q2/0-eval-function-win-states-2.test
*** PASS: test_cases/q2/0-lecture-6-tree.test
*** PASS: test_cases/q2/0-small-tree.test
*** PASS: test_cases/q2/1-1-minmax.test
*** PASS: test_cases/q2/1-2-minmax.test
*** PASS: test_cases/q2/1-3-minmax.test
*** PASS: test_cases/q2/1-4-minmax.test
*** PASS: test_cases/q2/1-5-minmax.test
*** PASS: test_cases/q2/1-6-minmax.test
*** PASS: test_cases/q2/1-7-minmax.test
*** PASS: test_cases/q2/1-8-minmax.test
*** PASS: test_cases/q2/2-1a-vary-depth.test
*** PASS: test_cases/q2/2-1b-vary-depth.test
*** PASS: test_cases/q2/2-2a-vary-depth.test
*** PASS: test_cases/q2/2-2b-vary-depth.test
*** PASS: test_cases/q2/2-3a-vary-depth.test
*** PASS: test_cases/q2/2-3b-vary-depth.test
*** PASS: test_cases/q2/2-4a-vary-depth.test
*** PASS: test_cases/q2/2-4b-vary-depth.test
*** PASS: test_cases/q2/2-one-ghost-3level.test
*** PASS: test_cases/q2/3-one-ghost-4level.test
*** PASS: test_cases/q2/4-two-ghosts-3level.test
*** PASS: test_cases/q2/5-two-ghosts-4level.test
*** PASS: test_cases/q2/6-tied-root.test
*** PASS: test_cases/q2/7-1a-check-depth-one-ghost.test
*** PASS: test_cases/q2/7-1b-check-depth-one-ghost.test
*** PASS: test_cases/q2/7-1c-check-depth-one-ghost.test
*** PASS: test_cases/q2/7-2a-check-depth-two-ghosts.test
*** PASS: test_cases/q2/7-2b-check-depth-two-ghosts.test
*** PASS: test_cases/q2/7-2c-check-depth-two-ghosts.test
*** Running MinimaxAgent on smallClassic 1 time(s).
Pacman died! Score: 84
Average Score: 84.0
Scores:        84.0
Win Rate:      0/1 (0.00)
Record:        Loss
*** Finished running MinimaxAgent on smallClassic after 0 seconds.
*** Won 0 out of 1 games. Average score: 84.000000 ***
*** PASS: test_cases/q2/8-pacman-game.test

### Question q2: 5/5 ###


Finished at 15:00:23

Provisional grades
==================
Question q2: 5/5
------------------
Total: 5/5

Your grades are NOT yet registered.  To register your grades, make sure
to follow your instructor's guidelines to receive credit on your project.

Starting on 5-24 at 15:00:23

Question q3
===========

*** PASS: test_cases/q3/0-eval-function-lose-states-1.test
*** PASS: test_cases/q3/0-eval-function-lose-states-2.test
*** PASS: test_cases/q3/0-eval-function-win-states-1.test
*** PASS: test_cases/q3/0-eval-function-win-states-2.test
*** PASS: test_cases/q3/0-lecture-6-tree.test
*** PASS: test_cases/q3/0-small-tree.test
*** PASS: test_cases/q3/1-1-minmax.test
*** PASS: test_cases/q3/1-2-minmax.test
*** PASS: test_cases/q3/1-3-minmax.test
*** PASS: test_cases/q3/1-4-minmax.test
*** PASS: test_cases/q3/1-5-minmax.test
*** PASS: test_cases/q3/1-6-minmax.test
*** PASS: test_cases/q3/1-7-minmax.test
*** PASS: test_cases/q3/1-8-minmax.test
*** PASS: test_cases/q3/2-1a-vary-depth.test
*** PASS: test_cases/q3/2-1b-vary-depth.test
*** PASS: test_cases/q3/2-2a-vary-depth.test
*** PASS: test_cases/q3/2-2b-vary-depth.test
*** PASS: test_cases/q3/2-3a-vary-depth.test
*** PASS: test_cases/q3/2-3b-vary-depth.test
*** PASS: test_cases/q3/2-4a-vary-depth.test
*** PASS: test_cases/q3/2-4b-vary-depth.test
*** PASS: test_cases/q3/2-one-ghost-3level.test
*** PASS: test_cases/q3/3-one-ghost-4level.test
*** PASS: test_cases/q3/4-two-ghosts-3level.test
*** PASS: test_cases/q3/5-two-ghosts-4level.test
*** PASS: test_cases/q3/6-tied-root.test
*** PASS: test_cases/q3/7-1a-check-depth-one-ghost.test
*** PASS: test_cases/q3/7-1b-check-depth-one-ghost.test
*** PASS: test_cases/q3/7-1c-check-depth-one-ghost.test
*** PASS: test_cases/q3/7-2a-check-depth-two-ghosts.test
*** PASS: test_cases/q3/7-2b-check-depth-two-ghosts.test
*** PASS: test_cases/q3/7-2c-check-depth-two-ghosts.test
*** Running AlphaBetaAgent on smallClassic 1 time(s).
Pacman died! Score: 84
Average Score: 84.0
Scores:        84.0
Win Rate:      0/1 (0.00)
Record:        Loss
*** Finished running AlphaBetaAgent on smallClassic after 0 seconds.
*** Won 0 out of 1 games. Average score: 84.000000 ***
*** PASS: test_cases/q3/8-pacman-game.test

### Question q3: 5/5 ###


Finished at 15:00:24

Provisional grades
==================
Question q3: 5/5
------------------
Total: 5/5

Your grades are NOT yet registered.  To register your grades, make sure
to follow your instructor's guidelines to receive credit on your project.

Pacman emerges victorious! Score: 1679
Average Score: 1679.0
Scores:        1679.0
Win Rate:      1/1 (1.00)
Record:        Win
```