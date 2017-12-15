'''
Created on 13/12/2017

@author: 

XXX: http://codeforces.com/problemset/problem/500/B
XXX: https://github.com/imressed/python-disjoint-set/blob/master/disjoint_set.py
XXX: https://gist.github.com/isaacl/7561953
XXX: https://codereview.stackexchange.com/questions/79208/disjoint-set-data-structure-in-python-3
'''

import logging
import sys
from asyncio.log import logger
from _operator import pos

nivel_log = logging.ERROR
nivel_log = logging.DEBUG
logger_cagada = None

# Python3 port of http://algs4.cs.princeton.edu/code/edu/princeton/cs/algs4/UF.java.html
class DisjointSet:
    """
    Execution:    python disjoint_set.py < input.txt
    Data files:   http://algs4.cs.princeton.edu/15uf/tinyUF.txt
                  http://algs4.cs.princeton.edu/15uf/mediumUF.txt
                  http://algs4.cs.princeton.edu/15uf/largeUF.txt
    
    Weighted quick-union by rank with path compression.
    
    % python disjoint_set.py < tinyUF.txt
    4 3
    3 8
    6 5
    9 4
    2 1
    5 0
    7 2
    6 1
    2 components
    """
    def __init__(self, n):
        # number of components
        self.count = n 
        # parent[i] = parent of i
        self.parent = list(range(n))
        # rank[i] = rank of subtree rooted at i (never more than 31)
        self.rank = [0] * n  
        self.es_raiz = set(list(range(n)))
        self.llaves = [set([x]) for x in range(n)]
        
    def find(self, p):
        """Returns the component identifier for the component 
        containing site p.
        
        Args:
            p (int): the integer representing one site
        
        Returns:
            int. the component identifier for the component containing site p
        """
        self.validate(p)
        if p != self.parent[p]:
            self.parent[p] = self.find(self.parent[p])  # path compression
        return self.parent[p]

    
    def connected(self, p, q):
        """Returns true if the the two sites are in the same component.
        
        Args:
            p (int): the integer representing one site
            q (int): the integer representing the other site
            
        Returns:
            Boolean. true if the two sites p and q are in the same component;
                false otherwise.
        """
        return self.find(p) == self.find(q)
        
    def union(self, p, q):
        """Merges the component containing site p with the 
        the component containing site q.
        
        Args:
            p (int): the integer representing one site
            q (int): the integer representing the other site
        """
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP == rootQ: return
        
        # make root of smaller rank point to root of larger rank
        if self.rank[rootP] < self.rank[rootQ]:
            self.parent[rootP] = rootQ
            self.es_raiz.remove(rootP)
            self.llaves[rootQ] |= self.llaves[rootP]
        else:
            if self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1
            self.es_raiz.remove(rootQ)
            self.llaves[rootP] |= self.llaves[rootQ]
        self.count -= 1

    def validate(self, p):
        """validate that p is a valid index"""
        n = len(self.parent)
        if p < 0 or p >= n:
            raise IndexError("index {} is not between 0 and {}".format(p, n - 1)) 
        
    def raices(self):
        return list(self.es_raiz)
    def llaves_en_conjuntos_disjuntos(self):
        return [self.llaves[x] for x in self.raices()]

def perputa_ano_nuevo_core(nodos_tam, llaves, ariscas):
    caca = DisjointSet(nodos_tam)
    for arisca in ariscas:
        if caca.connected(arisca[0], arisca[1]):
            continue
        caca.union(arisca[0], arisca[1])
    #logger_cagada.debug("las racies son {}".format(caca.raices()))
    #logger_cagada.debug("los conjuntos son {}".format(caca.llaves_en_conjuntos_disjuntos()))
    for monton in caca.llaves_en_conjuntos_disjuntos():
        nums_en_posiciones = []
        for pos_act in monton:
            nums_en_posiciones.append(llaves[pos_act])
        #logger_cagada.debug("los nums en pos {} son {}".format(monton, nums_en_posiciones))
        nums_en_posiciones.sort()
        idx_num = 0
        for pos_act in sorted(monton):
            llaves[pos_act] = nums_en_posiciones[idx_num]
            idx_num += 1
    #logger_cagada.debug("las llaves aora {}".format(llaves))
    return llaves
        

def caca_comun_lee_linea_como_num():
    return int(sys.stdin.readline().strip())

def caca_comun_lee_linea_como_monton_de_numeros():
    return list(map(int, sys.stdin.readline().strip().split(" ")))

def perputa_ano_nuevo_main():
    nodos_tam = caca_comun_lee_linea_como_num()
    llaves = caca_comun_lee_linea_como_monton_de_numeros()
    ariscas = []
    for i in range(nodos_tam):
        miedas = sys.stdin.readline().strip()
        #logger_cagada.debug("puta mierda {}".format(miedas))
        for j in range(nodos_tam):
            if miedas[j] == '1':
                ariscas.append((i, j))
        if not i:
#            assert ariscas
            pass
    #logger_cagada.debug("las ariscas {}".format(ariscas))
    fuck = perputa_ano_nuevo_core(nodos_tam, llaves, ariscas)
    print("{}".format(" ".join(map(str, fuck))))

if __name__ == '__main__':
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(level=nivel_log, format=FORMAT)
        logger_cagada = logging.getLogger("asa")
        logger_cagada.setLevel(nivel_log)
        perputa_ano_nuevo_main()
