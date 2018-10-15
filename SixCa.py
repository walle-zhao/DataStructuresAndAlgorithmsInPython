# coding: utf-8
from random import randint
from DateAndCompute.FiveCa import LQueue

class BinTNode:
    def __init__(self, dat, left=None, right=None):
        self.data = dat
        self.left = left
        self.right = right

"""
优先队列list实现
有O(1)复杂度peek，dequeue,is_empty
初始化函数是O(n)复杂度
enqueue函数是O(n)复杂度
"""
class PrioQueueList:
    def __init__(self, elist=[]):
        self._elems = list(elist)
        self._elems.sort(reverse=True)

    def is_empty(self):
        return not self._elems

    def peek(self):
        return self._elems[-1]

    def enqueue(self, e):
        i = len(self._elems) - 1
        while i >= 0:
            if e >= self._elems[i]:
                i -= 1
            else:
                break
        self._elems.insert(i+1, e)

    def dequeue(self):
        if self.is_empty():
            raise ValueError
        return self._elems.pop()

"""
优先队列的堆实现(小顶堆)，
初始时间复杂度O(n),
入队跟出队都是O(logn)
取得堆顶跟判空都是O(1)
"""
class PrioQueue:
    def __init__(self, elist=[]):  #注意默认函数为可变对象，会带来共享问题。
        self._elems = list(elist)  #所以这里用一个list进行转换，1是避免共享问题。2可以支持更多形式的可迭代对象作为实参。
        if elist:
            self.buildheap()

    def is_empty(self):
        return not self._elems

    def peek(self):
        if self.is_empty():
            raise ValueError
        return self._elems[0]

    def enqueue(self, e):
        self._elems.append(None)
        self.siftup(e, len(self._elems)-1)

    def siftup(self, e, last):
        elems, i, j = self._elems, last, (last-1)//2
        while i > 0 and e < elems[j]:
            elems[i] = elems[j]
            i, j = j, (j-1)//2
        elems[i] = e

    def dequeue(self):
        if self.is_empty():
            raise ValueError
        elems = self._elems
        e0 = elems[0]
        e = elems.pop()
        if len(elems) > 0:
            self.siftdown(e, 0, len(elems))
        return e0

    def siftdown(self, e, start, end):
        elems, i, j = self._elems, start, start*2+1
        while j < end:
            if j+1 < end and elems[j+1] < elems[j]:
                j += 1
            if e < elems[j]:
                break
            elems[i] = elems[j]
            i, j = j, j*2+1
        elems[i] = e

    def buildheap(self):
        end = len(self._elems)
        for i in range(end//2, -1, -1):
            self.siftdown(self._elems[i], i, end)

def sort_heap(elems):
    end = len(elems)
    def siftdown(elems, e, start, end):
        i, j = start, start*2+1
        while j < end:
            if j+1 < end and elems[j+1] < elems[j]:
                j += 1
            if e < elems[j]:
                break
            elems[i] = elems[j]
            i, j = j, j*2+1
        elems[i] = e

    for i in range(end//2, -1, -1):
        siftdown(elems, elems[i], i, end)

    for i in range((end-1), 0, -1):
        e = elems[i]
        elems[i] = elems[0]
        siftdown(elems, e, 0, i)
    return elems

"""
离散事件模拟系统例子：海关检查站
下面是一些条件与需求：
1、车辆按照一定的时间间隔到达，间隔有一定的随机性，设其范围为[a,b]分钟。
2、由于车辆的不同情况，每辆车的检查时间为[c,d]分钟。
3、海关可以开通K个通道。
4、希望理解开通不同数量的通道数对车辆通行的影响。
首先定义一个模拟系统的框架。
"""
class Simulation:
    def __init__(self, duration):
        self.eventg = PrioQueue()
        self._ctime = 0
        self._duration = duration

    def time(self):
        return self._ctime

    def add_event(self, event):
        self.eventg.enqueue(event)

    def run(self):
        while not self.eventg.is_empty():
            event = self.eventg.dequeue()
            self._ctime = event.time()
            if self._ctime > self._duration:
                break
            event.run()

class Event:
    def __init__(self, ctime, host):
        self._time = ctime
        self._host = host

    def __lt__(self, other):   #为优先队列的排序做比较使用，这里是按照事件发生的时间长短作为排序
        return self._time < other.time()

    def __le__(self, other):
        return self._time <= other.time()

    def time(self):
        return self._time

    def host(self):
        return self._host

    def run(self):
        pass


"""
现在假设对于检查站的模拟系统考虑如下：
1、海关的职责是检查过往的车辆，这里只模拟一个通行方向的检查。
2、假定车辆按照一定速率到达，有一定随机性，每a到b分钟有一辆车达到。
3、假定有k条检查通道，检查一辆车耗时c到d分钟。
4、到达的车辆在一条专用线路上排队等待，一旦有一个检查通道空闲，正在排队的第一辆车就进入该通道检查。
如果车辆到达时，有空闲通道而且当时没有等待车辆，它就立即进入通道开始检查。
5、希望得到的数据包括车辆的平均等待时间和通过检车站的平均时间。
"""

class Customs:
    def __init__(self, gate_num, duration, arrive_interval, check_interval, ):
        self.simulation = Simulation(duration)
        self.gates = [0] * gate_num
        self.waitline = LQueue()
        self.duration = duration
        self.total_wait_time = 0
        self.total_used_time = 0
        self.car_num = 0
        self.arrive_interval = arrive_interval
        self.check_interval = check_interval

    def wait_time_acc(self, n):
        self.total_wait_time += n

    def total_time_acc(self, n):
        self.total_used_time += n

    def car_count_1(self):
        self.car_num += 1

    def add_event(self, event):
        self.simulation.add_event(event)

    def cur_time(self):
        return self.simulation.time()

    def enqueue(self, car):
        self.waitline.enqueue(car)

    def has_queued_car(self):
        return not self.waitline.is_empty()

    def next_car(self):
        return self.waitline.dequeue()

    def find_gate(self):
        for i in range(len(self.gates)):
            if self.gates[i] == 0:
                self.gates[i] = 1
                return i
        return None

    def free_gate(self, i):
        if self.gates[i] == 1:
            self.gates[i] = 0
        else:
            raise ValueError('free_gate',i)

    def simulation(self):
        Arrive(0, self)
        self.simulation.run()
        self.statistics()

    def statistics(self):
        print('Simulate' + str(self.duration) + 'minutes, for' + str(len(self.gates)) + 'gates' )
        print(self.car_num, 'cars pass the customs')
        print('Average waiting time:', self.total_wait_time/self.car_num)
        print('Average passing time:', self.total_used_time/self.car_num)
        i = 0
        while not self.waitline.is_empty():
            self.waitline.dequeue()
            i += 1
        print(i, 'cars are waiting line')

class Car:
    def __init__(self, arrive_time):
        self.time = arrive_time

    def arrive_time(self):
        return self.time

def event_log(time, name):
    print('Event:'+ name + ',happens at' + str(time))

class Arrive(Event):
    def __init__(self, arrive_time, customs):
        super(Arrive, self).__init__(arrive_time, customs)
        customs.add_event(self)

    def run(self):
        customs, time = self.host(), self.time()
        event_log(time, 'car arrive')
        Arrive(time + randint(*customs.arrive_val), customs)
        car = Car(time)
        if customs.has_queued_car():
            customs.enqueue(car)
            return
        i = customs.find_gate()
        if i is not None:
            event_log(time, 'car check')
            Leave(time + randint(*customs.check_interval), i, car, customs)
        else:
            customs.enqueue(car)

class Leave(Event):
    def __init__(self, ctime, gate_num, car, customs):
        super(Leave, self).__init__(ctime, customs)
        self.car = car
        self.gate_num = gate_num
        customs.add_event(self)

    def run(self):
        customs, time = self.host(), self.time()
        event_log(time, 'car leave')
        customs.free_gate(self.gate_num)
        customs.car_count_1()
        customs.total_time_acc(time - self.car.arrive_time())
        if customs.has_queued_car():
            car = customs.next_car()
            i = customs.find_gate()
            event_log(time, 'car check')
            customs.wait_time_acc(time - car.arrive_time())
            Leave(time + randint(*customs.check_interval), i, car, customs)



