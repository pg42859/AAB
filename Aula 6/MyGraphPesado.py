# -*- coding: utf-8 -*-

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g    

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    def print_graph_costs(self):
        for a in self.graph.keys():
            for b in self.graph[a]:
                print(a, " => ", b[0], "costing", b[1])


    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())
        
    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d[0]))
        return edges

    def get_weights(self):
        ''' Returns a list with the costs of the graph '''
        custo = []
        for a in self.graph.values():
            custo.append(a[1])
        return custo
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
       
    
    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []
        
    def add_edge_w_cost(self, o, d, c):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph, receives the origin, the destiny and the cost associated ''' 
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o]: #se o vertice destino ainda não estiver associado
            self.graph[o].append(d, c) #adiciona-se o destino e o custo associado à travessia da origem para o destino

        
    def get_successors(self, v):
        l = []
        for a in self.graph[v]: #para cada tuplo da lista do nó fornecido
            l.append(a[0]) #adiciona o primeiro elemento do tuplo, que corresponde ao nó de destino, sendo o sucessor
        return l
             
    def get_predecessors(self, v):
        res = []
        for k in self.graph.keys(): #para todas as keys do graph
            destino = []
            for a in self.graph[k]: #para cada tuplo da key do ciclo anterior
                destino.append(a[0]) #vai adicionar o primeiro elemento do tuplo, correspondente ao destino
            if v in destino: # se o v estiver na lista de destinos
                res.append(k) #essa key será um predecessor
        return res
    
    def get_adjacents(self, v):
        suc = self.get_successors(v) #atribuir a lista dos sucessores a suc
        pred = self.get_predecessors(v) #atribuir a lista dos predecessors a pred
        res = []
        res.extend(pred) #adicionar os predecessors à lista resultado
        for a in suc: #para cada node na lista de sucessores
            if a not in res: #se esse node não estiver na lista resultado
                res.append(p) #adicionar esse node ao resultado
        return res
        
    ## degrees fica igual ao grafo normal, pois cada tuplo é considerado um unico elemento   
    
    def out_degree(self, v):
        return len(self.graph[v])
    
    def in_degree(self, v):
        return len(self.get_predecessors(v))
        
    def degree(self, v):
        return len(self.get_adjacents(v))
        
    
    def distance(self, s, d):
        ''' Return da distancia entre s e d com menor custo/peso'''
        if s == d: return 0
        l = [(s,0)] #lista de tuplos que guarda o node e o custo
        visited = [s] #lista onde estão os nodes já visitados
        score = 0
        while len(l) > 0: #enquanto a lista l tiver não for vazia
            node, score = l.pop(0) #node fica a ser o primeiro elemento do tuplo e o score o segundo, este tuplo é retirado da lista l, diminuindo assim o tamanho da lista
            for elem in self.graph[node]: #corre a lista que contem os tuplos com o node de destino e o custo
                if elem[0] == d: #se o no de destino for igual ao destino dado como parametro
                    return dist + 1 #dá return ao score
                elif elem[0] not in visited: #caso não se encontre o node
                    l.append((elem[0], score + elem[1])) #volta-se a adicionar o elemento à lista l, assim como o custo acumulado
                    visited.append(elem) #adiciona-se o node à lista dos visitados
        return None
        
    def shortest_path(self, s, d): #para além de dar return ao caminho com menor peso, retorna também os nodes por onde passa
        if s == d: return [s,d, 0] #se os vertices dados forem o mesmo
        l = [(s,[],0)] #tuplo com o node de origem s, lista de nodes até chegar a d, por fim, custo acumulado
        visited = [s] #lista que guarda os vertices já visitados
        while len(l) > 0: #enquanto a lista l não for vazia
            node, preds, score = l.pop(0) #atribuir cada elemnto do tuplo a uma variar e retirar o tuplo da lista l
            for elem in self.graph[node]: #corre todos os tuplos do node
                if elem[0] == d: #se o nó de destino for igual ao destino dado como parametro
                    return preds+[node, elem[0]], score + elem[1] #retorna-se o caminho gravado e o custo acumulado
                elif elem[0] not in visited: #se o node não for igual ao destino e ainda não tiver sido visitado
                    l.append((elem[0], preds + [node], score + elem[1])) #adiciona-se esse node, o caminho até ao momento e o score acumulado à lista l 
                    visited.append(elem) #adiciona-se o node aos visitados
        return None
        
    def reachable_with_dist(self, s):
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))
        return res

## cycles
    def node_has_cycle (self, v):
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res


def is_in_tuple_list (tl, val):
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res


def test1():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print (gr.get_nodes())
    print (gr.get_edges())
    

def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()
  
def test3():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()

    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))

def test4():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    
    print (gr.distance(1,4))
    print (gr.distance(4,3))

    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    print (gr.reachable_with_dist(1))
    print (gr.reachable_with_dist(3))

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    
    print (gr2.distance(2,1))
    print (gr2.distance(1,5))
    
    print (gr2.shortest_path(1,5))
    print (gr2.shortest_path(2,1))

    print (gr2.reachable_with_dist(1))
    print (gr2.reachable_with_dist(5))

def test5():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.node_has_cycle(2))
    print (gr. node_has_cycle(1))
    print (gr.has_cycle())

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2. node_has_cycle(1))
    print (gr2.has_cycle())


if __name__ == "__main__":
    test1()
    #test2()
    #test3()
    #test4()
    #test5()
