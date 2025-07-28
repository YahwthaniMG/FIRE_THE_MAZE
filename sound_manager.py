import pygame
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)
        
        # Cargar sonidos
        self.music = pygame.mixer.Sound('resources/MusicGame.mp3')
        self.power_up = pygame.mixer.Sound('resources/PowerUP.mp3')
        self.immunity = pygame.mixer.Sound('resources/Immunity.mp3')
        self.kill = pygame.mixer.Sound('resources/Shhhh.mp3')
        self.game_over = pygame.mixer.Sound('resources/GameOver.mp3')
        self.win = pygame.mixer.Sound('resources/Win.mp3')
        self.persecution = pygame.mixer.Sound('resources/Persecution.mp3')
        
        # Configurar canales
        self.music_channel = pygame.mixer.Channel(0)
        self.effect_channel = pygame.mixer.Channel(1)
        self.state_channel = pygame.mixer.Channel(2)
        
        # Configurar volúmenes
        self.music.set_volume(0.5)
        self.power_up.set_volume(1.0)
        self.immunity.set_volume(0.7)
        
        # Estado
        self.is_persecution = False
        
    def start_music(self):
        self.music_channel.play(self.music, loops=-1)
        
    def pause_music(self):
        self.music_channel.pause()
        
    def unpause_music(self):
        self.music_channel.unpause()
        
    def play_power_up(self):
        self.effect_channel.play(self.power_up)
        
    def start_immunity(self):
        self.pause_music()
        self.state_channel.play(self.immunity) 
        
    def stop_immunity(self):
        if self.state_channel.get_busy():
            self.state_channel.stop()
        self.unpause_music()
        
    def play_kill(self):
        self.effect_channel.play(self.kill)
        
    def play_game_over(self):
        self.stop_all_sounds()
        self.effect_channel.play(self.game_over)
        
    def play_win(self):
        self.stop_all_sounds()
        self.effect_channel.play(self.win)
        
    def start_persecution(self):
        if not self.is_persecution:
            self.pause_music()
            self.state_channel.play(self.persecution, loops=-1)
            self.is_persecution = True
            
    def stop_persecution(self):
        if self.is_persecution:
            self.state_channel.stop()
            self.unpause_music()
            self.is_persecution = False
            
    def stop_all_sounds(self):
        self.music_channel.stop()
        self.effect_channel.stop()
        self.state_channel.stop()
        self.is_persecution = False

    def return_to_menu(self):
        self.stop_all_sounds()
        self.start_music()