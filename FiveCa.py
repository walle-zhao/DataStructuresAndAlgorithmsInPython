class StackUnderflow(ValueError):
    pass


"""
用顺序表实现的栈结构。
可以在一大段存储里，连续存储元素，易于管理。但是会有替换存储的成本。
"""
class SStack:
    def __init__(self):
        self._elems = []

    def is_empty(self):
        return self._elems == []

    def top(self):
        if self.is_empty():
            raise StackUnderflow
        return self._elems[-1]

    def push(self, elem):
        self._elems.append(elem)

    def pop(self):
        if self.is_empty():
            raise StackUnderflow
        return self._elems.pop()

class LNode:
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_

"""
用单链表实现的栈结构，它省去了动态顺序表替换存储的成本。
但是，对解释的存储管理器有了比较高的要求。
"""
class LStack:
    def __init__(self):
        self._top = None

    def is_empty(self):
        return self._top is None

    def top(self):
        if self.is_empty():
            raise StackUnderflow
        return self._top.elem

    def push(self, elem):
        self._top = LNode(elem, self._top)

    def pop(self):
        if self.is_empty():
            raise StackUnderflow
        p = self._top
        self._top = p.next
        return p.elem

"""
栈的简单应用1，括号匹配问题
"""
def check_parens(text):
    parens = '()[]{}'
    open_parens = '([{'
    opposite = {')':'(',']':'[','}':'{'}

    def parenthese(text):
        i, n = 0, len(text)
        while True:
            while i < n and text[i] not in parens:
                i += 1
            if i >= n:
                return
            yield i, text[i]
            i += 1

    st = SStack()
    for j, p in parenthese(text):
        if p in open_parens:
            st.push(p)
        elif st.pop() != opposite[p]:
            print('Unmatching is found at', j, 'for', p)
            return False
        else:
            pass #这个是匹配成功
    print('All parenthese are correctly matched')
    return True

"""
栈的应用2，后缀表达式计算
"""
class ESStack(SStack):
    #当后缀表达式还有运算符，但是栈中只剩下一个元素，那么就是表达式错误。还有一点，运算完成后，检查是否栈中只剩一个元素。否则也是错误。
    def deep(self):
        return len(self._elems)

def suffix_exp_evaluator(line):
    return suf_exp_evaluator(line.split())

def suf_exp_evaluator(exp):
    oper = '+-*/'
    st = ESStack()
    for x in exp:
        if x not in oper:
            st.push(float(x))
            continue
        if st.deep() < 2:
            raise ValueError
        a = st.pop()
        b = st.pop()
        if x == '+':
            c = b + a
        elif x == '-':
            c = b - a
        elif x == '*':
            c = b * a
        elif x == '/':
            c = b / a
        else:
            break
        st.push(float(c))
    if st.deep() != 1:
        raise ValueError
    return st.pop()

"""
中缀表达式转换成后缀表达式
"""
def trans_infix_suffix(line):
    priority = {'(':1, '+':3, '-':3, '*':5, '/':5}
    operators = '+-*/()'
    st = SStack()
    exp = []
    for x in line.split():
        if x not in operators:
            exp.append(x)
        elif st.is_empty() or x == '(':
            st.push(x)
        elif x == ')':
            while not st.is_empty() and st.top() != '(':
                exp.append(st.pop())
            if st.is_empty():
                raise StackUnderflow
            st.pop()
        else:
            while not st.is_empty() and priority[st.top()] >= priority[x]:
                exp.append(st.pop())
            st.push(x)
    while not st.is_empty():
        if st.top() == '(':
            raise StackUnderflow
        exp.append(st.pop())
    return exp

