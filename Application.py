# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Application Class
"""
__author__ = "Gonzalo Chacaltana Buleje"
__copyright__ = "Copyright (C) 2020 Itensoft Digital Solutions"
__license__ = "Public Domain"
__version__ = "1.0"

import sys
from random import randint
from Individual import Individual


class Application(object):

    def __init__(self):
        self.maxLengthObjetive = 300
        self.minLengthObjetive = 1
        self.maxPopulation = 300
        self.minPopulation = 100
        self.minRateMutation = 0.0
        self.maxRateMutation = 1.0
        self.populations = []
        self.inputParams()
        self.executeGeneticAlgorithm()

    def inputParams(self):
        self.inputObjetive()
        self.inputPopulation()
        self.inputRateMutation()

    def inputObjetive(self):
        self.objetive = input("Enter the target text: ")
        if (len(self.objetive) == 0):
            raise Exception("Exception: The target text was not entered!")
        if (len(self.objetive) < self.minLengthObjetive):
            raise Exception("Exception: The target text is very short!")
        if (len(self.objetive) > self.maxLengthObjetive):
            raise Exception("Exception: The objective text is very extensive!")

    def inputPopulation(self):
        self.numberPopulation = int(
            input("Enter number of individuals per population [100 to 300]: "))
        if (self.numberPopulation == 0):
            raise Exception(
                "Exception: The population of individuals is invalid!")
        if (self.numberPopulation < self.minPopulation):
            raise Exception(
                "Exception: The population of individuals is very small!")
        if (self.numberPopulation > self.maxPopulation):
            raise Exception(
                "Exception: The population of individuals is very large!")

    def inputRateMutation(self):
        self.rateMutation = float(
            input("Enter the mutation rate [0 to 1]: "))
        if (self.rateMutation < self.minRateMutation):
            raise Exception(
                "Exception: The mutation rate cannot be less than %s" % self.minRateMutation)
        if (self.rateMutation > self.maxRateMutation):
            raise Exception(
                "Exception: The mutation rate cannot be greater than %s" % self.maxRateMutation)

    def executeGeneticAlgorithm(self):
        for _ in range(0, self.numberPopulation):
            individual = Individual()
            individual.generateGenes(len(self.objetive), self.objetive)
            self.populations.append(individual)
        self.generation = 0
        print("Looking for better individual....")
        while True:
            self.evaluateMembersGeneration()
            self.selectMembersGeneration()
            self.reproductionMembersGeneration()

    def evaluateMembersGeneration(self):
        self.generation += 1
        print("\n*************** GENERATION %s\n" % self.generation)
        for _ in range(0, self.numberPopulation):
            print("Generation[%s] | Individual[%s]: %s | fitness: %s" % (
                self.generation, _, self.populations[_].getPhenotype(), self.populations[_].getFitness()))
            if (self.evaluateObjetive(self.populations[_])):
                sys.exit()

    def selectMembersGeneration(self):
        self.parents = []
        for _ in range(0, self.numberPopulation):
            n = int(self.populations[_].getFitness()*100)
            #for j in range(0, n):
            if n>0:
                self.parents.append(self.populations[_])

    def reproductionMembersGeneration(self):
        totalParents = len(self.parents)
        print("Selected parents: ", totalParents)
        for i in range(0, self.numberPopulation):
            a = int(randint(0, (totalParents-1)))
            b = int(randint(0, (totalParents-1)))
            father = self.parents[a]
            mother = self.parents[b]
            children = father.cross(mother)
            children.mutate(self.rateMutation)
            self.populations[i] = children

    def evaluateObjetive(self, individual):
        if (individual.getFitness() == 1.0):
            print("Target found: %s" % individual.getPhenotype())
            return True
        return False

    def showIndividualPhenotype(self):
        for j in range(0, self.numberPopulation):
            print("Individual %s : %s" %
                  (j, self.populations[j].getPhenotype()))


if __name__ == "__main__":
    try:
        app = Application()
    except (ValueError, FileNotFoundError, AttributeError, Exception) as ex:
        print(ex)
