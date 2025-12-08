import pygame
from pygame.locals import *
import sys
import os

# Get the correct path for bundled resources (PyInstaller)
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize Pygame and the mixer
# pre_init helps avoid sound lag on some systems
pygame.mixer.pre_init(44100, -16, 2, 512) 
pygame.init()
pygame.mixer.init()

screen_width = 650
screen_height = 650

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

# Set custom dock icon (MUST be done AFTER set_mode on macOS!)
try:
    icon = pygame.image.load(resource_path('breakout3.png'))
    pygame.display.set_icon(icon)
except Exception as e:
    print(f"Could not load custom icon: {e}")

# define font
font = pygame.font.SysFont('Constantia', 30)

# define colours
bg = (0, 0, 0)
# block colours
block_red = (255, 27, 145)
block_green = (139, 255, 74)
block_blue = (0, 188, 255)
# paddle colours
paddle_col = (171, 71, 188)
paddle_outline = (171, 71, 188)
# text colour
text_col = (0, 251, 115)

# define game variables
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0 # 0 is playing, 1 is won, -1 is lost

# -----------------------------------------------------
# Sound Loading Section - Now using WAV files
# -----------------------------------------------------
sounds_loaded = False
try:
    # Try .wav files first (converted format) - using resource_path for PyInstaller
    SND_PADDLE = pygame.mixer.Sound(resource_path('sounds/ball.wav'))
    SND_BLOCK = pygame.mixer.Sound(resource_path('sounds/block.wav'))
    SND_GAMEOVER = pygame.mixer.Sound(resource_path('sounds/lost.wav'))
    SND_WIN = pygame.mixer.Sound(resource_path('sounds/won.wav'))
    sounds_loaded = True
    print("✓ All sound files loaded successfully (WAV format)!")
except:
    try:
        # Fall back to original formats
        SND_PADDLE = pygame.mixer.Sound(resource_path('sounds/ball.aif'))
        SND_BLOCK = pygame.mixer.Sound(resource_path('sounds/block.caf'))
        SND_GAMEOVER = pygame.mixer.Sound(resource_path('sounds/lost.aif'))
        SND_WIN = pygame.mixer.Sound(resource_path('sounds/won.aif'))
        sounds_loaded = True
        print("✓ All sound files loaded successfully (original format)!")
    except pygame.error as e:
        print(f"⚠️  Error loading sound files: {e}")
        print("Game will continue without sounds.")
        print("\nTo fix this, convert your sounds to WAV format:")
        print("1. Install ffmpeg: brew install ffmpeg")
        print("2. Run the converter script to create .wav files")
        # Create dummy sound objects
        class DummySound:
            def play(self): pass
        SND_PADDLE = DummySound()
        SND_BLOCK = DummySound()
        SND_GAMEOVER = DummySound()
        SND_WIN = DummySound()


# function for outputting text onto the screen
def draw_text(text, text_font, text_column, x, y):
    img = text_font.render(text, True, text_column)
    screen.blit(img, (x, y))


# brick wall class
class Wall:
    def __init__(self):
        self.blocks = []
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        self.blocks = []  # Clear existing blocks
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                strength = 0
                if row < 2:
                    strength += 3
                elif row < 4:
                    strength += 2
                elif row < 6:
                    strength += 1
                block_individual = [rect, strength]
                block_row.append(block_individual)
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                block_col = bg
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)


# paddle class
class Paddle():
    def __init__(self):
        self.direction = 1
        self.reset()

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def reset(self):
        self.height = 20
        self.width = int(screen_width / cols)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0


# ball class
class GameBall:
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        # collision threshold
        collision_thresh = 5
        wall_destroyed = 1
        
        for row_count, row in enumerate(wall.blocks):
            for item_count, item in enumerate(row):
                # check collision
                if self.rect.colliderect(item[0]):
                    # Play block hit sound
                    SND_BLOCK.play()
                    
                    # check if collision was from above
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    # check if collision was from below
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    # check if collision was from left
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    # check if collision was from right
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    # reduce the block's strength by doing damage to it
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        # Make block disappear (set to an empty rect)
                        wall.blocks[row_count][item_count][0] = pygame.Rect(0, 0, 0, 0)
                        wall.blocks[row_count][item_count][1] = 0

                # check if block still exists, in which case the wall is not destroyed
                if wall.blocks[row_count][item_count][1] > 0:
                    wall_destroyed = 0
        
        # Check if the wall is destroyed (game won)
        if wall_destroyed == 1:
            self.game_over = 1

        # check for collision with walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        # check for collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speed_y *= -1

        # look for collision with paddle
        if self.rect.colliderect(player_paddle):
            # Play paddle hit sound (only when ball is coming down)
            if self.speed_y > 0: 
                 SND_PADDLE.play()

            # check if colliding from the top
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Check for ball missing the paddle (game lost condition)
        if self.rect.bottom > screen_height:
            self.game_over = -1

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad, 3)

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0


# create a wall
wall = Wall()
wall.create_wall()

# create paddle
player_paddle = Paddle()

# create ball
ball = GameBall(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

run = True
sound_played = False # Flag to ensure game over/win sound plays only once

while run:

    clock.tick(fps)

    screen.fill(bg)

    # draw all objects
    wall.draw_wall()
    player_paddle.draw()
    ball.draw()

    if live_ball:
        # draw paddle
        player_paddle.move()
        # draw ball
        game_over = ball.move()
        if game_over != 0:
            live_ball = False
            # Play game over sound when game_over is set to -1 (lost) or 1 (won)
            if not sound_played:
                if game_over == -1:
                    SND_GAMEOVER.play()
                elif game_over == 1:
                    SND_WIN.play()
                sound_played = True

    # print player instructions
    if not live_ball:
        if game_over == 0:
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text('YOU WON!', font, text_col, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text('YOU LOST!', font, text_col, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()
            sound_played = False # Reset the sound flag for the new round

    pygame.display.update()

pygame.quit()