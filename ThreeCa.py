# coding: utf-8


class LinkedListUnderFlow(ValueError):
    pass

"""
单链表的结点
"""
class LNode:
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_

"""
只有表头变量的单链表
"""

class LList:

    def __init__(self):
        self._head = None

    def is_empty(self):
        return self._head is None

    def __len__(self):
        p = self._head
        e = 0
        while p is not None:
            e += 1
            p = p.next
        return e

    def head(self):
        return self._head

    # ==
    def __eq__(self, other):
        if not isinstance(other, LList):
            raise TypeError
        p, q = self._head, other.head()
        while (p is not None) and (q is not None):
            if p.elem == q.elem:
                p, q = p.next, q.next
            else:
                return False
        if (p and q) is not None:
            return False
        return True

    # <
    def __lt__(self, other):
        if not isinstance(other, LList):
            raise TypeError
        p, q = self._head, other.head()
        while (p is not None) and (q is not None):
            if p.elem < q.elem:
                return True
            elif p.elem == q.elem:
                p, q = p.next, q.next
            else:
                return False
        if (p is None) and (q is not None):
            return True
        return False

    # >
    def __gt__(self, other):
        if not isinstance(other, LList):
            raise TypeError
        p, q = self._head, other.head()
        while (p is not None) and (q is not None):
            if p.elem > q.elem:
                return True
            elif p.elem == q.elem:
                p, q = p.next, q.next
            else:
                return False
        if (p is not None) and (q is None):
            return True
        return False

    # <=
    def __le__(self, other):
        if not isinstance(other, LList):
            raise TypeError
        p, q = self._head, other.head()
        while (p is not None) and (q is not None):
            if p.elem < q.elem:
                return True
            elif p.elem == q.elem:
                p, q = p.next, q.next
            else:
                return False
        if (p is not None) and (q is None):
            return False
        return True

    # >=
    def __ge__(self, other):
        if not isinstance(other, LList):
            raise TypeError
        p, q = self._head, other.head()
        while (p is not None) and (q is not None):
            if p.elem > q.elem:
                return True
            elif p.elem == q.elem:
                p, q = p.next, q.next
            else:
                return False
        if (p is None) and (q is not None):
            return False
        return True

    def prepend(self, elem):
        self._head = LNode(elem, self._head)

    def pop(self):
        if self._head is None:
            raise LinkedListUnderFlow
        e = self._head.elem
        self._head = self._head.next
        return e

    def append(self, elem):
        if self._head is None:
            self._head = LNode(elem)
            return
        p = self._head
        while p.next is not None:
            p = p.next
        p.next = LNode(elem)

    def pop_last(self):
        if self._head is None:
            raise LinkedListUnderFlow
        elif self._head.next is None:
            e = self._head.elem
            self._head = None
            return e
        p = self._head
        while p.next.next is not None:
            p = p.next
        e = p.next.elem
        p.next = None
        return e

    def insert(self, elem, i):
        if i < 0 or i > len(self):
            raise LinkedListUnderFlow
        elif i == 0:
            self.prepend(elem)
        else:
            p = self._head
            while p is not None and i > 1:
                i -= 1
                p = p.next
            p.next = LNode(elem, p.next)

    def delt(self, i):
        if i < 0 or i >= len(self) or self._head is None:
            raise LinkedListUnderFlow
        elif i == 0:
            self.pop()
        else:
            p = self._head
            while p is not None and i > 1:
                i -= 1
                p = p.next
            p.next = p.next.next

    def search(self, elem):
        p = self._head
        e = 0
        while p is not None:
            if p.elem == elem:
                return e
            e += 1
            p = p.next
        return -1

# 只能返回满足pred谓词的第一个元素，如果要返回所有的元素，可以使用生成器做成的迭代器。
    def find(self, pred):
        p = self._head
        while p is not None:
            if pred(p.elem):
                return p.elem
            p = p.next

# 可以返回满足谓词的所有元素，可以用for来进行循环查看。
    def filter(self, pred):
        p = self._head
        while p is not None:
            if pred(p.elem):
                yield p.elem
            p = p.next

    def printall(self):
        p = self._head
        while p is not None:
            print(p.elem)
            p = p.next

    def for_each(self, proc):
        p = self._head
        while p is not None:
            proc(p.elem)
            p = p.next

# 迭代器，使用for i in mlist.elements:进行遍历
    def elements(self):
        p = self._head
        while p is not None:
            yield p.elem
            p = p.next

