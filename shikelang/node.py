class Node(object):
    def __init__(self, data):
        self._data = data
        self._children = []
        self._value = None
        self.slice_variable = None
        self.slice_index = None

    def getdata(self):
        return self._data

    def setvalue(self, value):
        self._value = value

    def getvalue(self):
        return self._value

    def getchild(self, i):
        return self._children[i]

    def getchildren(self):
        return self._children

    def add(self, node):
        self._children.append(node)

    def print_node(self, prefix):
        print("  " * prefix, "+", self._data)
        for child in self._children:
            if child is None:
                print("  " * (prefix + 1), "+", "ERR: None")
            else:
                child.print_node(prefix + 1)

    def __str__(self):
        return "<Node: {}-{}>".format(self._data, self._value)

    def __repr__(self):
        return self.__str__()


def num_node(data):
    t = Node(data)
    t.setvalue(int(data))
    return t


def string_node(data):
    t = Node(data)
    t.setvalue(str(data[1:-1]))
    return t


def bool_node(data):
    t = Node(data)
    if data in ["false", "False", 0, None]:
        val = False
    else:
        val = True
    t.setvalue(val)
    return t
