import math
from DateAndCompute.SixCa import BinTNode
from DateAndCompute.FiveCa import SStack

class Assoc:
    def __init__(self, key, value):
        self.key = key
        self.value = value
    def __lt__(self, other):
        return self.key < other.key
    def __le__(self, other):
        return self.key <= other.key
    def __str__(self):
        return 'Assoc({0},{1})'.format(self.key, self.value)

"""
采用顺序表实现的dic
其中使用二分查找进行检索。检索效率为O(log n)
但是，插入操作跟删除操作，由于顺序表的特征，还是需要O(n)
"""
class DicList:
    def __init__(self):
        self._elems = []

    def is_empty(self):
        return self._elems is None

    def num(self):
        return len(self._elems)

    def search(self, key):
        elems = self._elems
        dlen = self.num()
        low, high = 0, dlen-1
        while low <= high:
            mid = low + (high - low) // 2
            if key == elems[mid].key:
                return mid,elems[mid].value
            elif key < elems[mid].key:
                high = mid - 1
            else:
                low = mid + 1
        return low

    def insert(self, key, value):
        sult = self.search(key)
        if isinstance(sult, tuple):
            self._elems[sult[0]].value = value
        else:
            self._elems.insert(sult, Assoc(key, value))

    def delete(self, key):
        sult = self.search(key)
        if isinstance(sult,tuple):
            i, value = sult
            self._elems.pop(i)
            return value
        raise KeyError(key)

    def values(self):
        for i in range(self.num()):
            yield self._elems[i].value

    def entries(self):
        for i in range(self.num()):
            yield self._elems[i].key,self._elems[i].value

"""
基于顺序表实现集合
判断是否在集合，O(n)
交集、并集、差集，O(m*n)
"""
class LSet:
    def __init__(self):
        self._elems = []

    def length(self):
        return len(self._elems)

    def elems(self):
        for i in self._elems:
            yield i

    def __str__(self):
        r = ''
        for i in self.elems():
            r += str(i) + ', '
        return r

    def get_elem(self, i):
        return self._elems[i]

    def is_empty(self):
        return self._elems is None

    def member(self, elem):
        return elem in self._elems

    def insert(self, elem):
        if elem not in self._elems:
            self._elems.append(elem)

    def delete(self, elem):
        for i in range(len(self._elems)):
            if elem == self._elems[i]:
                self._elems.pop(i)
                return
        raise KeyError('LSet Delete Error, Not elem')

    def intersection(self, oset):
        if not isinstance(oset, LSet):
            raise TypeError('OsetTypeValue, intersection')
        new_set = LSet()
        for i in self.elems():
            for j in oset.elems():
                if i == j:
                    new_set.insert(i)
        return new_set

    def union(self, oset):
        if not isinstance(oset, LSet):
            raise TypeError('OsetTypeValue, union')
        new_set = LSet()
        for i in self.elems():
            new_set.insert(i)
        for j in oset.elems():
            if not new_set.member(j):
                new_set.insert(j)
        return new_set

    def different(self, oset):
        if not isinstance(oset, LSet):
            raise TypeError('OsetTypeValue, union')
        new_set = LSet()
        for i in self.elems():
            if not oset.member(i):
                new_set.insert(i)
        return new_set

    def subset(self, oset):
        if not isinstance(oset, LSet):
            raise TypeError('OsetTypeValue, union')
        count = 0
        for i in self.elems():
            if oset.member(i):
                count += 1
        return count == len(self._elems)

