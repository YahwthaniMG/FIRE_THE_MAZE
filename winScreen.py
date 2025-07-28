import pygame

class WinScreen:
    def __init__(self, font, screen, screen_width, screen_height):
        self.font = font
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Crear texto del botón primero para obtener sus dimensiones
        self.button_text = self.font.render("Return to Menu", True, (255, 255, 255))
        button_width = max(300, self.button_text.get_width() + 40)  # Padding de 20px a cada lado
        button_height = max(50, self.button_text.get_height() + 20)  # Padding de 10px arriba y abajo
        
        # Crear botón con dimensiones basadas en el texto
        self.restart_button = pygame.Rect(
            screen_width//2 - button_width//2,
            400,
            button_width,
            button_height
        )

    def display(self):
        self.screen.fill((0, 0, 0))
        
        # VICTORY! centrado y escalado
        victory_text = pygame.font.Font(None, int(self.screen_height/10)).render(
            "VICTORY!", True, (255, 255, 0))
        victory_x = self.screen_width//2 - victory_text.get_width()//2
        self.screen.blit(victory_text, (victory_x, self.screen_height//4))
        
        # Mensaje en verde
        save_text = self.font.render("You saved the fire!", True, (0, 255, 0))
        save_x = self.screen_width//2 - save_text.get_width()//2
        self.screen.blit(save_text, (save_x, self.screen_height//3))

        # Botón y texto centrados
        pygame.draw.rect(self.screen, (0, 0, 255), self.restart_button)
        text_x = self.restart_button.centerx - self.button_text.get_width()//2
        text_y = self.restart_button.centery - self.button_text.get_height()//2
        self.screen.blit(self.button_text, (text_x, text_y))

        pygame.display.flip()

    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button.collidepoint(event.pos):
                return True
        return False