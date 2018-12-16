# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 18:59:51 2018

@author: Darshit Pandya
@title: 0-1 Knapsack Problem solved using Genetic Algorithms
"""

'''
How it works?

1. Create population
2. If not maximum limit reached, go to 3, else 8
3. Fitness measurement
4. Selection to make up the next generation using Roulette wheel spinning
5. Crossover, considering the crossover rate of 0.95 i.e. maximum offsprings generation and elitism
6. Mutation, considering the mutation rate i.e. flipping the bit
7. Go to 2
8. Exit
'''
import random

#-----------------------------------------------------------------------------------
maximum_capacity = int(input("Enter the maximum capacity of knapsack (<2080): "))
items_maximum = int(input("Enter the maximum items possible (till 64): "))
gen_maximum = int(input("Enter the maximum generations: "))
init_population = int(input("Enter the initial population size: "))
crossover_rate = 0.95
mutation_rate = 0.05
#-----------------------------------------------------------------------------------

## Value range is 1 -> 100
## Weight range is 1 -> 20

item_weight = [random.randint(1, 10) for iteration in range(0, items_maximum)]
item_val = [random.randint(1, 100) for iteration in range(0, items_maximum)]
print("========Initial Weights============")
print(item_weight)
print("========Initial Values=============")
print(item_val)
#-----------------------------------------------------------------------------------
def create_initial_population():
    '''
    Creating initial population, with each chromosome
    having 64 0/1 genes. Initial population strength will be
    as per init_population
    '''
    temp = []
    for i in range(init_population):
            ## each value is a 64-bit integer
            temp_int = int(''.join([str(random.randint(0,1)) for k in range(items_maximum)]))
            ## to append in the list of initial population
            temp = temp + [temp_int] 
            #temp = temp + [[random.randint(0, 1) for k in range(items_maximum)]]
    return temp
#-----------------------------------------------------------------------------------
def fitness_check(chromosome):
    '''
    Fitness checking for value generation and weight check
    depending upon the value of genes in the chromosome i.e. each 
    member of the population
    '''
    chromosome_weight = 0
    chromosome = format(chromosome, '064b')
    chromosome_value = 0
    for i in range(0, items_maximum):
        if int(chromosome[i]) & 1 == 1:  ## <-- 'AND'operation
            chromosome_weight = chromosome_weight + item_weight[i]
            chromosome_value = chromosome_value + item_val[i]
        else:
            pass
    
    ##chromosome_weight = sum([gene*weight_item for gene,weight_item in zip(str(chromosome).split(''),item_weight)])
    if chromosome_weight <= maximum_capacity:
        return chromosome_value
    else:
        return 0
#-----------------------------------------------------------------------------------
def normal_form(values_valid_pop):
    '''
    value of each chromosome/ total value of the population
    '''
    pop_sum = sum(values_valid_pop)
    normed_form = [values_valid_pop[i] / pop_sum for i in range(0, len(values_valid_pop))]
    return normed_form
    
#-----------------------------------------------------------------------------------
def cumulative_normal_form(values_valid_pop, normal_form):
    '''
    cumulative sum for the generated normal form
    '''
    temp_sum = 0.0
    cumulated_form = []
    for n_sum in normed_values:
        temp_sum +=n_sum
        cumulated_form = cumulated_form + [temp_sum]
    return cumulated_form
#-----------------------------------------------------------------------------------
def selection_next_generation(population, cumulative_values):
    '''
    Roulette wheel is a probabilistic approach. Hence
    we will select a number randomly between 0 and 1.
    If the cumulative of that chromosome is greater or
    equal to the random generated number, we shall select that
    '''
    random_number = random.random() ## random value between 0 and 1
    for i in range(0, len(cumulative_values)):
        if cumulative_values[i] >= random_number:
            return population[i]
#-----------------------------------------------------------------------------------
def mutation(pop, mutation_parent):
    '''
    Considering the mutation probability, flip the bits 0->1 randomly and vice-versa
    '''
    random_bits = random.sample(range(0, 64), 5) ## finding the positions of the bits to be flipped
    child = mutation_parent
    for each_bit in random_bits:
        child[each_bit] = ~child[each_bit] ##for flipping the bits
    for i in range(0, len(mutation_parent)):
        if pop[i] == mutation_parent:
            pop[i] = child
    return pop
#-----------------------------------------------------------------------------------
def crossover(pop, cumulative_normal_values):
    try:
        '''
        Select a random number, if < cross-over-rate, do cross-over else avoid it
        '''
        crossover_mut_random = random.random()
        if crossover_mut_random < crossover_rate:
            cross_over_parent1 = selection_next_generation(pop, cumulative_normal_values) ##<--4
            cross_over_parent2 = selection_next_generation(pop, cumulative_normal_values) ##<--4  
            
            ##tree crossover will be employed here
            start = random.randint(0, random.randint(0, 40)) ## selecting the cut-point for dividing the tree
            child_1 = cross_over_parent1 & ~(2**start - 1) | cross_over_parent2 & (2**start - 1) ##< '&' - Bitwise AND; '|' - Bitwise OR ; '~' BITWISE NOT
            child_2 = cross_over_parent2 & ~(2**start - 1) | cross_over_parent1 & (2**start - 1) ##< '&' - Bitwise AND; '|' - Bitwise OR ; '~' BITWISE NOT
            
            for i in range(0, len(cross_over_parent1)):
                if pop[i] == cross_over_parent1:
                    pop[i] = child_1
                elif pop[i] == cross_over_parent2:
                    pop[i] = child_2
        if crossover_mut_random > 0.01:
            mutation_parent = selection_next_generation(pop, cumulative_normal_values)
            pop = mutation(pop, mutation_parent)
        return pop
    except:
        return pop
#-----------------------------------------------------------------------------------
def find_best(pop):
    max_index = 0
    max_sum = 0
    temp = []
    for i in range(0, len(pop)):
        chromosome = pop[i]
        chromosome = format(chromosome, '064b') ## binary conversion to make it iterable
        chromosome_value = 0
        for i in range(0, items_maximum):
            if int(chromosome[i]) & 1 == 1:
                chromosome_value = chromosome_value + item_val[i]
        if chromosome_value > max_sum:
            max_sum = chromosome_value
            max_index = i
    max_chr= format(pop[max_index], '064b')
    for i in range(0, items_maximum):
        if int(max_chr[i]) & 1 == 1:
            temp = temp + [i]
    print("==================== Best Solution ====================")
    print("Indexes of Elements  considered: ", temp)
    print("Best value knapsack found is: ", max_sum)

#-----------------------------------------------------------------------------------
if __name__ == '__main__':
    
    gen_iterator = 0 
    population = create_initial_population() ##<-- 1
    while gen_iterator < gen_maximum: ##<--2
            values_valid_pop = [fitness_check(chromosome) for chromosome in population]##<--3
            normed_values = normal_form(values_valid_pop)
            cumulative_normal_values = cumulative_normal_form(values_valid_pop, normed_values)
            population = crossover(population, cumulative_normal_values)
            gen_iterator += 1

    find_best(population)

