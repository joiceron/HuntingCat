'''
Created on Oct. 13, 2023
@author: joice
'''
'''
References: 
https://github.com/maxontech/chrome-dinosaur
https://www.youtube.com/watch?v=wnBGG7JLrkg&list=PL30AETbxgR-fAbwiuU1vDl3owNUPUuVrz&index=2
https://www.youtube.com/watch?v=cFq3dKa6q0o
'''

import pygame
import os
import random
import sys 

# Initialize Pygame
pygame.init()

# Global Constants
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1300
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Cat", "CatRun1.png")),
           pygame.image.load(os.path.join("Assets/Cat", "CatRun2.png")),
           pygame.image.load(os.path.join("Assets/Cat", "CatSick.png"))]

DUCKING = [pygame.image.load(os.path.join("Assets/Cat", "CatDuck1.png")),
           pygame.image.load(os.path.join("Assets/Cat", "CatDuck2.png")),
           pygame.image.load(os.path.join("Assets/Cat", "CatFeed.png"))]

MOUSE = [pygame.image.load(os.path.join("Assets/mouse", "mouse1.png")),
         pygame.image.load(os.path.join("Assets/mouse", "mouse2.png"))]

MOUSETOY = [pygame.image.load(os.path.join("Assets/mouse", "mouseToy.png")),
            pygame.image.load(os.path.join("Assets/mouse", "mouseToy2.png"))]

