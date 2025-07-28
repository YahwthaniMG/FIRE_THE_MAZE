import pygame

class Menu:
    def __init__(self, screen, main_font, secundary_font, timer):
        self.running = True
        self.screen = screen
        self.main_font = main_font
        self.secundary_font = secundary_font
        self.timer = timer
        self.credits_font = pygame.font.Font(None, 24)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)  # Más canales para los sonido
        self.menu_music = pygame.mixer.Sound('resources/MusicGame.mp3')
        self.button_sound = pygame.mixer.Sound('resources/Confirm.mp3')
        # Configurar volúmenes
        self.menu_music.set_volume(0.5)  # 50% volumen para música
        self.button_sound.set_volume(1.0)  # 100% volumen para efectos
        
        # Reproducir música de fondo
        self.menu_channel = pygame.mixer.Channel(0)
        self.menu_channel.play(self.menu_music, loops=-1)
        
        # Canal separado para efectos de sonido
        self.effect_channel = pygame.mixer.Channel(1)
        
    def play_button_sound(self):
        self.effect_channel.play(self.button_sound)

    def display_menu(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.play_button_sound()
                        return "start"
                    if instructions_button.collidepoint(event.pos):
                        self.play_button_sound()
                        return "instructions"

            # Título
            title_font = pygame.font.SysFont("Arial", 80)  # Aumentado de 50 a 80
            title_text = title_font.render("FIRE THE MAZE", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 200))  # Ajustado posición Y
            self.screen.blit(title_text, title_rect)

            # Botones
            button_font = pygame.font.Font(None, 60)
            # START button
            start_text = button_font.render("START", True, (0, 0, 0))
            start_button = pygame.Rect(self.screen.get_width() // 2 - 150, 350, 300, 70)  
            pygame.draw.rect(self.screen, (255, 255, 255), start_button)
            self.screen.blit(start_text, start_text.get_rect(center=start_button.center))

            # INSTRUCTIONS button
            instructions_text = button_font.render("INSTRUCTIONS", True, (0, 0, 0))
            instructions_button = pygame.Rect(self.screen.get_width() // 2 - 200, 450, 400, 70)  # Más ancho y alto
            pygame.draw.rect(self.screen, (255, 255, 255), instructions_button)
            self.screen.blit(instructions_text, instructions_text.get_rect(center=instructions_button.center))
        
            # Créditos
            developers = [
                "Developers:",
                "Gabriel Guerra",
                "Zaid Gutierrez",
                "Brandon Magaña",
                "Yahwthani Morales"
                
            ]
            y_offset = self.screen.get_height() - (len(developers) * 25) - 10
            for line in developers:
                credit_text = self.credits_font.render(line, True, (255, 255, 255))
                self.screen.blit(credit_text, (10, y_offset))
                y_offset += 25

            pygame.display.flip()
                

    def display_instructions(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        self.play_button_sound()
                        return

            instructions = [
                "Controls:",
                "- Use W, A, S, D or Arrow Keys to move the player.",
                "",
                "Objective:",
                "- SURVIVE and collect all your missing flames",
                "- Avoid the enemies that can extinguish you:",
                "  * Water drops will chase you",
                "  * Ice crystals will freeze you",
                "  * Fire extinguishers will put you out",
                "",
                "Tips:",
                "- Follow the green path to find the safest route",
                "- Collect all flames before reaching the exit",
                "- The exit will be orange until you collect all flames"
            ]

            # Renderizar instrucciones
            y_offset = 120  # Empezar más abajo para dar espacio al título
            for line in instructions:
                text = self.secundary_font.render(line, True, (255, 255, 255))
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 40

            # Botón de retorno
            button_font = pygame.font.Font(None, 60)
            back_text = button_font.render("Return to Menu", True, (0, 0, 0))
            back_button = pygame.Rect(self.screen.get_width() // 2 - 200, 700, 400, 70)
            pygame.draw.rect(self.screen, (255, 255, 255), back_button)
            self.screen.blit(back_text, back_text.get_rect(center=back_button.center))

            pygame.display.flip()
                

    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button.collidepoint(event.pos):
                return True
        return False
    
    def stop_music(self):
        self.menu_channel.stop()