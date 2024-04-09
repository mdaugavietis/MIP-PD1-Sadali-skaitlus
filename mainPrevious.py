from random import randint
from typing import Dict
import pygame


class Game:
    def __init__(self, opponent: bool):
        self.length = 0
        self.numbers = [0, 0, 0, 0]
        self.points = [0, 0]
        self.player = 0  # 0 is p1, 1 is p2
        self.player_vs_computer = opponent

    def __str__(self):
        self.f1 = f"Punkti: {self.points}, Gājiens: {self.player+1}. spēlētājam"
        self.f2 = f"Skaitļi (indekss, skaitlis): {list(enumerate(self.numbers))}"
        return self.f1+"\n"+self.f2
    
    def gen_numbers(self, length: int):
        #length = max(min(length, 20), 15)
        self.length = length
        for _ in range(length):
            self.numbers[randint(1, 4)-1] += 1
        
    def turn(self, mode: bool, ind: int):
        if self.numbers[ind] > 0:
            if mode:
                self.numbers[ind] -= 1
                self.points[self.player] += (ind + 1)
                self.player = (self.player + 1) % 2
            else:
                if ind % 2 != 1:
                    print("Nevar sadalīt")
                else:
                    self.numbers[ind] -= 1
                    self.numbers[ind // 2] += 2                    
                    self.points[self.player] += ind // 2
                    self.player = (self.player + 1) % 2
        print(self)
        # Automatic turn by AI
        if self.player_vs_computer and self.player == 1:
            self.strat1()
        
    # Always pick MAX strategy
    def strat1(self):
        for x in range(len(self.numbers)-1,-1,-1):
            if self.numbers[x]:
                self.turn(True, x)
                break


class GUI():
    def __init__(self, width: int, height: int, bg_color: str, caption: str, clock: int):
        self.clock = clock
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.bg_color = bg_color
        pygame.display.set_caption(caption)
        
    def prepare_rectangle(self, on_object, color, width: int, height: int, offset_x: int, offset_y: int, border_radius=0, border_width=0, top_left=-1, top_right=-1, bottom_left=-1, bottom_right=-1):
        rectangle = pygame.Rect((offset_x, offset_y),(width, height)) #Rect
        return pygame.draw.rect(on_object, color, rectangle, border_width, border_radius, top_left, top_right, bottom_left, bottom_right) #Rect
    
    def prepare_text(self, text: str, size: int, color, background=None, style=None, antialias=True):
        font = pygame.font.Font(style, size) #Font
        return font.render(text, antialias, color, background) #Surface
    
    def center_text(self, on_object, text_object):
        text_rect = text_object.get_rect()
        text_rect.center = on_object.center
        return text_rect
        

def main():
    ### GAME init
    game = Game(True) # switch opponent
    # user input
    valid_sequence = list(map(str, range(15,21)))
    sequence_length = ''
    input_done = False
    # dictionary of rectangles
    direct: Dict[int, Dict]={}
    
    ### GUI init
    pygame.init()
    clock = pygame.time.Clock()
    gui = GUI(1280, 720, "#222831", "AI", 25)
    center_x = int(gui.screen_width / 2)
    center_y = int(gui.screen_height / 2)
    # rect init for mouse events
    sadali2 = pygame.Rect((0, 0),(0, 0))
    sadali4 = pygame.Rect((0, 0),(0, 0))
    restart = pygame.Rect((0, 0),(0, 0))

    # PYGAME loop
    running = True
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # sequence input events
            if input_done == False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        sequence_length = sequence_length[:-1]
                    else:
                        if(len(sequence_length)<2):
                            sequence_length += event.unicode
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if any(game.numbers):
                        if sadali4.collidepoint(event.pos):
                            game.turn(False, 3)
                        elif sadali2.collidepoint(event.pos):
                            game.turn(False, 1)
                        else:
                            for di in direct:
                                if direct[di]['rect'].collidepoint(event.pos):
                                    game.turn(True, di)
                                    break
                    else:
                        if restart.collidepoint(event.pos):
                            game = Game(game.player_vs_computer)
                            sequence_length = ''
                            input_done = False

        # GAME RENDERS HERE
        gui.screen.fill(gui.bg_color)
        if sequence_length in valid_sequence:
            input_done = True
            if not game.length:
                game.gen_numbers(int(sequence_length))
                print(game)
            
            # Game info
            gui.screen.blit(gui.prepare_text(game.f1, 30, '#eeeeee'), (10, 10), area=None, special_flags=0) # Line 1
            # gui.screen.blit(gui.prepare_text(game.f2, 30, 'White'), (10, 40), area=None, special_flags=0) # Line 2

            if not any(game.numbers):
                # SCREEN 3
                if game.points[0] > game.points[1]:
                    result = "Uzvara :)"
                elif game.points[0] < game.points[1]:
                    result = "Zaudējums :("
                else:
                    result = "Neizšķirts"
                text = gui.prepare_text(result, 50, 'Red')
                gui.screen.blit(text, (center_x-int(text.get_rect().width/2), center_y-25), area=None, special_flags=0)
                
                restart = gui.prepare_rectangle(gui.screen, '#00adb5', 300, 100, center_x-150, center_y+100, 5)
                restart_text = gui.prepare_text("ATKĀRTOT", 50, '#eeeeee')
                gui.screen.blit(restart_text, gui.center_text(restart, restart_text), area=None, special_flags=0)
            else:
                # SCREEN 2
                x=90
                y=140
                for n in range(len(game.numbers)):
                    my_text1 = gui.prepare_text(str(game.numbers[n]), 50, '#222831') #small
                    my_text2 = gui.prepare_text('+' + str(n+1), 250, '#eeeeee') #BIG
                    
                    direct[n] = {'rect': gui.prepare_rectangle(gui.screen, '#00adb5', 200, 155, x, y, 0, 0, 0, 10, 10, 0), 'id': game.numbers[n]}
                    
                    gui.screen.blit(my_text1, direct[n]['rect'], area=None, special_flags=0)
                    gui.screen.blit(my_text2, direct[n]['rect'], area=None, special_flags=0)
                    
                    x+=300
            
                # Add buttonz
                sadali2 = gui.prepare_rectangle(gui.screen, '#00adb5', 200, 100, 390, 350, 10)
                sadali4 = gui.prepare_rectangle(gui.screen, '#00adb5', 200, 100, 990, 350, 10)
                text2 = gui.prepare_text("2/2 (+0)", 50, '#eeeeee')
                text4 = gui.prepare_text("4/2 (+1)", 50, '#eeeeee')
                gui.screen.blit(text2, gui.center_text(sadali2, text2), area=None, special_flags=0)
                gui.screen.blit(text4, gui.center_text(sadali4, text4), area=None, special_flags=0)
        else:
            # SCREEN 1
            title = "Ievadi cik skaitļus ģenerēt intervālā no 15 līdz 20: "
            gui.screen.blit(gui.prepare_text(title + sequence_length, 60, '#eeeeee'), (center_x-530, center_y-30), area=None, special_flags=0)


        pygame.display.flip()
        clock.tick(gui.clock)
        

    pygame.quit()
    print(f"Spēle beidzās ar rezultātu {game.points}")


if __name__ == "__main__":
    main()
