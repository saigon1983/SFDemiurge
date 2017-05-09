class MyDict:

    def __init__(self):
        self.mapping = {}

    def __getitem__(self, item):
        return self.mapping[item]

    def add(self, object):
        self.mapping.setdefault(object.x, {})
        self.mapping[object.x][object.y] = object


class MyObject:

    def __init__(self, x, y):
        self.x = x
        self.y = y

o1 = MyObject(1,4)
o2 = MyObject(1,3)
o3 = MyObject(16,7)
o4 = MyObject(8,1)

di = MyDict()
di.add(o1)
di.add(o2)
di.add(o3)
di.add(o4)

print(di[1][4])
