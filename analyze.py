import sys
import math
import pandas
import numpy
import os
import ast

directory = "lab2_data"

def analyze_genome(file_obj, first):
    v = first.split('"')

    best_gene = v[1]
    best_gene = ast.literal_eval(best_gene)
    best_gene = ''.join(['0' if val == False else '1' for val in best_gene])
    
    initials = first.split(",")
    average_fit = float(initials[1])
    max_fit = float(initials[1])
    generation = int(initials[0])

    perfect = 0

    if max_fit == 1:
        perfect = 1

    count = 1
    for line in file_obj:
        if line.strip() == "step,fitness,genome":
            break
        
        vals = line.split(",")
        fitness = float(vals[1])
        average_fit += fitness
        if max_fit < fitness:
            best_gene = line.split('"')[1]
            best_gene = ast.literal_eval(best_gene)
            best_gene = ''.join(['0' if val == False else '1' for val in best_gene])
            max_fit = fitness
        if fitness == 1:
            perfect += 1

        count += 1
    
    average_fit /= count

    found = 1 if perfect > 0 else 0

    return generation, average_fit, max_fit, best_gene, found, perfect, 0


def analyze_file(file_obj, file_name: str, out_file):
    params = file_name.split("_")
    throw = file_obj.readline()
    iteration = params[5].split(".")[0]
    for line in file_obj:
        gen, avg_fit, max_fit, best_gene, found, num_found, diversity = analyze_genome(file_obj, line)
        line_out = f"{params[1]},{params[2]},{params[3]},{params[4]},{iteration},{gen},{avg_fit},{max_fit},{best_gene},{found},{num_found},{diversity}\n"
        out_file.write(line_out)
    

if __name__ == "__main__":
    files = os.listdir(directory)
    out_file = open("output.csv", "w")
    start = "N,p_m,p_c,tournament_size,iteration,generation,average_fitness,best_fitness,best_genome,solution_found,num_solutions_found,diversity_metric\n"
    out_file.write(start)
    for file in files:
        with open(f"{directory}/{file}", "r") as data:
            analyze_file(data, file, out_file)

        