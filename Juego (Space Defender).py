import pygame
import random
import sys

# Configuración
pygame.init()
WIDTH, HEIGHT = 900, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Defender: Ultra Strike")
CLOCK = pygame.time.Clock()

# Estilo de la imagen
BG_DARK = (5, 5, 15)
WHITE = (240, 240, 240)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
RED = (255, 60, 60)
GOLD = (255, 215, 0)
PANEL_COLOR = (20, 30, 60, 180)

# Fuentes
FONT_L = pygame.font.SysFont("consolas", 50, bold=True)
FONT_M = pygame.font.SysFont("consolas", 25, bold=True)
FONT_S = pygame.font.SysFont("consolas", 18)

# Clases

class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.life = 25
        self.color = color
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
    def draw(self):
        if self.life > 0:
            pygame.draw.rect(SCREEN, self.color, (self.x, self.y, 3, 3))

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2, HEIGHT-125, 40, 40)
        self.health = 3
        self.cooldown = 0
    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 40: self.rect.x -= 8
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH-40: self.rect.x += 8
        if self.cooldown > 0: self.cooldown -= 1
    def draw(self):
        # Dibujo de la nave
        pygame.draw.polygon(SCREEN, CYAN, [(self.rect.centerx, self.rect.top), (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom)])
        pygame.draw.polygon(SCREEN, WHITE, [(self.rect.centerx, self.rect.top+5), (self.rect.left+5, self.rect.bottom-2), (self.rect.right-5, self.rect.bottom-2)], 2)

class Enemy:
    def __init__(self, level):
        self.x = random.randint(50, WIDTH-50)
        self.y = -50
        # Probabilidades según el nivel
        prob = random.random()
        if prob > 0.9 and level > 2: # El Tanque solo aparece desde nivel 3
            self.type, self.color, self.speed, self.hp, self.size = "TANK", MAGENTA, 1.5, 3, 35
        elif prob > 0.7 and level > 1: # El Rápido aparece desde nivel 2
            self.type, self.color, self.speed, self.hp, self.size = "FAST", GOLD, 5 + (level * 0.5), 1, 15
        else:
            # Enemigo básico: velocidad inicial lenta (2.0)
            self.type, self.color, self.speed, self.hp, self.size = "BASIC", RED, 2.0 + (level * 0.3), 1, 25
            
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    def update(self): self.rect.y += self.speed
    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect, border_radius=4)
        pygame.draw.rect(SCREEN, WHITE, self.rect, 1, border_radius=4)

# Funciones de Interfaz

def draw_glass_panel(rect, border_color=CYAN):
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(s, PANEL_COLOR, (0, 0, rect[2], rect[3]), border_radius=15)
    SCREEN.blit(s, (rect[0], rect[1]))
    pygame.draw.rect(SCREEN, border_color, rect, 2, border_radius=15)

def draw_text(text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x, y)) if center else img.get_rect(topleft=(x, y))
    SCREEN.blit(img, rect)

# Menús

def show_game_over(score, level, kills):
    while True:
        draw_glass_panel((WIDTH//2 - 200, HEIGHT//2 - 150, 400, 320), RED)
        draw_text("MISSION FAILED", FONT_L, RED, WIDTH//2, HEIGHT//2 - 100, True)
        draw_text(f"PUNTUACIÓN: {score}", FONT_M, WHITE, WIDTH//2, HEIGHT//2 - 30, True)
        draw_text(f"NIVEL: {level} | KILLS: {kills}", FONT_S, CYAN, WIDTH//2, HEIGHT//2 + 10, True)
        
        btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 60, 200, 50)
        pygame.draw.rect(SCREEN, CYAN, btn, border_radius=10)
        draw_text("REINTENTAR", FONT_M, BG_DARK, WIDTH//2, HEIGHT//2 + 85, True)

        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(e.pos): return

# Bucle Principal

def game():
    player = Player()
    enemies, bullets, particles = [], [], []
    score, kills, level, spawn_timer = 0, 0, 1, 0
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(70)]

    while True:
        SCREEN.fill(BG_DARK)
        for s in stars: pygame.draw.circle(SCREEN, (50, 50, 80), s, 1)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and player.cooldown == 0:
                bullets.append(pygame.Rect(player.rect.centerx-2, player.rect.top, 4, 15))
                player.cooldown = 15

        # Lógica
        player.move()
        
        # Generación de Enemigos: Comienza lento (cada 50 frames) y baja hasta un min de 15
        spawn_rate = max(50 - (level * 3), 15)
        spawn_timer += 1
        if spawn_timer > spawn_rate:
            enemies.append(Enemy(level))
            spawn_timer = 0

        # Actualizar proyectiles
        for b in bullets[:]:
            b.y -= 12
            if b.y < 0: bullets.remove(b)

        # Actualizar enemigos y colisiones
        for en in enemies[:]:
            en.update()
            if en.rect.top > HEIGHT:
                enemies.remove(en)
                player.health -= 1
            elif en.rect.colliderect(player.rect):
                enemies.remove(en)
                player.health -= 1

            for b in bullets[:]:
                if en.rect.colliderect(b):
                    en.hp -= 1
                    if b in bullets: bullets.remove(b)
                    if en.hp <= 0:
                        for _ in range(10): particles.append(Particle(en.rect.centerx, en.rect.centery, en.color))
                        score += 50 if en.type == "TANK" else 15 if en.type == "FAST" else 10
                        kills += 1
                        if kills % 8 == 0: level += 1 # Sube de nivel cada 8 kills
                        enemies.remove(en)
                    break

        for p in particles[:]:
            p.update()
            if p.life <= 0: particles.remove(p)

        # Dibujo
        for p in particles: p.draw()
        for b in bullets: pygame.draw.rect(SCREEN, CYAN, b)
        for en in enemies: en.draw()
        player.draw()

        # Panel de Información
        draw_glass_panel((20, HEIGHT - 75, WIDTH - 40, 60))
        draw_text(f"PUNTOS: {score}", FONT_S, WHITE, 50, HEIGHT - 55)
        draw_text(f"NIVEL: {level}", FONT_S, CYAN, 250, HEIGHT - 55)
        
        # Sección de Vidas
        draw_text("ESCUDOS:", FONT_S, WHITE, WIDTH - 200, HEIGHT - 55)
        for i in range(player.health):
            pygame.draw.circle(SCREEN, RED, (WIDTH - 100 + i*25, HEIGHT - 45), 8)

        pygame.display.flip()
        CLOCK.tick(60)

        if player.health <= 0:
            show_game_over(score, level, kills)
            return

def main_menu():
    while True:
        SCREEN.fill(BG_DARK)
        draw_glass_panel((WIDTH//2 - 250, 150, 500, 350))
        draw_text("SPACE DEFENDER", FONT_L, WHITE, WIDTH//2, 220, True)
        draw_text("¡DEFENSA GALÁCTICA!", FONT_M, CYAN, WIDTH//2, 280, True)
        
        btn = pygame.Rect(WIDTH//2 - 100, 380, 200, 60)
        pygame.draw.rect(SCREEN, CYAN, btn, border_radius=15)
        draw_text("INICIAR", FONT_M, BG_DARK, WIDTH//2, 410, True)

        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(e.pos): return

if __name__ == "__main__":
    while True:
        main_menu()
        game()