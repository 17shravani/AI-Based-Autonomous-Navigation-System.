import math

class Agent:
    def __init__(self, start_pos, cell_size):
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.cell_size = cell_size
        
        # Continuous pixel coordinates for smooth drawing
        self.px = self.x * self.cell_size + self.cell_size / 2
        self.py = self.y * self.cell_size + self.cell_size / 2
        
        self.path = []
        self.current_target_index = 0
        self.angle = 0  # In degrees
        self.speed = 3.0  # Pixels per frame

    def set_path(self, path):
        """Assigns the computed path to the agent."""
        if path and len(path) > 1:
            self.path = path
            self.current_target_index = 1 # Skip start node
        else:
            self.path = []

    def update(self):
        """Moves the agent along its path."""
        if not self.path or self.current_target_index >= len(self.path):
            return True # Reached goal
            
        target = self.path[self.current_target_index]
        target_px = target[0] * self.cell_size + self.cell_size / 2
        target_py = target[1] * self.cell_size + self.cell_size / 2
        
        dx = target_px - self.px
        dy = target_py - self.py
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.speed:
            # Reached current waypoint, move to next
            self.px = target_px
            self.py = target_py
            self.x = target[0]
            self.y = target[1]
            self.current_target_index += 1
        else:
            # Move towards waypoint
            direction_x = dx / distance
            direction_y = dy / distance
            self.px += direction_x * self.speed
            self.py += direction_y * self.speed
            
            # Calculate heading angle
            self.angle = math.degrees(math.atan2(-dy, dx))
            
        return False # Still moving