"""
课后练习直接求中缀表达式的值
"""
def infix_exp_evaluator(line):
    priority = {'(': 1, '+': 3, '-': 3, '*': 5, '/': 5}
    operators = '+-*/()'
    s_oper = SStack()
    s_num = ESStack()

    def get_str_oper():
        opr = s_oper.pop()
        if s_num.deep() < 2:
            raise StackUnderflow('s_num Deep Error < 2')
        a = s_num.pop()
        b = s_num.pop()
        if opr == '+':
            c = b + a
        elif opr == '-':
            c = b - a
        elif opr == '*':
            c = b * a
        elif opr == '/':
            c = b / a
        else:
            raise ValueError
        s_num.push(c)

    for x in line.split():
        if x not in operators:
            s_num.push(int(x))
        elif s_oper.is_empty() or x == '(':
            s_oper.push(x)
        elif x == ')':
            while not s_oper.is_empty() and s_oper.top() != '(':
                get_str_oper()
            s_oper.pop()
        else:
            while not s_oper.is_empty() and priority[s_oper.top()] >= priority[x]:
                get_str_oper()
            s_oper.push(x)
    while not s_oper.is_empty():
        get_str_oper()
    if s_num.deep() != 1:
        raise StackUnderflow('s_num Deep Error != 1')
    return s_num.pop()

# print(infix_exp_evaluator('( 3 - 5 ) + ( 6 + 17 * 4 ) / 3'))
# print(trans_infix_suffix('( 3 - 5 ) * ( 6 + 17 * 4 ) / 3'))

"""
递归的阶乘函数
"""
def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n-1)

"""
将上面的递归阶乘函数转化为利用栈保存信息的非递归函数。
之所以将递归函数利用栈转化为非递归函数，是为了函数执行的效率。
因为递归函数对函数调用频繁，而函数调用本身除了有前序动作和后序动作之外，还会保存其他额外的局部信息。
这样会影响程序的效率。
但是，在现在计算机的硬件下，这种影响并不大。除非是对程序有特别严格的要求之外。
"""
def norec_fact(n):
    st = SStack()
    res = 1
    while n > 0:
        st.push(n)
        n -= 1
    while not st.is_empty():
        res *= st.pop()
    return res

"""
有时候，使用递归函数解决问题的思路很简单。如果涉及到的程序对效率不是特别严格的问题，可以考虑使用递归函数。
下面是一个经典的背包问题。
问题描述：
一个背包里面可放入重量为weight的物品，现在有n件物品的集合S，其中物品的重量分别为W0,W1.....Wn-1。
那么能否从中选出若干件物品，使其重量之和正好等于weight。如果存在就说明这个问题有解，不存在就说明无解。
"""
def knap_rec(weight, wlist, n):
    if weight < 0:
        return False
    if weight > 0 and n < 1:
        return False
    if knap_rec(weight-wlist[n-1], wlist, n-1):
        return True
    if knap_rec(weight, wlist, n-1):
        return True
    else:
        return False

"""
队列的链表实现方式
这个比较简单。因为带有尾指针的单链表支持O(1)时间的尾端加入和O(1)时间的首端删除，直接实现即可。
这是一个没有规定大小的队列。
"""

class QueueUnderflow(ValueError):
    pass

class LLQueue:
    def __init__(self):
        self._top = None
        self._rear = None

    def is_empty(self):
        return self._top is None

    def enqueue(self, elem):
        p = self._rear
        if self.is_empty():
            self._top = LNode(elem)
            self._rear = self._top
        else:
            p.next = LNode(elem)
            self._rear = p.next

    def peek(self):
        if self.is_empty():
            raise QueueUnderflow
        return self._top.elem

    def dequeue(self):
        if self.is_empty():
            raise QueueUnderflow
        e = self._top.elem
        if self._top.next is None:
            self._top = None
        else:
            e = self._top.elem
            self._top = self._top.next
        return e

"""
队列顺序表的实现方式。
由于顺序表的O(1)尾端添加和O(n)首端删除的特点。
考虑使用循环顺序表实现队列
"""

