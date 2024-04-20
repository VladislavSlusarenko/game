import pygame
import random
import sys
import os

# Инициализация Pygame
pygame.init()

# Определение констант
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CHARACTER_WIDTH = 50
CHARACTER_HEIGHT = 50
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра")

# Пути к папкам
animation_path = "/Users/admin/Downloads/game2/idle_animation"
obstacle_path = "/Users/admin/Downloads/game2/obstacle"
background_path = "/Users/admin/Downloads/game2/background"

# Проверка папок и файлов
def check_directory(path):
    if not os.path.exists(path):
        print(f"Папка {os.path.basename(path)} не найдена в {os.getcwd()}")
        sys.exit()

    files = os.listdir(path)
    if not files:
        print(f"В папке {os.path.basename(path)} нет файлов")
        sys.exit()

    for file in files:
        print(f"Найден файл в папке {os.path.basename(path)}: {file}")

check_directory(animation_path)
check_directory(obstacle_path)
check_directory(background_path)

# Загрузка изображений
try:
    right_idle_images = [pygame.image.load(os.path.join(animation_path, f"right{i}.png")) for i in range(1, 4)]
    left_idle_images = [pygame.image.load(os.path.join(animation_path, f"left{i}.png")) for i in range(1, 4)]
    obstacle_img = pygame.image.load(os.path.join(obstacle_path, "obstacle.png"))
    obstacle_img = pygame.transform.scale(obstacle_img, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
    background_img = pygame.image.load(os.path.join(background_path, "background.png"))
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print("Ошибка загрузки изображений:", e)
    sys.exit()

# Класс для персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = "idle"  # Начальное направление движения
        self.idle_images = right_idle_images  # Начальная анимация - вправо
        self.image = self.idle_images[0]  # Начальное изображение анимации
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - CHARACTER_HEIGHT // 2)
        self.velocity = 0
        self.jump = False
        self.jump_speed = 10
        self.last_idle_update = pygame.time.get_ticks()  # Время последнего обновления анимации покоя
        self.idle_animation_interval = 200  # Интервал обновления анимации покоя

    def update(self):
        # Обновление анимации покоя
        current_time = pygame.time.get_ticks()
        if current_time - self.last_idle_update > self.idle_animation_interval:
            self.last_idle_update = current_time
            self.update_idle_animation()

        # Обновление положения персонажа в прыжке
        if self.jump:
            self.rect.y -= self.velocity
            self.velocity -= 1
            if self.velocity < 0:
                self.jump = False
                self.velocity = self.jump_speed
        elif self.rect.y < SCREEN_HEIGHT - CHARACTER_HEIGHT // 2:
            self.rect.y += self.velocity
            self.velocity += 1
        else:
            self.rect.y = SCREEN_HEIGHT - CHARACTER_HEIGHT // 2
            self.velocity = self.jump_speed

    def jump_start(self):
        if not self.jump:
            self.velocity = self.jump_speed
            self.jump = True

    def update_idle_animation(self):
        # Обновление кадра анимации покоя
        if self.direction == "left":
            self.idle_images = left_idle_images
        elif self.direction == "right":
            self.idle_images = right_idle_images
        self.image = self.idle_images[current_idle_image]

# Класс для препятствия
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH + OBSTACLE_WIDTH // 2, SCREEN_HEIGHT - OBSTACLE_HEIGHT // 2)
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH + OBSTACLE_WIDTH // 2
            self.speed = random.randint(3, 5)

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
character = Character()
all_sprites.add(character)

# Таймер для генерации препятствий
obstacle_timer = pygame.time.get_ticks()
obstacle_generation_interval = 2000000  # Интервал генерации препятствий (в миллисекундах)

# Основной игровой цикл
running = True
current_idle_image = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                character.jump_start()

    current_time = pygame.time.get_ticks()
    if current_time - obstacle_timer > obstacle_generation_interval:
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)
        obstacle_timer = current_time

    screen.blit(background_img, (0, 0))

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()