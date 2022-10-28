import numpy as np
import pandas as pd
import re
import random
import time
import csv
from collections import Counter

def ReadGraphFile(filename):
        with open(filename) as file:
            fin = file.readlines()
        vertices = 0
        edges = 0
        for i in range(0, len(fin)):
            lst = fin[i].split()
            #lst = re.findall(r'\w+', fin[i])
            if lst[0] == 'c':
                continue

            if lst[0] == 'p':
                vertices = int(lst[2])
                edges = int(lst[3])
                neighbour_sets = [set() for i in range(0, vertices)]
            
            else:
                start = int(lst[1])
                finish = int(lst[2])
                #Edges in DIMACS file can be repeated, but it is not a problem for our sets
                neighbour_sets[start - 1].add(finish - 1)
                neighbour_sets[finish - 1].add(start - 1)
                
        return neighbour_sets, vertices
    
def rand(graph):
    #сортируем вершины по убыванию степеней вершин
    vertices = sorted(graph, key=lambda x: len(graph[x]), reverse=True)
    
    best_clique = []
    
    
    for i in range(len(vertices) * 30):

        candidates = vertices.copy()
    
        clique = []
        
        #выбираем рандомную вершину из 20% первых вершин, добавляем ее в клику
        index = random.randint(0, int(len(candidates)/5)) 
        vert = candidates[index]
        clique.append(vert)
        
        #пересчитываем кандидатов
        for ver in candidates.copy():
                if ver not in graph[vert] and ver in candidates:
                    candidates.remove(ver)
    
        while len(candidates) != 0:
            #выбираем рандомного кандидата
            index = random.randint(0, int(len(candidates))-1)
            vert = candidates[index]
            clique.append(vert)
        
            #пересчитываем кандидатов
            for ver in candidates.copy():
                if ver not in graph[vert] and ver in candidates:
                    candidates.remove(ver)
                    
        
        #проверка на лучшую клику
        if len(clique) > len(best_clique):
            best_clique = clique
                
    return best_clique

def Check(neighbour_sets, best_clique):
    counter = Counter(best_clique)
    
    if sum(counter.values()) > len(counter):
        print("Duplicated vertices in the clique\n")
        return False
    
    for i in best_clique:
        
        for j in best_clique:
            
            if i != j and j not in neighbour_sets[i]:
                print("Returned subgraph is not a clique\n")
                return False
            
    return True

files = ["brock200_1.clq", 
        "brock200_2.clq", 
        "brock200_3.clq", 
        "brock200_4.clq",
        "brock400_1.clq",
        "brock400_2.clq",
        "brock400_3.clq",
        "brock400_4.clq",
        "C125.9.clq", 
        "gen200_p0.9_44.clq",
        "gen200_p0.9_55.clq",
        "hamming8-4.clq",
        "johnson16-2-4.clq",
        "johnson8-2-4.clq",
        "keller4.clq",
        "MANN_a27.clq",
        "MANN_a9.clq", 
        "p_hat1000-1.clq",
        "p_hat1000-2.clq",
        "p_hat1500-1.clq",
        "p_hat300-3.clq",
        "p_hat500-3.clq",
        "san1000.clq",
        "sanr200_0.9.clq",
        "sanr400_0.7.clq"]

with open("clique.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter = ";", lineterminator="\r")
    file_writer.writerow(["Instance", "Time (sec)", "Clique size", "Clique vertices"])
    
    print("Instance", "Time (sec)", "Clique size", "Clique vertices")
    
    for file in files:
        neighbour_sets, vertices = ReadGraphFile("C:\\Users\\Елена\\Documents\\" + file)
        
        graph = {}
        
        for i in range(len(neighbour_sets)):
            graph[i] = neighbour_sets[i]
            
        start = time.time()
        
        clique = rand(graph)
        
        clique_size = len(clique)
        
        check = Check(neighbour_sets, clique)
        
        if check == False:
            print("*** WARNING: incorrect coloring: ***\n")
            
        finish = time.time()
        
        file_writer.writerow([file, round((finish - start), 3), clique_size, clique, "\n"])
        print("Instance: ", file, ";", "Time: ", round((finish - start), 3), ";", "Clique size: ", clique_size, ";", "Clique vertices: ", clique, "\n")

        print('---------------------------------')
            
w_file.close()