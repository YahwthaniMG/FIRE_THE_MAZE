import pygame
import heapq
import random
import math
from menu import Menu
from fire import Fire
from winScreen import WinScreen
from gameOver import GameOverScreen
from enemy import Enemy, EnemyType
from sound_manager import SoundManager

pygame.init()

# Obtener resolución de la pantalla
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h
GRID_SIZE = 40
ROWS = SCREEN_HEIGHT // GRID_SIZE
COLS = SCREEN_WIDTH // GRID_SIZE

main_font = pygame.font.SysFont("Arial", 50)
secundary_font = pygame.font.Font(None, 40)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
maze_density = 4

player_image = pygame.image.load("assets/firePlayer.png")
player_image = pygame.transform.scale(player_image, (GRID_SIZE, GRID_SIZE))

# Inicializar pantalla en modo completo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("FIRE THE MAZE")

# Calcular tamaño de grid basado en la pantalla
GRID_SIZE = min(SCREEN_WIDTH // 20, SCREEN_HEIGHT // 20)  # 20x20 celdas aproximadamente
ROWS = SCREEN_HEIGHT // GRID_SIZE
COLS = SCREEN_WIDTH // GRID_SIZE

# Calcular offset para centrar el laberinto
MAZE_WIDTH = COLS * GRID_SIZE
MAZE_HEIGHT = ROWS * GRID_SIZE
OFFSET_X = (SCREEN_WIDTH - MAZE_WIDTH) // 2
OFFSET_Y = (SCREEN_HEIGHT - MAZE_HEIGHT) // 2

clock = pygame.time.Clock()

def generate_maze(rows, cols, start, end):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    create_random_maze(maze, start[0], start[1], rows, cols)
    
    # Asegurar que hay camino hacia la meta
    path_found = False
    while not path_found:
        temp_maze = [row[:] for row in maze]
        temp_maze[end[0]][end[1]] = 0
        
        test_path = dijkstra(temp_maze, start, end)
        if test_path:
            path_found = True
            maze = temp_maze
        else:
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                new_r, new_c = end[0] + dr, end[1] + dc
                if 0 < new_r < rows-1 and 0 < new_c < cols-1:
                    maze[new_r][new_c] = 0

    open_paths = (rows * cols) // maze_density
    for _ in range(open_paths):
        random_row = random.randint(1, rows - 2)
        random_col = random.randint(1, cols - 2)
        maze[random_row][random_col] = 0
    
    return maze

def create_random_maze(maze, x, y, total_rows, total_cols):
    maze[x][y] = 0
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    random.shuffle(directions)
    for directionX, directionY in directions:
        next_row = x + directionX
        next_col = y + directionY

        if valid_cell(next_row, next_col, total_rows, total_cols, maze):
            maze[next_row][next_col] = 0
            create_random_maze(maze, next_row, next_col, total_rows, total_cols)

def valid_cell(next_row, next_col, total_rows, total_cols, maze):
    if not (1 <= next_row < total_rows - 1 and 1 <= next_col < total_cols - 1):
        return False

    open_neighbors = 0
    for row_offset, col_offset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        neighbor_row = next_row + row_offset
        neighbor_col = next_col + col_offset
        if 0 <= neighbor_row < total_rows and 0 <= neighbor_col < total_cols:
            if maze[neighbor_row][neighbor_col] == 0:
                open_neighbors += 1

    return maze[next_row][next_col] == 1 and open_neighbors < 2

def calculate_weights(maze, enemies, fires, current_pos):
    rows, cols = len(maze), len(maze[0])
    weights = [[float('inf') if maze[r][c] == 1 else 1.0 for c in range(cols)] for r in range(rows)]
    
    # Aumentar significativamente el radio de influencia
    enemy_influence_radius = 8  # Aumentado de 4 a 8
    danger_multiplier = 10     # Aumentado de 5 a 10
    
    # Añadir pesos por proximidad a enemigos
    for enemy in enemies:
        enemy_r, enemy_c = int(enemy.pos[0]), int(enemy.pos[1])
        
        for r in range(max(0, enemy_r - enemy_influence_radius), 
                        min(rows, enemy_r + enemy_influence_radius + 1)):
            for c in range(max(0, enemy_c - enemy_influence_radius), 
                        min(cols, enemy_c + enemy_influence_radius + 1)):
                if maze[r][c] == 0:
                    # Usar distancia Manhattan para mayor área de influencia
                    distance = abs(r - enemy_r) + abs(c - enemy_c)
                    if distance <= enemy_influence_radius:
                        # Peso exponencial más agresivo
                        danger_weight = ((enemy_influence_radius - distance + 1) ** 2.5) * danger_multiplier
                        weights[r][c] += danger_weight
                        
                        # Añadir peso extra a las celdas muy cercanas
                        if distance <= 3:  # Área de peligro inmediato
                            weights[r][c] += danger_weight * 2
    
    # Reducir pesos cerca de llamas no recolectadas (mantenido igual)
    if fires and not fires.all_collected():
        fire_influence_radius = 3
        for fire_pos in fires.collectible_fires:
            fire_r, fire_c = fire_pos
            
            for r in range(max(0, fire_r - fire_influence_radius), 
                        min(rows, fire_r + fire_influence_radius + 1)):
                for c in range(max(0, fire_c - fire_influence_radius), 
                            min(cols, fire_c + fire_influence_radius + 1)):
                    if maze[r][c] == 0:
                        distance = math.sqrt((r - fire_r)**2 + (c - fire_c)**2)
                        if distance <= fire_influence_radius:
                            weights[r][c] *= max(0.5, distance / fire_influence_radius)

    return weights

def dijkstra(maze, start, end, enemies=None, fires=None):
    if enemies is None:
        enemies = []
    
    weights = calculate_weights(maze, enemies, fires, start)
    rows, cols = len(maze), len(maze[0])
    distances = {(r, c): float('inf') for r in range(rows) for c in range(cols)}
    distances[start] = 0
    priority_queue = [(0, start)]
    came_from = {}

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)
        
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        r, c = current
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                weight = weights[nr][nc]
                new_distance = current_distance + weight
                
                if new_distance < distances[(nr, nc)]:
                    distances[(nr, nc)] = new_distance
                    heapq.heappush(priority_queue, (new_distance, (nr, nc)))
                    came_from[(nr, nc)] = current

    return []

