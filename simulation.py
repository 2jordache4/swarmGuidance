import pygame
import sys
import heapq
import robot as Robot
import random
import time
import os


# CONSTANTS
thickness = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0,255,0)
ORANGE = (255, 140, 0)
GRID_SIZE = 15  # each cell in pixels

FIRE_COLORS = [
    (255, 255, 255),  # Blanco
    (255, 200, 0),    # Amarillo
    (255, 100, 0),    # Naranja
    (255, 0, 0),      # Rojo
    (50, 0, 0)        # Oscuro
]

# OBJECTS DICTIONARY

objects = {
    "Walls": {
        "Wall1": [(50, 50), (100, 50)],
        "Wall2": [(150, 50), (400, 50)],
        "Wall3": [(450, 50), (500, 50)],
        "Wall4": [(600, 50), (750, 50)],
        # these are the top ^
        "Wall5": [(750, 50), (750, 450)],
        "Wall6": [(750, 520), (750, 550)],
        # these are the right ^
        "Wall7": [(50, 550), (150, 550)],
        "Wall8": [(200, 550), (400, 550)],
        "Wall9": [(450, 550), (550, 550)],
        "Wall10": [(600, 550), (750, 550)],
        # these are the bottom ^
        "Wall11": [(50, 50), (50, 100)],
        "Wall12": [(50, 150), (50, 300)],
        "Wall13": [(50, 350), (50, 450)],
        "Wall14": [(50, 500), (50, 550)],
        # right side ^
        "Wall15": [(350, 50), (350, 250)],
        "Wall16": [(350, 395), (350, 550)],
        "Wall17": [(50, 400), (280, 400)],
        "Wall18": [(250, 250), (250, 350)],
        "Wall19": [(50, 250), (280, 250)],
        # interior ^
    },
    "Windows": {
        "Window1": [(50, 100), (50, 150)],
        "Window2": [(50, 300), (50, 350)],
        "Window3": [(50, 450), (50, 500)],
        "Window4": [(100, 50), (150, 50)],
        "Window5": [(400, 50), (450, 50)],
        "Window6": [(500, 50), (600, 50)],
        "Window7": [(400, 550), (450, 550)],
        "Window8": [(550, 550), (600, 550)],
        "Window9": [(150, 550), (200, 550)],
        #"Window10": [(750, 450), (750, 520)],
        # Window 10 might be the front door
    },
    "Kitchen": {
        "Counter": {"rect": (630, 60, 100, 50)},
        "Table" : {"rect": (420, 150, 100, 50)},
        "chair1" : {"rect": (490, 120, 20, 10)},
        "chair2" : {"rect": (430, 120, 20, 10)},
        "chair3" : {"rect": (490, 230, 20, 10)},
        "chair4" : {"rect": (430, 230, 20, 10)},
        "Stove": {"rect": (550, 60, 60, 50)},
        "Burner1": {"center": (560, 80), "radius": 10},
        "Burner2": {"center": (560, 100), "radius": 10},
        "Burner3": {"center": (580, 80), "radius": 10},
        "Burner4": {"center": (580, 100), "radius": 10},
    },
    "Living_room": {
        "Coach": {"rect": (500, 400, 50, 100)},
        "TV": {"rect": (400,420,20,50)}
    },
    "Beds": {
        "Bed1": {"rect": (70, 140, 100, 50)},
        "Bed2": {"rect": (70,420,100,50)},
        "Closets1": {"rect": (320,70,20,100)},
        "Closets2": {"rect": (170,420,20,50)}
    },
    "Bath": {
        "Tub": {"rect": (70, 300, 50, 80)},
        "taza": {"rect": (200,250,50,50)}},
    "Door": {
        "door1":[(750, 460),(750,500)]
    }
}

