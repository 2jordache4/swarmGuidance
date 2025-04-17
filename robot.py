import pygame
import heapq
from enum import IntEnum
import math

GRID_SIZE = 15
thickness = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0,255,0)

class MockRobot:

    def __init__(self, start_position, target_position, speed, sensor):
        """
        Inicializa el robot para usar A* en un grid.
        """
        #self.grid_robot = grid  # Rejilla ocupada (0: libre, 1: obstáculo)
        self.current_cell = (int(start_position[0] // GRID_SIZE),
                           int(start_position[1] // GRID_SIZE))
        self.target_cell = (int(target_position[0] // GRID_SIZE),
                            int(target_position[1] // GRID_SIZE))
        self.position = pygame.Vector2(
            start_position)  # Posición actual en píxeles
        self.path = []  # Lista de celdas que el robot seguirá
        self.speed = speed  # Velocidad en píxeles por frame
        self.radius = 5  # Radio visual del robot
        self.sensor = sensor

    def move(self):
        """
        Mueve el robot a lo largo del camino calculado.
        """
        if self.path:
            next_cell = self.path[0]
            next_position = pygame.Vector2(
                next_cell[0] * GRID_SIZE + GRID_SIZE // 2,
                next_cell[1] * GRID_SIZE + GRID_SIZE // 2,
            )
            self.current_cell = (next_position[0] // GRID_SIZE, next_position[1]//GRID_SIZE)

            direction = next_position - self.position
            if direction.length() > self.speed:
                direction = direction.normalize() * self.speed

            self.position += direction

            # Si llegamos a la celda objetivo, removemos la celda de la ruta
            if self.position.distance_to(next_position) < 1:
                self.path.pop(0)

    def draw(self, screen, color):
        """
        Dibuja el robot en su posición actual.
        """
        pygame.draw.circle(
            screen,  # Accede directamente a la pantalla
            color,
            (int(self.position.x), int(self.position.y)),
            self.radius)
        pygame.draw.circle(
            screen,
            color,  # green for visibility, can be adjusted
            (int(self.position.x), int(self.position.y)),
            self.sensor,  # sensor as radius
            width=1  # outline
        )

    def get_sensor_reading(self,grid_robot):
        current = self.get_grid_coordinates()
        neighbor_offsets = [
            (1, 0),   # Derecha (Right)
            (-1, 0),  # Izquierda (Left)
            (0, 1),   # Abajo (Down)
            (0, -1),  # Arriba (Up)
            (1, -1),  # Diagonal Down-Right
            (-1, -1), # Diagonal Down-Left
            (1, 1),   # Diagonal Up-Right
            (-1, 1),  # Diagonal Up-Left
        ]

        for offset in neighbor_offsets:
            neighbor = (current[0] + offset[0], current[1] + offset[1])
            try:
                cell = grid_robot.grid[neighbor[1]][neighbor[0]]
                if cell == 2:
                    # self.grid_robot.mark_cell(neighbor[0], neighbor[1])
                    #^ deleted this function, wasn't needed
                    grid_robot.grid[neighbor[1]][neighbor[0]] = 1
            except IndexError:
                continue

    def get_grid_coordinates(self):
        return (int(self.current_cell[0]),
                           int(self.current_cell[1]))

    def get_screen_coordinates(self):
        return self.current_cell
    
    def get_grid_target(self):
        return self.target_cell
    
    def goal_reached(self):
        if self.current_cell == self.target_cell:
            return False
        else:
            return True

class PathPlanning:

    def __init__(self, robot, grid):
        self.robot = robot
        self.grid = grid

    def heuristic(self, cell1, cell2):
        """Calcula la distancia EUCLIDEAN entre dos celdas."""
        return ((cell1[0] - cell2[0])**2 + (cell1[1] - cell2[1])**2)**0.5
    
    def find_path(self):
        """
        Calcula el camino de ida y vuelta usando A*.
        """
        start = self.robot.get_grid_coordinates()
        target = self.robot.get_grid_target()

        # Camino de inicio al objetivo // Way back to the target
        path_to_goal = self.a_star(start, target)

        # Camino de regreso al inicio // Way back to the start
        path_to_start = self.a_star(target, start)

        # Concatenar ambos caminos // 
        self.robot.path = path_to_goal + path_to_start

    def a_star(self, start, target):
        """
        Implementa el algoritmo A* para calcular un camino.
        """
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, target)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == target:  # Llegamos al destino
                return self.reconstruct_path(came_from, current)

            neighbors = [
                (current[0] + 1, current[1]),  # Derecha
                (current[0] - 1, current[1]),  # Izquierda
                (current[0], current[1] + 1),  # Abajo
                (current[0], current[1] - 1),  # Arriba
                (current[0] + 1, current[1] - 1),
                (current[0] - 1, current[1] - 1),
                (current[0] + 1, current[1] - 1),
                (current[0] - 1, current[1] - 1),
            ]

            for neighbor in neighbors:
                # Verifica que la celda esté dentro del grid y sea transitable
                if 0 <= neighbor[0] < len(self.grid[0]) and 0 <= neighbor[1] < len(self.grid):
                    if self.grid[neighbor[1]][neighbor[0]] == 1 or self.grid[neighbor[1]][neighbor[0]] == 2:  # Obstáculo
                        continue

                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, target)
                        if neighbor not in [i[1] for i in open_set]:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return []  # Retorna lista vacía si no hay camino

    def reconstruct_path(self, came_from, current):
        """
        Reconstruye el camino desde el inicio hasta el destino.
        """
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()  # Invertimos para que el camino sea del inicio al destino
        return path


class Sweep:

    def __init__(self, robot):
        self.robot = robot
        #self.grid = robot.grid_robot
        self.visited = set()

    def is_valid_cell(self, cell, grid):
        """
        Verifica si una celda es válida para moverse.
        """
        x, y = cell
        return (
            0 <= x < len(grid[0]) and  # Dentro de los límites horizontales
            0 <= y < len(grid) and  # Dentro de los límites verticales
            grid[y][x] == 0 and  # Libre de obstáculos / Obstacle free
            cell not in self.visited  # No visited
        )

    def explore_grid(self,grid):
        """
        Usa DFS para generar la ruta que visite todas las celdas libres.
        """
        stack = [self.robot.current_cell]  
        came_from = {}  

        while stack:
            current = stack.pop()

            if current not in self.visited:
                self.visited.add(current)  
                self.robot.path.append(current)  

                # Get valid neighbors
                neighbors = [
                    (current[0] + 1, current[1]),  # Right
                    (current[0] - 1, current[1]),  # Left
                    (current[0], current[1] + 1),  # Down
                    (current[0], current[1] - 1),  # Up
                ]

                # valid neighbors
                valid_neighbors = [neighbor for neighbor in neighbors if self.is_valid_cell(neighbor, grid)]

                # continue exploring
                if valid_neighbors:
                    for neighbor in valid_neighbors:
                        came_from[neighbor] = current
                    stack.extend(valid_neighbors)
                else:
                    # backtrack to the previous cell
                    if current in came_from:
                        prev_cell = came_from[current]
                        stack.append(prev_cell)
