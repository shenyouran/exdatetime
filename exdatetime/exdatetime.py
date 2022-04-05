class date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
class check:
    def istype(x, t, s):
        if type(x) != t:
            raise ValueError(f"Type of {s} is non-{t}: {type(x)}")
    def inrange(x, l, r, s):
        if not l <= x <= r:
            raise ValueError(f"{s} violates [{l}, {r}]")
    def inlbound(x, l, s):
        if x < l:
            raise ValueError(f"{s} should not be less than {l}")
    def inrbound(x, r, s):
        if x > r:
            raise ValueError(f"{s} should not be greater than {r}")
    def isnonzero(x, s):
        if x == 0:
            raise ValueError(f"{s} should be non-zero")
def isleap(y, isjulian = True):
    check.istype(y, int, "year")
    check.isnonzero(y, "Year")
    check.istype(isjulian, bool, "isjulian")
    if isjulian and y < 1582:
        if y < 0:
            return (-y) % 4 == 1
        return y % 4 == 0
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
def daysofmonth(y, m, isjulian = True):
    check.istype(y, int, "year")
    check.isnonzero(y, "Year")
    check.istype(m, int, "month")
    check.inrange(m, 1, 12, "Month")
    check.istype(isjulian, bool, "isjulian")
    if m == 2:
        if isleap(y, isjulian):
            return 29
        return 28
    elif m == 4 or m == 6 or m == 9 or m == 11:
        return 30
    return 31
def cmpdate(d1, d2):
    check.istype(d1, date, "date1")
    check.istype(d2, date, "date2")
    if d1.year == d2.year:
        if d1.month == d2.month:
            if d1.day == d2.day:
                return 0
            elif d1.day > d2.day:
                return 1
            return -1
        elif d1.month > d2.month:
            return 1
        return -1
    elif d1.year > d2.year:
        return 1
    return -1
class julian:
    N = 146097
    y = []
    m = []
    d = []
    status = False
    def init(self):
        if self.status:
            return
        self.status = True
        self.y.append(400)
        self.m.append(1)
        self.d.append(1)
        for i in range(1, self.N + 1):
            self.y.append(self.y[i-1])
            self.m.append(self.m[i-1])
            self.d.append(self.d[i-1] + 1)
            if self.d[i] > daysofmonth(self.y[i], self.m[i], False):
                self.m[i] += 1
                self.d[i] = 1
            if self.m[i] > 12:
                self.y[i] += 1
                self.m[i] = 1
            self.y[i-1] -= 400
        self.y[self.N] -= 400
    def getdate(self, x):
        check.istype(x, int, "julian cardinal date number")
        check.inlbound(x, 0, "Julian cardinal date number")
        self.init()
        if x > 2299160:
            x -= 2159351
            t = x // self.N * 400 + 1200
            x %= self.N
        else:
            t = x // 1461 * 4 - 4712
            x %= 1461
        return date(self.y[x] + t - (t + self.y[x] <= 0), self.m[x], self.d[x])
    def todate(self, x):
        date = self.getdate(x)
        if date.year > 0:
            return f"{date.year} {date.month} {date.day}"
        return f"BC {-date.year} {date.month} {date.day}"
    def tojulian(self, y, m, d):
        check.istype(y, int, "year")
        check.inlbound(y, -4713, "Year")
        check.istype(m, int, "month")
        check.inrange(m, 1, 12, "Month")
        check.istype(d, int, "day")
        check.inrange(d, 1, daysofmonth(y, m), "Day")
        if y == 1582 and m == 10 and 5 <= d <= 14:
            raise ValueError(f"{d} October 1582 has been deleted from the Julian calendar")
        l = 0
        r = 400 * (y + 5000)
        while l <= r:
            mid = (l + r) >> 1
            if ~cmpdate(self.getdate(mid), date(y, m, d)):
                r = mid - 1
            else:
                l = mid + 1
        return l
julian=julian()