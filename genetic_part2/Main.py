import cities as cities

city_dict = cities.load_cities("cities.txt")

class Individual:
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

    def reset_population(self,city_dict, pop_size=20):
        for _ in range(pop_size):
            chromosome = cities.default_road(city_dict)
            import random
            random.shuffle(chromosome) # works inplace
            fitness = -cities.road_length(city_dict, chromosome)
            new_individual = Individual(chromosome, fitness)
            self._population.append(new_individual)
        
        

        

    def evolve_for_one_generation(self, city_dict):
        self._initial_population= self._population
        self._population.sort(reverse=False)
        num_to_keep= int(len(self._population)*self._selection_rate)
        self._population=self._population[:num_to_keep]

        while len(self._population) < len(self._initial_population):
            import random
            parent1, parent2 = random.sample(self._population, 2)
            #print("parent1",parent1)
            #print("parent2",parent2)
            x_point = random.randrange(0, min(len(parent1.chromosome), len(parent2.chromosome)))
            #print("x_point",x_point)
            new_chromosome = parent1.chromosome[:x_point]

            for city in parent2.chromosome:
                if city not in new_chromosome:
                    new_chromosome.append(city)
                    
                if(len(new_chromosome)>12):
                        print("faire attention à city not in parent1.chromosome[:x_point]")
                



            if random.random() < self._mutation_rate:
                pos = random.randrange(0, len(new_chromosome))
                possible_cities = cities.default_road(city_dict)
                new_gene = random.choice(possible_cities)
                print("new_gene",new_gene)
                for city in new_chromosome:
                    if city not in new_chromosome:
                        #print("city not in newchromosome",city)
                        new_chromosome[pos] = new_gene
                

            new_individual = Individual(new_chromosome, -cities.road_length(city_dict, new_chromosome))
            self._population.append(new_individual)
    
    def evolve_until(self,city_dict, max_nb_of_generations=500, threshold_fitness=25):
           
        self._population.sort(reverse=False)
        count =0
        print(self._population[0].fitness)
        while(count<max_nb_of_generations and self._population[0].fitness<threshold_fitness):
            solver.evolve_for_one_generation(city_dict)
            count=count+1
            #print(count)
            self._population.sort(reverse=False)
    
    def get_best_individual(self):
        """ Return the best Individual of the population """
        print(self._population[0])  
        return self._population[0] 





solver = GASolver()
solver.reset_population(city_dict)
solver.evolve_until(city_dict)

best = solver.get_best_individual()
cities.draw_cities(city_dict, best.chromosome) 



