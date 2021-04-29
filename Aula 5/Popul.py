# -*- coding: utf-8 -*-

from Indiv import Indiv, IndivInt, IndivReal
from random import random


class Popul:

    def __init__(self, popsize, indsize, indivs=[]):
        self.popsize = popsize #nº de indivs na população
        self.indsize = indsize #tamanha do individuo
        if indivs: #se uma lista de indivs for dada
            self.indivs = indivs
        else: #criação da lista aleatoriamente
            self.initRandomPop()

    def getIndiv(self, index): #busca do individuo pelo indice
        return self.indivs[index]

    def initRandomPop(self): 
        self.indivs = [] #se não existirem indivs
        for _ in range(self.popsize): #para o tamanho da população fornecido
            indiv_i = Indiv(self.indsize, []) #crir um objeto Indic com o tamanho fornecido no inicio da classe Popul
            self.indivs.append(indiv_i) #adiciona-se o novo individuo à lista

    def getFitnesses(self, indivs=None): #valores de aptidão para os individuos
        fitnesses = []
        if not indivs:
            indivs = self.indivs
        for ind in indivs:
            fitnesses.append(ind.getFitness())
        return fitnesses

    def bestSolution(self):
        return max(self.indivs)

    def bestFitness(self): #melhor valor de aptidão
        indv = self.bestSolution()
        return indv.getFitness()


    def selection(self, n, indivs=None): #seleção para a reprodução
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs))) #normalização dos scores de fitness
        for _ in range(n): 
            sel = self.roulette(fitnesses) #seleção dos indivs que vão gerar novas soluções, tendo em conta o su score (quanto maior, maior a probabilidade de ser selecionado)
            fitnesses[sel] = 0.0 #score do indiv fica 0
            res.append(sel) #adiciona o indice do indiv ao resultado
        return res

    def roulette(self, f):
        tot = sum(f)
        val = random()
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] / tot)
            ind += 1
        return ind-1

    def linscaling(self, fitnesses):
        mx = max(fitnesses)
        mn = min(fitnesses)
        res = []
        for f in fitnesses:
            val = (f-mn)/(mx-mn)
            res.append(val)
        return res

    def recombination(self, parents, noffspring): #parents foram selecionados na função de seleção
        offspring = [] #descendente
        new_inds = 0
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]] #vai buscar os indivs que foram selecionados ao self.indivs onde estão guardados
            parent2 = self.indivs[parents[new_inds+1]]
            offsp1, offsp2 = parent1.crossover(parent2) #crossover entre os parents, que cria dois novos descendentes
            offsp1.mutation()
            offsp2.mutation() #a cada descendente é feita uma mutação
            offspring.append(offsp1)
            offspring.append(offsp2) #descendentes são adicionados à lista dos descendentes
            new_inds += 2 #cada iteração forma dois novos individuos
        return offspring

    def reinsertion(self, offspring): #seleção dos indivs que vão fazer parte da população seguinte
        tokeep = self.selection(self.popsize-len(offspring)) #seleciona individuos da pop anterior para serem mantidos
        ind_offsp = 0
        for i in range(self.popsize): #corre a população
            if i not in tokeep: #se o indiv não tiver sido selecionado para ser mantido
                self.indivs[i] = offspring[ind_offsp] #preenche-se a nova pop com um indiv novo
                ind_offsp += 1


class PopulInt(Popul):

    def __init__(self, popsize, indsize, ub, indivs=[]):
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivInt(self.indsize, [], 0, self.ub)
            self.indivs.append(indiv_i)


class PopulReal(Popul):

    def __init__(self, popsize, indsize, lb=0.0, ub=1.0, indivs=[]):
        self.lb = lb
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivReal(self.indsize, [], lb=self.lb, ub=self.ub)
