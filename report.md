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
A\*算法使用优先队列来排序。按照$f(n)=h(n)+g(n)$排序。期中$h$启发式函数，预估到目标点的距离。$g$是到当前节点的cost。初始时初始节点$g=0，f=h$。在算法实现中，使用一个字典`cost`记录到每个节点的距离（即g(n)）。初始时字典中只有初始节点,value是0.0。在扩展节点时，使用`cost[next_state] = cost[state] + step_cost`记录该路径上下个子节点的cost。循环方式与BFS类型。每次从优先队列弹出第一个元素。判断是否是目标节点，若是则通过visited找到路径并返回。之后判断是否在visited中。若不在，则获取其所有子节点，并得到到子节点的cost，之后将子节点压入优先队列。循环上述过程，直至优先队列为空。

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
`result.txt`中部分结果:

![](./media/1.png)