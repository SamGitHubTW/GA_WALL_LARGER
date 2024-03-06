# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(generic genetic algorithm module)
"""


class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm

        Args:
            chromosome (list[]): a list representing the individual's
            chromosome
            fitness (float): the individual's fitness (the higher the value,
            the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GAProblem:
    """Defines a Genetic algorithm problem to be solved by ga_solver"""
    pass  # REPLACE WITH YOUR CODE


class GASolver:
    def __init__(self, problem: GAProblem, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            problem (GAProblem): GAProblem to be solved by this ga_solver
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._problem = problem
        
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals """
        if(type(self._problem).__name__ =="MastermindProblem"):
            for i in range(pop_size):
                chromosome = self._problem.generate_random_guess()
                fitness = self._problem.rate_guess(chromosome)
                new_individual = Individual(chromosome, fitness)
                self._population.append(new_individual)
        elif(type(self._problem).__name__ =="TSProblem"):
            for _ in range(pop_size):
                chromosome = self._problem.default_road(self._problem.cities)
                import random
                random.shuffle(chromosome) # works inplace
                fitness = -self._problem.road_length(self._problem.cities, chromosome)
                new_individual = Individual(chromosome, fitness)
                #print(new_individual)
                self._population.append(new_individual) 
        else:
            raise ValueError("Erreur: Type de problème non reconnu")

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
        if(type(self._problem).__name__ =="MastermindProblem"):
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
                    valid_colors = self._problem.get_possible_colors()
                    new_gene = random.choice(valid_colors)
                    new_chromosome[pos] = new_gene
                
                new_individual = Individual(new_chromosome, self._problem.rate_guess(new_chromosome))
                self._population.append(new_individual)
            
        elif(type(self._problem).__name__ =="TSProblem"):
            self._initial_population= self._population
            self._population.sort(reverse=False)
            num_to_keep= int(len(self._population)*self._selection_rate)
            self._population=self._population[:num_to_keep]

            while len(self._population) < len(self._initial_population):
                import random
                parent1, parent2 = random.sample(self._population, 2)
                x_point = random.randrange(0, min(len(parent1.chromosome), len(parent2.chromosome)))
                new_chromosome = parent1.chromosome[:x_point]

                for city in parent2.chromosome:
                    if city not in new_chromosome:
                        new_chromosome.append(city)
                        

                if random.random() < self._mutation_rate:
                    pos = random.randrange(0, len(new_chromosome))
                    possible_cities = self._problem.default_road(self._problem.cities)
                    new_gene = random.choice(possible_cities)
                    #print("new_gene",new_gene)
                    for city in new_chromosome:
                        if city not in new_chromosome:
                            #print("city not in newchromosome",city)
                            new_chromosome[pos] = new_gene
                    

                new_individual = Individual(new_chromosome, -self._problem.road_length(self._problem.cities, new_chromosome))
                self._population.append(new_individual)
            


    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        pass  # REPLACE WITH YOUR CODE

    def get_best_individual(self):
        """ Return the best Individual of the population """
        #print(self._population[0])  
        return self._population[0]  

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=20):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        if(type(self._problem).__name__ =="MastermindProblem"):
            self._population.sort(reverse=True)
            count =0
            
            while(count<max_nb_of_generations and self._population[0].fitness<threshold_fitness):
                GASolver.evolve_for_one_generation(self)
                count=count+1
                #print(count)
            self._population.sort(reverse=True)
        elif(type(self._problem).__name__ =="TSProblem"):
            self._population.sort(reverse=False)
            count =0
            #print(self._population[0].fitness)
            while(count<max_nb_of_generations and self._population[0].fitness<threshold_fitness):
                GASolver.evolve_for_one_generation(self)
                count=count+1
                #print(count)
                self._population.sort(reverse=False)

