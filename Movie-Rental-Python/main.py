
# main.py - Runs the movie rental system
# Author: Maurizio Gonzalez

from system import MovieManagementSystem

if __name__ == "__main__":
    system = MovieManagementSystem()
    system.read_file("data.csv")
    system.run()