from src.simulation import Simulation

def main():
    print("==========================================")
    print(" AI-Based Autonomous Navigation Simulator ")
    print("==========================================")
    print("Press [SPACE] to generate a new random map.")
    print("Close the window to exit.")
    
    # Initialize the 2D Virtual Environment
    # 800x600 resolution with 20x20 pixel cells
    sim = Simulation(width=800, height=600, cell_size=20)
    
    # Start the simulation loop
    sim.run()

if __name__ == "__main__":
    main()
