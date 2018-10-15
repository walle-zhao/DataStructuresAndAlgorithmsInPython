inf = float('inf')

class Graph:
    def __init__(self, mat, unconn=0):
        vnum = len(mat)
        for i in mat:
            if len(i) != vnum:
                raise ValueError
        self._vnum = vnum
        self._unconn = unconn
        self._mat = [mat[i][:] for i in range(num)]

    def vertes_num(self):
        return self._vnum

    def _invalid(self, v):
        return 0 > v or self._vnum -1 < v

    def add_vertes(self):
        raise ValueError('Graph Error op')

    def add_edge(self, vi, vj, val=1):
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError
        self._mat[vi][vj] = val

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError
        return self._mat[vi][vj]

    def out_edges(self, vi):
        if self._invalid(vi):
            raise ValueError
        return self._out_edges(self._mat[vi], self._unconn)

    @staticmethod
    def _out_edges(row, unconn):
        edges = []
        for i in range(len(row)):
            if row[i] != unconn:
                edges.append((i,row[i]))
        return edges

class GraphAL(Graph):
    def __init__(self, mat=[], unconn=0):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise ValueError
        self._vnum = vnum
        self._mat = [Graph._out_edges(mat[i], unconn) for i in range(vnum)]
        self._unconn = unconn

    def add_vertes(self):
        self._mat.append([])
        self._vnum += 1
        return self._vnum - 1

    def add_edge(self, vi, vj, val=1):
        if self._vnum == 0:
            raise ValueError
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError
        row = self._mat[vi]
        i = 0
        while i < len(row):
            if row[i][0] == vj:
                self._mat[vi][i] = (vj, val)
            if row[i][0] > vj:
                break
            i += 1
        self._mat[vi].insert(i,(vj, val))

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError
        for i, val in self._mat[vi]:
            if i == vj:
                return val
        return self._unconn

    def out_edges(self, vi):
        if self._invalid(vi):
            raise ValueError
        return self._mat[vi]

