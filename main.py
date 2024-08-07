import pygame
import math
import random
from sys import exit

pygame.init()
clock = pygame.time.Clock()

#stores resolution for game
screen_vertical = 720
screen_horizontal = 551
screen = pygame.display.set_mode((screen_horizontal, screen_vertical))

#images used for game
bird_images = [pygame.image.load("Assets/bird_down.png"),
               pygame.image.load("Assets/bird_mid.png"),
               pygame.image.load("Assets/bird_up.png")]
background_images = pygame.image.load("Assets/background.png")
game_over_image = pygame.image.load("Assets/game_over.png")
ground_image = pygame.image.load("Assets/ground.png")
pipe_images = [pygame.image.load("Assets/pipe_top.png"),
               pygame.image.load("Assets/pipe_bottom.png")]
start_image = pygame.image.load("Assets/start.png")

#game variables
scroll_speed = 1
bird_start_pos = (100, 250)
score = 0
font = pygame.font.SysFont('Segoe', 26)
game_stopped = True
Normal, Hard, Impossible = False, False, False


#class to create the pipes
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type, bird):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type
        self.bird = bird
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -screen_horizontal:
            self.kill()

        #keeping score
        global score
        if self.pipe_type == 'bottom':
            if self.bird.sprite.rect.x > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if self.bird.sprite.rect.x > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit:
                self.passed = True
                score += 1
        self.enter, self.exit = False, False


#class to handel the bird
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_images[0]
        self.current_index = 0
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_pos
        self.flap = False
        self.jump_velocity = 0
        self.Death = False

    def update(self):
        self.current_index += 0.08

        if self.current_index > 3:
            self.current_index = 0

        self.image = bird_images[math.floor(self.current_index)]

        self.fall()

        self.image = pygame.transform.rotate(self.image, self.jump_velocity * -4)

    def fall(self):
        self.jump_velocity += 0.5

        if self.jump_velocity > 5:
            self.jump_velocity = 5

        if self.rect.y < 500:
            self.rect.y += int(self.jump_velocity)

        if self.jump_velocity <= 0:
            self.flap = False

    def jump(self):
        self.flap = True
        self.jump_velocity = -5



#class to handel the floor
class Ground(pygame.sprite.Sprite):
    #constructor
    def __init__(self, x, y):
        super().__init__() #if giving error use pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    #plays ground animation
    def move_ground(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -screen_horizontal:
            self.kill()

    def update(self):
        self.move_ground()

#used for main game logic
def main():
    global score
    global game_stopped
    global Normal, Hard, Impossible

    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))

    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    pipe_timer = 0
    pipe = pygame.sprite.Group()


    continue_game = True
    while continue_game:
        #quits game
        quit()

        #fills frame
        screen.fill((0, 0, 0))

        # set background
        screen.blit(background_images, (0, 0))

        if len(ground) <= 2:
            ground.add(Ground(screen_horizontal, y_pos_ground))

        #drawing world + objects
        ground.draw(screen)
        bird.draw(screen)
        pipe.draw(screen)

        #show score
        score_txt = font.render('Score: ' + str(score), True, pygame.Color(255, 255, 255))
        screen.blit(score_txt, (20, 20))

        #update ground position
        if bird.sprite.Death == False:
            ground.update()
            bird.update()
            pipe.update()

        # collision handeling
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipe, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            bird.sprite.Death = True


        #spawning of pipes
        if pipe_timer <= 0 and bird.sprite.Death == False:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + pipe_images[1].get_height()
            pipe.add(Pipe(x_top, y_top, pipe_images[0], 'top', bird))
            pipe.add(Pipe(x_bottom, y_bottom, pipe_images[1], 'bottom', bird))
            if Normal:
                pipe_timer = random.randint(180, 250)
            elif Hard:
                pipe_timer = random.randint(60, 90)
            elif Impossible:
                pipe_timer = random.randint(20, 50)

        pipe_timer -= 1

        #user input
        keys = pygame.key.get_pressed()

        #handles the movement of the bird
        if keys[pygame.K_SPACE] and bird.sprite.flap == False and bird.sprite.rect.y > 0:
            bird.sprite.jump()

        if bird.sprite.Death:
            screen.blit(game_over_image, (screen_horizontal // 2 - game_over_image.get_width() // 2,
                                          screen_vertical // 2 - game_over_image.get_height() // 2))
            if keys[pygame.K_r]:
                score = 0
                game_stopped = True
                menu()
                break

        #sets fps to 60
        clock.tick(60)
        pygame.display.update()



#used to quit the game
def quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

#main game menu
def menu():
    global scroll_speed
    global game_stopped
    global Normal, Hard, Impossible

    while game_stopped:
        quit()

        #displaying menu to screen
        screen.fill((0, 0, 0))
        screen.blit(background_images, (0, 0))
        screen.blit(ground_image, (0, 520))
        screen.blit(bird_images[1], (100, 250))
        screen.blit(start_image, (screen_horizontal // 2 - game_over_image.get_width() // 2,
                                       screen_vertical // 2 - game_over_image.get_height() // 2))

        difficulty_options = font.render('Difficulty!: ' + '1 = Normal, 2 = Hard, 3 = Impossible', True, pygame.Color(255, 255, 255))

        screen.blit(difficulty_options, (0, 5))

        #user input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_1]:
            Normal = True
            Hard = False
            Impossible = False
            scroll_speed = 1
            main()
        elif keys[pygame.K_2]:
            Normal = False
            Hard = True
            Impossible = False
            scroll_speed = 3
            main()
        elif keys[pygame.K_3]:
            Normal = False
            Hard = False
            Impossible = True
            scroll_speed = 3
            main()

        pygame.display.update()


menu()
