import pygame

class GameOverScreen:
    def __init__(self, font, screen, screen_width, screen_height):
        self.font = font
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.button_text = self.font.render("Return to Menu", True, (255, 255, 255))
        # Ajustar tamaño del botón
        button_width = max(300, self.button_text.get_width() + 40)
        button_height = max(50, self.button_text.get_height() + 20)
        
        # Centrar botón en la pantalla
        self.restart_button = pygame.Rect(
            screen_width//2 - button_width//2,
            screen_height//2 + 100,  # Posición más baja en la pantalla
            button_width,
            button_height
        )

    def display(self, enemy_type):
        self.screen.fill((0, 0, 0))
        
        # Game Over centrado y escalado
        game_over = pygame.font.Font(None, int(self.screen_height/10)).render(
            "GAME OVER", True, (255, 0, 0))
        game_over_x = self.screen_width//2 - game_over.get_width()//2
        self.screen.blit(game_over, (game_over_x, self.screen_height//4))
        
        # Mensaje personalizado según enemigo
        messages = {
            "WATER": "¡Una gota de agua te ha extinguido!",
            "ICE": "¡El frío del hielo te ha congelado!",
            "EXTINGUISHER": "¡El extintor te ha apagado!"
        }
        message = self.font.render(messages.get(enemy_type, "¡Game Over!"), True, (255, 255, 255))
        message_x = self.screen_width//2 - message.get_width()//2
        self.screen.blit(message, (message_x, self.screen_height//3))

        # Botón mejorado
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