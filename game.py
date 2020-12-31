import pygame,sys
import random

pygame.init()

#CONSTANTS
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000
FLOOR_HEIGHT = 100
FLOOR_WIDTH = 1250
MARIO_HEIGHT = 66
MARIO_WIDTH = 58
MARIOJMP_HEIGHT = 70
MARIOJMP_WIDTH = 68
MARIO_START = 100
FLOOR_TOP = SCREEN_HEIGHT - FLOOR_HEIGHT
GOOMBA_HEIGHT = 67
GOOMBA_WIDTH = 69
FONT = pygame.font.Font('freesansbold.ttf', 32)

# setting things up (screen and initialization)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # size of screen
clock = pygame.time.Clock()

# caption and icon
pygame.display.set_caption("Super Mario")
icon = pygame.image.load('mushroom.png')
pygame.display.set_icon(icon)

#loading images for the game
floor_surface = pygame.image.load('floor.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (FLOOR_WIDTH, FLOOR_HEIGHT))

mario = pygame.image.load('mmario.png').convert_alpha()
mario = pygame.transform.scale(mario, (MARIO_WIDTH, MARIO_HEIGHT))
mariojump = pygame.image.load('mmariojump.png').convert_alpha()
mariojump = pygame.transform.scale(mariojump, (MARIOJMP_WIDTH, MARIOJMP_HEIGHT))
mario_frames = [mario, mariojump]
mario_current = mario_frames[0]
mario_rect = mario_current.get_rect(midbottom = (MARIO_START, FLOOR_TOP))

goomba = pygame.image.load('mgoomba.png').convert_alpha()
goomba = pygame.transform.scale(goomba, (GOOMBA_WIDTH, GOOMBA_HEIGHT))
goomba_list = []
SPAWNGOOMBA = pygame.USEREVENT
pygame.time.set_timer(SPAWNGOOMBA,1000) #spawn goomba every 1.5 seconds

#setting up game
gravity = 0.25
mario_y = 0
floor_x = 0 #to give the illusion of movement
lives = 1
distance = 0
highscore = 0

#helper functions       
def clear_goomba():
        global goomba_list
        for i in goomba_list:
                goomba_list.remove(i)
        
def draw_floor(x):
	screen.blit(floor_surface,(floor_x, FLOOR_TOP))
	screen.blit(floor_surface,(floor_x + FLOOR_WIDTH, FLOOR_TOP))

def can_jump():
        """returns true if mario is on land false otherwise,
        this is to ensure that mario can't do multiple jumps at once
        """
        if mario_rect.bottom<500:
                return False
        return True

def create_goomba():
	rand_x = random.randint(1100, 1500)
	goomba_rect= goomba.get_rect(midbottom=(rand_x, FLOOR_TOP))
	return goomba_rect

def draw_goomba():
        global goomba_list
        for i in goomba_list:
                if i.centerx <= -100:
                        goomba_list.remove(i)
                else:
                        screen.blit(goomba, i)

def move_goomba():
        global goomba_list
        for i in goomba_list:
                i.centerx -= 2.5

def collide():
        for i in goomba_list:
                if mario_rect.colliderect(i):
                        return True
        return False

def stats_display_alive():
        lives_disp = FONT.render("lives: "+ str(lives), True,(255,255,255))
        lives_disp_rect = lives_disp.get_rect(center = (100, 150))
        screen.blit(lives_disp, lives_disp_rect)

        distance_disp = FONT.render("distance: " + str(int(distance)), True,(255,255,255))
        distance_disp_rect = lives_disp.get_rect(center = (100, 100))
        screen.blit(distance_disp, distance_disp_rect)

def stats_display_dead(x):
        gameover_disp = FONT.render("GAME OVER", True, (255, 0, 0))
        gameover_disp_rect = gameover_disp.get_rect(center = (500,300))
        screen.blit(gameover_disp, gameover_disp_rect)
                
        score_disp = FONT.render("score: " + str(int(x)), True,(255,255,255))
        score_disp_rect = score_disp.get_rect(center = (100, 100))
        screen.blit(score_disp, score_disp_rect)

        hscore_disp = FONT.render("high score: " + str(int(highscore)), True,(255,255,255))
        hscore_disp_rect = hscore_disp.get_rect(midleft = (30, 50))
        screen.blit(hscore_disp, hscore_disp_rect)

                
#GAME LOOP
while True:
        for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE: #replay
                                        lives = 1
                                        if (can_jump()):
                                                mario_y -= 10
        while (lives>0):
                screen.fill((106, 140, 255)) #blue color of sky
            
                for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE: #mario jump
                                        if (can_jump()):
                                                mario_y -= 10
                        if event.type == SPAWNGOOMBA:
                                goomba_list.append(create_goomba())
                                
                mario_rect.centery += mario_y
                if (mario_rect.bottom + gravity) <= 500: #is jumping
                        mario_y += gravity #go back to land after jumping
                        mario_current = mario_frames[1]
                else:
                        mario_y = 0
                        mario_rect.bottom = FLOOR_TOP
                        mario_current = mario_frames[0]
                screen.blit(mario_current, mario_rect)

                move_goomba()
                draw_goomba()

                floor_x -= 1 
                distance += 0.06
                
                draw_floor(floor_x)
                if floor_x <= -1000:
                        floor_x = 0

                if collide():
                        lives -= 1
                        clear_goomba()

                #displaying stats
                if lives>0:
                        stats_display_alive()
                else:
                        if distance > highscore:
                                highscore = distance
                        stats_display_dead(distance)
                        distance = 0
                
                pygame.display.update()
                clock.tick(150) #run loop at most 150 times per second
        