# 将这个例子比作桌子上的一摞书，然后一本一本放到另外一边。
    def reverse(self):
        p = None
        while self._head is not None:
            q = self._head
            self._head = q.next
            q.next = p
            p = q
        self._head = p

    def list_llist(self, mlist):
        for i in range(len(mlist)-1, -1, -1):
            self.prepend(mlist[i])

    def llist_list(self):
        return [i for i in self.elements()]

    def rev_visit(self, op):
        self.reverse()
        self.for_each(op)
        self.reverse()

    def del_minimal(self):
        if self._head is None:
            raise LinkedListUnderFlow
        p = self._head
        min_num = p.elem
        while p.next is not None:
            if min_num > p.next.elem:
                min_num = p.next.elem
            p = p.next

        p = self._head
        q = None
        while p is not None:
            if not q and p.elem == min_num:
                self._head = self._head.next
                q = self._head
            elif p.elem == min_num:
                q.next = p.next
                if p.next is None:
                    return
            else:
                q = p
            p = p.next

    def del_if(self, pred):
        """"
        这种方法比较复杂，不能达到O(n)的复杂度要求
        """
        # p = self._head
        # index, i = [],0
        # while p is not None:
        #     if pred(p.elem):
        #         index.append(i)
        #     p = p.next
        #     i += 1
        #
        # print(index)
        # for j in range(len(index)-1,-1,-1):
        #     self.delt(index[j])
        # return index
        p = self._head
        q = None
        while p is not None:
            if not q and pred(p.elem):
                self._head = self._head.next
                q = self._head
            elif pred(p.elem):
                q.next = p.next
                if p.next is None:
                    return
            else:
                q = p
            p = p.next

    def del_duplicate(self):
        p = self._head
        mlist = []
        q = None
        while p is not None:
            if p.elem not in mlist:
                mlist.append(p.elem)
                q = p
            else:
                q.next = p.next
                if p.next is None:
                    return
            p = p.next

    def interleaving(self, another):
        if not isinstance(another, LList):
            raise LinkedListUnderFlow
        p = self._head
        q = another.head()
        while (p is not None) or (q is not None):
            # e = q.next
            # if not p.next:
            #     pass
            #     p.next = e
            #     p = p.next
            #     # p = q.next
            #     # p.next = q
            #     # q = q.next
            #     # p = p.next
            # elif not q:
            #     p = p.next
            # else:
            #     # e = q.next
            #     q.next = p.next
            #     p.next = q
            #     p = q.next
            #     q = e
            pass

    def sort(self):
        p = self._head
        if p is None or p.next is None:
            return
        # lst = [12, 3, 4, 89, 21, 2, 3]

        rem = p.next
        p.next = None
        while rem is not None:
            p = self._head
            q = None
            while p is not None and p.elem <= rem.elem:
                q = p
                p = p.next
            if q is None:
                self._head = rem
            else:
                q.next = rem
            q = rem
            rem = rem.next
            q.next = p

"""
课后练习第一题
给链表添加本章开始定义的线性抽象数据类型中没有的操作。

答案：
见上面的
__len__,求出链表的长度。
insert(elem, i)，在指定位置i添加elem元素。
delt(i),在指定位置i删除。
search(elem),找出该元素的位置。
"""

"""
课后练习第二题
请为Llist类增加定位插入和删除操作。

答案：
见上面第一题
"""

"""
课后练习第三题
给Llist增加一个元素计数值域num，并修改类中操作，维护这个计数值。
另外定义有一个求表中元素个数的len函数。
请比较这种实现和原来没有元素计数值域的实现，
个说明其优缺点。

答案：
这个实现很简单，就是在
def __init__(self):
    self._head = None
    self._num = 0
初始化计数值为0。
然后在进行加入元素操作的时候，比如prepend,append,insert等方法中，令self._num += 1
在删除元素操作的时候，比如pop,pop_last,delt等方法中，令self._num -= 1
最后写一个len方法。
def len(self):
    return self._num
这样做的好处是可以在O(1)时间内得到链表的个数，而原来是O(n)时间。
因此代码执行效率大大提高了。
但是它的缺点是要实时维护一个计数变量num。
"""

"""
课后练习第四题
请基于元素相等操作'=='定义一个单链表的相等比较函数。
另请基于字典序的概念，为链接表定义大于、小于、大于等于和小于等于判断。

答案：
见上面函数__eq__(==),__lt__(<),__gt__(>),__le__(<=),__ge__(>=)
"""

"""
课后练习第五题
请为链接表定义一个方法，它基于顺序表参数构造一个链接表，
另请定义一个函数，它从一个链接表构造出一个顺序表

答案：
见上面函数list_llist,llist_list
"""

