# -*- coding: utf-8 -*-

from MySeq import MySeq
from MyMotifs import MyMotifs

class MotifFinding:
    
    def __init__(self, size = 8, seqs = None):
        self.motifSize = size
        if seqs is not None:
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []
                    
    def __len__ (self):
        return len(self.seqs)
    
    def __getitem__(self, n):
        return self.seqs[n]
    
    def seqSize (self, i):
        return len(self.seqs[i])
    
    def readFile(self, fic, t):
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()
        
        
    def createMotifFromIndexes(self, indexes):
        pseqs = []
        for i,ind in enumerate(indexes):
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) )
        return MyMotifs(pseqs)
        
        
    # SCORES
        
    def score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s) #O MyMotifs é atribuido a motif
        motif.doCounts() # função de MyMotifs
        mat = motif.counts # matriz de contagem
        for j in range(len(mat[0])): # percorre todas as colunas
            maxcol = mat[0][j]
            for  i in range(1, len(mat)): # percorre todas as linhas
                if mat[i][j] > maxcol: # para cada coluna, vê todas as linhas qual o nucleotido que aparece mais vezes
                    maxcol = mat[i][j] # encontra o maior valor
            score += maxcol # adiciona ao score
        return score
    
    def ps_score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts_ps()
        mat = motif.counts
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score += maxcol
        return score

   
    def scoreMult(self, s): #igual ao score, só que em vez de somar, multiplica
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score     
       
    # EXHAUSTIVE SEARCH
       
    def nextSol (self, s): #iterar sobre o vetor de posições iniciais
        nextS = [0]*len(s)
        pos = len(s) - 1     
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize: #enquanto não chegar ao fim das combinações
            pos -= 1
        if (pos < 0): 
            nextS = None
        else:
            for i in range(pos): 
                nextS[i] = s[i]
            nextS[pos] = s[pos]+1
            for i in range(pos+1, len(s)):
                nextS[i] = 0
        return nextS
        
    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0]* len(self.seqs)
        while s is not None:
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res
     
    # BRANCH AND BOUND     
     
    def nextVertex (self, s): #s são posições parciais
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level
            for i in range(len(s)): 
                res.append(s[i])
            res.append(0)
        else: # bypass
            pos = len(s)-1 
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0: res = None # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos]+1)
        return res
    
    
    def bypass (self, s):
        res =  []
        pos = len(s) -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: res = None 
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos]+1)
        return res
        
    def branchAndBound (self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size # no inicio é (0,0,0)
        while s is not None:
            if len(s) < size: #a partir avalia o segundo bypass
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore: #se for pior que o maior score
                    s = self.bypass(s) # saltará para o próximo
                else: s = self.nextVertex(s)
            else: # avalia as folhas iniciais
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif  = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)
  
    def heuristicConsensus(self):
        mf = MotifFinding(self.motifSize, self.seqs[:2]) #cria objeto um objeto MotifFinding para as 2 primeiras seqs
        s = mf. exhaustiveSearch() # procura exaustiva para determinar s1 e s2
        for i in range(2, len(self.seqs)): #para cada uma das restantes seqs
            s.append(0)
            melhorScore = -1
            melhorPosicao = 0
            for j in range(self.seqSize(i) - self.motifSize + 1): 
                s[i] = j #adiciona a seq seguinte para ser comparada com o consenso das primeiras
                score_atual = self.score(s) #calcula o score
                if score_atual > melhorScore: #se o score aumentar
                    melhorScore = score_atual #passa a ser o melhor score
                    melhorPosicao = j # melhor posição passa ser a de j
                s[i] = melhorPosicao  #adiciona o indice ao vetor de posições iniciais   
        return s

    # Consensus (heuristic)

    def heuristicStochastic (self):
        from random import randint
        s = [0] * len(self.seqs) #vetor de posições iniciais
        for i in range(len(self.seqs)): #para cada seq
            s[i] = randint(0, self.seqSize(i) - self.motifSize) # atribui posições aleatorias ao vetor de posições iniciais        
        best_score = self.score(s) #função score cria os motifs e a matriz de contagem, calculando o score para as posições aleatorias
        improve = True
        while improve: #enquando houver melhoria
            motif = self.createMotifFromIndexes(s) #cria os motifs a partir do vetor de posições iniciais
            motif.createPWM() # cria a PWM dos motifs criados
            for i in range(len(self.seqs)): #para todas as seqs
                s[i] = motif.mostProbableSeq(self.seqs[i]) #vê qual a subsequencia mais provavel, mudando a posição inicial para a posição encontrada
            scr = self.score(s) #calcula o score
            if scr > best_score: #se esse score for melhor do que o anterior
                best_score = scr #fica como melhor score
            else:
                improve = False  #a partir do momento que o score deixa de aumentar, improve fica falso e o ciclo acabou      
        return s

    # Gibbs sampling 

    def gibbs (self, n):
        from random import randint
        s = [0] * len(self.seqs) #vetor de posições iniciais com zeros
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize) #criar o vetor das posições iniciais aleatórias
        vfinal = s #variavel que vai receber as posições iniciais com melhor score
        bestscr = self.score(s) #score do s com as posições aleatorias
        k = 0
        while k < n:
            seq_idx = randint(0, len(self.seqs) - 1) #escolher uma seq aleatoria
            igno_seq = self.seqs.pop(seq_idx) #remover a seq seleciona aleatoriamente e atribuir a uma nova variavel
            s.pop(seq_idx) #retirar o valor da posição inicial da seq escolhida do vetor de posições iniciais
            motif = self.createMotifFromIndexes(s) # fazer motifs para as seqs escolhidas
            motif.createPWM() #fazer pwm e ver o consenso
            prob = motif.probAllPositions(igno_seq) #calcular a probabilidade de todas as sequencias possiveis na seq removida
            novo_ind = self.roulette(prob) # escolher um indice de acordo com a probabilidade obtida na função anterior
            self.seqs.insert(seq_idx, igno_seq) #adicionar de novo a seq retirada no sitio onde estava anteriormente
            s.insert(seq_idx, novo_ind) #adicionar o novo indice que vem da função roulette no sitio onde estava anteriormente
            scr = self.score(s) #faz o score para o novo vetor
            if scr > bestscr:
                bestscr = scr
                vfinal = s
            k += 1
        return vfinal


    def roulette(self, f):
        from random import random
        tot = 0.0
        for x in f: tot += (0.01+x)
        val = random()* tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1
    
    #Consensus (heuristic stochastic) pseudo

    def heuristicStochastic_ps(self):
        from random import randint
        s = [0] * len(self.seqs) #vetor de posições iniciais
        for i in range(len(self.seqs)): #para cada seq
            s[i] = randint(0, self.seqSize(i) - self.motifSize) # atribui posições aleatorias ao vetor de posições iniciais        
        best_score = self.ps_score(s) #função score cria os motifs e a matriz de contagem, calculando o score para as posições aleatorias
        improve = True
        while improve: #enquando houver melhoria
            motif = self.createMotifFromIndexes(s) #cria os motifs a partir do vetor de posições iniciais
            motif.createPWM_ps() # cria a PWM dos motifs criados
            for i in range(len(self.seqs)): #para todas as seqs
                s[i] = motif.mostProbableSeq(self.seqs[i]) #vê qual a subsequencia mais provavel, mudando a posição inicial para a posição encontrada
            scr = self.ps_score(s) #calcula o score
            if scr > best_score: #se esse score for melhor do que o anterior
                best_score = scr #fica como melhor score
            else:
                improve = False  #a partir do momento que o score deixa de aumentar, improve fica falso e o ciclo acabou      
        return s
    
    #Gibbs sampling pseudo

    def gibbs_ps(self, n):
        from random import randint
        s = [0] * len(self.seqs) #vetor de posições iniciais 
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize) #criar o vetor das posições iniciais aleatórias
        vfinal = s #variavel que vai receber as posições iniciais com melhor score
        bestscr = self.score(s) #score do s com as posições aleatorias
        k = 0
        while k < n:
            seq_idx = randint(0, len(self.seqs) - 1) #escolher uma seq aleatoria
            igno_seq = self.seqs.pop(seq_idx) #remover a seq seleciona aleatoriamente e atribuir a uma nova variavel
            s.pop(seq_idx) #retirar o valor da posição inicial da seq escolhida do vetor de posições iniciais
            motif = self.createMotifFromIndexes(s) # fazer motifs para as seqs escolhidas
            motif.createPWM_ps() #fazer pwm e ver o consenso
            prob = motif.probAllPositions(igno_seq) #calcular a probabilidade de todas as sequencias possiveis na seq removida
            novo_ind = self.roulette(prob) # escolher um indice de acordo com a probabilidade obtida na função anterior
            self.seqs.insert(seq_idx, igno_seq) #adicionar de novo a seq retirada no sitio onde estava anteriormente
            s.insert(seq_idx, novo_ind) #adicionar o novo indice que vem da função roulette no sitio onde estava anteriormente
            scr = self.ps_score(s) #faz o score para o novo vetor
            if scr > bestscr:
                bestscr = scr
                vfinal = s
            k += 1
        return vfinal

# tests

def test1():  
    sm = MotifFinding()
    sm.readFile("exemploMotifs.txt","dna")
    sol = [25,20,2,55,59]
    sa = sm.score(sol)
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)

def test2():
    print ("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA","dna")
    seq2 = MySeq("ACGTAGATGA","dna")
    seq3 = MySeq("AAGATAGGGG","dna")
    mf = MotifFinding(3, [seq1,seq2,seq3])
    sol = mf.exhaustiveSearch()
    print ("Solution", sol)
    print ("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print ("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print ("Solution: " , sol2)
    print ("Score:" , mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())
    
    print ("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print ("Solution: " , sol1)
    print ("Score:" , mf.score(sol1))

def test3():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print ("Branch and Bound:")
    sol = mf.branchAndBound()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

def test4():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Score mult:" , mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    
    sol2 = mf.gibbs(1000)
    print ("Score:" , mf.score(sol2))
    print ("Score mult:" , mf.scoreMult(sol2))

test4()