class Cat:
    X_POS = 10
    Y_POS = 200
    Y_POS_DUCK = 300
    DUCK_VEL = 0.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.kitty_duck = False
        self.kitty_run = True
        self.step_index = 0
        self.image = self.run_img[0]
        self.kitty_rect = self.image.get_rect()
        self.kitty_rect.x = self.X_POS
        self.kitty_rect.y = self.Y_POS

    def update(self, userInput):
        if self.kitty_duck:
            self.duck()
            duck_time = pygame.time.get_ticks()

            if duck_time - self.start_duck_time >= 250:
                self.kitty_duck = False
                self.kitty_run = True

        if self.kitty_run:
            self.run()

        if self.step_index >= 10:
            self.step_index = 0

        elif userInput[pygame.K_SPACE]:
            self.kitty_duck = True
            self.kitty_run = False
            self.start_duck_time = pygame.time.get_ticks()

    def duck(self):
        self.image = self.duck_img[0]
        self.kitty_rect = self.image.get_rect()
        self.kitty_rect.x = self.X_POS
        self.kitty_rect.y = self.Y_POS_DUCK
        self.step_index += 1
        if self.kitty_duck:
            self.kitty_rect.y += self.DUCK_VEL * -0.5

    def run(self):
        self.image = self.run_img[self.step_index // 8]
        self.kitty_rect = self.image.get_rect()
        self.kitty_rect.x = self.X_POS
        self.kitty_rect.y = self.Y_POS
        self.step_index += 1

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.kitty_rect.x, self.kitty_rect.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= 40

        if self.rect.x < -self.rect.width + 300:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

# Define the MouseToy class, which is a type of obstacle
class MouseToy(Obstacle):
    def __init__(self, image, player):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 495
        self.player = player 
        self.duck_img = DUCKING  # Agrega el atributo duck_img a MouseToy

    def update(self):
        super().update()
        self.handle_collision()

    def handle_collision(self):
        # Handle collision with the cat
        global points, death_count
        if self.player.kitty_rect.colliderect(self.rect):
            death_count += 1
            menu(death_count)
            self.player.type = self.duck_img[2]

    def draw(self, SCREEN):
        # Draw the obstacle on the screen
        SCREEN.blit(self.image[self.type], self.rect)


class Mouse(Obstacle):
    def __init__(self, image, player):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 500
        self.player = player

    def update(self):
        super().update()
        self.handle_collision()

    def handle_collision(self):
        global points
        if self.player.kitty_rect.colliderect(self.rect):
            points += 1
            obstacles.pop()

def read_high_score():
    try:
        with open("Assets/Other/highScore.txt", "r") as file:
            content = file.read().split()
            if len(content) == 0:
                return 0, ""  # Devuelve una tupla con valores predeterminados
            else:
                high_score, initials = int(content[0]), content[1]
                return high_score, initials

    except FileNotFoundError:
        return 0, ""  # Devuelve una tupla con valores predeterminados

def write_high_score(score, initials):
    with open("Assets/Other/highScore.txt", "r") as file:
        lines = file.readlines()

    lines.append(f"{score} {initials}\n")

    lines = lines[-5:]

    with open("Assets/Other/highScore.txt", "w") as file:
        file.writelines(lines)

def enter_initials():
    initials = ""
    font = pygame.font.Font('freesansbold.ttf', 30)
    text = font.render("Enter your initials: ", True, (0, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(initials) > 0:
                    return initials.upper()[:3]
                elif event.key == pygame.K_BACKSPACE:
                    initials = initials[:-1]
                elif event.unicode.isalpha() and len(initials) < 3:
                    initials += event.unicode
                elif event.key == pygame.K_KP_ENTER and len(initials) == 3:
                    break
                text = font.render("Enter your initials: " + initials, True, (0, 0, 0))
                SCREEN.fill((255, 255, 255))
                SCREEN.blit(text, text_rect)
                pygame.display.flip()

def show_high_scores():
    SCREEN.fill((255, 255, 255))
    font = pygame.font.Font('freesansbold.ttf', 30)
    high_scores_text = font.render("High Scores", True, (0, 0, 0))
    high_scores_rect = high_scores_text.get_rect()
    high_scores_rect.center = (SCREEN_WIDTH // 2, 50)
    SCREEN.blit(high_scores_text, high_scores_rect)
    SCREEN.blit(RUNNING[2], (SCREEN_WIDTH // 3 - 26, SCREEN_HEIGHT  -290))
    text = font.render("Press any key to restart", True, (0, 0, 0))
    score_text = font.render("Your Score: " + str(points), True, (0, 0, 0))
    score_rect = score_text.get_rect()
    score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    SCREEN.blit(score_text, score_rect)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.blit(text, text_rect)
    try:
        with open("Assets/Other/highScore.txt", "r") as file:
            lines = file.readlines()
            y_position = 100
            for line in lines:
                data = line.split()
                if len(data) == 2:
                    initials, score = data
                    high_score_text = font.render(f"{initials}: {score}", True, (0, 0, 0))
                    high_score_rect = high_score_text.get_rect()
                    high_score_rect.center = (SCREEN_WIDTH // 2, y_position)
                    SCREEN.blit(high_score_text, high_score_rect)
                    y_position += 40
    except FileNotFoundError:
        pass

    pygame.display.flip()


# Main game function
# Main game function
def main():
    global game_speed, points, obstacles, death_count
    run = True
    clock = pygame.time.Clock()
    player = Cat()
    game_speed = 1  # Initial speed

    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        # Display the current score
        global points, game_speed
        if points % 2 == 0:
            game_speed += 1  # Increase speed every 1000 points

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    while run:
        # Main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not run:
            pygame.quit()  # Asegúrate de llamar a pygame.quit() antes de salir
            sys.exit()

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0 and len(obstacles) < game_speed:
            if random.randint(0, 1) == 0:
                obstacles.append(MouseToy(MOUSETOY, player))
            else:
                obstacles.append(Mouse(MOUSE, player))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()

        score()

        clock.tick(20)
        pygame.display.update()


# Menu function to handle game start and restart
def menu(death_count):
    global points
    run = True
    while run:
        try:
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font('freesansbold.ttf', 30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if death_count == 0:
                text = font.render("Press enter to start", True, (0, 0, 0))
                SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 3 - 26, SCREEN_HEIGHT // 3 - 145))
            elif death_count > 0:
                text = font.render("Press enter to restart", True, (0, 0, 0))
                score_text = font.render("Your Score: " + str(points), True, (0, 0, 0))
                score_rect = score_text.get_rect()
                score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                SCREEN.blit(score_text, score_rect)

                # Read the highest score and compare it with the current score
                high_score, _ = read_high_score()
                if points > high_score:
                    high_score = points
                    initials = enter_initials()
                    write_high_score(high_score, initials)

                show_high_scores()

#                SCREEN.blit(RUNNING[2], (SCREEN_WIDTH // 3 - 26, SCREEN_HEIGHT // 3 - 200))

            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, text_rect)
            
            pygame.display.update()

            keys = pygame.key.get_pressed()        
            if keys[pygame.K_RETURN]:

                main()  # Call the main game function
                points = 0  # Reset points after each game
                death_count = 0  # Reset death count after each game

        except pygame.error as e:
            print(f"Error in menu(): {e}")
            break  # Salir del bucle en caso de error

    pygame.quit()  # Cerrar Pygame adecuadamente después de salir del bucle


# Start the game by calling the menu function with initial death_count value
menu(death_count=0)