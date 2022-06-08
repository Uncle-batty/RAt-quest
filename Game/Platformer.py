#system ussage
import pygame
from pygame.locals import *
from pygame import mixer
import pickle
import time

#Load in text file data
Game_data = open('DATA/Gamedata.txt','r')
init_level = Game_data.readline().split("\n")
init_Score = Game_data.readline().split("\n")
lives = Game_data.readline().split("\n")
#Game_data.close() 

#initlixing
pygame.mixer.pre_init(44000, -8, 1, 1024)
mixer.init()
pygame.init()

#time
clock = pygame.time.Clock()
fps =60

#game setings
screen_width =1300
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('RAT Quest')

#game-veriables
block_width = 50
game_over = False
menu = True
level = init_level[0]
game_over1 = 0
Level_menu = False
Score = int(init_Score[0])
score_font = pygame.font.SysFont("comicsansms", 28   )
white = (255, 255, 255)
lives = int(lives[0])

#images
bg_pic = pygame.image.load('ART/Untitled.png')
title_pic = pygame.image.load('ART/Title.png')
try_image = pygame.image.load('ART/Try_again.png')
start_pic = pygame.image.load('ART/START.png')
exit_pic = pygame.image.load('ART/END.png')
Levels_pic = pygame.image.load('ART/Levels.png')
floor_pic = pygame.image.load('ART/floor.png')
lives_pic = pygame.image.load('ART/lifes.png')
Alegator_pic = pygame.image.load('ART/Try_again.png')
Credits_pic = pygame.image.load('ART/CREDITS.png')
#music
menu_music = pygame.mixer.Sound('Music/bg.mp3')
Level1_music = pygame.mixer.Sound('Music/level_2.mp3')
Coin_music = pygame.mixer.Sound('Music/pickupCoin.wav')
Hit_music = pygame.mixer.Sound('Music/hitHurt.wav')
Jump_music = pygame.mixer.Sound('Music/jump.wav')


#classes
class buttons():
    def __init__(self,x,y,pic):
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.click = False
    
    def draw(self):
        click = False
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False :
                self.click = True
                click = True
                
        if pygame.mouse.get_pressed()[0] ==0 :
            self.click = False
            
        screen.blit(self.image,self.rect)
        
        return click
        
