"""
朴素匹配字符串的方法
"""
def match(p,t):
    m, n = len(p), len(t)
    i, j = 0, 0
    while i < m and j < n:
        if p[i] == t[j]:
            i, j = i + 1, j + 1
        else:
            i, j = 0, j-i+1
    if m == i:
        return j-i
    return -1

"""
KMP匹配字符串的方法
"""
def KMP_match(p, t, pnext):
    m, n = len(p), len(t)
    i, j = -1, 0
    while i < m and j < n:
        if i == -1 or p[i] == t[j]:
            i, j = i+1, j+1
        else:
            i = pnext[i]
    if i == m:
        return j-i
    return -1

"""
生成KMP匹配方法中需要的pnext表
"""
def gen_pnext(p):
    i, k, m = 0, -1, len(p)
    pnext = [-1]*m
    while i < m-1:
        if k == -1 or p[i] == p[k]:
            i, k = i+1, k+1
            pnext[i] = k
        else:
            k = pnext[k]

"""
生成KMP匹配方法中需要的pnext表
优化后的代码。其中少去了一些执行操作。
"""
def gen_pnext1(p):
    i, k, m = 0, -1, len(p)
    pnext = [-1]*m
    while i < m-1:
        if k == -1 or p[i] == p[k]:
            i, k = i+1, k+1
            if p[i] == p[k]:
                pnext[i] = pnext[k]
            else:
                pnext[i] = k
        else:
            k = pnext[k]
    return pnext

class MyStr(str):
    @staticmethod
    def gen_pnext(p):
        i, k, m = 0, -1, len(p)
        pnext = [-1] * m
        while i < m - 1:
            if k == -1 or p[i] == p[k]:
                i, k = i + 1, k + 1
                if p[i] == p[k]:
                    pnext[i] = pnext[k]
                else:
                    pnext[i] = k
            else:
                k = pnext[k]
        return pnext

    def KMP_match(self, p):
        m, n = len(p), len(self)
        i, j = 0, 0
        pnext = MyStr.gen_pnext(p)
        while i < m and j < n:
            if i == -1 or p[i] == self[j]:
                i, j = i + 1, j + 1
            else:
                i = pnext[i]
        if i == m:
            return j - i
        return -1

    def replace(self, str1, str2, count=-1):
        m, n = len(str1), len(self)
        i, j = 0, 0
        pnext = MyStr.gen_pnext(str1)
        aftstr, a, b ='', 0, -m
        while j < n:
            if i == m:
                a, b = b+m, j-i
                aftstr += self[a:b] + str2
                i, j= 0, j+1
            if i == -1 or str1[i] == self[j]:
                i, j = i + 1, j + 1
            else:
                i = pnext[i]
        aftstr += self[b+m:]
        return aftstr

    def tokens(self, seqs):
        m, n = len(seqs), len(self)
        i, j = 0, 0
        pnext = MyStr.gen_pnext(seqs)
        a, b = 0, -m
        while j < n:
            if i == m:
                a, b = b + m, j - i
                yield self[a:b]
                i, j = 0, j + 1
            if i == -1 or seqs[i] == self[j]:
                i, j = i + 1, j + 1
            else:
                i = pnext[i]
        yield self[b + m:]


"""
课后练习编码第一题
针对Python的str对象，自己实现一个replace操作函数
答案：
见上面MyStr中的replace方法。
"""

"""
编程练习第二题
定义生成器函数tokens(string,seps),其中string参数是被处理的字符串，seps是描述分隔字符的字符串，
都是str类型的对象。该生成器逐个给出string里一个个不包含seps中分隔字符的最大子串。
答案：
见上面的函数tokens
"""

"""
编程练习第三题
请基于链接表的概念定义一个字符串类，每个链接结点保存一个字符。实现其构造函数(以python的str对象为参数)。
请定义下面方法：求串长度，完成字符串替换，采取朴素方式和KMP算法实现子串匹配。
答案：
见下面的LStr类
"""

"""
编程练习第四题
为上述链接表字符串类增加下面的方法：
1、find_in(self, another),确定本字符串中第一个属于字符串another的字符所在结点的位置，返回表示这个位置的整数。
2、find_not_in(self, another),与上面函数类似，但它要查找的是不属于another的字符。
3、remove(self, another),从self里删除串another里的字符
答案：
见下面find_in函数和find_not_in函数和remove函数
"""

