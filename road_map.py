"""
each road will have general view
Road_Name: (Number, Start_Node, Finish_Node, w)

    Start_Node == (x1 , y1) #start point
    Finish_Node == (x2, y2) #finnish point
    w == range(0, 11) #trafic
"""
import random
graph = {
    "A": ["B", "C", "E"],
    "B": ["C", "A"],
    "C": ["B", "A", "F"],
    "D": ["F"],
    "E": ["A"],
    "F": ["C", "D"]}

coordinates = {"A": [0, 10, 10],
               "B": [1, 40, 100],
               "C": [2, 60, 50],
               "D": [3, 100, 180],
               "E": [4, 120, 50],
               "F": [5, 70, 130]}

                #_A__B__C__D__E__F_
boolean_graph = [[0, 1, 1, 0, 1, 0],
                 [1, 0, 1, 0, 0, 0],
                 [1, 1, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0],
                 [0, 0, 1, 1, 0, 0]]

for x in range(len(boolean_graph)):
    for y in range(len(boolean_graph[x])):
        if boolean_graph[x][y] == 1 and y >= x:
            num = random.randrange(10)
            boolean_graph[y][x] = num
            boolean_graph[x][y] = num