class player():
    def __init__(self, x, y):
        self.tryagain(x,y)
        
    def update(self):
        #var
        dx =0
        dy =0
        Lenght_ = 20
        if game_over1 != - 3 :
        #movement
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jump == False and self.jumped ==False:
                self.vel_y = -17
                Jump_music.play()
                self.jump =True
            if key[pygame.K_SPACE] == False:
                self.jump = False
            if key[pygame.K_LEFT]:
                dx-= 5
            if key[pygame.K_RIGHT]:
                dx+= 5
                
            #gravity
            self.vel_y =  int(self.vel_y + 2.4)
            if self.vel_y >10:
                self.vel_y = 10
            dy+= self.vel_y
                
            #physics
            self.jumped= True
            for tile in world.block_list :
            #x
                if tile[1].colliderect(self.rect.x +dx, self.rect.y, self.width, self.height) :
                    dx = 0
            #y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height) :
                    if self.vel_y <0 :
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >=0 :
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.jumped = False
                        
        
                
            for Move in Move_group:
                #collision in the x direction
                if Move.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #collision in the y direction
                if Move.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below platform
                    if abs((self.rect.top + dy) - Move.rect.bottom) < Lenght_:
                        self.vel_y = 0
                        dy = Move.rect.bottom - self.rect.top
                    #check if above platform
                    elif abs((self.rect.bottom + dy) - Move.rect.top) < Lenght_:
                        self.rect.bottom = Move.rect.top - 10
                        self.jumped = False
                        dy = 0
                    #move sideways with the platform
                    if Move.move_x != 0:
                        self.rect.x += Move.move_direction

                if game_over1 == -3:
                    self.image = self.Dead_pic
            #position 
            dy+= self.vel_y 
            self.rect.x += dx
            self.rect.y += dy
            
            if self.rect.bottom> screen_height:
                self.rect.bottom = screen_height
                dy= 0
                
            screen.blit(self.image, self.rect)
          
        return 
    
    def tryagain(self,x,y):
        player1 = pygame.image.load('ART/guy.png')
        self.image = pygame.transform.scale(player1, (20,45))
        self.Dead_pic = pygame.image.load('ART/Toomestone.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jump =False
        self.jumped  = False

     
class level1():
    def __init__(self, data):
        self.block_list = []
        
        Ground_pic = pygame.image.load('ART/GrassBlockV2.png')
        Grass_pic = pygame.image.load('ART/grass.png')
        
        row_c = 0
        ##Building the world according to tile in group
        for row in data:
            col = 0
            for tile in row :
                if tile == 1:
                    pic = pygame.transform.scale(Grass_pic,(block_width,block_width))
                    pic_rect = pic.get_rect()
                    pic_rect.x = col * block_width
                    pic_rect.y = row_c * block_width
                    tile = (pic, pic_rect)
                    self.block_list.append(tile)
                if tile == 2:
                    pic = pygame.transform.scale(Ground_pic,(block_width,block_width))
                    pic_rect = pic.get_rect()
                    pic_rect.x = col * block_width
                    pic_rect.y = row_c * block_width
                    tile = (pic, pic_rect)
                    self.block_list.append(tile)
                if tile == 3:
                    block = enemy(col * block_width-30, row_c * block_width+30 )
                    block_group.add(block)
                if tile == 4:
                    crock = Move(col * block_width,row_c * block_width, 1, 0)
                    Move_group.add(crock)
                if tile == 5:
                    crock = Move(col * block_width,row_c * block_width, 0, 1)
                    Move_group.add(crock)
                if tile == 6 :
                    spike = spikes(col * block_width, row_c * block_width + (block_width//2))
                    spike_group.add(spike)
                if tile == 7:
                    gcoin = GoldCoin((col * block_width)+25, (row_c * block_width)+25)
                    gCoin_group.add(gcoin)
                if tile == 8 :
                    lids = lid(col * block_width, row_c * block_width)
                    lid_group.add(lids)
                if tile == 10:
                    pic = pygame.transform.scale(floor_pic,(block_width,block_width))
                    pic_rect = pic.get_rect()
                    pic_rect.x = col * block_width
                    pic_rect.y = row_c * block_width
                    tile = (pic, pic_rect)
                    self.block_list.append(tile)
                    
                    
                col += 1
            row_c += 1
    def draw(self):
        for tile in self.block_list:
            screen.blit(tile[0], tile[1])

class enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ART/RAT.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.counter = 0 
        
    def update(self):
        self.rect.x += self.direction
        self.counter += 1
        if abs(self.counter) >50 :
            self.direction *= -1
            self.counter *= -1
            
class spikes(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        spike= pygame.image.load('ART/Trash.png')
        self.image = pygame.transform.scale(spike,(block_width,block_width//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class lid(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        lid_v= pygame.image.load('ART/lid.png')
        self.image = pygame.transform.scale(lid_v,(block_width,block_width))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        

class GoldCoin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('ART/Coin.png')
        self.image = pygame.transform.scale(img, (block_width // 2, block_width // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
class Move(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('ART/Floor.png')
        self.image = pygame.transform.scale(img, (block_width, block_width // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y
        
    def update(self):#Move the pkatforms 
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
            

#functions
def reset_level():
    player.tryagain(100,100)
    block_group.empty()
    spike_group.empty()
    Move_group.empty()
    lid_group.empty()
    pickle_file = open(f'DATA/level{level}_data', 'rb')
    world_data = pickle.load(pickle_file)
    world = level1(world_data)
    
    return world

def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])
    
def Level_(level):
    value = score_font.render("level: " + str(level), True, white)
    screen.blit(value, [600, 0])
    
    
def gameover(game_over1):
    if pygame.sprite.spritecollide(player, spike_group, False):
            game_over1 = -3
    if pygame.sprite.spritecollide(player, lid_group, False):
            game_over1 = 1
    return game_over1
            
            
def Update_textfile():
      if int(init_level[0]) < int(level):
        Game_data = open('DATA/Gamedata.txt','w')
        Game_data.write(f"{level}\n")
        Game_data.write(str(f"{Score}\n"))
        Game_data.write(str(f"{lives}\n"))
        Game_data.close()
#instants
player = player(100,100)

#groups
block_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
lid_group = pygame.sprite.Group()
gCoin_group = pygame.sprite.Group()
Move_group = pygame.sprite.Group()
Wepon_group = pygame.sprite.Group()

#load map data
pickle_file = open(f'DATA/level{level}_data', 'rb')
world_data = pickle.load(pickle_file)
world = level1(world_data)

#buttons
tryAgain_button = buttons(425,300,try_image)
start_button = buttons(100,400,start_pic)
end_button = buttons(1050 ,400,exit_pic)
Level_button = buttons(550 ,400 ,Levels_pic)
creduts_button = buttons(500 ,300 ,Credits_pic)

#loop to keep game running
while game_over == False :
   
    clock.tick(fps)
    screen.blit(title_pic,(0,0))
    #run menu
    if menu == True :
        menu_music.play()
        if end_button.draw():
            game_over = True
        if start_button.draw():
            menu = False
        if Level_button.draw():
            Level_menu = True
            menu = False
    elif Level_menu == True :
        creduts_button.draw()
        if end_button.draw():
            game_over = True
        if start_button.draw():
            menu = False
            Level_menu = False
    else:
        #run game
        #menu_music.pause()
        screen.blit(bg_pic,(0,0))
        world.draw()
        block_group.update()
        Move_group.update()
        block_group.draw(screen)
        lid_group.draw(screen)
        spike_group.draw(screen)
        gCoin_group.draw(screen)
        Move_group.draw(screen)
        
        Wepon_group.draw(screen)
        
        Level_(level)
        if pygame.sprite.spritecollide(player, gCoin_group, True):
            Coin_music.play()
            Score += 1
        Your_score(Score)
        if pygame.sprite.spritecollide(player, block_group, False):
                lives = lives - 1
                Hit_music.play()
                
          
               
        #lives
        if lives == 3 : 
            screen.blit(lives_pic ,(1250,5))
            screen.blit(lives_pic ,(1200,5))
            screen.blit(lives_pic ,(1150,5))
        elif lives == 2 : 
            screen.blit(lives_pic ,(1250,5))
            screen.blit(lives_pic ,(1200,5))
        elif lives == 1 : 
            screen.blit(lives_pic ,(1250,5))
        else :
            game_over1 = -3
            
        player.update()
        #game Over Code
        game_over1 = gameover(game_over1)
        if game_over1 == - 3 :
            if tryAgain_button.draw():
                world_data = []
                world = reset_level()
                player.tryagain(100,100)
                game_over1 = 0
                buttons.click = False
                Score = int(init_Score[0])
                lives = 3
        #next levle code        
        if game_over1 == 1:
            level = int(level) + 1
            if level <= 10:#maxlevel
                world_data = []
                world = reset_level()
                game_over1 = 0
            else:
                menu  = True
                
    #Exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            
    pygame.display.update()
    Update_textfile()
pygame.quit()