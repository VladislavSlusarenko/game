import pygame
import sys
import os

# Ініціалізація Pygame
pygame.init()

# Визначення констант
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CHARACTER_WIDTH = 50
CHARACTER_HEIGHT = 50
PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Створення вікна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ігра")

# Шляхи до папок
animation_path = "/Users/admin/Downloads/game2/idle_animation"
obstacle_path = "/Users/admin/Downloads/game2/obstacle"
background_path = "/Users/admin/Downloads/game2/background"

# Перевірка папок і файлів
def check_directory(path):
    if not os.path.exists(path):
        print(f"Папка {os.path.basename(path)} не знайдена в {os.getcwd()}")
        sys.exit()

    files = os.listdir(path)
    if not files:
        print(f"У папці {os.path.basename(path)} немає файлів")
        sys.exit()

    for file in files:
        print(f"Знайдено файл у папці {os.path.basename(path)}: {file}")

check_directory(animation_path)
check_directory(obstacle_path)
check_directory(background_path)

# Завантаження зображень
try:
    right_idle_images = [pygame.image.load(os.path.join(animation_path, f"right{i}.png")) for i in range(1, 4)]
    left_idle_images = [pygame.image.load(os.path.join(animation_path, f"left{i}.png")) for i in range(1, 4)]
    obstacle_img = pygame.image.load(os.path.join(obstacle_path, "obstacle.png"))
    obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))
    background_img = pygame.image.load(os.path.join(background_path, "background.png"))
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print("Помилка завантаження зображень:", e)
    sys.exit()

# Установка початкової позиції персонажа
character_start_x = SCREEN_WIDTH // 2
character_start_y = SCREEN_HEIGHT // 2 + 50  # Трохи нижче центру

# Клас для персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = "idle"  # Початковий напрямок руху
        self.idle_images = right_idle_images  # Початкова анімація - вправо
        self.image = self.idle_images[0]  # Початкове зображення анімації
        self.rect = self.image.get_rect()
        self.rect.center = (character_start_x, character_start_y)  # Установка початкової позиції
        self.velocity_y = 0  # Встановлюємо початкову вертикальну швидкість персонажа
        self.velocity_x = 0  # Встановлюємо початкову горизонтальну швидкість персонажа
        self.jump = False
        self.jump_speed = 15
        self.gravity = 1
        self.on_ground = False
        self.last_idle_update = pygame.time.get_ticks()  # Відстеження часу останнього оновлення анімації в спокої

    def update(self):
        if self.jump:
            self.velocity_y -= self.gravity
            self.rect.y -= self.velocity_y
            if self.velocity_y <= 0:
                self.jump = False
        else:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True
            self.velocity_y = 0

        if pygame.sprite.collide_rect(self, platform):
            if self.rect.bottom <= platform.rect.top + self.velocity_y:
                self.rect.bottom = platform.rect.top
                self.on_ground = True
                self.velocity_y = 0
            else:
                self.on_ground = False

        self.rect.x += self.velocity_x

    def jump_start(self):
        if self.on_ground:
            self.velocity_y = self.jump_speed
            self.jump = True
            self.on_ground = False

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        IDLE_ANIMATION_INTERVAL = 150  # 150 мілісекунд
        if current_time - self.last_idle_update > IDLE_ANIMATION_INTERVAL:
            self.last_idle_update = current_time
            if self.direction == "left":
                self.idle_images = left_idle_images
            elif self.direction == "right":
                self.idle_images = right_idle_images
            self.image = self.idle_images[0]  # Цей рядок встановлює поточне зображення анімації

# Клас для платформи
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Невидима платформа
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Створення груп спрайтів
all_sprites = pygame.sprite.Group()
character = Character()
platform = Platform(SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2, SCREEN_HEIGHT // 2, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # Платформа розташована вище
all_sprites.add(character)
all_sprites.add(platform)

# Основний ігровий цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                character.jump_start()
            elif event.key == pygame.K_LEFT:
                character.direction = "left"
                character.velocity_x = -5  # Встановлення швидкості по горизонталі
            elif event.key == pygame.K_RIGHT:
                character.direction = "right"
                character.velocity_x = 5  # Встановлення швидкості по горизонталі
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character.velocity_x = 0  # Обнуляємо швидкість по горизонталі, коли клавіша відпущена

    # Відображення заднього фону
    screen.blit(background_img, (0, 0))

    all_sprites.update()
    character.update_animation()
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()