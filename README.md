# MazePathFinding
Implementing the A* pathfinding algorithm, the script is able to find the shortest path from a user-selected start and end point on a randomly generated maze like grid.

When the script is run, a window displaying a randomly generated maze-like grid will pop up. 
The dark blue colored squares represent obstacles and white colored squares represent where the search algorithm is free to travel.
By left clicking on a white square we set the start point (green) and by right clicking on a white square we set an end point (red).
To run the search algorithm we press the space bar.

Algorithm:
In this script we implement the A* path-finding algorithm. Starting from the user-selected start cell, we explore the valid neighbors of each cell
in order of lowest f score. Note: f_score = g_score + heuristic. We use a function for manhattan distance as the heuristic function.
All weights of edges in the grid are 1.

If the algorithim is able to find the shortest path from start to end cell, the shortest path is displayed in yellow. 
The white cells that become light blue represent cells whose neighbors have all been explored
and those which become purple are cells who still remain in the priority queue, yet to be explored. 
The cells that remain white have not been added to the priority queue.

If the algorithm is not able to find the shortest path, no yellow path will be displayed. Only the visualization of the algorithm's search will be displayed.
The caption of the window will display "Path not found".

To reset the grid press z.

Feel free to download the demo video to see how the progam works
