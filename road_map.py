"""
each road will have general view
Road_Name: (Start_Node, Finish_Node, w)

    Start_Node == (x1 , y1) #start point
    Finish_Node == (x2, y2) #finnish point
    w == range(0, 11) #trafic
"""

graph = {
    "A": ["B", "C", "E"],
    "B": ["C", "A"],
    "C": ["B", "A", "F"],
    "D": ["F"],
    "E": ["A"],
    "F": ["C", "D"]
}

coordinates = {"A": [10, 10],
               "B": [40, 100],
               "C": [50, 50],
               "D": [100, 180],
               "E": [150, 50],
               "F": [100, 130]
}
