from Popul import Popul


class EvolAlgorithm:

    def __init__(self, popsize, numits, noffspring, indsize):
        self.popsize = popsize
        self.numits = numits
        self.noffspring = noffspring
        self.indsize = indsize

    def initPopul(self, indsize): #gerar a população inicial
        self.popul = Popul(self.popsize, indsize)

    def evaluate(self, indivs):
        for i in range(len(indivs)): #para cada individuo
            ind = indivs[i]
            fit = 0.0
            for x in ind.getGenes(): #para o tamanho do individuo
                if x == 1: #cada gene igual a 1
                    fit += 1.0 #aumenta o score de aptidão
            ind.setFitness(fit) #atribui o score 
        return None

    def iteration(self):
        parents = self.popul.selection(self.noffspring) #pop que queremos manter
        offspring = self.popul.recombination(parents, self.noffspring) #novas soluções
        self.evaluate(offspring) #avaliação dessas soluções
        self.popul.reinsertion(offspring) #juntamos tudo na mesma pop

    def run(self):
        self.initPopul(self.indsize) #nova pop
        self.evaluate(self.popul.indivs) #avaliação dos individuos
        self.bestsol = self.popul.bestSolution()
        for i in range(self.numits+1):
            self.iteration()
            bs = self.popul.bestSolution() #para ver se a aptidão melhora
            if bs > self.bestsol:
                self.bestsol = bs
            print("Iteration:", i, " ", "Best: ", self.bestsol)

    def printBestSolution(self):
        print("Best solution: ", self.bestsol.getGenes())
        print("Best fitness:", self.bestsol.getFitness())


def test():
    ea = EvolAlgorithm(100, 20, 50, 10)
    ea.run()


if __name__ == "__main__":
    test()