"""
编程练习第五题
实际中经常需要在一个长字符串里查找与某几个字符串之一匹配的子串。请考虑这一问题并设计一个合理的算法，
实现这个算法并分析复杂性。
"""
class LNode:
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_

class LStr:
    @staticmethod
    def gen_pnext(p):
        i,k,m = 0, -1, len(p)
        pnext = [-1]*m
        while i < m-1:
            if p[k] == p[i] or k == -1:
                i, k = i+1, k+1
                pnext[i] = k
            else:
                k = pnext[k]
        return pnext


    def __init__(self, str):
        self._head = None
        print(len(str)-1)
        for i in range(len(str)-1, -1, -1):
            self.prepend(str[i])

    def prepend(self, elem):
        self._head = LNode(elem, self._head)

    def printall(self):
        p = self._head
        while p is not None:
            print(p.elem)
            p = p.next

    def __len__(self):
        p, i = self._head, 0
        while p is not None:
            p = p.next
            i += 1
        return i

    def search(self, i):
        if i<0  or i>= self.__len__():
            print(self.__len__())
            raise ValueError
        p, e = self._head, 0
        while p is not None and i>=0:
            e = p.elem
            p = p.next
            i -= 1
        return e

    def match(self, p):
        m, n = len(p), self.__len__(),
        i, j = 0, 0
        while i<m and j<n:
            if self.search(j) == p[i]:
                i, j = i+1, j+1
            else:
                i, j = 0, j-i+1
        if i == m:
            return j-i
        return -1

    def print_a_b(self, a, b):
        p = self._head
        s = ''
        while p is not None and b>0:
            if a<=0:
                s += p.elem
            a, b = a-1, b-1
            p = p.next
        return s

    def KMP_match(self, p):
        m, n = len(p), self.__len__(),
        i, j = 0, 0
        pnext = LStr.gen_pnext(p)
        while i<m and j<n:
            if i == -1 or self.search(j) == p[i]:
                i, j = i+1, j+1
            else:
                i = pnext[i]
        if i == m:
            return j-i
        return -1

    """
    这个函数可以优化，因为链表可以修改其中的结点，所以完全不必要重新创建一个字符串来存替换后的字符串。只需要在原链表上进行替换就可以。
    """
    def replace(self, str1, str2, count=-1):
        m, n = len(str1), len(self)
        i, j = 0, 0
        pnext = LStr.gen_pnext(str1)
        aftstr, a, b ='', 0, -m
        while j < n:
            if i == m:
                a, b = b+m, j-i
                aftstr += self.print_a_b(a, b) + str2
                i, j= 0, j+1
            if i == -1 or str1[i] == self.search(j):
                i, j = i + 1, j + 1
            else:
                i = pnext[i]
        aftstr += self.print_a_b(b+m, n)
        return aftstr

    def find_in(self, another):
        if not isinstance(another, str):
            raise TypeError
        p,i = self._head,0
        while p is not None:
            if p.elem in another:
                return i
            i += 1
            p = p.next

    def find_not_in(self, another):
        if not isinstance(another, str):
            raise TypeError
        p,i = self._head,0
        while p is not None:
            if p.elem not in another:
                return i
            i += 1
            p = p.next

    def remove(self, another):
        if not isinstance(another, str):
            raise TypeError
        p, q = self._head, None
        while p is not None:
            if p.elem in another:
                if p == self._head:
                    self._head = self._head.next
                else:
                    q.next = p.next #这里q都不必要变。
            else:
                q = p
            p = p.next

if __name__ == '__main__':
    with open('gudu', 'r') as f:
        wen = f.read()
    mys = MyStr('dsajs123ldjsaljdo;saj123dpajsdopsaopdjpos[jao[dj[a123osjdo[pasj;jojdospsad;')
    print(mys.replace('123','---'))
    ydui = mys.tokens('123')
    print(ydui)
    for i  in ydui:
        print(i)
    sstr = 'dsajs123ldjsaljdo;saj123dpajsdopsaopdjpos[jao[dj[a123osjdo[pasj;jojdospsad;'
    lstr = LStr(sstr)
    print(lstr.KMP_match('123'))
    print(lstr.replace('123','---'))
    print(lstr.find_in('s796'))
    print(lstr.find_not_in('1796'))
    lstr.remove('dsabc')
    print(lstr.print_a_b(0,len(lstr)))




