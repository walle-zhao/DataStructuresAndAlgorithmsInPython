"""
排序问题
"""
import time

def timer(func):
    def decor(*args):
        start_time = time.time()
        func(*args)
        end_time = time.time()
        d_time = end_time - start_time
        print("run the func use : ", d_time)
    return decor
"""
1、插入排序
它具有稳定性与适应性。
O(n²)的时间复杂度
O(1)的空间复杂度
"""

def insert_sort(lst):
    for i in range(1, len(lst)):
        x = lst[i]
        j = i
        while j > 0 and lst[j-1] >= x:
            lst[j] = lst[j-1]
            j -= 1
        lst[j] = x
    return lst
"""
交换排序之起泡排序
"""
@timer
def dubble_sort(lst):
    for i in range(len(lst)):
        found = False
        for j in range(1, len(lst)-i):
            if lst[j] < lst[j-1]:
                lst[j], lst[j-1] = lst[j-1], lst[j]
                found = True
        if not found:
            break
    return lst
"""
选择排序
"""
def select_sort(lst):
    for i in range(len(lst)-1):
        k = i
        for j in range(k, len(lst)):
            if lst[j] < lst[k]:
                k = j
        if i != k:
            lst[i], lst[k] = lst[k], lst[i]
    return lst
"""
快速排序
"""
def quick_sort(lst):
    quick_rct(lst, 0, len(lst)-1)
    return lst

def quick_rct(lst, l, r):
    if l >= r:
        return
    i, j = l, r
    prioe = lst[i]
    while i < j:
        while i < j and lst[j] >= prioe:
            j -= 1
        if i < j:
            lst[i] = lst[j]
            i += 1
        while i < j and lst[i] <= prioe:
            i += 1
        if i < j:
            lst[j] = lst[i]
            j -= 1
    lst[i] = prioe
    quick_rct(lst, l, i-1)
    quick_rct(lst, i+1, r)
"""
归并排序
"""
"""
这个函数主要是将合并两个排序好的list。可以执行下面代码观察一下
lst1 = [2,6,9,3,5,8]
lst2 = [None]*6
merge(lst1, lst2, 0, 3, 6)
print(lst2)
"""
def merge(lfrom, lto, low, mid, high):
    i, j, k = low, mid, low
    while i < mid and j < high:
        if lfrom[i] <= lfrom[j]:
            lto[k] = lfrom[i]
            i += 1
        else:
            lto[k] = lfrom[j]
            j += 1
        k += 1
    while i < mid:
        lto[k] = lfrom[i]
        i += 1
        k += 1
    while j < high:
        lto[k] = lfrom[j]
        j += 1
        k += 1

"""
这个函数是不断合并lfrom表中的相邻的两个排序好的子段。直到整个lfrom都合并完成，并且将合并好的放到lto表中。
"""
def merge_pass(lfrom, lto, llen, slen):
    i = 0
    while i + 2 * slen < llen:
        merge(lfrom, lto, i, i+slen, i+2*slen)
        i += 2 * slen
    if i + slen < llen:  # 剩下两段，后段长度小于slen
        merge(lfrom, lto, i, i+slen, llen)
    else:                # 只剩下一段，直接复制到lto
        for j in range(i, llen):
            lto[j] = lfrom[j]
"""
这个是归并排序的主函数。
"""
def merge_sort(lst):
    slen, llen =1, len(lst)
    templst = [None] * llen
    while slen < llen:
        merge_pass(lst, templst, llen, slen)
        slen *= 2
        merge_pass(templst, lst, llen, slen)
        slen *= 2
    return lst
"""
1.请用一组随机生成的数据试验本章正文中讨论的几个排序算法，关键码用某个范围内的整数表示。分析得到的试验数据，并对其做一些总结。
2.请定义一个插入排序算法，让它在原序列的高端积累已排序的元素。
3.请采用二分法在插入排序中找到插入位置，而后再实际插入元素。请分析所做的算法，特别关注其稳定性。如果它不稳定，请设法修改使之稳定。
4.请定义一个选择排序函数，它每次选择剩余记录中最大的记录，完成从小到大递增顺序的排序工作。
5.请实现一个稳定的选择排序算法。
6.第9.2.3节最后提出了一种交错起泡的排序技术。请定义一个采用这种技术的排序函数，并用随机生成的表做一些试验，比较它和简单起泡排序的性能。
7.请为第3章的单链表类定义一个采用选择排序思想的排序方法。
8.请为第3章的单链表类定义一个采用快速排序思想的排序方法。
9.请实现采用“三者取中”策略的快速排序函数，用随机生成的表作为实例，比较采用这种策略的函数和本章正文中的快速排序函数。
10.请提出另一种改进划分标准的方法，基于该方法实现一个快速排序函数，并将实现的函数与正文中的快速排序函数比较。
11.请实现一个非递归的快速排序算法，算法在选择处理分段时采用本章正文中提出的相关方法，保证其空间需求达到最少。
12.考虑9.5.1节提出的基于绩点对学生记录排序的工作。请根据具体情况做出一种设计和实现，保证排序工作可以在O(n) 时间完成（n是学生记录数）。
13.第9.5.1节最后说基数排序算法的另一种常见技术是用链接表实现桶，那样做可以摆脱Python中list操作的潜在影响（空间复杂度不再依赖于Python表操作的实现技术）。用链表作为记录存储桶，收集时可以简单地取下链表结点链，顺序连接起来，因此可以节省时间。请采用这种技术实现一个基数排序函数。
14.请考虑9.5.2节提出的组合方法，选择一种组合方式实现相应的排序函数，并通过一些试验确定合适的方法转换时机。
15.请基于蒂姆排序算法实现一个排序函数。
"""

