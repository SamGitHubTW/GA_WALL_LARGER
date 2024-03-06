# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving TSP example)
"""
from ga_solver import GAProblem
import cities

class TSProblem(GAProblem):
    """Implementation of GAProblem for the traveling salesperson problem"""
    
    def __init__(self, city_dict):
        """Initialize the traveling salesperson problem with a list of cities"""
        self.cities = city_dict
    
    def default_road(self,city_dict):
        return cities.default_road(city_dict)
    
    def road_length(self,city_dict, chromosome):
        return cities.road_length(city_dict, chromosome)
    



if __name__ == '__main__':

    from ga_solver import GASolver

    city_dict = cities.load_cities("cities.txt")
    problem = TSProblem(city_dict)
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until()
    solver.get_best_individual().chromosome
    cities.draw_cities(city_dict, solver.get_best_individual().chromosome) 
