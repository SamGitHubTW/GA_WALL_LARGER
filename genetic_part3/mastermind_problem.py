# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving Mastermind example)
"""
from ga_solver import GAProblem
import mastermind as mm


class MastermindProblem(GAProblem):
    """Implementation of GAProblem for the mastermind problem"""
    def __init__(self, mastermind_match):
        """Initialize the Mastermind problem with a mastermind_match instance"""
        self.mastermind_match = mastermind_match
    
    def generate_random_guess(self):
        return match.generate_random_guess()
    
    def rate_guess(self,guess):
        return match.rate_guess(guess)
    def get_possible_colors(self):
        return mm.get_possible_colors()
    def rate_guess(self,new_chromosome):
        return match.rate_guess(new_chromosome)


if __name__ == '__main__':

    from ga_solver import GASolver

    match = mm.MastermindMatch(secret_size=6)
    problem = MastermindProblem(match)
    solver = GASolver(problem)

    solver.reset_population()
    solver.evolve_until()
    best = solver.get_best_individual()
    print(f"Best guess {best.chromosome}")
    print(f"Problem solved? {match.is_correct(best.chromosome)}") 