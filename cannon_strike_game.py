import pygame
import pymunk
import pymunk.pygame_util

# Initialize
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cannon Strike Game")
clock = pygame.time.Clock()
running = True
score = 0
attempts = 5
game_over = False
game_won = False
game_ended = False 

# Pymunk Space Setup
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

pygame.mixer.init()

# Load Music and Sound Effects
win_sound = pygame.mixer.Sound('win_sound_cannon_strike.mp3')
lose_sound = pygame.mixer.Sound('lose_sound_cannon_strike.mp3')
launch_sound = pygame.mixer.Sound('shoot_sound_cannon_strike.mp3')
hit_sound = pygame.mixer.Sound('brick_hit_cannon_strike.mp3')
"Background music"
background_music = pygame.mixer.Sound("background_music_cannon_strike.mp3")
background_music.play(-1)
background_music.set_volume(0.3)

# Load Images
cannon_image = pygame.image.load('cannon_image.png')
cannon_ball_image = pygame.image.load('cannon_ball_image.png')
brick_image = pygame.image.load('brick_image.png')
background_image = pygame.image.load('background_image_cannon_strike.jpg')

# Resize Images
background_image = pygame.transform.scale(background_image, (800, 600))
cannon_ball_image = pygame.transform.scale(cannon_ball_image, (50, 50))
cannon_image = pygame.transform.scale(cannon_image, (200, 200))
brick_image = pygame.transform.scale(brick_image, (60, 60))

# Ground
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground_body, (0, 580), (800, 580), 5)
ground_shape.friction = 1
space.add(ground_body, ground_shape)

# Cannon
def create_cannon(x, y):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (60, 60))
    space.add(body, shape)
    return body, shape

cannon_body, cannon_shape = create_cannon(10, 500)

# Create Block
def create_block(x, y):
    body = pymunk.Body(1, pymunk.moment_for_box(1, (60, 60)))
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (60, 60))
    shape.elasticity = 0.4
    shape.friction = 0.6
    shape.collision_type = 2
    space.add(body, shape)
    return body, shape

# Create stacked blocks
blocks = [
    create_block(540, 520), create_block(600, 520), create_block(660, 520),
    create_block(720, 520), create_block(780, 520),
    create_block(600, 460), create_block(660, 460), create_block(720, 460),
    create_block(630, 400), create_block(690, 400),
    create_block(660, 340)
]

# Cannonball list
cannonballs = []

# Create Cannonball
def create_cannonball(x, y, velocity):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    body.position = x, y
    shape = pymunk.Circle(body, 20)
    shape.elasticity = 0.2
    shape.friction = 0.2
    shape.collision_type = 1
    space.add(body, shape)
    body.velocity = velocity
    cannonballs.append((body, shape))

# Draw everything
def draw_objects():
    screen.blit(background_image, (0, 0))

    # Cannonballs
    for body, shape in cannonballs:
        pos = body.position
        screen.blit(cannon_ball_image, (pos.x - 25, pos.y - 25))

    # Cannon
    pos = cannon_body.position
    screen.blit(cannon_image, (pos.x - 20, pos.y - 20))

    # Blocks
    for body, shape in blocks[:]:
        pos = body.position
        angle = body.angle * (180 / 3.14159)
        rotated = pygame.transform.rotate(brick_image, angle)
        rect = rotated.get_rect(center=(pos.x, pos.y))
        if pos.x > 820 or pos.y > 620:
            hit_sound.play()
            space.remove(body, shape)
            blocks.remove((body, shape))
            global score 
            score +=10
        else:
            screen.blit(rotated, rect.topleft)

    # Score + Attempts
    font = pygame.font.SysFont(None, 36)
    screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(f"Attempts: {attempts}", True, (0, 0, 0)), (10, 50))

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and attempts > 0
            and not game_over
            and not game_won
        ):
            mouse_pos = pygame.mouse.get_pos()
            velocity = ((mouse_pos[0] - 150) * 4, (mouse_pos[1] - 500) * 4)
            create_cannonball(150, 500, velocity)
            attempts -= 1
            launch_sound.play()

    # Only process game logic if not ended
    if not game_ended:
        # Physics step
        space.step(1 / 60.0)

        # Win condition
        if len(blocks) == 0 and not game_won:
            pygame.time.delay(100)
            background_music.stop()
            pygame.mixer.stop()
            win_sound.play()
            game_won = True
            game_ended = True

        # Lose condition
        elif attempts == 0 and len(blocks) > 0 and not game_over:
            pygame.time.delay(1000)
            background_music.stop()
            pygame.mixer.stop()
            lose_sound.play()
            game_over = True
            game_ended = True

    # Draw everything
    draw_objects()

    # End messages
    if game_won:
        pygame.time.delay(1000)
        font = pygame.font.SysFont(None, 72)
        win_text = font.render("YOU WON!", True, (0, 255, 0))
        screen.blit(win_text, (280, 250))
        pygame.display.flip()      
        pygame.time.delay(10000)    
        running = False       

    elif game_over:
        pygame.time.delay(1000)
        font = pygame.font.SysFont(None, 72)
        lose_text = font.render("YOU LOST", True, (255, 0, 0))
        screen.blit(lose_text, (300, 250))
        pygame.display.flip()      
        pygame.time.delay(3000)
        running = False


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
