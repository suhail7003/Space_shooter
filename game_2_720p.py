import pygame
import sys
import os
from random import randint

pygame.init()

pygame.display.set_caption("Space Shooter")

SCREEN_HEIGHT,SCREEN_WIDTH = 720,1280

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


class Environment(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Graphics/star.png").convert_alpha()
        self.rect = self.image.get_rect(center = (randint(-2,SCREEN_WIDTH),randint(-500,-10)))
        
    


    def draw(self,surface):

        
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.y += 2
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = randint(-500,-10)
    
class Objects(pygame.sprite.Sprite):

    
    def __init__(self,type):

        super().__init__()
        self.type = type
        self.shoot = False
        
        
        if type == "meteor":
            self.original_image = pygame.image.load(os.path.join('yt assets','space shooter','images','meteor.png')).convert_alpha()
            self.image = self.original_image
            self.rect = self.image.get_frect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            self.direction = pygame.math.Vector2((randint(-1,1)),1)
            self.speed = randint(400,500)
            self.rotation = 0
            self.roto_speed = randint(-20,50)
        if type == "ship":
            self.image = pygame.image.load(os.path.join('yt assets','space shooter','images','player.png')).convert_alpha()
            self.rect = self.image.get_frect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

        if type == "laser":
            self.image = pygame.image.load(os.path.join('yt assets','space shooter','images','laser.png')).convert_alpha()
            self.rect = self.image.get_frect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            self.direction =self.direction = pygame.math.Vector2()

    
    def draw(self,surface):
        
        surface.blit(self.image,self.rect)



    def movement(self):

        if self.type == "meteor":
            self.rect.center += self.direction * self.speed * dt
            self.rotation += 2*self.roto_speed*dt
            self.image = pygame.transform.rotozoom(self.original_image,self.rotation,1)
            self.rect = self.image.get_frect(center = self.rect.center)
        if self.type == "ship":
            self.rect.center = mouse
        if self.type == "laser":
            self.direction.y = -1
            self.speed = 800
            self.rect.center += self.direction * self.speed * dt

            

    def collision(self):
        if self.type == "meteor":
            if self.rect.right >= SCREEN_WIDTH:
                self.direction += pygame.math.Vector2(-1,0)
            if self.rect.left <= 0:
                self.direction += pygame.math.Vector2(1,0)
  
    def update(self):

        self.movement()
        self.collision()

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "timer":
            
            self.time = (pygame.time.get_ticks() - start_time_game) // 100
            self.font = pygame.font.Font(os.path.join('yt assets','space shooter','images','Oxanium-Bold.ttf'),35)
            self.image = self.font.render(str(self.time),True,"white")
            self.rect = self.image.get_rect(midbottom = (SCREEN_WIDTH/2,SCREEN_HEIGHT -40)).inflate(20,20)
        if type == "points":
            self.score = 0
            self.font = pygame.font.Font(os.path.join('yt assets','space shooter','images','Oxanium-Bold.ttf'),35)
            self.image = self.font.render(f"Hits: {str(shoot_points)}",True,"white")
            self.rect = self.image.get_rect(midbottom = (SCREEN_WIDTH-80,100)).inflate(20,20)
    def draw(self,surface,color):

        pygame.draw.rect(surface,"black",self.rect.move(-9,-13),0,10)
        pygame.draw.rect(surface,color,self.rect.move(-9,-13),3,10)
        surface.blit(self.image,self.rect)

class Explosion(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)

        frames = [pygame.image.load(os.path.join('yt assets','space shooter','images','explosion',f"{i}.png")).convert_alpha() for i in range(21)]

        self.frames = frames
        self.index = 0
        self.image = self.frames[int(self.index)]
        self.rect = self.image.get_frect(center = pos)

    def draw(self,surface):

        surface.blit(self.image,self.rect)

    def update(self):

        self.index += 100 *dt
        if self.index < len(self.frames):
            self.image = self.frames[int(self.index)]
        else:
            self.kill()


#SOUND
laser_sound = pygame.mixer.Sound(os.path.join('yt assets','space shooter','audio','laser.wav'))
damage_sound = pygame.mixer.Sound(os.path.join('yt assets','space shooter','audio','explosion.wav'))
game_music = pygame.mixer.Sound(os.path.join('yt assets','space shooter','audio','game_music.wav'))



#all sprite group
all_sprites = pygame.sprite.Group()


stars = pygame.sprite.Group()
for i in range(20):
    env = Environment()
    stars.add(env)


#meteor object
meteors = pygame.sprite.Group()

#laser group
laser_group = pygame.sprite.Group()

#ship object
ship = Objects("ship")

shoot_points = 0

clock = pygame.time.Clock()

#METEOR SPAWN TIMER
event1 = pygame.event.custom_type()
pygame.time.set_timer(event1, randint(700,1000))

game_music.set_volume(0.1)
game_music.play(loops=-1)

#game states

game_state = "main menu"

if game_state == "main menu":

    main_menu_image = pygame.image.load("mainmenu_720.png")

    while True:

        dt = clock.tick(120) /1000
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("dark blue")
        screen.blit(main_menu_image)

        if keys[pygame.K_k]:
            game_state = "gameplay"
            break

        pygame.display.update()

if game_state == "gameplay":
    start_time_game = pygame.time.get_ticks() 
    while True:

        
        dt = clock.tick(120) /1000

        keys = pygame.key.get_just_pressed()
        ship_key = pygame.mouse.get_pressed()

        mouse = pygame.mouse.get_pos(desktop=False)
        pygame.mouse.set_visible(False)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == event1:
                meteor = Objects("meteor")
                # all_sprites.add(meteor)
                meteors.add(meteor)
                meteor.rect.center = (randint(40,700),-20)


        screen.fill("#03000a")

        stars.draw(screen)
        stars.update()

        all_sprites.draw(screen)
        all_sprites.update()

        laser_group.draw(screen)
        laser_group.update()

        ship.draw(screen)
        ship.update()

        meteors.draw(screen)
        meteors.update()



        if keys[pygame.K_f]:
            laser = Objects("laser")
            laser.rect.center = ship.rect.center
            laser_group.add(laser)
            laser_sound.play()
            laser_sound.set_volume(0.1)

    
        for laser in laser_group:
           
            hit_meteors = pygame.sprite.spritecollide(laser, meteors, True)  
            if hit_meteors:
                print("Hit!")
                laser.kill() 
                damage_sound.play()
                damage_sound.set_volume(0.1)
                exp = Explosion(laser.rect.center,all_sprites)
                shoot_points+=1
        
        for meteor in meteors:
            if meteor.rect.colliderect(ship.rect):
                pygame.quit()
                sys.exit("game over")
            


        score = Scoreboard("timer")
        score.draw(screen,"white")
        
        points = Scoreboard("points")
        points.draw(screen,"blue")


        pygame.display.update()
        