class LQueue:
    def __init__(self, int_len=8):
        self._len = int_len
        self._elems = [0] * self._len
        self._num = 0
        self._head = 0

    def is_empty(self):
        return self._num == 0

    def peek(self):
        if self.is_empty():
            raise QueueUnderflow
        return self._elems[self._head]

    def dequeue(self):
        if self.is_empty():
            raise QueueUnderflow
        e = self._elems[self._head]
        self._head = (self._head+1) % self._len
        self._num -= 1
        return e

    def enqueue(self, elem):
        if self._num == self._len:
            self.extend()
        self._elems[(self._head+self._num)%self._len] = elem
        self._num += 1

    def extend(self):
        old_len = self._len
        self._len *= 2
        new_elems = [0] * self._len
        for i in range(old_len):
            new_elems[i]= self._elems[(self._head+i)%old_len]
        self._elems, self._head = new_elems, 0

"""
迷宫求解问题
"""
def mark(maze, pos):
    maze[pos[0]][pos[1]] = 2

def passble(maze, pos):
    return maze[pos[0]][pos[1]] == 0

dirs = ((1,0),(0,1),(-1,0),(0,-1))
def maze_solver_queue(maze, start, end):
    if start == end:
        return True
    qu = LQueue()
    mark(maze, start)
    qu.enqueue(start)
    dict = {}
    while not qu.is_empty():
        pos = qu.dequeue()
        for i in range(4):
            nextp = pos[0]+dirs[i][0], pos[1]+dirs[i][1]
            if passble(maze, nextp):
                dict[nextp] = pos
                if nextp == end:
                    prve = end
                    while prve != start:
                        prve = dict[prve]
                        print(prve)
                    return True
                mark(maze, nextp)
                qu.enqueue(nextp)
    print('No Found the Path')

"""
课后编程练习第一题
改造括号匹配问题函数check_parens，让它从指定的文件读入数据，在发现不匹配的时候，不仅输出不匹配的括号，还输出该括号在原文件里的行号和字符位置。
答案：
见下面的函数parents_match
"""
def parents_match(file):
    parents = '[](){}'
    open_parent = '([{'
    item_parent = {')': '(', '}': '{', ']': '['}
    st = SStack()

    def parentheses(line):
        len_line = len(line)
        iden_list = [0]*3
        for i in range(len_line):
            if line[i] == '#':
                break
            elif line[i] == '\'' and line[i-1] != '\\':
                iden_list[0] += 1
            elif line[i] == '\"' and line[i-1] != '\\':
                iden_list[1] += 1
            if line[i] in parents and iden_list[0]%2==0 and iden_list[1]%2==0:
                yield i, line[i]

    with open(file, 'r') as f:
        lines = f.readlines()

    for j in range(len(lines)):

        for i, pr in parentheses(lines[j]):
            if pr in open_parent:
                st.push(pr)
            elif item_parent[pr] != st.pop():
                print('match error', i,pr,j+1)
                return False
            else:
                pass
    print('All parenthese are correctly matched')
    return True

"""
课后练习第二题
请修改前一题完成的函数，使之可以检查实际Python程序里的三种括号匹配。
注意：#，"，'，三种符号。
"""
# maze = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#         [1,0,0,0,1,1,0,0,0,1,0,0,0,1],
#         [1,0,1,0,0,0,0,1,0,1,0,1,0,1],
#         [1,0,1,0,1,1,1,1,0,1,0,1,0,1],
#         [1,0,1,0,0,0,0,0,0,1,1,1,0,1],
#         [1,0,1,1,1,1,1,1,1,1,0,0,0,1],
#         [1,0,1,0,0,0,0,0,0,0,0,1,0,1],
#         [1,0,0,0,1,1,1,0,1,0,1,1,0,1],
#         [1,0,1,0,1,0,1,0,1,0,1,0,0,1],
#         [1,0,1,0,1,0,1,0,1,1,1,1,0,1],
#         [1,0,1,0,0,0,1,0,0,1,0,0,0,1],
#         [1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
# print(maze_solver_queue(maze, (1,1), (10,12)))
