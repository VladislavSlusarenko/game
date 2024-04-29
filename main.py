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

# Создание прозрачных границ
border_top = pygame.Surface((SCREEN_WIDTH, 10), pygame.SRCALPHA)
border_bottom = pygame.Surface((SCREEN_WIDTH, 10), pygame.SRCALPHA)
border_left = pygame.Surface((10, SCREEN_HEIGHT), pygame.SRCALPHA)
border_right = pygame.Surface((10, SCREEN_HEIGHT), pygame.SRCALPHA)

# Заполнение прозрачных границ
border_top.fill((0, 0, 0, 0))
border_bottom.fill((0, 0, 0, 0))
border_left.fill((0, 0, 0, 0))
border_right.fill((0, 0, 0, 0))

# Класс для персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = "idle"  # Начальное направление движения
        self.idle_images = right_idle_images  # Начальная анимация - вправо
        self.image = self.idle_images[0]  # Начальное изображение анимации
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - CHARACTER_HEIGHT // 2)
        self.velocity = 0.5
        self.jump = False
        self.jump_speed = 15
        self.last_idle_update = pygame.time.get_ticks()  # Отслеживание времени последнего обновления анимации в покое

    def update(self):
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

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        IDLE_ANIMATION_INTERVAL = 150 # 150миллисекунд
        if current_time - self.last_idle_update > IDLE_ANIMATION_INTERVAL:
            self.last_idle_update = current_time
            if self.direction == "left":
                self.idle_images = left_idle_images
            elif self.direction == "right":
                self.idle_images = right_idle_images
            self.image = self.idle_images[0]  # Это строка устанавливает текущее изображение анимации

# Класс для препятствия
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH + OBSTACLE_WIDTH // 0, SCREEN_HEIGHT - OBSTACLE_HEIGHT // 0)
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
            elif event.key == pygame.K_LEFT:
                character.direction = "left"
            elif event.key == pygame.K_RIGHT:
                character.direction = "right"

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        character.rect.x += 5

    current_time = pygame.time.get_ticks()
    if current_time - obstacle_timer > obstacle_generation_interval:
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)
        obstacle_timer = current_time

    # Отображение заднего фона
    screen.blit(background_img, (0, 0))

    # Отображение прозрачных границ
    screen.blit(border_top, (0, 0))
    screen.blit(border_bottom, (0, SCREEN_HEIGHT - 10))
    screen.blit(border_left, (0, 0))
    screen.blit(border_right, (SCREEN_WIDTH - 10, 0))

    all_sprites.update()
    character.update()
    character.update_animation()
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()

