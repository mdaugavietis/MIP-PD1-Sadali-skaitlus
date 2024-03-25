from random import randint
from typing import Dict
import pygame


class Game:
    def __init__(self):
        self.length = 0
        self.points = [0, 0]
        self.player = 0  # 0 is p1, 1 is p2

    def __str__(self):
        f1 = f"Punkti: {self.points}, Gājiens: {self.player+1}. spēlētājam"
        f2 = f"Skaitļi (indekss, skaitlis): {list(enumerate(self.numbers))}"
        return f1+'\n'+f2
    
    def gen_numbers(self, length: int):
        #length = max(min(length, 20), 15)
        self.length = length
        self.numbers = [randint(1, 4) for i in range(length)]
        
    def turn(self, mode: bool, ind: int):
        # False is take, True is split
        if ind < len(self.numbers):
            if mode:
                self.points[self.player] += self.numbers[ind]
                self.numbers.pop(ind)
                self.player = (self.player + 1) % 2
            else:
                if self.numbers[ind] % 2 == 1:
                    print("nevar sadalīt")
                else:
                    self.numbers[ind] //= 2 # 1 or 2
                    self.numbers.insert(ind, self.numbers[ind])
                    self.points[self.player] += self.numbers[ind] // 2
                    self.player = (self.player + 1) % 2


def main():
    ### GAME init
    game = Game()
    # user input
    sequence_length = ''
    valid_sequence = list(map(str, range(15,21)))
    # Dictionary of rectangles
    direct: Dict[int, Dict]={}
    
    ### PYGAME setup
    pygame.init()
    # screen size
    width = 1280
    height = 720
    screen = pygame.display.set_mode((width, height))
    # refresh rate
    clock = pygame.time.Clock()
    # background color
    bg_color = "pink"
    # name of the game
    pygame.display.set_caption('AI')
    
    # default font and color
    font_size = 50
    font = pygame.font.Font(None, font_size)
    color = pygame.Color(255,255,255)

    # surface for sequence input
    seq_width = 520
    seq_height = 50
    seq_input = pygame.Surface((seq_width,seq_height))
    
    # buttons -> text and location
    s2_text = font.render('Sadali 2', True, 'Red')
    sadali2 = pygame.Rect((350,645),(250,50))
    s4_text = font.render('Sadali 4', True, 'Red')
    sadali4 = pygame.Rect((680,645),(250,50))
    # game over -> text and location
    go_text = font.render('Game over!', True, 'Red')
    gameover = pygame.Rect((540,310),(200,50))
    
    
    # PYGAME loop
    running = True
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # sequence input events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    sequence_length = sequence_length[:-1]
                else:
                    if(len(sequence_length)<2):
                        sequence_length += event.unicode
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sadali4.collidepoint(event.pos):
                    if 4 in game.numbers:
                        ind = game.numbers.index(4)
                        game.turn(False, ind)
                    #game.points[player] += def3()
                    #switch_player()
                elif sadali2.collidepoint(event.pos):
                    if 2 in game.numbers:
                        ind = game.numbers.index(2)
                        game.turn(False, ind)
                    #game.points[player] += def2()
                    #switch_player()
                else:
                    for di in direct:
                        if direct[di]['rect'].collidepoint(event.pos):
                            game.turn(True, di)
                            #game.points[player] += def1(di)
                            #switch_player()
                            break
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill(bg_color)


        # GAME RENDERS HERE
        if sequence_length in valid_sequence:
            if not game.length:
                game.gen_numbers(int(sequence_length))

            if not game.numbers:
                # SCREEN 3
                p1 = 'P1 score is: ' + str(game.points[0])
                p2 = 'P2 score is: ' + str(game.points[1])
                s2_text = font.render(p1, True, 'Red')
                s4_text = font.render(p2, True, 'Red')
                
                pygame.draw.rect(screen, color, gameover)
                screen.blit(go_text, gameover)
            else:
                # SCREEN 2
                x=65
                y=25
                for n in range(len(game.numbers)):
                    my_text = font.render(str(game.numbers[n]), True, 'Red')
                    
                    direct[n] = {'rect': pygame.Rect((x,y),(100,100)), 'id': game.numbers[n]}
                    pygame.draw.rect(screen, color, direct[n]['rect'])
                    screen.blit(my_text, direct[n]['rect'])
                    
                    x+=150
                    if x>width-150:
                        y+=150
                        x=65
                        

            # Add buttonz
            pygame.draw.rect(screen, color, sadali2)
            screen.blit(s2_text, sadali2)
            pygame.draw.rect(screen, color, sadali4)
            screen.blit(s4_text, sadali4)
        
        else:
            # SCREEN 1
            title = "Ievadi cik skaitļus ģenerēt: "
            x = int(width / 2 - seq_width / 2)
            y = int(height / 2 - seq_height / 2)
            my_text = font.render(title + sequence_length, True, 'White')
            screen.blit(seq_input, (x,y))
            seq_input.fill("pink")
            seq_input.blit(my_text, (10,10))

        
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        clock.tick(60)
        

    pygame.quit()
    print(f"Spēle beidzās ar rezultātu {game.points}")


if __name__ == "__main__":
    main()
