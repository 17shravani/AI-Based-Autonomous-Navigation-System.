import heapq
import math

class Node:
    """Helper class to represent a node in the grid for pathfinding."""
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic (estimated cost from current to goal)
        self.f = 0  # Total cost (g + h)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.f < other.f

class AStarPlanner:
    def __init__(self, grid_width, grid_height, cell_size):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size

    def heuristic(self, node_a, node_b):
        """Calculate the Euclidean distance heuristic."""
        return math.sqrt((node_a.x - node_b.x)**2 + (node_a.y - node_b.y)**2)

    def get_neighbors(self, node, obstacles):
        """Returns valid adjacent nodes (up, down, left, right, diagonals)."""
        neighbors = []
        # Support moving in 8 directions
        directions = [
            (0, -1), (0, 1), (-1, 0), (1, 0),    # orthogonal
            (-1, -1), (-1, 1), (1, -1), (1, 1)   # diagonal
        ]
        
        for dx, dy in directions:
            new_x = node.x + dx
            new_y = node.y + dy
            
            # Check bounds
            if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
                if (new_x, new_y) not in obstacles:
                    neighbors.append(Node(new_x, new_y))
                    
        return neighbors

    def plan(self, start_pos, goal_pos, obstacles):
        """
        Executes the A* algorithm.
        start_pos: (x, y) tuple
        goal_pos: (x, y) tuple
        obstacles: list/set of (x, y) tuples
        Returns list of (x, y) coordinates representing the path.
        """
        start_node = Node(start_pos[0], start_pos[1])
        goal_node = Node(goal_pos[0], goal_pos[1])

        open_list = []
        closed_list = set()

        heapq.heappush(open_list, (start_node.f, start_node))
        
        # To quickly check if a node is in the open list
        open_set = { (start_node.x, start_node.y): start_node }

        while open_list:
            # Pop current node with lowest f cost
            current_f, current_node = heapq.heappop(open_list)
            
            # Remove from open_set
            coords = (current_node.x, current_node.y)
            if coords in open_set:
                del open_set[coords]

            closed_list.add(coords)

            # Check if goal is reached
            if current_node == goal_node:
                path = []
                while current_node is not None:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return path[::-1]  # Return reversed path

            # Generate children
            for neighbor in self.get_neighbors(current_node, obstacles):
                if (neighbor.x, neighbor.y) in closed_list:
                    continue

                # Cost is 1 for orthogonal, 1.414 for diagonal
                move_cost = 1 if neighbor.x == current_node.x or neighbor.y == current_node.y else 1.414
                neighbor.g = current_node.g + move_cost
                neighbor.h = self.heuristic(neighbor, goal_node)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node

                neighbor_coords = (neighbor.x, neighbor.y)
                
                # If neighbor already in open list with a lower g cost, skip
                if neighbor_coords in open_set:
                    existing_node = open_set[neighbor_coords]
                    if neighbor.g >= existing_node.g:
                        continue

                # Add to open list
                open_set[neighbor_coords] = neighbor
                heapq.heappush(open_list, (neighbor.f, neighbor))

        # No path found
        return None
