# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""
import mastermind as mm
MATCH = mm.MastermindMatch(secret_size=4)
class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm 

        Args:
            chromosome (list[]): a list representing the individual's chromosome
            fitness (float): the individual's fitness (the higher, the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GASolver:
    def __init__(self, selection_rate=0.25, mutation_rate=0.1):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals """
        for i in range(pop_size):
            chromosome = MATCH.generate_random_guess()
            fitness = MATCH.rate_guess(chromosome)
            new_individual = Individual(chromosome, fitness)
            self._population.append(new_individual)

        



    def evolve_for_one_generation(self):
        """ Apply the process for one generation : 
            -	Sort the population (Descending order)
            -	Selection: Remove x% of population (less adapted)
            -   Reproduction: Recreate the same quantity by crossing the 
                surviving ones 
            -	Mutation: For each new Individual, mutate with probability 
                mutation_rate i.e., mutate it if a random value is below   
                mutation_rate
        """
        self._initial_population= self._population
        self._population.sort(reverse=True)
        num_to_keep= int(len(self._population)*self._selection_rate)
        self._population=self._population[:num_to_keep]
       # print(self._population)
        
        while len(self._population) < len(self._initial_population):
            import random
            parent1, parent2 = random.sample(self._population, 2)
            x_point = random.randrange(0, min(len(parent1.chromosome), len(parent2.chromosome)))
            new_chromosome = parent1.chromosome[:x_point] + parent2.chromosome[x_point:]

            if random.random() < self._mutation_rate:
                pos = random.randrange(0, len(new_chromosome))
                valid_colors = mm.get_possible_colors()
                new_gene = random.choice(valid_colors)
                new_chromosome[pos] = new_gene
            
            new_individual = Individual(new_chromosome, MATCH.rate_guess(new_chromosome))
            self._population.append(new_individual)
        
        #print(self._population)



    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        pass  # REPLACE WITH YOUR CODE

    def get_best_individual(self):
        """ Return the best Individual of the population """
        print(self._population[0])  
        return self._population[0]      

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=25):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        self._population.sort(reverse=True)
        count =0
        
        while(count<max_nb_of_generations and self._population[0].fitness<threshold_fitness):
            solver.evolve_for_one_generation()
            count=count+1
            #print(count)
        self._population.sort(reverse=True)
       



#aaaa

solver =GASolver()
solver.reset_population()
solver.evolve_for_one_generation()
solver.evolve_until(threshold_fitness=MATCH.max_score())
best = solver.get_best_individual()
print(f"Best guess {best.chromosome}")
print(f"Problem solved? {MATCH.is_correct(best.chromosome)}")