"""
课后练习第六题
请为单链表类增加一个反向遍历方法rev_visit(self, op),它能从后向前的顺序把
操作op逐个作用于表元素。你定义的方法在整个遍历中访问点的次数与表长度n是什么关系？
如果不是线性关系，请设法修改，使之达到线性关系。这里要求遍历方法的空间代价是O(1)
提示：
你可以考虑为了遍历而修改表的结构，只要能在遍历的最后将表的结构复原。

答案：
见上面rev_visit函数。
"""

"""
课后练习第七题
请为单链表类定义下面几个元素删除方法，并保持其他元素的相对顺序
1、del_minimal() 删除当时链表中的最小元素
2、del_if(pred) 删除当前链表里所有满足谓词函数pred的元素
3、del_duplicate()删除表中所有重复出现的元素。也就是说，表中任何元素的第一次出现保留不动，
后续与之相等的元素都删除
要求所有的操作，复杂度均为O(n)

答案：
见上面del_minimal,del_if,del_duplicate
"""

"""
课后练习第八题
请为单链表类定义一个变动方法interleaving(self, another),它把另一个但链表another的元素交错
地加入本链表。也就是说，结果单链表中的元素是其原有元素与单链表another中元素的一一交错的序列。
如果某个表更长，其剩余元素应位于修改后的单链表的最后。
"""

"""
增加表尾变量的单链表
"""


class LList1(LList):

    def __init__(self):
        super(LList1, self).__init__()
        self._rear = None

    def rear(self):
        return self._rear

    def prepend(self, elem):
        if self._head is None:
            self._head = LNode(elem, self._head)
            self._rear = self._head
        else:
            self._head = LNode(elem, self._head)

    # 因为这里判断空表是用的self._head,所以pop操作跟LList的一样，当删除了表头的元素外，并不需要维护self._rear的值。

    def append(self, elem):
        if self._head is None:
            self._head = LNode(elem, self._head)
            self._rear = self._head
        else:
            self._rear.next = LNode(elem)
            self._rear = self._rear.next

    def pop_last(self):
        if self._head is None:
            raise LinkedListUnderFlow
        p = self._head
        if p.next is None:
            e = p.elem
            self._head = None
            return e
        else:
            while p.next.next is not None:
                p = p.next
            e = p.next.elem
            p.next = None
            self._rear = p
            return e

"""
循环单链表
值需要使用self._rear一个表尾变量，然后将self._rear.next指向表头。而不在是None值。
这里的关键是怎么判断一个循环的结束，也就是遍历的时候不一样。
"""


class CLList:

    def __init__(self):
        self._rear = None

    def is_empty(self):
        return self._rear is None

    def prepend(self, elem):
        if self.is_empty():
            self._rear = LNode(elem)
            self._rear.next = self._rear
        else:
            self._rear.next = LNode(elem, self._rear.next)

    def append(self, elem):
        self.prepend(elem)
        self._rear = self._rear.next

    def pop(self):
        if self.is_empty():
            raise LinkedListUnderFlow
        p = self._rear.next
        if p is self._rear:
            e = self._rear.elem
            self._rear = None
        else:
            e = p.elem
            self._rear.next = p.next
        return e

    def pop_last(self):
        if self.is_empty():
            raise LinkedListUnderFlow
        p = self._rear
        if p.next is self._rear:
            e = p.elem
            self._rear = None
        else:
            while True:
                if p.next is self._rear:
                    break
                p = p.next
            e = p.elem
            p.next = p.next.next
            self._rear = p
        return e

    def print_all(self):
        p = self._rear.next
        while True:
            print(p.elem)
            if p is self._rear:
                break
            p = p.next


"""
上面的单链表的操作只能支持O(1)时间的首段加入/删除元素，和O(1)时间的尾端加入元素，并不能支持O(1)时间的尾端删除元素。
要想支持O(1)时间的尾端删除元素，必须修改表的结构，使其能从后面也能找到前面的元素。这样就能很方便找到尾端元素的前一个元素。
所以它的时间复杂度为O(1)，但是这样的话，就必须给每一个结点添加一个prep域，通过这个域才能找到其前一个元素。使链表的空间开销
与结点数成正比。不过如果元素本身占用的空间特别大，这样做是很值得的。
这种设计也就是所谓的双链表。
不但从任一结点出发能找到它的下一个元素，也能从任一结点找到它的上一个元素。
"""


