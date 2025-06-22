from maze import *
from exception import *
from stack import *
from typing import List, Tuple

class PacMan:
    def __init__(self, grid: Maze) -> None:
        self.navigator_maze = grid.grid_representation

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        if self.navigator_maze[start[0]][start[1]] == 1 or self.navigator_maze[end[0]][end[1]] == 1:
            raise PathNotFoundException
        
        n = len(self.navigator_maze)
        m = len(self.navigator_maze[0])

        st = Stack()
        vis = set()

        delrow = [0, -1, 1, 0]
        delcol = [-1, 0, 0, 1]

        st.push(start)
        vis.add(start)
        path = [start]
        
        while not st.empty():
            temp = st.top()
            row, col = temp

            if temp == end:
                return path
            
            moved = False
            for i in range(4):
                nrow = row + delrow[i]
                ncol = col + delcol[i]
                if 0 <= nrow < n and 0 <= ncol < m and self.navigator_maze[nrow][ncol] == 0 and (nrow, ncol) not in vis:
                    st.push((nrow, ncol))
                    vis.add((nrow, ncol))
                    path.append((nrow, ncol))
                    moved = True
                    break
                    
            if not moved:
                st.pop()
                path.pop()

        raise PathNotFoundException
