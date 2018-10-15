# coding: utf-8


"""
有理数的抽象数据类型
"""
class Rational:

    @staticmethod
    def _gcd(m, n):
        if n == 0:
            m, n = n, m
        while m != 0:
            m, n = n%m, m
        return n

    def __new__(cls, num, den=1):
        if isinstance(num, int) and isinstance(den, int) and den != 0:
            return super(Rational, cls).__new__(cls)
        else:
            raise ValueError

    def __init__(self, num, den=1):
        sign = 1
        if num < 0:
            num, sign = -num, -sign
        if den < 0:
            den, sign = -den, -sign

        g = Rational._gcd(num, den)

        self._num = sign * (num//g)
        self._den = den // g
        print('e')


    def num(self):
        return self._num

    def den(self):
        return self._den

    def __add__(self, other):
        if not isinstance(other, Rational):
            raise TypeError
        num = self._num * other.den() + self._den * other.num()
        den = self._den * other.den()
        return Rational(num, den)

    def __sub__(self, other):
        if not isinstance(other, Rational):
            raise TypeError
        num = self._num * other.den() - self._den * other.num()
        den = self._den * other.den()
        return Rational(num, den)

    def __mul__(self, other):
        if not isinstance(other, Rational):
            raise TypeError
        num = self._num * other.num()
        den = self._den * other.den()
        return Rational(num, den)

    def __truediv__(self, other):
        if not isinstance(other, Rational):
            raise TypeError
        num = self._num * other.den()
        den = self._den * other.num()
        return Rational(num, den)

    def __eq__(self, other):
        if not isinstance(other, Rational):
            raise TypeError
        return self._num * other.den() == self._den * other.num()

    def __lt__(self, other):
        if not isinstance(other, Rational):
            raise TypeError
        return self._num * other.den() < self._den * other.num()

    def __str__(self):
        if self._den == 1:
            r = str(self._num)
        else:
            r = str(self._num) + '/' +str(self._den)
        return r

    def printl(self):
        print(str(self._num) + '/' +str(self._num))


"""
学校人事管理系统抽象数据类型的设计
"""
import datetime

class PersonTypeError(TypeError):
    pass

class PersonValueError(ValueError):
    pass

class Person:
    _num = 0

    @classmethod
    def num(cls):
        return Person._num


    def __init__(self, name, sex, birthday, id):
        if not (isinstance(name, str) and sex in ('男', '女') and isinstance(birthday, tuple) and isinstance(id ,int)):
            raise PersonTypeError
        self._name = name
        self._sex = sex
        try:
            birth = datetime.date(*birthday)
        except:
            raise PersonValueError('Wrong date:',birthday)
        self._birthday = birth
        self._id = id
        Person._num += 1

        # self._age = datetime.datetime.now().year - datetime.date(*birthday).year

    def id(self):
        return self._id

    def name(self):
        return self._name

    def sex(self):
        return self._sex

    def birthday(self):
        return self._birthday

    def age(self):
        return datetime.datetime.now().year - self._birthday.year

    def set_name(self, rename):
        if not isinstance(rename, str):
            raise PersonTypeError('Wrong name', rename)
        self._name = rename

    def __lt__(self, other):
        if not isinstance(other, Person):
            raise PersonTypeError('Not Person',other)
        return self._id < other.id()

    def __str__(self):
        return '.'.join((self._id, self._name, self._birthday, self.sex))

    def details(self):
        return ''.join(('编号：'+ str(self._id), '姓名：'+self._name, '性别：'+self._sex, '生日：'+str(self._birthday)))

class Student(Person):
    _id_num = 0

    @classmethod
    def _id_gen(cls):
        cls._id_num += 1
        year = datetime.date.today().year
        return '1{:04}{:05}'.format(year, cls._id_num)


    def __init__(self, name, sex, birthday, department):
        Person.__init__(self, name, sex, birthday, Student._id_gen())
        self._department = department
        self._enroll_date = datetime.date.today()
        self._courses = {}

    def set_course(self, course_name):
        self._courses[course_name] = None

    def set_score(self, course_name, score):
        if course_name  not in self._courses:
            raise PersonValueError('Not set course_name', course_name)
        self._courses[course_name] = score

    def scores(self):
        return [(cname, self._courses[cname]) for cname in self._courses]

    def details(self):
        return ''.join((Person.details(self), '入学日期：'+str(self._enroll_date), '学校院系：'+self._department, '分数：'+
                        str(self.scores())))


"""
课后练习第一题
定义一个表示时间的类，提供下面的操作。
1.Time(hours, minutes, seconds)创建一个时间对象;
2.t.hours()、t.minutes()、t.seconds()分别返回时间对象t小时、分钟、秒值。
3.为Time对象定义加法和减法操作(用运算符+和-)
4.定义时间对象的等于和小于关系运算(用运算符=和<)
关于运算符的特殊函数名查看语言手册3.3.7节
"""

class Time:

    def __init__(self, hours, minutes=0, seconds=0):
        if not (isinstance(hours, int) or isinstance(minutes, int) or isinstance(seconds, int)):
            raise TypeError
        if hours>24 or minutes >60 or seconds >60:
            raise ValueError
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds

    def hours(self):
        return self._hours

    def minutes(self):
        return self._minutes

    def seconds(self):
        return self._seconds

    def __add__(self, other):
        if not isinstance(other, Time):
            raise TypeError

        h = self._hours + other.hours()
        m = self._minutes + other.minutes()
        s = self._seconds + other.seconds()
        if s > 60:
            s -= 60
            m += 1
        if m > 60:
            m -= 60
            h += 1
        if h > 24:
            h -= 24
        return Time(h, m, s)

    def  __sub__(self, other):
        if not isinstance(other, Time):
            raise TypeError
        if self < other:
            raise ValueError

        s = self._seconds
        m = self._minutes
        h = self._hours

        if s < other.seconds():
            s = s + 60 - other.seconds()
            m -= 1
        else:
            s -= other.seconds()
        if m < other.minutes():
            m = m + 60 - other.minutes()
            h -= 1
        else:
            m -= other.minutes()
        h -= other.hours()
        return Time(h, m, s)

    def __eq__(self, other):
        if not isinstance(other, Time):
            raise TypeError
        return self._hours == other.hours() and self._minutes == other.minutes() and self._seconds == other.seconds()

    def __lt__(self, other):
        if not isinstance(other, Time):
            raise TypeError
        return self._hours < other.hours() or (self._hours == other.hours() and self._minutes < other.minutes()) or (
            self._hours == other.hours() and self._minutes == other.minutes() and self._seconds < other.seconds()
        )
    def __str__(self):
        return str(self._hours)+'时'+str(self._minutes)+'分'+str(self._seconds)+'秒'

"""
课后练习第二题
请定义一个类，Date抽象数据类型，使其满足下面的条件：
1.构造表示/year/month/day的对象
2.求出d1和d2的日期差
3.计算出日期d之后n天的日期
4.计算year年之后第n天的日期
5.将日期d调整n天(n为带符号的整数)
"""

class Date:
    dan = (1, 3, 5, 7, 8, 10, 12)
    shuang = (4, 6, 9, 11)

    @staticmethod
    def month_day(year, month):
        if month in Date.dan:
            month_day = 31
        elif month in Date.shuang:
            month_day = 30
        elif (year % 4 == 0 and year % 100 != 0)  or (year % 400 == 0) or (year % 3200 == 0 and year % 172800 == 0)and month == 2:
            month_day = 29
        else:
            month_day = 28
        return month_day

    def __init__(self, year, month=1, day=1):
        self._year = year
        self._month = month
        self._day = day
        self._leap_year = 0
        if (self._year % 4 == 0 and self._year % 100 != 0)  or (self._year % 400 == 0) or (self._year % 3200 == 0 and self._year % 172800 == 0):
            self._leap_year = 1

    def year(self):
        return self._year

    def month(self):
        return self._month

    def day(self):
        return self._day

    def __sub__(self, other):
        if self._year < other.year():
            raise ValueError('date1 < date1, not sub')
        oday = 0
        print('oday1',oday,other.month())
        for i in range(1,other.month()):
            oday += Date.month_day(self._year, i)
        oday += other.day()
        sday = 0
        for j in range(other.year(), self._year):
            if (j % 4 == 0 and j % 100 != 0) or (j % 400 == 0) or (j % 3200 == 0 and j % 172800 == 0):
                sday += 366
            else:
                sday += 365
        for m in range(1,self._month):
            sday += Date.month_day(self._year, m)
        sday += self._day
        return sday - oday

    def after_day(self, n):
        month_day = Date.month_day(self._year, self._month)
        if self._day + n <= month_day :
            return Date(self._year, self._month, self._day+n)
        else:
            n -= (month_day - self._day)
        month = self._month + 1
        year = self._year
        if month == 13:
            month = 1
            year += 1

        while n > Date.month_day(year, month):
            if month == 13:
                month = 1
                year += 1
            for i in range(month, 13):
                month_day = Date.month_day(year, month)
                if n < month_day:
                    break
                n -= month_day
                month += 1
        day = n
        return Date(year, month, day)

    def num_date(self, n):
        return self.after_day(n-1)

    def adjust(self, n):
        if n >=0 :
            return self.after_day(n)
        else:
            month_day = Date.month_day(self._year, self._month)
            if self._day + n > 0:
                return Date(self._year, self._month, self._day + n)
            else:
                n += self._day
            month = self._month - 1
            year = self._year
            if month == 0:
                month = 12
                year -= 1

            while n + Date.month_day(year, month) <= 0:
                if month == 0:
                    month = 12
                    year -= 1
                for i in range(month, 0, -1):
                    month_day = Date.month_day(year, month)
                    if n + month_day > 0:
                        break
                    n += month_day
                    month -= 1
            day = month_day + n
            return Date(year, month, day)

    def __str__(self):
        return str(self._year) + '/' + str(self._month) + '/' + str(self._day)

"""
课后联系第3题
扩充本章给出的有理数类，加入一些功能：
1、其他运算符的定义。
2、各种比较和判断运算符的定于
3、转换到整数(取整)和浮点数的方法
4、给初始化函数加入从浮点数构造有理数的功能
"""

if __name__ == '__main__':
    """
    有理数
    """
    r1 = Rational('1', 2)
    # r2 = r1 + Rational(1, 4)
    # r3 = r1 - Rational(1, 4)
    # r4 = r1 * Rational(1, 4)
    # r5 = r1 / Rational(1, 4)
    # print(r2, r3, r4, r5, r1==r2, r1<r2)
    #
    # t = Time(13,16,37)
    # t1 = Time(13,15,47)
    # print(t.hours(), t.minutes(), t.seconds(), t+t1, t-t1, t1<t, t1==t)
    #
    # d = Date(2017,11,12)
    # d1 = Date(2018,5,1)
    # d2 = Date(2017)
    #
    # print(d1-d, d2.num_date(1000), d.adjust(-100000))