rooms={
    "Entrance": {
            "Wall1": [(350, 50), (750, 50)],
            "Wall2": [(750, 50), (750, 550)],
            "Wall3": [(750, 550), (350, 550)],
            "Wall4": [(350, 550), (350, 50)],},

    "Hall": {
            "Wall1": [(250, 250), (350, 250)],
            "Wall2": [(350, 250), (350, 400)],
            "Wall3": [(350, 400), (250, 400)],
            "Wall4": [(250, 400), (250, 250)],
            },

    "Bathroom": {
            "Wall1": [(50, 250), (250, 250)],
            "Wall2": [(250, 250), (250, 400)],
            "Wall3": [(250, 400), (50, 400)],
            "Wall4": [(50, 400), (50, 250)],},

    "RoomUp": {
            "Wall1": [(50, 50), (350, 50)],
            "Wall2": [(350, 50), (350, 250)],
            "Wall3": [(350, 250), (50, 250)],
            "Wall4": [(50, 250), (50, 50)],},

    "RoomDown": {
            "Wall1": [(50, 400), (350, 400)],
            "Wall2": [(350, 395), (350, 550)],
            "Wall3": [(350, 550), (50, 550)],
            "Wall4": [(50, 550), (50, 400)],}
}

class Screen:
    def __init__(self,width, height,objects):
        """Constructor""" 
        self.width = width
        self.height = height
        self.objects = objects
        
        self.game = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Simulation")

    def draw_objects(self):
        """Draw elements from dictionary."""
        for category, items in objects.items():
            if category == "Walls":
                for _, coords in items.items():
                    pygame.draw.line(self.game, BLACK, coords[0], coords[1], thickness)
            elif category == "Windows":
                for _, coords in items.items():
                    pygame.draw.line(self.game, BLUE, coords[0], coords[1], 5)
            elif category == "Kitchen":
                for _, details in items.items():
                    if "rect" in details:
                        pygame.draw.rect(self.game, GRAY, details["rect"])
                    elif "center" in details:
                        pygame.draw.circle(self.game, BLACK, details["center"], details["radius"], 2)
            elif category == "Living_room":
                for _, details in items.items():
                    if "rect" in details:
                        pygame.draw.rect(self.game, GRAY, details["rect"])
            elif category == "Beds":
                for _, details in items.items():
                    if "rect" in details:
                        pygame.draw.rect(self.game, GRAY, details["rect"])
            elif category == "Bath":
                for _, details in items.items():
                    if "rect" in details:
                        pygame.draw.rect(self.game, GRAY, details["rect"])
            elif category == "Fire":
                for _, coords in items.items():
                    pygame.draw.line(self.game, WHITE, coords[0], coords[1], 1)
            elif category == "Door":
                for _, coords in items.items():
                    pygame.draw.line(self.game, WHITE, coords[0], coords[1], 1)

class Draw_Rooms:
    def __init__(self, width, height, rooms):
        """
        Constructor para inicializar la pantalla y los cuartos.
        """
        self.width = width
        self.height = height
        self.rooms = rooms  # rooms
        self.game = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Simulation")

    def draw_rooms(self):
        """
        Dibuja los cuartos a partir del diccionario rooms.
        """
        for room_name, walls in self.rooms.items():  # Itera por los cuartos
            for _, coords in walls.items():  # Itera por las paredes de cada cuarto
                pygame.draw.line(
                    self.game, BLACK, coords[0], coords[1], thickness
                )

