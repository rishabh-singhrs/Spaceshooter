import random
import pygame
from random import uniform
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image=pygame.image.load('images/player.png').convert_alpha()
        self.rect=self.image.get_frect(center=(window_width/2,window_height/2))
        self.direction=pygame.math.Vector2(0,0)
        self.speed=300

        #Cooldown timer
        self.can_shoot=True
        self.laser_shoot_time=0
        self.cooldown_time=500
    def laser_timer(self):
        if not self.can_shoot:
            current_time=pygame.time.get_ticks()
            if current_time-self.laser_shoot_time>=self.cooldown_time:
                self.can_shoot=True
            
    def update(self,dt):       
        keys=pygame.key.get_pressed()
        self.direction.x =int(keys[pygame.K_RIGHT])-int(keys[pygame.K_LEFT])
        self.direction.y =int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP])
        self.direction=self.direction.normalize() if self.direction else self.direction
        self.rect.center+=self.direction*dt*self.speed
        recent_keys=pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surface,self.rect.midtop,(all_sprites,laser_sprites))
            self.can_shoot=False
            self.laser_shoot_time=pygame.time.get_ticks()  
            laser_sound.play() 
        self.laser_timer()
class Star(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.image=surf
        self.positions=[(random.randint(0,window_width),random.randint(0,window_height))for i in range(20)]
        self.rect=self.image.get_frect(center=(random.randint(0,window_width),random.randint(0,window_height)))
class Laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)   
        self.image=surf
        self.rect=self.image.get_frect(midbottom=(pos))   
    def update(self,dt):
        self.rect.centery=self.rect.centery-400*dt 
        if self.rect.bottom<0:
            self.kill()  
class Meteor(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.original_surf=surf
        self.image=self.original_surf
        self.rect=self.image.get_frect(center=pos)
        self.meteor_time=pygame.time.get_ticks()
        self.lifetime=2000
        self.directions=pygame.math.Vector2(uniform(-0.5,0.5),1)
        self.speed=random.randint(400,500)
        self.rotation=0
        self.rotation_speed=random.randint(0,50)
    def update(self,dt): 
        self.rect.center+=self.directions*self.speed*dt
        if pygame.time.get_ticks()-self.meteor_time>=2000:
            self.kill()
        self.rotation+=self.rotation_speed*dt
        self.image=pygame.transform.rotozoom(self.original_surf,self.rotation,1)
        self.rect=self.image.get_frect(center=self.rect.center)
class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups):
        super().__init__(groups)
        self.frame=frames
        self.frame_index=0
        self.image=self.frame[int(self.frame_index)]
        self.rect=self.image.get_frect(center=pos)
    def update(self,dt):
        self.frame_index+=20*dt
        if self.frame_index<=len(self.frame):
            self.image=self.frame[int(self.frame_index)]
        else:
            self.kill()

def collisions():
    global running
    global countinghealth
    collision_sprites=pygame.sprite.spritecollide(player,meteor_sprites,True,pygame.sprite.collide_mask)
    if collision_sprites:
        damage_sound.play()
        countinghealth+=1
        if countinghealth>4:
            running=False
    for laser in laser_sprites :
        collided_sprite=pygame.sprite.spritecollide(laser,meteor_sprites,True)
        if collided_sprite:
            laser.kill()
            AnimatedExplosion(explosion_frames,laser.rect.midtop,all_sprites)
            explosion_sound.play()
def display_score():
    current_score=pygame.time.get_ticks()//1000
    text_surf=font.render(str(current_score),True,(240,240,240))
    text_rect=text_surf.get_frect(center=(window_width/2,window_height-50)) 
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface,(240,240,240),text_rect.inflate(20,20).move(0,-8),5,10)
#General Setup 
pygame.init()
window_width,window_height = 1280,720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(" Space Shooter")
running=True
clock=pygame.time.Clock()

#imports
meteor_surface=pygame.image.load('images/meteor.png').convert_alpha()
laser_surface=pygame.image.load('images/laser.png').convert_alpha()
star_surf=pygame.image.load('images/star.png').convert_alpha()
explosion_frames=[pygame.image.load(join('images','explosion',f'{i}.png')).convert_alpha() for i in range(21)]
laser_sound=pygame.mixer.Sound(join('audio','laser.wav'))
explosion_sound=pygame.mixer.Sound(join('audio','explosion.wav'))
damage_sound=pygame.mixer.Sound(join('audio','damage.ogg'))
game_sound=pygame.mixer.Sound(join('audio','game_music.wav'))
game_sound.set_volume(0.1)
game_sound.play()
#Sprites
all_sprites=pygame.sprite.Group()
meteor_sprites=pygame.sprite.Group()
laser_sprites=pygame.sprite.Group()
font=pygame.font.Font('images/Oxanium-Bold.ttf',50)


countinghealth=0


for i in range(20):
    Star(all_sprites,star_surf)
player=Player(all_sprites)

# custom event --> meteor event
meteor_event=pygame.event.custom_type()
pygame.time.set_timer(meteor_event,500)


while running:
    dt=clock.tick()/1000
    
    #event loop
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False 
        if event.type==meteor_event:
            x,y=random.randint(0,window_width),random.randint(-20,-10)
            Meteor(meteor_surface,(x,y),(all_sprites,meteor_sprites))

    all_sprites.update(dt)
    #draw the surface
    display_surface.fill('#3a2e3f')

    collisions()
    all_sprites.draw(display_surface)
    display_score()
    
    
    
    pygame.display.update()

pygame.quit()
















