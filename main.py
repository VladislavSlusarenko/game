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
GROUND_HEIGHT = 50

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра")

# Пути к папкам
idle_animation_path = "/Users/admin/Downloads/game2/idle_animation"
move_animation_path = "/Users/admin/Downloads/game2/animation_images"
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

check_directory(idle_animation_path)
check_directory(move_animation_path)
check_directory(obstacle_path)
check_directory(background_path)

# Загрузка изображений
try:
    right_idle_images = [pygame.image.load(os.path.join(idle_animation_path, f"right{i}.png")) for i in range(1, 4)]
    left_idle_images = [pygame.image.load(os.path.join(idle_animation_path, f"left{i}.png")) for i in range(1, 4)]
    right_move_images = [pygame.image.load(os.path.join(move_animation_path, f"right{i}.png")) for i in range(1, 11)]
    left_move_images = [pygame.image.load(os.path.join(move_animation_path, f"left{i}.png")) for i in range(1, 11)]
    obstacle_img = pygame.image.load(os.path.join(obstacle_path, "obstacle.png"))
    obstacle_img = pygame.transform.scale(obstacle_img, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
    background_img = pygame.image.load(os.path.join(background_path, "background.png"))  # Загрузка изображения фона из локального пути
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print("Ошибка загрузки изображений:", e)
    sys.exit()
except FileNotFoundError as e:
    print("Файл не найден:", e)
    sys.exit()

# Создание прозрачной платформы
PLATFORM_HEIGHT = 10
platform = pygame.Surface((SCREEN_WIDTH, PLATFORM_HEIGHT), pygame.SRCALPHA)
platform.fill((0, 0, 0, 0))

# Класс для персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = "idle"  # Начальное направление движения
        self.idle_images = right_idle_images  # Начальная анимация - вправо
        self.move_images = right_move_images  # Начальная анимация движения - вправо
        self.image = self.idle_images[0]  # Начальное изображение анимации
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - CHARACTER_HEIGHT - 70)  # Задаем начальную позицию по изображению
        self.velocity = 0.5
        self.jump = False
        self.jump_speed = 15
        self.last_idle_update = pygame.time.get_ticks()  # Отслеживание времени последнего обновления анимации в покое
        self.last_move_update = pygame.time.get_ticks()  # Отслеживание времени последнего обновления анимации движения
        self.idle_image_index = 0  # Индекс текущего изображения анимации покоя
        self.move_image_index = 0  # Индекс текущего изображения анимации движения
        self.is_moving = False  # Флаг для проверки движения

    def update(self):
        keys = pygame.key.get_pressed()
        self.is_moving = False  # По умолчанию персонаж стоит

        if keys[pygame.K_LEFT]:
            self.rect.x -= 2
            self.direction = "left"
            self.is_moving = True  # Персонаж движется

        if keys[pygame.K_RIGHT]:
            self.rect.x += 2
            self.direction = "right"
            self.is_moving = True  # Персонаж движется

        # Гравитация
        self.rect.y += self.velocity  # Обновляем позицию по оси Y
        self.velocity += 1

        # Проверка столкновений с платформами
        if pygame.sprite.spritecollide(self, platforms, False):
            self.velocity = 0  # Останавливаем падение
            self.jump = False
            self.rect.bottom = platform.rect.top  # Устанавливаем персонажа на платформу

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT  # Останавливаем персонажа на нижней границе экрана
            self.velocity = 0
            self.jump = False

    def jump_start(self):
        if not self.jump:
            self.velocity = -self.jump_speed
            self.jump = True

    def update_animation(self):
        current_time = pygame.time.get_ticks()

        if self.is_moving:
            ANIMATION_INTERVAL = 100  # Интервал для анимации движения
            if current_time - self.last_move_update > ANIMATION_INTERVAL:
                self.last_move_update = current_time
                if self.direction == "left":
                    self.move_images = left_move_images
                elif self.direction == "right":
                    self.move_images = right_move_images
                
                self.move_image_index = (self.move_image_index + 1) % len(self.move_images)
                self.image = self.move_images[self.move_image_index]  # Обновляем изображение анимации движения
        else:
            IDLE_ANIMATION_INTERVAL = 400  # Интервал для анимации покоя
            if current_time - self.last_idle_update > IDLE_ANIMATION_INTERVAL:
                self.last_idle_update = current_time
                if self.direction == "left":
                    self.idle_images = left_idle_images
                elif self.direction == "right":
                    self.idle_images = right_idle_images
                
                self.idle_image_index = (self.idle_image_index + 1) % len(self.idle_images)
                self.image = self.idle_images[self.idle_image_index]  # Обновляем изображение анимации покоя

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

# Класс для платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
platforms = pygame.sprite.Group()

character = Character()
all_sprites.add(character)

# Создание платформы
platform = Platform(0, SCREEN_HEIGHT - 38, SCREEN_WIDTH, PLATFORM_HEIGHT)  # Установите платформу по уровню дороги на изображении
all_sprites.add(platform)
platforms.add(platform)

# Таймер для генерации препятствий
obstacle_timer = pygame.time.get_ticks()
obstacle_generation_interval = 20000000  # Интервал генерации препятствий (в миллисекундах)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Изменено на стрелку вверх
                character.jump_start()
            elif event.key == pygame.K_LEFT:
                character.direction = "left"
            elif event.key == pygame.K_RIGHT:
                character.direction = "right"

    current_time = pygame.time.get_ticks()
    if current_time - obstacle_timer > obstacle_generation_interval:
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)
        obstacle_timer
        
    # Отображение заднего фона
    screen.blit(background_img, (0, 0))

    all_sprites.update()
    character.update_animation()
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()

# Создание платформы
platform = Platform(0, SCREEN_HEIGHT - 70 + 100, SCREEN_WIDTH, PLATFORM_HEIGHT)  # Опустить платформу на 100 пикселей
all_sprites.add(platform)
platforms.add(platform)
