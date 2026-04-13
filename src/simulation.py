import pygame
import random
import math
from src.path_planning import AStarPlanner
from src.agent import Agent

# Colors - Modern Technical Aesthetic
BG_COLOR = (12, 14, 20)           # Dark Cyberpunk Background
GRID_COLOR = (25, 35, 50)         # Faint blue lines
OBS_BORDER = (0, 255, 255)        # Neon Cyan outline for objects
OBS_FILL = (0, 70, 100)           # Cyan inner fill
START_COLOR = (0, 255, 100)       # Glowing Green
GOAL_COLOR = (255, 50, 100)       # Glowing Red/Pink target
PATH_COLOR = (255, 255, 0, 100)   # Yellow path
TEXT_COLOR = (200, 220, 255)

class Simulation:
    def __init__(self, width=800, height=600, cell_size=20):
        pygame.init()
        # Initialize font for HUD
        pygame.font.init()
        self.font = pygame.font.SysFont("consolas", 14)
        self.large_font = pygame.font.SysFont("consolas", 20, bold=True)
        
        self.width = width
        self.height = height
        self.cell_size = cell_size
        
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AI Autonomous Navigation System - LiDAR/Radar Simulation Vis")
        self.clock = pygame.time.Clock()
        
        self.planner = AStarPlanner(self.grid_width, self.grid_height, self.cell_size)
        self.reset()
        
    def reset(self):
        """Resets the environment with new obstacles, start, and goal."""
        self.obstacles = set()
        self.generate_random_obstacles(density=0.25)
        
        # Ensure start and goal are free
        self.start_pos = (2, 2)
        self.goal_pos = (self.grid_width - 3, self.grid_height - 3)
        
        # Clear out a small 3x3 radius around start and goal
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                self.obstacles.discard((self.start_pos[0]+dx, self.start_pos[1]+dy))
                self.obstacles.discard((self.goal_pos[0]+dx, self.goal_pos[1]+dy))
        
        self.agent = Agent(self.start_pos, self.cell_size)
        
        # Pre-compute path
        path = self.planner.plan(self.start_pos, self.goal_pos, self.obstacles)
        self.agent.set_path(path)
        self.path = path
        
        self.running = True
        self.done = False

    def generate_random_obstacles(self, density=0.2):
        """Randomly blocks cells in the grid to simulate objects."""
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if random.random() < density:
                    self.obstacles.add((x, y))

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (self.width, y))

    def draw_cell(self, x, y, fill_color, border_color=None):
        rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, fill_color, rect)
        if border_color:
            pygame.draw.rect(self.screen, border_color, rect, 1)

    def draw_agent(self):
        """Draws a visually impressive car/robot instead of a simple triangle."""
        # Create a surface with alpha channel
        agent_size = int(self.cell_size * 1.5)
        agent_surface = pygame.Surface((agent_size, agent_size), pygame.SRCALPHA)
        
        # We assume the car points to the RIGHT (0 degrees) natively
        car_width = int(agent_size * 0.8)
        car_height = int(agent_size * 0.5)
        cx = agent_size // 2
        cy = agent_size // 2
        
        # Car body (Metallic Blue)
        body_rect = pygame.Rect(cx - car_width//2, cy - car_height//2, car_width, car_height)
        pygame.draw.rect(agent_surface, (50, 100, 200), body_rect, border_radius=4)
        
        # Windshield
        wind_rect = pygame.Rect(cx - car_width//4, cy - car_height//2 + 2, car_width//2, car_height - 4)
        pygame.draw.rect(agent_surface, (30, 40, 60), wind_rect, border_radius=2)
        
        # Wheels (Dark Gray)
        wheel_w = car_width // 4
        wheel_h = 4
        pygame.draw.rect(agent_surface, (20, 20, 20), (cx - car_width//2 + 2, cy - car_height//2 - 2, wheel_w, wheel_h)) # Top Left
        pygame.draw.rect(agent_surface, (20, 20, 20), (cx + car_width//2 - wheel_w - 2, cy - car_height//2 - 2, wheel_w, wheel_h)) # Top Right
        pygame.draw.rect(agent_surface, (20, 20, 20), (cx - car_width//2 + 2, cy + car_height//2 - 2, wheel_w, wheel_h)) # Bot Left
        pygame.draw.rect(agent_surface, (20, 20, 20), (cx + car_width//2 - wheel_w - 2, cy + car_height//2 - 2, wheel_w, wheel_h)) # Bot Right
        
        # Headlights (Glowing Yellow/White)
        pygame.draw.circle(agent_surface, (255, 255, 150), (cx + car_width//2, cy - car_height//4), 3)
        pygame.draw.circle(agent_surface, (255, 255, 150), (cx + car_width//2, cy + car_height//4), 3)

        # Rotate the car based on agent's angle
        rotated_agent = pygame.transform.rotate(agent_surface, self.agent.angle)
        rect = rotated_agent.get_rect(center=(self.agent.px, self.agent.py))
        self.screen.blit(rotated_agent, rect.topleft)

    def draw_hud(self):
        """Draws a Heads-Up Display (HUD) for technical aesthetics."""
        # Top HUD Bar
        pygame.draw.rect(self.screen, (10, 15, 25, 200), (0, 0, self.width, 40))
        pygame.draw.line(self.screen, OBS_BORDER, (0, 40), (self.width, 40), 2)
        
        title_surf = self.large_font.render("AUTONOMOUS NAVIGATION SYSTEM // RADAR VISUALIZATION", True, OBS_BORDER)
        self.screen.blit(title_surf, (10, 10))
        
        # Display Agent Coordinates & Status
        status_text = "STATUS: ARRIVED" if self.done else ("STATUS: EN ROUTE (No Path Found)" if not self.path else "STATUS: EN ROUTE")
        coord_text = f"GPS (X,Y): {self.agent.x}, {self.agent.y}"
        speed_text = f"TELEMETRY: {self.agent.speed} units/tick"
        
        stat_surf = self.font.render(status_text, True, TEXT_COLOR)
        coord_surf = self.font.render(coord_text, True, TEXT_COLOR)
        speed_surf = self.font.render(speed_text, True, TEXT_COLOR)
        
        self.screen.blit(stat_surf, (10, self.height - 60))
        self.screen.blit(coord_surf, (10, self.height - 40))
        self.screen.blit(speed_surf, (10, self.height - 20))
        
        # Key Controls overlay
        controls = "[SPACE] Reboot Simulation Engine"
        ctrl_surf = self.font.render(controls, True, (150, 150, 150))
        self.screen.blit(ctrl_surf, (self.width - 250, self.height - 20))

    def render(self):
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        
        # Draw obstacles
        for (obs_x, obs_y) in self.obstacles:
            self.draw_cell(obs_x, obs_y, OBS_FILL, OBS_BORDER)
            
        # Draw path using connected lines instead of blocks for a "laser" effect
        if self.path and len(self.path) > 1:
            line_points = []
            for node in self.path:
                px = node[0] * self.cell_size + self.cell_size // 2
                py = node[1] * self.cell_size + self.cell_size // 2
                line_points.append((px, py))
            pygame.draw.lines(self.screen, (255, 200, 0), False, line_points, 3)
            
        # Draw Start and Goal pulsing slightly
        time_ms = pygame.time.get_ticks()
        pulse = abs(math.sin(time_ms / 300.0)) * 50
        
        start_rgb = (START_COLOR[0], max(0, START_COLOR[1] - pulse), START_COLOR[2])
        goal_rgb = (max(0, GOAL_COLOR[0] - pulse), GOAL_COLOR[1], GOAL_COLOR[2])
        
        self.draw_cell(self.start_pos[0], self.start_pos[1], start_rgb)
        self.draw_cell(self.goal_pos[0], self.goal_pos[1], goal_rgb)
        
        # Draw Agent
        self.draw_agent()
        
        # Draw HUD overlays
        self.draw_hud()
        
        pygame.display.flip()

    def run(self):
        """Main simulation loop."""
        print("Simulation Started. Attempting to navigate...")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset() # Press SPACE to restart with new map
                        
            if not self.done:
                self.done = self.agent.update()
                if self.done:
                    print("Navigation Successful! Reached Target.")
                    
            self.render()
            self.clock.tick(60) # 60 FPS
            
        pygame.quit()