def draw_maze(maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            color = WHITE if maze[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, 
                           (col * GRID_SIZE + OFFSET_X, 
                            row * GRID_SIZE + OFFSET_Y, 
                            GRID_SIZE, GRID_SIZE))

def main():
    global GRID_SIZE, player_image  # Declarar ambas variables como globales
    # Generate maze and initial setup
    maze = generate_maze(ROWS, COLS, (1,1), (ROWS - 2, COLS - 2))
    fire = Fire(maze, ROWS, COLS, GRID_SIZE, OFFSET_X, OFFSET_Y)
    power_up_active = False
    power_up_end_time = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    is_fullscreen = False
    
    sound_manager = SoundManager()
    sound_manager.start_music()

    player_start_pos = (1, 1)
    player_pos = player_start_pos
    exit_pos = (ROWS - 2, COLS - 2)
    
    # Crear enemigos aleatorios con distancia segura al jugador
    enemy_types = [EnemyType.WATER, EnemyType.ICE, EnemyType.EXTINGUISHER]
    enemies = []
    for _ in range(6):  # Crear 6 enemigos
        random_type = random.choice(enemy_types)
        enemies.append(Enemy(maze, random_type, GRID_SIZE, player_start_pos, OFFSET_X, OFFSET_Y))
    
    win_screen = WinScreen(main_font, screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    game_over_screen = GameOverScreen(main_font, screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    EXIT_LOCKED = (255, 165, 0)
    EXIT_UNLOCKED = (0, 255, 0)

    running = True
    last_move_time = 0
    move_delay = 100

    # Game Loop
    while running:
        current_time = pygame.time.get_ticks()
        if power_up_active and current_time >= power_up_end_time:
            power_up_active = False
            sound_manager.stop_immunity()
        else:
            power_up_active = power_up_end_time > current_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Tecla 'F' para alternar pantalla completa
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                    # Actualizar tamaño del grid
                    current_w, current_h = screen.get_size()
                    GRID_SIZE = min(current_w // COLS, current_h // ROWS)
                    # Reescalar imágenes
                    player_image = pygame.transform.scale(player_image, (GRID_SIZE, GRID_SIZE))
                    for enemy in enemies:
                        enemy.image = pygame.transform.scale(enemy.image, (GRID_SIZE, GRID_SIZE))
                    fire.rescale_images(GRID_SIZE)
            elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                GRID_SIZE = min(event.w // COLS, event.h // ROWS)

        # Player movement
        if current_time - last_move_time >= move_delay:
            keys = pygame.key.get_pressed()
            r, c = player_pos
            new_pos = player_pos

            if (keys[pygame.K_w] or keys[pygame.K_UP]) and r > 0 and maze[r-1][c] == 0:
                new_pos = (r-1, c)
            elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and r < ROWS-1 and maze[r+1][c] == 0:
                new_pos = (r+1, c)
            elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and c > 0 and maze[r][c-1] == 0:
                new_pos = (r, c-1)
            elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and c < COLS-1 and maze[r][c+1] == 0:
                new_pos = (r, c+1)

            if new_pos != player_pos:
                player_pos = new_pos
                last_move_time = current_time

        # Victory condition
        if player_pos == exit_pos and fire.all_collected():
            sound_manager.stop_all_sounds()  # Detener todos los sonidos
            sound_manager.play_win()
            win_screen.display()
            pygame.display.flip()
            win_screen_shown = True
            while win_screen_shown:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        win_screen_shown = False
                    elif win_screen.handle_click(event):
                        sound_manager.return_to_menu()  # Reiniciar música del menú
                        win_screen_shown = False
                        return
                pygame.time.delay(50)

        # Draw game state
        draw_maze(maze)
        fire.draw(screen)
        
        # Draw path
        path = dijkstra(maze, player_pos, exit_pos, enemies, fire)
        path_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(path_surface, (0, 255, 0, 128), (0, 0, GRID_SIZE, GRID_SIZE))
        for step in path:
            if step != player_pos:  # No dibujar el path donde está el jugador
                screen.blit(path_surface, 
                        (step[1] * GRID_SIZE + OFFSET_X, 
                        step[0] * GRID_SIZE + OFFSET_Y))

        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen)

        # Draw exit with lock indicator
        exit_color = EXIT_UNLOCKED if fire.all_collected() else EXIT_LOCKED
        pygame.draw.rect(screen, exit_color, 
                        (exit_pos[1] * GRID_SIZE + OFFSET_X, 
                        exit_pos[0] * GRID_SIZE + OFFSET_Y, 
                        GRID_SIZE, GRID_SIZE))

        if not fire.all_collected():
            lock_size = GRID_SIZE // 2
            lock_x = exit_pos[1] * GRID_SIZE + OFFSET_X + (GRID_SIZE - lock_size) // 2
            lock_y = exit_pos[0] * GRID_SIZE + OFFSET_Y + (GRID_SIZE - lock_size) // 2
            pygame.draw.line(screen, BLACK, (lock_x, lock_y), 
                            (lock_x + lock_size, lock_y + lock_size), 3)
            pygame.draw.line(screen, BLACK, (lock_x + lock_size, lock_y), 
                            (lock_x, lock_y + lock_size), 3)

        # Dibujar jugador
        screen.blit(player_image, 
                    (player_pos[1] * GRID_SIZE + OFFSET_X, 
                    player_pos[0] * GRID_SIZE + OFFSET_Y))

        # Verificación de colisiones  
        for enemy in enemies[:]:  # Usar copia para poder eliminar mientras iteramos
            enemy.update(player_pos, current_time, power_up_active)
            if enemy.check_collision(player_pos):
                if power_up_active:
                    enemies.remove(enemy)  # Eliminar enemigo si está activo el power-up
                    sound_manager.play_kill()
                else:
                    # Game Over si no está activo
                    sound_manager.stop_all_sounds()  # Detener todos los sonidos
                    sound_manager.play_game_over()
                    game_over_screen.display(enemy.enemy_type.name)
                    pygame.display.flip()
                    game_over_shown = True
                    while game_over_shown:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                game_over_shown = False
                            elif game_over_screen.handle_click(event):
                                sound_manager.return_to_menu()  # Reiniciar música del menú
                                game_over_shown = False
                                return
                        pygame.time.delay(50)
            enemy.draw(screen)
            
        collected, is_powerup = fire.collect(player_pos)
        # Al recolectar powerup
        if collected:
            if is_powerup:
                power_up_end_time = current_time + 5000  # 5 segundos de powerup
                sound_manager.start_immunity()
            else:
                sound_manager.play_power_up()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    menu = Menu(screen,main_font, secundary_font, clock)
    while True:
        action = menu.display_menu()
        if action == "start":
            main()
        elif action == "instructions":
            menu.display_instructions()


