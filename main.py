import pygame
import sys
import os

# Инициализация Pygame
pygame.init()

# Определение констант
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CHARACTER_WIDTH = 50
CHARACTER_HEIGHT = 50
PLATFORM_HEIGHT = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра")

# Пути к папкам
idle_animation_path = "/Users/admin/Downloads/game2/idle_animation"
move_animation_path = "/Users/admin/Downloads/game2/animation_images"
hit_animation_path = "/Users/admin/Downloads/game2/hit"
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
check_directory(hit_animation_path)
check_directory(background_path)

# Загрузка изображений
try:
    right_idle_images = [pygame.image.load(os.path.join(idle_animation_path, f"right{i}.png")) for i in range(1, 4)]
    left_idle_images = [pygame.image.load(os.path.join(idle_animation_path, f"left{i}.png")) for i in range(1, 4)]
    right_move_images = [pygame.image.load(os.path.join(move_animation_path, f"right{i}.png")) for i in range(1, 11)]
    left_move_images = [pygame.image.load(os.path.join(move_animation_path, f"left{i}.png")) for i in range(1, 11)]
    right_hit_images = [pygame.image.load(os.path.join(hit_animation_path, f"right{i}.png")) for i in range(1, 3)]
    obstacle_img = pygame.image.load(os.path.join(background_path, "background.png"))
    background_img = pygame.image.load(os.path.join(background_path, "background.png"))
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print("Ошибка загрузки изображений:", e)
    sys.exit()
except FileNotFoundError as e:
    print("Файл не найден:", e)
    sys.exit()

# Класс для персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = "idle"  # Начальное направление движения
        self.idle_images = right_idle_images
        self.move_images = right_move_images
        self.hit_images = right_hit_images  # Анимация удара
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - CHARACTER_HEIGHT - PLATFORM_HEIGHT - 20)
        self.velocity = 0.5
        self.jump = False
        self.jump_speed = 10  # Уменьшена высота прыжка
        self.last_idle_update = pygame.time.get_ticks()
        self.last_move_update = pygame.time.get_ticks()
        self.last_hit_update = pygame.time.get_ticks()
        self.idle_image_index = 0
        self.move_image_index = 0
        self.hit_image_index = 0
        self.is_moving = False
        self.is_hitting = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        self.is_hitting = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= 2
            self.direction = "left"
            self.is_moving = True

        if keys[pygame.K_RIGHT]:
            self.rect.x += 2
            self.direction = "right"
            self.is_moving = True

        if keys[pygame.K_SPACE]:  # Удар на пробел
            self.is_hitting = True

        # Гравитация
        self.rect.y += self.velocity
        self.velocity += 0.5

        if pygame.sprite.spritecollide(self, platforms, False):
            self.velocity = 0
            self.jump = False
            self.rect.bottom = platform.rect.top

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
            self.jump = False

    def jump_start(self):
        if not self.jump:
            self.velocity = -self.jump_speed
            self.jump = True

    def update_animation(self):
        current_time = pygame.time.get_ticks()

        if self.is_hitting:
            HIT_ANIMATION_INTERVAL = 200  # Увеличен интервал для замедления удара
            if current_time - self.last_hit_update > HIT_ANIMATION_INTERVAL:
                self.last_hit_update = current_time
                self.hit_image_index = (self.hit_image_index + 1) % len(self.hit_images)
                self.image = self.hit_images[self.hit_image_index]
                if self.hit_image_index == 0:  # После окончания анимации удара возвращаемся к idle
                    self.is_hitting = False
                    self.direction = "idle"
        elif self.is_moving:
            ANIMATION_INTERVAL = 100
            if current_time - self.last_move_update > ANIMATION_INTERVAL:
                self.last_move_update = current_time
                if self.direction == "left":
                    self.move_images = left_move_images
                elif self.direction == "right":
                    self.move_images = right_move_images

                self.move_image_index = (self.move_image_index + 1) % len(self.move_images)
                self.image = self.move_images[self.move_image_index]
        else:
            IDLE_ANIMATION_INTERVAL = 400
            if current_time - self.last_idle_update > IDLE_ANIMATION_INTERVAL:
                self.last_idle_update = current_time
                if self.direction == "left":
                    self.idle_images = left_idle_images
                elif self.direction == "right":
                    self.idle_images = right_idle_images

                self.idle_image_index = (self.idle_image_index + 1) % len(self.idle_images)
                self.image = self.idle_images[self.idle_image_index]

# Класс для платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Используем прозрачность
        self.image.fill((0, 0, 0, 0))  # Платформа прозрачная
        self.rect = self.image.get_rect(topleft=(x, y))
PLATFORM_HEIGHT = 35  # Измените это значение в зависимости от толщины зеленой полосы


# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

character = Character()
all_sprites.add(character)

# Создание платформы
platform = Platform(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, SCREEN_WIDTH, PLATFORM_HEIGHT)
all_sprites.add(platform)
platforms.add(platform)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Прыжок на стрелку вверх
                character.jump_start()

    # Отображение заднего фона
    screen.blit(background_img, (0, 0))

    all_sprites.update()
    character.update_animation()
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
