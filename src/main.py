import pygame
from constants import *
from random import randint
from os.path import join # takes folder and files for and creates path depending on os type

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups) # to initialize parent class
        self.image = pygame.image.load(join('images', 'medium_crab1.png')).convert_alpha() #b/c my crab image has transparent pixels, I'm using convert_alpha() instead of convert()
        self.rect = self.image.get_frect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.direction = pygame.Vector2()
        self.speed = 300
        self.hitbox = self.rect.inflate(-42,-22)
        # cooldown for jump
        self.can_jump = True
        self.jump_time = 0
        self.cooldown_duration = 500
    def jump_timer(self):
        if not self.can_jump:
            current_time = pygame.time.get_ticks() # gets time since start of game (pygame_init()) in ms
            #print(current_time)
            if current_time - self.jump_time >= self.cooldown_duration:
                self.can_jump = True
    def update(self, dt):
        key = pygame.key.get_pressed()
        self.direction.x = int(key[pygame.K_RIGHT] or key[pygame.K_d]) - int(key[pygame.K_LEFT] or key[pygame.K_a])
        self.direction.y = int(key[pygame.K_DOWN] or key[pygame.K_s]) - int(key[pygame.K_UP] or key[pygame.K_w])
        
        #if self.rect.bottom < SCREEN_HEIGHT:
            #if self.can_jump:
            #    self.direction.y = -int(key[pygame.K_SPACE])
            #if not self.can_jump:
            #    self.direction.y = + 1
        #elif self.rect.bottom > SCREEN_HEIGHT:
            #self.direction.y = 0
            #if self.can_jump:
            #    self.direction.y = -int(key[pygame.K_SPACE])

        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        self.hitbox.center += self.direction * self.speed * dt

        recent_key = pygame.key.get_just_pressed()
        if recent_key[pygame.K_SPACE] and self.can_jump:
            print("crab jumps")
            Jump(surface_jump, self.rect.midbottom, all_sprites)
            self.can_jump = False
            self.jump_time = pygame.time.get_ticks()

        self.jump_timer()
        
class Fish(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, SCREEN_WIDTH),randint(0,SCREEN_HEIGHT)))
        self.direction = pygame.Vector2(1,0)
        self.speed = 100
    def update(self, dt):
        key = pygame.key.get_pressed()
        self.rect.center += self.direction * self.speed * dt

class Jump(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midtop = pos)

class Hook(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.hook_hold = False
        self.hook_time = 0
        self.cooldown_duration = 2000
        self.hook_drops = True

        self.hitbox = self.rect.copy()
        self.hitbox.update(self.hitbox.left+8,self.hitbox.top+600,100,100)
    def hook_timer(self):
        #print(self.hook_hold)
        if self.hook_hold:
            current_time = pygame.time.get_ticks() # gets time since start of game (pygame_init()) in ms
            #print("current_time = ",current_time)
            #print(current_time)
            if current_time - self.hook_time >= self.cooldown_duration:
                self.hook_hold = False
                self.hook_drops = False
                #print("self.hook_drops = ", self.hook_drops)

    def update(self, dt):
        #print(self.rect.midbottom)
        #print("self.hook_time = ", self.hook_time)
        if not self.hook_drops and self.rect.midbottom[1] >= 0:
            self.rect.centery -= 750 * dt
            self.hitbox.centery -= 750 * dt
        if self.hook_drops and self.rect.midbottom[1] <= SCREEN_HEIGHT:
            self.rect.centery += 250* dt
            self.hitbox.centery += 250* dt
        elif self.hook_drops == True:
            self.hook_hold = True
            self.rect.centery += 0
            self.hitbox.centery += 0
            #print("rect.centery =", self.rect.centery)
        if self.hook_hold and self.hook_time == 0:
            #print("hook holds")
            self.hook_time = pygame.time.get_ticks()
        self.hook_timer()
        if not self.hook_hold and self.rect.midbottom[1] < -1000:
            print("hook destroyed")
            self.kill()

class Bubble(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 15000

    def update(self, dt):
        self.rect.centery -= 50 * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()




def collided(sprite, other):
    global run
    """Check if the hitboxes of the two sprites collide."""
    if sprite.hitbox.colliderect(other.hitbox) == True:
        run = False
        print("game ends")
    return sprite.hitbox.colliderect(other.hitbox)
 

# general setup
pygame.init()
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Crab Catch')
clock = pygame.time.Clock()
run = True

# image imports
fish_surf = pygame.image.load(join('images', 'bigredeyefish1.png')).convert_alpha()
surface_kelp = pygame.image.load(join('images', 'kelp_forest1.png')).convert_alpha()
surface_hook = pygame.image.load(join('images', 'hook1.png')).convert_alpha()
surface_jump = pygame.image.load(join('images', 'crab_jump_graphic1.png')).convert_alpha()

kelp_rect = surface_kelp.get_frect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

surface_bubble = pygame.image.load(join('images', 'bubble1.png')).convert_alpha()
#direction_bubble = pygame.math.Vector2(0,1)

# sprites
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bubble_sprites = pygame.sprite.Group()
popper_sprite = pygame.sprite.Group()

for i in range(5):
    Fish(all_sprites, fish_surf)
crab = Player((all_sprites, popper_sprite))


# custom event -> hook event
hook_event = pygame.event.custom_type() # creates custom event
pygame.time.set_timer(hook_event, 5000) # event that gets triggered + duration in ms
bubble_event = pygame.event.custom_type() # creates custom event
pygame.time.set_timer(bubble_event, 3000) # event that gets triggered + duration in ms

#test_rect = pygame.FRect(0, 0, 300, 600)

while run:
    #print("run", run)
    dt = clock.tick(FRAME_RATE) / 1000 # dt is delta time (second/frames). division by 1000 to obtain seconds result.
    #print('game loops')
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == hook_event:
            x, y = randint(0, SCREEN_WIDTH), randint(-900, -100)
            #x, y = 400,500
            Hook(surface_hook, (x, y), (all_sprites, enemy_sprites))
        if event.type == bubble_event:
            #x, y = 400,500
            x, y = randint(0, SCREEN_WIDTH), randint(SCREEN_HEIGHT, SCREEN_HEIGHT+100)
            Bubble(surface_bubble, (x, y), (all_sprites, bubble_sprites))
    
    # background color + scenery (kelp forest, reef, etc.)
    display_surface.fill((0, 150, 155))
    display_surface.blit(surface_kelp, kelp_rect)

    # update
    all_sprites.update(dt)
    #pygame.draw.rect(display_surface, (0, 230, 0), enemy_sprites.hitbox, 2)
    #collisions()
    collided_sprites = pygame.sprite.spritecollide(crab, enemy_sprites, False, collided)
    key = pygame.key.get_pressed()
    if key[pygame.K_q] == True:
       run = False
    

    # test collision
    #print(crab.rect.colliderect(test_rect))


    # drawing the game
    all_sprites.draw(display_surface)
    pygame.display.update()
    

pygame.quit()