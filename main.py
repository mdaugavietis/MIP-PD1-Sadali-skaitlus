from random import randint
from typing import Dict
import pygame


class Game:
    def __init__(self):
        self.length = 0
        self.numbers = [0, 0, 0, 0]
        self.points = [0, 0]
        self.player = 0  # 0 is p1, 1 is p2

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
        # True is take, False is split
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
        if self.player == 1:
            self.strat1()
        
    # Always pick MAX
    def strat1(self):
        for x in range(len(self.numbers)-1,-1,-1):
            if self.numbers[x]:
                self.turn(True, x)
                break


def main():
    ### GAME init
    game = Game()
    game.strat1()
    # user input
    sequence_length = ''
    valid_sequence = list(map(str, range(15,21)))
    # Dictionary of rectangles
    direct: Dict[int, Dict]={}
    flag = False
    
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
    
    # font BIG
    font2_size = 500
    font2 = pygame.font.Font(None, font2_size)
    
    # font small
    font3_size = 22
    font3 = pygame.font.Font(None, font3_size)

    # surface for sequence input
    seq_width = 520
    seq_height = 50
    seq_input = pygame.Surface((seq_width,seq_height))
    
    # surface for game info output
    seq2_width = 1280
    seq2_height = 100
    seq_output = pygame.Surface((seq2_width,seq2_height))
    
    # buttons -> text and location
    s2_text = font.render('Sadali 2', True, 'Red')
    sadali2 = pygame.Rect((350,580),(250,50))
    s4_text = font.render('Sadali 4', True, 'Red')
    sadali4 = pygame.Rect((680,580),(250,50))
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
            if flag == False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        sequence_length = sequence_length[:-1]
                    else:
                        if(len(sequence_length)<2):
                            sequence_length += event.unicode
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sadali4.collidepoint(event.pos):
                    game.turn(False, 3)
                elif sadali2.collidepoint(event.pos):
                    game.turn(False, 1)
                else:
                    for di in direct:
                        if direct[di]['rect'].collidepoint(event.pos):
                            game.turn(True, di)
                            break
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill(bg_color)


        # GAME RENDERS HERE
        if sequence_length in valid_sequence:
            flag = True
            if not game.length:
                game.gen_numbers(int(sequence_length))
                print(game)
            
            # Game info
            my_text1 = font3.render(game.f1, True, 'White')
            my_text2 = font3.render(game.f2, True, 'White')
            screen.blit(seq_output, (0,0))
            seq_output.fill("pink")
            seq_output.blit(my_text1, (10,10))
            seq_output.blit(my_text2, (10,40))

            if not any(game.numbers):
                # SCREEN 3
                p1 = 'P1 score is: ' + str(game.points[0])
                p2 = 'P2 score is: ' + str(game.points[1])
                s2_text = font.render(p1, True, 'Red')
                s4_text = font.render(p2, True, 'Red')
                
                pygame.draw.rect(screen, "pink", gameover)
                screen.blit(go_text, gameover)
            else:
                # SCREEN 2
                x=90
                y=140
                for n in range(len(game.numbers)):
                    my_text = font.render(str(game.numbers[n]), True, 'Red')
                    my_text2 = font2.render(str(n+1), True, 'Red')
                    
                    direct[n] = {'rect': pygame.Rect((x,y),(200,300)), 'id': game.numbers[n]}
                    pygame.draw.rect(screen, color, direct[n]['rect'])
                    
                    screen.blit(my_text, direct[n]['rect'])
                    screen.blit(my_text2, direct[n]['rect'])
                    
                    x+=300


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
