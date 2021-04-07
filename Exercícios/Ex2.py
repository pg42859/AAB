# -*- coding: utf-8 -*-

class SuffixTree_2Seq:
    
    def __init__(self):
        self.nodes = { 0:(0, -1,{}) } # {root node:(numero da sequencia, se for nó será -1, {simbolo: nó a seguir})}
        self.num = 0
        self.seq1 = ""
        self.seq2 = ""

    def print_tree(self):
        for k in self.nodes.keys(): 
            if self.nodes[k][1] < 0: # se não for folha
                print (k, "->", self.nodes[k][2]) 
            else: # se for folha
                print (k,":", self.nodes[k][0],":", self.nodes[k][1])


    def add_node(self, origin, symbol, seqnum = 0, leafnum = -1): #adiciona um no que ainda não exista
        self.num += 1 #incrementa o nº do no
        self.nodes[origin][2][symbol] = self.num  #acede ao dicionário do tuplo do nó
        self.nodes[self.num] = (seqnum, leafnum,{})  # cria o no a seguir


    def add_suffix(self, p, seqnum, sufnum): #fornecido o padrão e o nº da seq
        pos = 0
        node = 0
        while pos < len(p): #enquanto a posição for inferior ao padrão
            if p[pos] not in self.nodes[node][2].keys(): # se a letra na posição pos não estiver no dicionário nó
                if pos == len(p)-1: #se a posição for a ultima do padrão
                    self.add_node(node, p[pos], seqnum, sufnum)  #adiciona a folha (nó final)
                else: #se não for a ultima posição
                    self.add_node(node, p[pos], seqnum) #adiciona um nó e o sufnum mantem-se -1
            node = self.nodes[node][2][p[pos]] #passar para o próximo no
            pos += 1 #incrementar a posição
            

    def suffix_tree_from_seq(self, s1, s2): #criar a arvore de sufixos a partir de 2 seqs
        self.seq1 = s1
        self.seq2 = s2
        seq1 = s1 + "$" #adicionar dollar ao final da s1
        seq2 = s2 + "#" #adicionar hashtag ao final da s2
        for i in range(len(seq1)):
            self.add_suffix(seq1[i:], 0, i)  #sufixos vão sendo adicionados, i representa a posicao incial do sufixo na sequencia e o 0 representa a sequencia 1
        for j in range(len(seq2)):
            self.add_suffix(seq2[j:], 1, j)  #sufixos vão sendo adicionaods, j representa a posicao incial do sufixo na sequencia e o 1 representa a sequencia 2


    def find_pattern(self, pattern):
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][2].keys():
                node = self.nodes[node][2][pattern[pos]]
            else:
                return None
        return self.get_leafes_below(node)


    def get_leafes_below(self, node):
        res1 = []
        res2 = []
        if self.nodes[node][0] == 0: #se a sequencia for a 1
            if self.nodes[node][1] >= 0: # e se o nó for uma folha
                res1.append(self.nodes[node][1]) #adicionar a posição da folha à lista
            else: #se ainda não for uma folha
                for k in self.nodes[node][2].keys(): # percorrer todas as keys do nó
                    newnode = self.nodes[node][2][k] #criar o novo nó com o k
                    leafes = self.get_leafes_below(newnode) #recursividade para chegar até à folha
                    res1.extend(leafes) #concatenar a lista da 1 sequencia com a lista das leafs
        else: #se for seq2
            if self.nodes[node][1] >= 0: #se for uma folha
                res2.append(self.nodes[node][1]) #adicionar posição à lista
            else:
                for k in self.nodes[node][2].keys(): #percorrer todas as keys do nó
                    newnode = self.nodes[node][2][k] #criar novo nó com k
                    leafes = self.get_leafes_below(newnode) #recursividade até chegar à folha
                    res2.extend(leafes) #concatenar lista da 2seq com a lista das leafs
        return res1, res2


    def largestCommonSubstring(self):
        subseq = ""  # maior sequencia será guardada
        for x in range(len(self.seq1)):  # corre a primeira sequencia
            for y in range(len(self.seq2)):  # corre a segunda sequencia
                c = 1
                while x + c <= len(self.seq1) and y + c <= len(self.seq2):  # ciclo while que vai permitir aumentar a janela a analisar em ambas as sequencias
                    if self.seq1[x:x+c] == self.seq2[y:y+c]:  # se os caracteres fruto deste splicing forem iguais de uma seq para a outra
                        if len(subseq) <= len(self.seq1[x:x+c]):  # e se o tamanho desse for maior ou igual que o tamanho da subsequencia já gravada
                            subseq = self.seq1[x:x+c]  # subsquencia comum passa a ser essa
                    c += 1  # vai correr até que o tamanho da janela supere o tamanha de uma das sequencias
        return subseq


def test():
    seq1 = "TACTA"
    seq2 = "TATGC"
    st = SuffixTree_2Seq()
    st.suffix_tree_from_seq(seq1, seq2)
    st.print_tree()
    #print (st.find_pattern("TA"))
    #print (st.get_leafes_below(0))
    #print (st.find_pattern("AGC"))
    print(st.largestCommonSubstring())

def test2():
    seq1 = "TACTA"
    seq2 = "ATGAC"
    st = SuffixTree_2Seq()
    st.suffix_tree_from_seq(seq1, seq2)
    # print (st.find_pattern("TA"))


test()
#print()
#test2()