"""
基于排序顺序表实现集合
主要是检索使用二分查找，O(log n)
交集、并集、差集，O(m+n)
"""
class LSet1(LSet):
    def member(self, elem):
        low, high = 0, len(self._elems)-1
        while low <= high:
            mid = low + (high-low) // 2
            if elem == self._elems[mid]:
                return True
            elif elem < self._elems[mid]:
                high = mid - 1
            else:
                low = mid + 1
        return False

    def search(self, elem):
        low, high = 0, len(self._elems) - 1
        while low <= high:
            mid = low + (high - low) // 2
            if elem == self._elems[mid]:
                return mid
            elif elem < self._elems[mid]:
                high = mid - 1
            else:
                low = mid + 1
        return low

    def insert(self, elem):
        if self.member(elem):
            return
        self._elems.insert(self.search(elem), elem)

    def delete(self, elem):
        if not self.member(elem):
            raise KeyError('LSet Delete Error, Not elem')
        self._elems.pop(self.search(elem))

    def intersection(self, oset):
        if not isinstance(oset, LSet):
            raise TypeError('OsetTypeValue, intersection')
        i, j = 0, 0
        new_set = LSet1()
        while i < len(self._elems) and j < oset.length():
            if self._elems[i] < oset.get_elem(j):
                i += 1
            elif self._elems[i] > oset.get_elem(j):
                j += 1
            else:
                new_set.insert(self._elems[i])
                i += 1
                j += 1
        return new_set

    def union(self, oset):
        if not isinstance(oset, LSet):
            raise TypeError('OsetTypeValue, union')
        i, j = 0, 0
        new_set = LSet1()
        while i < len(self._elems) and j < oset.length():
            if self._elems[i] < oset.get_elem(j):
                new_set.insert(self._elems[i])
                i += 1
            elif self._elems[i] > oset.get_elem(j):
                new_set.insert(oset.get_elem(j))
                j += 1
            else:
                new_set.insert(self._elems[i])
                i += 1
                j += 1
        while i < len(self._elems):
            new_set.insert(self._elems[i])
            i += 1
        while j < oset.length():
            new_set.insert(oset.get_elem(j))
            j += 1
        return new_set

    def different(self, oset):
        if not isinstance(oset, LSet):
            raise TypeError('OsetTypeValue, different')
        i, j = 0, 0
        new_set = LSet1()
        while i < len(self._elems) and j < oset.length():
            if self._elems[i] < oset.get_elem(j):
                new_set.insert(self._elems[i])
                i += 1
            elif self._elems[i] > oset.get_elem(j):
                j += 1
            else:
                i += 1
                j += 1
        while i < len(self._elems):
            new_set.insert(self._elems[i])
            i += 1
        return new_set

