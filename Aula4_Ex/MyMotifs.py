# -*- coding: utf-8 -*-

def createMatZeros (nl, nc):
    res = [ ] 
    for i in range(0, nl):
        res.append([0]*nc)
    return res

def printMat(mat):
    for i in range(0, len(mat)): print(mat[i])

class MyMotifs:

    def __init__(self, seqs):
        self.size = len(seqs[0])
        self.seqs = seqs # objetos classe MySeq
        self.alphabet = seqs[0].alfabeto()
        self.doCounts()
        self.createPWM()
        
    def __len__ (self):
        return self.size        
        
    def doCounts(self):
        self.counts = createMatZeros(len(self.alphabet), self.size)
        for s in self.seqs:
            for i in range(self.size):
                lin = self.alphabet.index(s[i])
                self.counts[lin][i] += 1
    
    def doCounts_ps(self):
        self.counts = createMatZeros(len(self.alphabet), self.size) #cria matriz de zeros
        for j in range(len(self.counts)): #para cada linha da matriz
            for i in range(len(self.counts[0])): #para cada coluna da matriz
                self.counts[j][i] +=1 #adiciona 1 a todos valores
            for s in self.seqs:
                for i in range(self.size): #vai preenchendo a matriz tendo em conta a ocorrencia de cada caracter (nucleotidos)
                    lin = self.alphabet.index(s[i])
                    self.counts[lin][i] +=1
                
    def createPWM(self):
        self.doCounts() #faz matriz contagens
        self.pwm = createMatZeros(len(self.alphabet), self.size) #cria uma matriz de zeros com 4 linhas e nº de colunas do tamanho da seq
        for i in range(len(self.alphabet)): #percorre as linhas
            for j in range(self.size): #percorre as colunas
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs) #divide o valor presente na matriz contagens pelo numero de seqs, mudando na matriz de zeros
    
    def createPWM_ps(self):
        self.doCounts_ps() #faz matriz das pseudo-contagens
        self.pwm = createMatZeros(len(self.alphabet), self.size) #matriz de zeros
        for i in range(len(self.alphabet)): #percorre as linhas
            for j in range(self.size): #percorre as colunas
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs) #divide o valor presente na matriz contagens pelo numero de seqs, substituindo na matriz de zeros
                
    def consensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]        
        return res

    def maskedConsensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self.alphabet[maxcoli]        
            else:
                res += "-"
        return res

    def probabSeq (self, seq): #uma seq inteira
        res = 1.0
        for i in range(self.size): #percorre todas as posições da seq
            lin = self.alphabet.index(seq[i]) #tendo em conta o alfabeto, encontra a linha para ser usada na pwm
            res *= self.pwm[lin][i] #multiplica-se o valor
        return res
    
    def probAllPositions(self, seq): #recebe uma seq e vai calculando as probabilidades de cada posição
        res = []
        for k in range(len(seq)-self.size+1):
            res.append(self.probabSeq(seq)) #dúvida
        return res

    def mostProbableSeq(self, seq): #recebe uma seq
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.size): #itera num range entre o tamanho da seq menos o tamanho do motif
            p = self.probabSeq(seq[k:k+ self.size]) #probabilidade de cada motif ocorrer
            if(p > maximo): #devolve maior probabilidade
                maximo = p
                maxind = k
        return maxind #indice com maior probabilidade

def test():
    # test
    from MySeq import MySeq
    seq1 = MySeq("AAAGTT")
    seq2 = MySeq("CACGTG")
    seq3 = MySeq("TTGGGT")
    seq4 = MySeq("GACCGT")
    seq5 = MySeq("AACCAT")
    seq6 = MySeq("AACCCT")
    seq7 = MySeq("AAACCT")
    seq8 = MySeq("GAACCT")
    lseqs = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    motifs = MyMotifs(lseqs)
    printMat (motifs.counts)
    motifs.doCounts_ps()
    printMat(motifs.count)
    print()
    printMat (motifs.pwm)
    motifs.createPWM_pseudo()
    printMat(motifs.pwm)
    print(motifs.alphabet)
    
    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))
    
    print(motifs.consensus())
    print(motifs.maskedConsensus())

if __name__ == '__main__':
    test()