class DLNode(LNode):
    def __init__(self, elem, prev=None, next_=None):
        super(DLNode, self).__init__(elem, next_)
        self.prev = prev


class DLList(LList1):
    def __init__(self):
        super(DLList, self).__init__()

    def prepend(self, elem):
        p = DLNode(elem, None, self._head)
        if self.is_empty():
            self._rear = p
        else:
            self._head.prev = p
        self._head = p

    def append(self, elem):
        p = DLNode(elem, self._rear, None)
        if self.is_empty():
            self._head = p
        else:
            p.prev.next = p
        self._rear = p

    def pop(self):
        if self.is_empty():
            raise LinkedListUnderFlow
        p = self._head
        e = p.elem
        self._head = p.next
        if p.next is not None:
            p.next.prev = None
        return e

    def pop_last(self):
        if self.is_empty():
            raise LinkedListUnderFlow
        p = self._rear
        e = p.elem
        if self._head.next is None:
            self._head = None
        else:
            p.prev.next = None
            self._rear = p.prev
        return e


"""
关于lst的插入排序。
"""


def sort_list(lst):
    for i in range(1, len(lst)):
        x = lst[i]
        j = i
        while j > 0 and lst[j-1] > x:
            lst[j] = lst[j-1]
            j -= 1
        lst[j] = x
    return lst

"""
关于lst的反转元素
"""


def rev(lst):
    i, j = 0, len(lst)-1
    while i < j:
        lst[i], lst[j] = lst[j], lst[i]
        i += 1
        j -= 1
    return lst


"""
关于joseph问题求解的三种解决方案
简单说明一下joseph问题
假设有n个人围坐一圈，现在要求从第k个人开始报数
1、数组方式，
基本思想是
"""

"""
用顺序表实现joseph
"""


def joseph_l(n, k, m):
    people = list(range(1, n+1))
    num, i = n, k-1
    for num in range(n, 0, -1):
        i = (i + (m-1)) % num
        print(people.pop(i))
    return


"""
用链表实现joseph
"""


class Joseph(CLList):

    def turn(self, m):
        for i in range(m):
            self._rear = self._rear.next

    def __init__(self, n, k, m):
        super(Joseph, self).__init__()
        for i in range(n):
            self.append(i+1)
        self.turn(m)
        while not self.is_empty():
            self.turn(k-1)
            print(self.pop())


if __name__ == '__main__':
     # mlist = LList()
     # for i in range(1,10):
     #     mlist.prepend(i)
     # mlist.printall()
     # mlist.for_each(print)
     # print('len', len(mlist))
     # mlist.insert(13,9)
     # mlist.printall()
     # mlist.delt(9)
     # mlist.printall()
     # print(mlist.search(1))
     # llist = LList()
     # for i in range(1,9):
     #     llist.prepend(i)
     # print(mlist == llist, mlist<llist, mlist>llist, mlist<=llist,mlist>=llist,)
     # llist1 = LList()
     # mylist = ['walle','eva','cici']
     # llist1.list_llist(mylist)
     # llist1.printall()
     # print(llist1.llist_list())
     # print(mlist.del_minimal())
     # mlist.printall()
     clist =LList()
     mylist = [2,198,243,989,2,13,198,11,0,123,5]
     clist.list_llist(mylist)
     # clist.printall()
     # clist.del_minimal()
     # clist.printall()
     # clist.del_if(lambda x:x==2)
     # clist.printall()
     clist.del_duplicate()
     clist.printall()
     # mlist.interleaving(clist)
     # mlist.printall()
     # clist.interleaving(mlist)
     # clist.printall()

     # llist1 = LList1()
     # for i in range(1,10):
     #     llist1.append(i)
     # llist1.printall()
     # llist1.pop()
     # llist1.pop_last()
     # llist1.printall()

     # cllist = CLList()
     # for i in range(1,10):
     #    cllist.prepend(i)
     # cllist.pop()
     # cllist.pop_last()
     # cllist.print_all()

     # dllist = DLList()
     # for i in range(1, 10):
     #     dllist.prepend(i)
     # for j in range(19,9,-1):
     #     dllist.append(j)
     # dllist.pop()
     # dllist.pop_last()
     # dllist.printall()

     # lst =[12,3,4,89,21,2,3]
     # # rev(lst)
     # # print(lst)
     # # print(sort_list(lst))
     #
     # sllist = LList()
     # sllist.list_llist(lst)
     # sllist.sort()
     # sllist.printall()
     #
     # num = josephas_A(10, 5, 3)
     # for i in num:
     #     print(i)
