"""
采用散列表实现的集合
其中散列表初始长度设置为8，
当均衡因子大于0.7的时候，会扩大散列表的容量，为原来的4倍。
解决冲突的方法，使用的方法是内消解的开地址法(具体是使用双散列探查方式)。
这种方法有个缺陷是，一个集合使用时间长，它的效率就会逐渐变低。
当然，如果要均衡因子大于0.7进行扩容后，又变成新的结构了。
散列函数是用的除余法(对小于容量的最大素数进行求余运算)
"""
class HSet:
    # 判断整数n是不是素数
    @staticmethod
    def prime(n):
        if n == 1:
            return False
        t = int(math.sqrt(n) + 1)
        for i in range(2, t):
            if n % i == 0:
                return False
        return True

    #将字符串转化成31进制的整数
    @staticmethod
    def set_hash(key):
        h1 = 0
        for i in key:
            h1 = 31 * h1 + ord(i)
        return h1

    def __init__(self, length = 8):
        self._elems = [None] * length
        self._length = length #哈希表的长度
        self._prime = 7 #self._length的初始最大素数为7
        self._elelength = 0 #哈希表中实际的元素个数
        self._loadfac = 0.0 #负载因子

    # 取得比容量值小的最大素数
    def get_max_prime(self):
        for i in range(self.hllength(), -1, -1):
            if HSet.prime(i):
                self._prime = i
                return self._prime
        raise ValueError('get_max_prime error, prime is too small')

    # 重新计算负载因子
    def recal_loadfac(self):
        self._loadfac = round(self._elelength/self._length, 1)  #保留一位小数
        return self._loadfac

    # 判断是否为空
    def is_empty(self):
        for i in range(self._length):
            if self._elems[i] is not None and self._elems[i] is not False:
                return False
        return True

    # 哈希表的容量
    def hllength(self):
        return self._length

    # 实际存在的元素个数
    def elelength(self):
        return self._elelength

    # 判断元素是否在集合里面
    def member(self, elem):
        index = self.search_index(elem)
        if self._elems[index] == elem:
            return True
        return False

    # 查找插入点的下标
    def get_insert_index(self, key):
        if isinstance(key, str):
            int_key = HSet.set_hash(key)
        else:
            int_key = key
        f_index = int_key % self._prime
        for i in range(0, self._length):
            d = i * (int_key % 5 + 1)
            index = (f_index + d) % self._prime
            if self._elems[index] is None or self._elems[index] is False or self._elems[index] is key:
                return index
        raise ValueError('Explore_index Error,change hash list')

    # 查找key，如果存在返回下标，不存在返回False
    def search_index(self, key):
        if isinstance(key, str):
            int_key = HSet.set_hash(key)
        else:
            int_key = key
        f_index = int_key % self._prime
        for i in range(0, self._length):
            d = i * (int_key % 5 + 1)
            index = (f_index + d) % self._prime
            if self._elems[index] == key:
                return index
            elif self._elems[index] is None:
                return False
        raise ValueError('Serach_index Error,change hash list')

    #扩大哈希表的容量
    def extend(self):
        self._length *= 4
        old_elems = self._elems
        self._elems = [None] * self._length
        self._elelength = 0
        self.get_max_prime()
        for i in range(len(old_elems)):
            if old_elems[i] is not None and old_elems[i] is not False:
                self.insert(old_elems[i])
        old_elems.clear()

    #遍历集合元素
    def entries(self):
        elems = self._elems
        for i in range(self._length):
            if (elems[i] is not None) and (elems[i] is not False):
                yield elems[i]

    # 集合里面插入元素
    def insert(self, elem):
        loadfac = self.recal_loadfac()
        if loadfac >= 0.7:
            self.extend()   #扩大哈希表的容量
        index = self.get_insert_index(elem)
        if self._elems[index] == elem:
            return
        else:
            self._elems[index] = elem
        self._elelength += 1

    def delete(self, elem):
        index = self.search_index(elem)
        if index and self._elems[index] == elem:
            self._elems[index] = False
        else:
            raise KeyError('Delete Error, not exist key')
        self._elelength -= 1

    def intersection(self, oset):
        if not isinstance(oset, HSet):
            raise TypeError('HsetTypeValue, intersection')
        new_set = HSet()
        for elem in self.entries():
            if oset.member(elem):
                new_set.insert(elem)
        return new_set

    def union(self, oset):
        if not isinstance(oset, HSet):
            raise TypeError('HsetTypeValue, union')
        new_set = HSet()
        for elem in self.entries():
            new_set.insert(elem)
        for elem in oset.entries():
            new_set.insert(elem)
        return new_set

    def different(self, oset):
        if not isinstance(oset, HSet):
            raise TypeError('HsetTypeValue, different')
        new_set = HSet()
        for elem in self.entries():
            if not oset.member(elem):
                new_set.insert(elem)
        return new_set

    def get_elems(self):
        return self._elems

"""
采用二叉排序树实现字典。
利用二叉树的平均高度远小于树中结点的性质，来实现二叉树的高效率操作。
"""
class DictBinTree:
    def __init__(self):
        self._root = None

    def is_empty(self):
        return self._root is None

    def search(self, key):
        bt = self._root
        while bt is not None:
            entry = bt.data
            if key < entry.key:
                bt = bt.left
            elif key > entry.key:
                bt = bt.right
            else:
                return bt.data.value
        return None

    def insert(self, key, value):
        if self._root is None:
            self._root = BinTNode(Assoc(key, value))
        bt = self._root
        while bt is not None:
            entry = bt.data
            if key < entry.key:
                if bt.left is None:
                    bt.left = BinTNode(Assoc(key, value))
                bt = bt.left
            elif key > key.data:
                if bt.right is None:
                    bt.right = BinTNode(Assoc(key, value))
                bt = bt.right
            else:
                bt.data.value = value
                return

    def values(self):
        t, s = self._root, SStack()
        while t is not None or not s.is_empty():
            while t is not None:
                s.push(t)
                t = t.left
            t = s.pop()
            yield t.data.value
            t = t.right

    def entries(self):
        t, s = self._root, SStack()
        while t is not None or not s.is_empty():
            while t is not None:
                s.push(t)
                t = t.left
            t = s.pop()
            yield t.data.key, t.data.value
            t = t.right

    def delete(self, key):
        p, q = None, self._root  #初始化p, q
        while q is not None and q.data.key != key: #找到要删除的结点q和它的父结点q。
            p = q
            if key < q.data.key:
                q = q.left
            else:
                q = q.right
        if q is None: #key并不在二叉树内。
            return
        if q.left is None:  #当要删除的结点q的左子树为空时的情况。
            if p is None:  #要删除的结点q是根结点。
                self._root = q.right
            elif q is p.left:  #要删除的结点q是父结点p的左子树
                p.left = q.right
            else:               #要删除的结点q是父结点p的右子树
                p.right = q.right
            return
        r = q.left     #否则，要删除的结点q的左子树不为空，并且找到q的左子树的最右结点r
        while r.right is not None:
            r = r.right
        r.right = q.right   #将要删除的结点q的右子树接到r的右子树上
        if p is None:   #当q的左子树不为空时，要删除的结点q是根结点。
            self._root = q.left
        elif q is p.left: # 当q的左子树不为空时，并且q是父结点p的左子树
            p.left = q.left
        else:              # 当q的左子树不为空时，q是父结点p的右子树
            p.right = q.left

    def print(self):
        for k, v in self.entries():
            print(k, v)

