from random import randint, random, shuffle


class Indiv:

    def __init__(self, size, genes=[], lb=0, ub=1):
        self.lb = lb 
        self.ub = ub
        self.genes = genes #caract
        self.fitness = None #valores de aptidão
        self.multifitness = None #valores de aptidão score multiplo
        if not self.genes:
            self.initRandom(size)

    # comparadores.
    # Permitem usar sorted, max, min

    def __eq__(self, solution):
        if isinstance(solution, self.__class__):
            return self.genes.sort() == solution.genes.sort()
        return False

    def __gt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness
        return False

    def __ge__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness
        return False

    def __lt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness
        return False

    def __le__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness
        return False

    def __str__(self):
        return f"{str(self.genes)} {self.getFitness()}"

    def __repr__(self):
        return self.__str__()

    def setFitness(self, fit):
        self.fitness = fit

    def getFitness(self):
        return self.fitness
    
    def setMultiFitness(self, fit):
        self.multifitness = fit
    
    def getMultiFitness(self):
        return self.multifitness

    def getGenes(self):
        return self.genes

    def initRandom(self, size): #gerar individuos aleatoriamente
        self.genes = []
        for _ in range(size): #tendo em conta o tamanho da pop dado
            self.genes.append(randint(self.lb, self.ub)) #valores de individuos são gerados tendo em conta os bounds definidos

    def mutation(self):
        s = len(self.genes) #tamanho da população
        pos = randint(0, s-1) #é escolhido uma posição aleatoriamente
        if self.genes[pos] == 0: #se o gene da pos correspondente for 0
            self.genes[pos] = 1 #passa a ser 1
        else: #caso já fosse 1
            self.genes[pos] = 0 #passa ser 0

    def crossover(self, indiv2): #criar o segundo individuo
        return self.one_pt_crossover(indiv2)

    def one_pt_crossover(self, indiv2): 
        offsp1 = []
        offsp2 = [] #vetores de descendentes
        s = len(self.genes)
        pos = randint(0, s-1) #posição aleatoria onde vai ocorrer crossover, dependente do numero de genes do primeiro individuo
        for i in range(pos): #iterar até chegar ao valor encontrado anteriormente
            offsp1.append(self.genes[i]) #adiciona ao descendente 1 os genes até à posição encontrada
            offsp2.append(indiv2.genes[i]) #o mesmo
        for i in range(pos, s): #para as posiões seguintes
            offsp2.append(self.genes[i]) #genes que estavam no individuo 1 passam para o descendente 2
            offsp1.append(indiv2.genes[i]) #vice versa
        res1 = self.__class__(s, offsp1, self.lb, self.ub)
        res2 = self.__class__(s, offsp2, self.lb, self.ub)
        return res1, res2


class IndivInt (Indiv):

    def __init__(self, size, genes=[], lb=0, ub=1):
        self.lb = lb
        self.ub = ub
        self.genes = genes
        self.fitness = None
        if not self.genes:
            self.initRandom(size)

    def initRandom(self, size): #gerar individuos aleatorios
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(0, self.ub)) #gerar valores de individuos de acordo com os bounds

    def mutation(self):
        s = len(self.genes) #nº de genes do individuo
        pos = randint(0, s-1) #indice aleatório onde vai ocorrer a mutação
        self.genes[pos] = randint(0, self.ub) #novo valor para a posição encontrada anteriormente


class IndivReal(Indiv):

    def __init__(self, size, genes=[], lb=0, ub=1):
        self.lb = lb
        self.ub = ub
        Indiv.__init__(self, size, genes, lb, ub)

    def initRandom(self, size):
        self.genes = []
        for _ in range(size):
            self.genes.append(uniform(self.lb, self.ub))

    def mutation(self):
        s = len(self.genes)
        pos = randint(0, s-1)
        self.genes[pos] = uniform(self.lb, self.ub)
