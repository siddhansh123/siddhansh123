import pygame, random, sys


pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⚔️ Dungeon Wars ⚔️")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


WHITE = (255, 255, 255)
RED   = (220, 20, 60)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)


bg = pygame.Surface((WIDTH, HEIGHT))
bg.fill((25, 25, 45))

# add images
player_img = pygame.Surface((120, 120), pygame.SRCALPHA)
enemy_img  = pygame.Surface((120, 120), pygame.SRCALPHA)
pygame.draw.circle(player_img, (0,150,255), (60,60), 55)
pygame.draw.circle(enemy_img, (255,60,60), (60,60), 55)

# --- Game Stats ---
player_hp = 100
enemy_hp  = 100
actions = ["attack", "defend", "heal"]
message = "Battle Start!"

# --- Button Setup ---
class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 150, 50)
    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect, border_radius=10)
        t = font.render(self.text, True, BLACK)
        screen.blit(t, (self.rect.centerx - t.get_width()/2, self.rect.centery - t.get_height()/2))
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

attack_btn = Button("⚔️ Attack", 150, 400)
defend_btn = Button("🛡️ Defend", 330, 400)
heal_btn   = Button("💖 Heal",   510, 400)

# --- Functions ---
def draw_health_bar(x, y, hp, max_hp):
    ratio = max(hp, 0) / max_hp
    pygame.draw.rect(screen, WHITE, (x-2, y-2, 204, 24), 2)
    pygame.draw.rect(screen, RED, (x, y, 200, 20))
    pygame.draw.rect(screen, GREEN, (x, y, 200 * ratio, 20))

def draw_scene():
    screen.blit(bg, (0, 0))
    screen.blit(player_img, (150, 200))
    screen.blit(enemy_img, (530, 200))
    draw_health_bar(150, 150, player_hp, 100)
    draw_health_bar(530, 150, enemy_hp, 100)
    t1 = font.render(f"You: {player_hp}", True, WHITE)
    t2 = font.render(f"Enemy: {enemy_hp}", True, WHITE)
    screen.blit(t1, (150, 120))
    screen.blit(t2, (530, 120))
    m = font.render(message, True, YELLOW)
    screen.blit(m, (WIDTH/2 - m.get_width()/2, 80))
    attack_btn.draw()
    defend_btn.draw()
    heal_btn.draw()

def battle_turn(player_action):
    global player_hp, enemy_hp, message
    enemy_action = random.choice(actions)
    message = f"You {player_action}, enemy {enemy_action}."

    if player_action == "attack":
        if enemy_action == "attack":
            p_dmg = random.randint(7, 25)
            e_dmg = random.randint(7, 25)
            player_hp -= e_dmg
            enemy_hp  -= p_dmg
            message = f"Both attack! You -{e_dmg}, Enemy -{p_dmg}"
        elif enemy_action == "defend":
            message = "Enemy blocked your attack!"
        else:
            dmg = random.randint(7, 25)
            enemy_hp -= dmg
            message = f"Enemy tried to heal! You dealt {dmg}"
    elif player_action == "defend":
        if enemy_action == "attack":
            message = "You blocked the enemy attack!"
        elif enemy_action == "heal":
            enemy_hp = min(100, enemy_hp + 10)
            message = "Enemy healed 10 HP!"
        else:
            message = "Both defended."
    elif player_action == "heal":
        player_hp = min(100, player_hp + 10)
        message = "You healed 10 HP."
        if enemy_action == "attack":
            dmg = random.randint(7, 25)
            player_hp -= dmg
            message += f" Enemy hit you for {dmg}!"

# --- Main Loop ---
running = True
while running:
    screen.fill(BLACK)
    draw_scene()
    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if attack_btn.is_clicked(pos):
                battle_turn("attack")
            elif defend_btn.is_clicked(pos):
                battle_turn("defend")
            elif heal_btn.is_clicked(pos):
                battle_turn("heal")

    if player_hp <= 0 or enemy_hp <= 0:
        screen.fill(BLACK)
        msg = "🏆 You Won!" if enemy_hp <= 0 else "💀 You Died!"
        text = font.render(msg, True, YELLOW)
        screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()
