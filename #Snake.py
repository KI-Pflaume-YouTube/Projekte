#Snake
import pygame
import random

# Initialisierung von pygame
pygame.init()

# Farben definieren
SCHWARZ = (0, 0, 0)
GRÜN = (0, 255, 0)
ROT = (255, 0, 0)
WEISS = (255, 255, 255)

# Spielgrößen festlegen
BREITE_ZELLE = 20
ANZAHL_ZELLEN = 20
BREITE = BREITE_ZELLE * ANZAHL_ZELLEN
HÖHE = BREITE_ZELLE * ANZAHL_ZELLEN

# Fenster und Uhr erstellen
fenster = pygame.display.set_mode((BREITE, HÖHE))
pygame.display.set_caption("Snake Spiel")
uhr = pygame.time.Clock()

# Highscore initialisieren und laden
HIGHSCORE_DATEI = "highscore.txt"

def lade_highscores():
    try:
        with open(HIGHSCORE_DATEI, 'r') as f:
            return [int(line.strip()) for line in f.readlines()]
    except:
        return [0, 0, 0]

def speichere_highscore(score):
    scores = lade_highscores()
    scores.append(score)
    scores.sort(reverse=True)
    scores = scores[:3]
    with open(HIGHSCORE_DATEI, 'w') as f:
        for s in scores:
            f.write(str(s) + '\n')

# Töne
ESS_TON = pygame.mixer.Sound("C:/Users/Timo/Desktop/Snake/Swoosh.wav")
ENDE_TON = pygame.mixer.Sound("C:/Users/Timo/Desktop/Snake/Crash.wav")

class Snake:
    def __init__(self):
        self.länge = 3
        self.positionen = [(ANZAHL_ZELLEN // 2, ANZAHL_ZELLEN // 2)]
        self.richtung = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.neue_richtung = self.richtung
        self.score = 0
        self.paused = False

    def bewegen(self):
        if self.paused:
            return
        kopf_x, kopf_y = self.positionen[0]
        if self.neue_richtung == pygame.K_UP:
            self.positionen = [(kopf_x, kopf_y - 1)] + self.positionen[:-1]
        elif self.neue_richtung == pygame.K_DOWN:
            self.positionen = [(kopf_x, kopf_y + 1)] + self.positionen[:-1]
        elif self.neue_richtung == pygame.K_LEFT:
            self.positionen = [(kopf_x - 1, kopf_y)] + self.positionen[:-1]
        elif self.neue_richtung == pygame.K_RIGHT:
            self.positionen = [(kopf_x + 1, kopf_y)] + self.positionen[:-1]

        self.richtung = self.neue_richtung

    def wenden(self, richtung):
        if self.paused:
            return
        if richtung == pygame.K_UP and not self.richtung == pygame.K_DOWN:
            self.neue_richtung = pygame.K_UP
        if richtung == pygame.K_DOWN and not self.richtung == pygame.K_UP:
            self.neue_richtung = pygame.K_DOWN
        if richtung == pygame.K_LEFT and not self.richtung == pygame.K_RIGHT:
            self.neue_richtung = pygame.K_LEFT
        if richtung == pygame.K_RIGHT and not self.richtung == pygame.K_LEFT:
            self.neue_richtung = pygame.K_RIGHT

    def essen(self):
        pygame.mixer.Sound.play(ESS_TON)
        self.länge += 1
        self.positionen.append(self.positionen[-1])
        self.score += 1

    def kollision(self):
        kopf_x, kopf_y = self.positionen[0]
        return (kopf_x < 0 or kopf_x >= ANZAHL_ZELLEN or
                kopf_y < 0 or kopf_y >= ANZAHL_ZELLEN or
                (kopf_x, kopf_y) in self.positionen[1:])

    def zeichnen(self, fenster):
        for segment in self.positionen:
            pygame.draw.rect(fenster, GRÜN, (segment[0]*BREITE_ZELLE, segment[1]*BREITE_ZELLE, BREITE_ZELLE, BREITE_ZELLE))
            pygame.draw.rect(fenster, WEISS, (segment[0]*BREITE_ZELLE, segment[1]*BREITE_ZELLE, BREITE_ZELLE, BREITE_ZELLE), 1)

    def toggle_pause(self):
        self.paused = not self.paused

class Essen:
    def __init__(self, snake):
        self.position = (random.randint(0, ANZAHL_ZELLEN - 1), random.randint(0, ANZAHL_ZELLEN - 1))
        while self.position in snake.positionen:
            self.position = (random.randint(0, ANZAHL_ZELLEN - 1), random.randint(0, ANZAHL_ZELLEN - 1))

    def zeichnen(self, fenster):
        pygame.draw.rect(fenster, ROT, (self.position[0]*BREITE_ZELLE, self.position[1]*BREITE_ZELLE, BREITE_ZELLE, BREITE_ZELLE))

def zeige_punkte(score):
    font = pygame.font.SysFont(None, 36)
    punkte_text = font.render(f'Punkte: {score}', True, WEISS)
    fenster.blit(punkte_text, (BREITE // 2 - punkte_text.get_width() // 2, 5))

def zeige_highscores():
    highscores = lade_highscores()
    font = pygame.font.SysFont(None, 36)
    titel_text = font.render('Höchste Punktzahl', True, WEISS)
    fenster.blit(titel_text, (BREITE // 2 - titel_text.get_width() // 2, HÖHE // 2 - 40))
    
    for index, score in enumerate(highscores, 1):
        score_text = font.render(f'{index}. {score}', True, WEISS)
        fenster.blit(score_text, (BREITE // 2 - score_text.get_width() // 2, HÖHE // 2 - 40 + index * 30))

    pygame.display.flip()
    
    warten = True
    while warten:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                warten = False

def spiel_loop():
    snake = Snake()
    essen = Essen(snake)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    snake.toggle_pause()
                else:
                    snake.wenden(event.key)

        snake.bewegen()

        if snake.kollision():
            pygame.mixer.Sound.play(ENDE_TON)
            speichere_highscore(snake.score)
            zeige_highscores()
            return

        if snake.positionen[0] == essen.position:
            snake.essen()
            essen = Essen(snake)

        fenster.fill(SCHWARZ)
        snake.zeichnen(fenster)
        essen.zeichnen(fenster)
        zeige_punkte(snake.score)
        pygame.display.flip()
        uhr.tick(10)

spiel_loop()