# def build_dictBinTree(entries):
#     dic = DictBinTree
#     for k, v in

if __name__ == '__main__':
    # dic = DicList()
    # dic.insert('walle',29)
    # dic.insert('eva',21)
    # dic.insert('cici', 4)
    # dic.insert('seci', 20)
    # dic.insert('wuci',23)
    # dic.insert('qiqi',15)
    # dic.insert('seven',26)
    # dic.insert('elen',32)
    # dic.insert('allen',25)
    # dic.insert('cici', 21)
    # print(dic.search('cici'))
    # for i in dic.entries():
    #     print(i)
    # lset = LSet()
    # lset.insert(12)
    # lset.insert(13)
    # lset.insert(65)
    # lset.insert(89)
    # lset.insert(19)
    # lset.insert(21)
    # lset.insert(34)
    # lset.insert(70)
    # lset.insert(99)
    # lset.insert(67)
    # oset = LSet()
    # oset.insert(23)
    # oset.insert(33)
    # oset.insert(65)
    # oset.insert(89)
    # oset.insert(19)
    # oset.insert(21)
    # oset.insert(34)
    # oset.insert(66)
    # oset.insert(98)
    # oset.insert(78)
    # aset = LSet()
    # aset.insert(12)
    # print(lset.intersection(oset))
    # print(lset.union(oset))
    # print(lset.different(oset))
    # print(aset.subset(lset))
    #
    # for elem in lset.elems():
    #     print(elem)
    #
    # lset = LSet1()
    # lset.insert(12)
    # lset.insert(13)
    # lset.insert(65)
    # lset.insert(89)
    # lset.insert(19)
    # lset.insert(21)
    # lset.insert(34)
    # lset.insert(70)
    # lset.insert(99)
    # lset.insert(67)
    # oset = LSet1()
    # oset.insert(23)
    # oset.insert(33)
    # oset.insert(65)
    # oset.insert(89)
    # oset.insert(19)
    # oset.insert(21)
    # oset.insert(34)
    # oset.insert(66)
    # oset.insert(98)
    # oset.insert(78)
    # aset = LSet1()
    # aset.insert(12)
    # print(lset.intersection(oset))
    # print(lset.union(oset))
    # print(lset.different(oset))
    # print(aset.subset(lset))
    #
    # for elem in lset.elems():
    #     print(elem)

    hset = HSet()
    hset.insert('walle')
    hset.insert('eva')
    hset.insert('cici')
    hset.insert('seci')
    ohset = HSet()
    ohset.insert('walle')
    ohset.insert('eva')
    ohset.insert('cici')
    ohset.insert('allen')
    print(hset.intersection(ohset).get_elems())
    print(hset.union(ohset).get_elems())
    print(hset.different(ohset).get_elems())

    # hset.insert('seven')
    # hset.insert('eight')
    # hset.insert('nine')
    # hset.insert('one')
    # hset.insert('two')
    # hset.insert('three')
    # hset.insert('four')
    # hset.insert('five')
    # hset.insert('six')
    # hset.insert('eleven')
    # hset.insert('twift')
    # hset.insert('thity')
    # hset.insert('forth')
    # hset.insert('fivth')
    # hset.insert('dsd')

    # hset.delete('walle')
    # hset.delete('two')
    # hset.delete('eva')

    # hset.delete('three')
    # print(hset.get_elems())
    # print(hset.recal_loadfac())
    # print(hset.member('walle'))
    # print(hset.member('eva'))
    # print(hset.member('three'))