class Grid:
    def __init__(self, screen):
        """Constructor"""
        self.screen = screen
        # ^this one is just in case, not sure if we need
        self.width = screen.width
        self.height = screen.height
        self.grid = [[0 for _ in range(self.width // GRID_SIZE)] for _ in range(self.height // GRID_SIZE)]

    def get_grid_size(self):
        print(len(self.grid[0]),len(self.grid[1]))

    def mark_grid(self, fire):
        """
        Sweeps the entire grid and marks cells as occupied if they overlap with objects on the screen.
        Input:
            grid: The occupancy grid.
            screen: Pygame screen where objects are drawn.
            objects: List of drawable objects (rectangles, lines, etc.).
            thickness: Thickness of the objects to check for overlap.
        """
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                cell_rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                if x < 3 or x >= len(self.grid[0]) - 3 or y < 3 or y >= len(self.grid) - 3:
                    self.grid[y][x] = 3
                for category, elements in objects.items(): # category will be 'Walls' etc
                    for name, details in elements.items(): # name will be 'Wall1' etc
                        if category == 'Walls':
                            min_x = min(details[0][0], details[1][0])
                            max_x = max(details[0][0], details[1][0])
                            min_y = min(details[0][1], details[1][1])
                            max_y = max(details[0][1], details[1][1])

                            line_rect = pygame.Rect(min_x - thickness // 2,
                                                    min_y - thickness // 2,
                                                    max_x - min_x + thickness,
                                                    max_y - min_y + thickness)

                            if cell_rect.colliderect(line_rect):
                                self.grid[y][x] = 1
                                break

                            # ^ this is correct
                            # detects that a cell is occupied by a wall (:
                            # noticed that wall 16 was giving a little bit
                            # of trouble from the box, changed its start y coord
                            # from 400 to 410

                        elif category == 'Windows':
                            min_x = min(details[0][0], details[1][0])
                            max_x = max(details[0][0], details[1][0])
                            min_y = min(details[0][1], details[1][1])
                            max_y = max(details[0][1], details[1][1])

                            rect = pygame.Rect(min_x - thickness // 2,
                                                    min_y - thickness // 2,
                                                    max_x - min_x + thickness,
                                                    max_y - min_y + thickness)
                            if cell_rect.colliderect(rect):
                                self.grid[y][x] = 2
                                break
                        # copied from above 

                        elif category == 'Door':
                            min_x = min(details[0][0], details[1][0])
                            max_x = max(details[0][0], details[1][0])
                            min_y = min(details[0][1], details[1][1])
                            max_y = max(details[0][1], details[1][1])

                            rect = pygame.Rect(min_x - thickness // 2,
                                                    min_y - thickness // 2,
                                                    max_x - min_x + thickness,
                                                    max_y - min_y + thickness)
                            if cell_rect.colliderect(rect):
                                self.grid[y][x] = 3
                                break

                        elif category == 'Fire':
                            min_x = min(details[0][0], details[1][0])
                            max_x = max(details[0][0], details[1][0])
                            min_y = min(details[0][1], details[1][1])
                            max_y = max(details[0][1], details[1][1])

                            rect = pygame.Rect(min_x - thickness // 2,
                                                    min_y - thickness // 2,
                                                    max_x - min_x + thickness,
                                                    max_y - min_y + thickness)
                            if cell_rect.colliderect(rect):
                                self.grid[y][x] = 2
                                break
                        # copied from above 

                        elif category == 'Kitchen':
                            # only need the perimeter of the shape
                            if ('rect' in details):
                                stove_rect = pygame.Rect(details.get("rect"))
                                if cell_rect.colliderect(stove_rect):
                                    self.grid[y][x] = 2
                                    break
                        
                        elif category == 'Living_room':
                            # only need the perimeter of the shape
                            if ('rect' in details):
                                stove_rect = pygame.Rect(details.get("rect"))
                                if cell_rect.colliderect(stove_rect):
                                    self.grid[y][x] = 2
                                    break
                        
                        elif category == 'Beds':
                            # only need the perimeter of the shape
                            if ('rect' in details):
                                stove_rect = pygame.Rect(details.get("rect"))
                                if cell_rect.colliderect(stove_rect):
                                    self.grid[y][x] = 2
                                    break
                        # this one is a little chunky
                        elif category == 'Bath':
                            # only need the perimeter of the shape
                            if ('rect' in details):
                                stove_rect = pygame.Rect(details.get("rect"))
                                if cell_rect.colliderect(stove_rect):
                                    self.grid[y][x] = 2
                                    break
        for cell in fire.fire_cells:
            self.grid[cell[1]][cell[0]] = 2  # Marcar como obstáculo (fuego)

    def draw_grid(self,show_grid):
        """Draws the occupancy grid on the screen."""
        if(show_grid == True):
            for y, row in enumerate(self.grid):
                for x, cell in enumerate(row):
                    if (cell != 1):
                        color = WHITE
                        # this means no collision
                    else:
                        color = RED
                        # this means collision
                    pygame.draw.rect(
                        self.screen.game,
                        color,
                        (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                        1
                    )


class Fire:
    def __init__(self, grid, fire_cells, expansion_interval):
        """
        Inicializa el fuego en el mapa.
        :param grid: El mapa del entorno.
        :param fire_cells: Lista inicial de celdas con fuego.
        :param expansion_interval: Intervalo en segundos para la expansión del fuego.
        """
        self.grid = grid  # Referencia al grid
        self.fire_cells = {tuple(cell): 0 for cell in fire_cells}  # Diccionario con el tiempo de vida
        self.expansion_interval = expansion_interval * 1000  # Convertir a milisegundos
        self.last_expansion_time = pygame.time.get_ticks()  # Tiempo de última expansión

        # Marcar las celdas iniciales como fuego en el grid
        for cell in fire_cells:
            self.grid[cell[1]][cell[0]] = 2  # Marcar como obstáculo (fuego)

    def expand_fire(self):
        """
        Expande el fuego a las celdas vecinas.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_expansion_time < self.expansion_interval:
            return  # No es tiempo de expandir el fuego

        new_fire_cells = {}
        for cell, lifetime in self.fire_cells.items():
            neighbors = [
                (cell[0] + 1, cell[1]),  # Derecha
                (cell[0] - 1, cell[1]),  # Izquierda
                (cell[0], cell[1] + 1),  # Abajo
                (cell[0], cell[1] - 1),  # Arriba
            ]
            for neighbor in neighbors:
                # Si la celda vecina está dentro del grid y no es un obstáculo
                if 0 <= neighbor[0] < len(self.grid[0]) and 0 <= neighbor[1] < len(self.grid):
                    if self.grid[neighbor[1]][neighbor[0]] == 0:  # Celda libre
                        self.grid[neighbor[1]][neighbor[0]] = 2  # Marcar como fuego
                        new_fire_cells[neighbor] = 0  # Nueva celda en llamas

        # Actualizar tiempos de vida del fuego
        for cell in self.fire_cells.keys():
            self.fire_cells[cell] += 1

        self.fire_cells.update(new_fire_cells)  # Añadir nuevas celdas en llamas
        self.last_expansion_time = current_time  # Actualizar el tiempo de última expansión

    def draw_fire(self, screen):
        """
        Dibuja las celdas en llamas en la pantalla.
        """
        for cell, lifetime in self.fire_cells.items():
            # Cambiar el color según el tiempo de vida
            if lifetime < 3:
                color = (255, 200, 0)  # Amarillo
            elif lifetime < 6:
                color = (255, 140, 0)  # Naranja
            else:
                color = (255, 0, 0)  # Rojo

            pygame.draw.rect(
                screen.game,
                color,
                (cell[0] * GRID_SIZE, cell[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )


def main():
    pygame.init()

    screen = Screen(800, 600, objects)
    grid = Grid(screen)
    clock = pygame.time.Clock()
    
    # Inicializar el fuego
    initial_fire_cells = [(36, 8), (36, 9), (36, 10),
                          (37, 8), (37, 9), (37, 10),
                          (38, 8), (38, 9), (38, 10),
                          (39, 8), (39, 9), (39, 10),
                          (40, 8), (40, 9), (40, 10),
                          (41, 8), (41, 9), (41, 10)]  # Coordenadas iniciales en el grid
    fire = Fire(grid.grid, initial_fire_cells, expansion_interval=3)
    grid.mark_grid(fire)
    print(fire.fire_cells)
    # Inicializar los robots
    robot = Robot.MockRobot(start_position=(700, 500), target_position=(500, 500), speed=15, sensor=20)
    robot2 = Robot.MockRobot(start_position=(600, 500), target_position=(500, 500), speed=15, sensor=20)
    sweep1 = Robot.Sweep(robot)
    sweep2 = Robot.Sweep(robot2)
    sweep1.explore_grid(grid.grid)
    sweep2.explore_grid(grid.grid)

    pilot = Robot.MockRobot(start_position=(700, 500),
                            target_position=(90, 100),
                            speed=10,sensor=25)
    A_star = Robot.PathPlanning(pilot,grid.grid)
    A_star.find_path()
    x = 1
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Expansión del fuego
        fire.expand_fire()
        # Movimiento de los robots
        robot.move()
        robot2.move()
        robot.get_sensor_reading(grid)
        robot2.get_sensor_reading(grid)
        sweep2.explore_grid(grid.grid)
        sweep1.explore_grid(grid.grid)
        
        # Actualización de la pantalla
        screen.game.fill(WHITE)
        screen.draw_objects()
        fire.draw_fire(screen)  # Dibujar el fuego
        grid.draw_grid(True)
        robot.draw(screen.game, BLUE)
        robot2.draw(screen.game, GREEN)
        #print(fire.fire_cells.keys())
        if len(robot.path) == 0:
            if x == 1:
                pygame.time.wait(3000)
                x=0
            pilot.move()
            pilot.draw(screen.game, RED)
            
        pygame.display.flip()
        clock.tick(50)  # Frames por segundo

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

