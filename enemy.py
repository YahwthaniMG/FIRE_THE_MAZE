import pygame
import random
import math
from enum import Enum
from sound_manager import SoundManager
class EnemyType(Enum):
    WATER = "waterEnemy.png"
    ICE = "iceEnemy.png"
    EXTINGUISHER = "extintorEnemy.png"

class Enemy:
    def __init__(self, maze, enemy_type, grid_size, player_start_pos, offset_x, offset_y):
        self.maze = maze
        self.enemy_type = enemy_type
        self.grid_size = grid_size
        self.player_start_pos = player_start_pos
        self.sound_manager = SoundManager()
        self.offset_x = offset_x
        self.offset_y = offset_y
        
        # Velocidades diferentes por tipo
        self.speeds = {
            EnemyType.WATER: 0.04,
            EnemyType.ICE: 0.02,
            EnemyType.EXTINGUISHER: 0.06
        }
        self.speed = self.speeds[enemy_type]
        
        # Posición y movimiento
        self.pos = self.find_valid_spawn_position()
        self.target = None
        self.patrol_distance = {
            EnemyType.WATER: 5,    # Distancia media
            EnemyType.ICE: 3,      # Distancia corta
            EnemyType.EXTINGUISHER: 7  # Distancia larga
        }[enemy_type]
        
        self.grid_pos = self.find_valid_spawn_position()
        self.pos = self.grid_pos
        self.next_move_time = 0
        self.move_delay = {
            EnemyType.WATER: 500,      
            EnemyType.ICE: 750,        
            EnemyType.EXTINGUISHER: 375
        }[enemy_type]
        
        # Radio de detección aumentado
        self.detection_radius = {
            EnemyType.WATER: 6,      
            EnemyType.ICE: 5,        
            EnemyType.EXTINGUISHER: 8  
        }[enemy_type]
        
        # Velocidad de persecución
        self.chase_delay = {
            EnemyType.WATER: 333,     # Más rápido en persecución
            EnemyType.ICE: 500,
            EnemyType.EXTINGUISHER: 250
        }[enemy_type]
        
        # Estado de persecución
        self.chasing = False
        
        # Colisión y visualización
        self.collision_radius = 0.7
        self.image = pygame.image.load(f"assets/{enemy_type.value}")
        self.image = pygame.transform.scale(self.image, (grid_size, grid_size))

    def can_see_player(self, player_pos):
        r, c = int(self.pos[0]), int(self.pos[1])
        player_r, player_c = player_pos
        
        # Verificar distancia Manhattan
        distance = abs(player_r - r) + abs(player_c - c)
        if distance > self.detection_radius:
            return False
        
        # Verificar línea de visión
        points = self.get_line(r, c, player_r, player_c)
        return all(self.maze[int(p[0])][int(p[1])] == 0 for p in points)

    def get_line(self, x1, y1, x2, y2):
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        sx = 1 if x2 > x1 else -1
        sy = 1 if y2 > y1 else -1
        
        if dx > dy:
            err = dx / 2
            while x != x2:
                points.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2
            while y != y2:
                points.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        points.append((x, y))
        return points
    
    def get_chase_move(self, player_pos):
        r, c = int(self.pos[0]), int(self.pos[1])
        player_r, player_c = player_pos
        
        possible_moves = self.get_valid_moves()
        if not possible_moves:
            return None
            
        # Elegir movimiento más cercano al jugador
        return min(possible_moves, 
                    key=lambda pos: abs(pos[0] - player_r) + abs(pos[1] - player_c))
    
    def find_valid_spawn_position(self):
        rows, cols = len(self.maze), len(self.maze[0])
        safe_distance = 5
        
        while True:
            r = random.randint(1, rows-2)
            c = random.randint(1, cols-2)
            player_r, player_c = self.player_start_pos
            distance_to_player = abs(r - player_r) + abs(c - player_c)
            
            if self.maze[r][c] == 0 and distance_to_player >= safe_distance:
                return [float(r), float(c)]

    def find_random_target(self):
        rows, cols = len(self.maze), len(self.maze[0])
        current_r, current_c = int(self.pos[0]), int(self.pos[1])
        max_attempts = 20
        
        for _ in range(max_attempts):
            # Generar punto aleatorio dentro del radio de patrulla
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(2, self.patrol_distance)
            target_r = int(current_r + math.cos(angle) * distance)
            target_c = int(current_c + math.sin(angle) * distance)
            
            # Verificar si el punto es válido
            if (0 < target_r < rows-1 and 
                0 < target_c < cols-1 and 
                self.maze[target_r][target_c] == 0):
                return [float(target_r), float(target_c)]
        
        # Si no se encuentra punto válido, usar punto cercano
        return self.find_nearby_valid_point()

    def get_valid_moves(self):
        r, c = int(self.pos[0]), int(self.pos[1])
        possible_moves = []
        
        # Comprobar las cuatro direcciones
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            new_r, new_c = r + dr, c + dc
            if (0 < new_r < len(self.maze)-1 and 
                0 < new_c < len(self.maze[0])-1 and 
                self.maze[new_r][new_c] == 0):
                possible_moves.append((new_r, new_c))
        
        return possible_moves

    def find_nearby_valid_point(self):
        current_r, current_c = int(self.pos[0]), int(self.pos[1])
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_r = current_r + dr
                new_c = current_c + dc
                if (0 < new_r < len(self.maze)-1 and 
                    0 < new_c < len(self.maze[0])-1 and 
                    self.maze[new_r][new_c] == 0):
                    return [float(new_r), float(new_c)]
        return self.pos

    def move_towards_target(self):
        if not self.target:
            return
        
        dx = self.target[0] - self.pos[0]
        dy = self.target[1] - self.pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 0.1:  # Llegamos al objetivo
            self.target = None
            return
        
        # Normalizar y aplicar velocidad
        dx = (dx/distance) * self.speed
        dy = (dy/distance) * self.speed
        
        # Verificar colisión antes de mover
        new_pos = [self.pos[0] + dx, self.pos[1] + dy]
        if self.is_valid_position(new_pos[0], new_pos[1]):
            self.pos = new_pos

    def is_valid_position(self, r, c):
        grid_r, grid_c = int(r), int(c)
        return (0 < grid_r < len(self.maze)-1 and 
                0 < grid_c < len(self.maze[0])-1 and 
                self.maze[grid_r][grid_c] == 0)
        
    def get_flee_move(self, player_pos):
        r, c = int(self.pos[0]), int(self.pos[1])
        player_r, player_c = player_pos
        
        possible_moves = self.get_valid_moves()
        if not possible_moves:
            return None
        
        # Elegir el movimiento que más nos aleje del jugador
        return max(possible_moves, 
                key=lambda pos: abs(pos[0] - player_r) + abs(pos[1] - player_c))

    def update(self, player_pos, current_time, player_is_powered):
        if current_time < self.next_move_time:
            return
        
        if player_is_powered and self.can_see_player(player_pos):
            # Modo huida
            new_pos = self.get_flee_move(player_pos)
            if new_pos:
                self.pos = [float(new_pos[0]), float(new_pos[1])]
            self.next_move_time = current_time + self.chase_delay  # Usar velocidad de persecución para huir
        else:
            # Comportamiento normal
            self.chasing = self.can_see_player(player_pos)
            if self.chasing:
                self.sound_manager.start_persecution()
                new_pos = self.get_chase_move(player_pos)
                if new_pos:
                    self.pos = [float(new_pos[0]), float(new_pos[1])]
                self.next_move_time = current_time + self.chase_delay
            else:
                self.sound_manager.stop_persecution()
                possible_moves = self.get_valid_moves()
                if possible_moves:
                    new_pos = random.choice(possible_moves)
                    self.pos = [float(new_pos[0]), float(new_pos[1])]
                self.next_move_time = current_time + self.move_delay

    def check_collision(self, player_pos):
        player_r, player_c = player_pos
        distance = abs(player_r - self.pos[0]) + abs(player_c - self.pos[1])
        return distance < self.collision_radius

    def draw(self, screen):
        screen_x = self.pos[1] * self.grid_size + self.offset_x
        screen_y = self.pos[0] * self.grid_size + self.offset_y
        screen.blit(self.image, (screen_x, screen_y))