import random
import pygame

class FireType:
    NORMAL = "fireFlames.png"
    BLUE = "bluefireFlame.png"

class Fire:
    def __init__(self, maze, rows, cols, grid_size, offset_x, offset_y):
        self.positions = []
        self.grid_size = grid_size
        self.collectible_fires = []
        self.fire_types = {}  # Almacena el tipo de cada fuego
        self.offset_x = offset_x
        self.offset_y = offset_y
        
        # Cargar imágenes
        self.fire_images = {
            FireType.NORMAL: pygame.image.load(f"assets/{FireType.NORMAL}"),
            FireType.BLUE: pygame.image.load(f"assets/{FireType.BLUE}")
        }
        
        # Escalar imágenes
        for key in self.fire_images:
            self.fire_images[key] = pygame.transform.scale(self.fire_images[key], (grid_size, grid_size))

        # Encontrar posiciones válidas
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                if maze[r][c] == 0:
                    self.positions.append((r, c))

        # Seleccionar posiciones aleatorias
        selected_positions = random.sample(self.positions, k=8)
        
        # Asignar tipos a las posiciones
        for i, pos in enumerate(selected_positions):
            self.collectible_fires.append(pos)
            # Las primeras 6 son normales, las últimas 2 son azules
            self.fire_types[pos] = FireType.BLUE if i >= 6 else FireType.NORMAL

    def draw(self, screen):
        for fire_pos in self.collectible_fires:
            fire_x = fire_pos[1] * self.grid_size + self.offset_x
            fire_y = fire_pos[0] * self.grid_size + self.offset_y
            fire_type = self.fire_types[fire_pos]
            screen.blit(self.fire_images[fire_type], (fire_x, fire_y))

    def collect(self, player_pos):
        if player_pos in self.collectible_fires:
            fire_type = self.fire_types[player_pos]
            self.collectible_fires.remove(player_pos)
            return True, fire_type == FireType.BLUE
        return False, False

    def all_collected(self):
        return len(self.collectible_fires) == 0
    
    def rescale_images(self, new_size):
        for key in self.fire_images:
            self.fire_images[key] = pygame.transform.scale(self.fire_images[key], (new_size, new_size))