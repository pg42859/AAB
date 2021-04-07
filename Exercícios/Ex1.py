# -*- coding: utf-8 -*-

class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node
        self.num = 0
        sef.seq = ""
    
    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0: # se não for folha
                print (k, "->", self.nodes[k][1]) 
            else: # se for folha 
                print (k, ":", self.nodes[k][0])
                
    def add_node(self, origin, symbol, leafnum = -1): #adiciona um no que ainda não exista
        self.num += 1 #incrementa o nº do no
        self.nodes[origin][1][symbol] = self.num #acede ao dicionário do tuplo do nó
        self.nodes[self.num] = (leafnum,{}) #cria o tuplo para o no a seguir
        
    def add_suffix(self, p, sufnum): # fornecido o padrão e a posição no padrão
        pos = 0
        node = 0
        while pos < len(p): #enquanto a posição for inferior ao padrão
            if p[pos] not in self.nodes[node][1].keys(): # se a letra na posição pos não estiver no dicionário nó
                if pos == len(p)-1: #se a posição for a última do padrão ($)
                    self.add_node(node, p[pos], sufnum) #adiciona a folha (no final)
                else: #se não for $
                    self.add_node(node, p[pos]) #adiciona um no, sendo que o sufnum se mantem -1
            node = self.nodes[node][1][p[pos]] #passar para o próximo no
            pos += 1 # incrementar a posição
    
    def suffix_tree_from_seq(self, text): #criar a arvore de sufixos a partir de uma sequencia
        self.seq = text
        t = text+"$" #adicionar dollar no final da seq
        for i in range(len(t)):
            self.add_suffix(t[i:], i) #os sufixos vão sendo adicionados
            
    def find_pattern(self, pattern): #procura um padrão e retorna a sua posição inicial   
        node = 0
        for pos in range(len(pattern)): #percorre o padrão 
            if pattern[pos] in self.nodes[node][1].keys(): #se o caracter estiver no dicionário
                node = self.nodes[node][1][pattern[pos]] # diz o valor do no que se deve ir para continuar a ver o sufixo
            else: return None
        return self.get_leafes_below(node) #se o padrão for encontrado, devolve uma lista com os nós da arvore onde começa o padrão
        

    def get_leafes_below(self, node): #encontrar as folhas que estão por baixo de um nó
        res = []
        if self.nodes[node][0] >=0: # se o nó for uma folha o padrão foi encontrado
            res.append(self.nodes[node][0]) #adicionar a posição da folha à lista            
        else: #se ainda não for uma folha
            for k in self.nodes[node][1].keys(): # percorrer todas as keys do nó
                newnode = self.nodes[node][1][k] # criar o novo nó com k
                leafes = self.get_leafes_below(newnode) # recursivividade para chegar até à folha
                res.extend(leafes) #concatenar a lista res com a lista das leafes
        return res
    

    #Ex 1a
    def nodes_below(self, node):
        res = []
        if node in self.nodes.keys(): # se o nó estiver presente na árvore
            for x in self.nodes[node][1].values(): # para cada nó proveniente do nó dado
                res.append(x) #adicionar à lista 
            for n in res: #para cada nó na lista resultado
                for y in self.nodes[n][1].values(): # para cada nó proveniente do nó n
                    res.append(y) #adicionar à lista
            return res
        else:
            return None

    
    #Ex 1b
    def matches_prefix(self, prefix):
        if self.find_pattern(prefix) is None: #ver se o prefixo existe
            return None
        else:
            res = []
            padrao = self.find_pattern(prefix) #posições dos nós do padrão
            s = self.seq
            for a in padrao: #iterar os nós do padrão
                k = len(seq) - a #tamanho da sequencia que ainda não foi percorrida
                tamanho = len(prefix) #tamanho da tentativa atual, começa por ser do tamanho do prefixo
                while k >= tamanho: #enquanto o tamanho da tentativa atual é menor do que o tamanho da sequencia não percorrida
                    res.append(s[a : a+k]) #adiciona à lista a parte da sequencia em foco
                    tamanho += 1 #incrementação para quebrar o ciclo
        return res


def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print (st.find_pattern("TA"))
    print (st.find_pattern("ACG"))
    print (st.nodes_below())
    print(st.matches_prefix("TA"))

def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print (st.find_pattern("TA"))
    print(st.repeats(2,2))

test()
test2()
        
            
    
    