"""
课后编程练习第二题答案：
见下面insert_sort1函数
"""
def insert_sort1(lst):
    for i in range(len(lst)-2, -1, -1):
        k = lst[i]
        j = i
        while j < len(lst)-1 and k > lst[j+1]:
            lst[j] = lst[j+1]
            j += 1
        lst[j] = k
    return lst
"""
课后编程练习第三题答案：
"""
def biserch(lst, key):
    low, high = 0, len(lst)-1
    while low <= high:
        mid = low + (high-low)//2
        if key < lst[mid]:
            high = mid - 1
        elif key > lst[mid]:
            low = mid + 1
        else:
            return mid
    return low

def insert_sort_biserch(lst):
    for i in range(1, len(lst)):
        x = lst[i]
        j = biserch(lst[:i], x)
        lst[:i+1].insert(j, x)
    return lst

"""
课后编程练习第四题答案：
"""
def select_sort1(lst):
    for i in range(len(lst)-1, 0, -1):
        k = i
        for j in range(0, k+1):
            if lst[j] > lst[k]:
                k = j
        if k != i:
            lst[k], lst[i] = lst[i], lst[k]
    return lst
"""
课后编程练习第五题答案：
"""
def select_sort2(lst):
    for i in range(len(lst)-1):
        k = i
        for j in range(k, len(lst)):
            if lst[j] < lst[k]:
                k = j
        if k != i:
            teme = lst[k]
            while i < k:
                lst[k] = lst[k-1]
                k -= 1
            lst[i] = teme
    return lst
"""
课后编程练习第六题答案：
"""
@timer
def dubble_sort1(lst):
    for i in range(len(lst)):
        found = False
        for j in range(1, len(lst)-i):
            if lst[j] < lst[j-1]:
                lst[j], lst[j-1] = lst[j-1], lst[j]
                found = True
        for k in range(len(lst)-1-i, 0, -1):
            if lst[k] < lst[k-1]:
                lst[k], lst[k-1] = lst[k-1], lst[k]
                found = True
        if not found:
            break
    return lst
"""
课后编程练习第七题答案：
主要思想还是对调元素，并不是更改链接结点的方向。
"""
from DateAndCompute.ThreeCa import LList
class LList1(LList):
    def sort(self):
        cur = self._head
        while cur.next is not None:
            x = cur.elem
            p = cur
            while p is not None:
                if p.elem < x:
                    x = p.elem
                p = p.next
            p = cur
            while p.elem is not x:
                p = p.next
            p.elem = cur.elem
            cur.elem = x
            cur = cur.next

    """
    课后编程练习第八题答案：
    """
    def sort1_rec(self, l, r):
        # i, j, k = l, l, l
        # priom = i.elem
        # q = None
        # while i is not r:
        #     if i.elem < priom:
        #         q.next = i.next
        #         i.next = k
        #         k = i
        #     else:
        #         q = i
        #     i = i.next
        # if j == self._head:
        #     self._head = k
        # self.sort1_rec(self._head, j)
        # self.sort1_rec(j.next, r)
        i, j = l, r
        priom, p = i.elem, i.next
        q = l
        while p is not r.next:
            if p.elem < priom:
                q.next = p.next
                p.next = l
                self._head = p
                l = p
            else:
                q = p
            p = p.next




    def sort1(self):
        p = self._head
        while p.next is not None:
            p = p.next
        self.sort1_rec(self._head, p)


if __name__ == '__main__':
    lst = [24,4,55,22,457,89,3,2,67,24,55]
    # print(insert_sort(lst))
    # print(merge_sort(lst))
    # print(biserch(lst, 55))
    # print(insert_sort_biserch(lst))
    # print(select_sort2(lst))
    # print(dubble_sort(lst))
    # print(dubble_sort1(lst))
    llst = LList1()
    llst.list_llist(lst)
    llst.sort1()
    # llst.printall()
    # print(quick_sort(lst))
