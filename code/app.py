import pygame, json
from random import *

with open("code/listeDechet.json", "r") as f:
    data = json.load(f)

# Initialisation
pygame.init()
WIDTH, HEIGHT = 1800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plan de Déchetterie")
clock = pygame.time.Clock()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
JAUNE = (255, 255, 0)   # plastique
GRIS = (128, 128, 128)  # zone de sol
BEIGE = (245, 245, 220)
BLEU = (0, 0, 153)
VOITURE_COLOR = (255,0,255)

# Dimensions et rotation des bennes
benne_width, benne_height = 120, 50
angles_bennes = -15

# Positions et noms des bennes
positions_bennes = [(20 + i*160, 760) for i in range(10)]
nomsBenne = ["Encombrants","Bois","Mobilier","Bois Rond","Gravats",
             "Placo","Non Incinérable","Carton","Végétaux","Végétaux"]

# Textes et positions
texte = ["ENTREE","Loge","Emmaus","DDS","Salle de repos","SORTIE",
         "Pneu","Bidons","Huile","Pile/Ampoule/Néon","Jouets","Verre","Papier"]
pos_texte = [[50,450],[25,330],[350,330],[500,330],[700,330],[WIDTH-50,450],
             [1350,460],[880,310],[950,310],[1050,310],[1180,310],[WIDTH-80,310],[WIDTH-80,340],]

# Créer des surfaces et rects pour les bennes
bennes = []
for i, (x, y) in enumerate(positions_bennes):
    benne_surf = pygame.Surface((benne_width, benne_height), pygame.SRCALPHA)
    benne_surf.fill(JAUNE)
    benne_tournee = pygame.transform.rotate(benne_surf, angles_bennes)
    rect = benne_tournee.get_rect(center=(x + benne_width//2, y + benne_height//2))
    bennes.append({"rect": rect, "nom": nomsBenne[i], "surf": benne_tournee})

# Conteneurs noirs
conteneurs_noirs = [
    {"rect": pygame.Rect(880-20, 320, 40, 10), "nom": "Bidons"},
    {"rect": pygame.Rect(950-20, 320, 40, 10), "nom": "Huile"},
    {"rect": pygame.Rect(1050-20, 320, 40, 10), "nom": "Pile/Ampoule/Néon"},
    {"rect": pygame.Rect(1180-20, 320, 40, 10), "nom": "Jouets"},
    {"rect": pygame.Rect(1350-20, 470, 40, 10), "nom": "Pneu"},
    {"rect": pygame.Rect(1280, 350, 10, 80), "nom": "Articles De Sport"},
    {"rect": pygame.Rect(WIDTH-100, 320, 40, 10), "nom": "Verre"},
    {"rect": pygame.Rect(WIDTH-100, 350, 40, 10), "nom": "Papier"},
]

# Bâtiments cliquables
batiments_cliquables = [
    {"rect": pygame.Rect(350-40, 330-20, 80, 40), "nom": "Emmaus"},
    {"rect": pygame.Rect(500-40, 330-20, 80, 40), "nom": "DDS"}
]

# Voiture
voiture_width, voiture_height = 60, 30
voiture_x, voiture_y = 0, 520
voiture_vitesse = 2

# Texte bulle
texte_bulle = ""
for i in range(randint(1,4)):
    categorie = choice(list(data["dechets"].keys()))  # clé au hasard
    choix = choice(data["dechets"][categorie])  
    if choix not in texte_bulle:
        texte_bulle += choix + ", "

# Préparer les mots pour drag
font_bulle = pygame.font.SysFont(None, 20)
mots_bulle = [mot.strip() for mot in texte_bulle.split(",") if mot.strip() != ""]
mots_rects = []

# Drag variables
dragging_mot = None
offset_x_mot, offset_y_mot = 0, 0

running = True
while running:
    screen.fill(BLANC)
    font = pygame.font.SysFont(None, 20)

    # Dessiner le sol et zones
    pygame.draw.rect(screen, GRIS, (0, 300, WIDTH, 550))
    pygame.draw.rect(screen, NOIR, (0, 500, WIDTH, 200))
    pygame.draw.rect(screen, BLANC, (0, 590, WIDTH, 20))
    pygame.draw.rect(screen, BEIGE, (0, 310, 50, 50))
    pygame.draw.rect(screen, BEIGE, (300, 310, 550, 80))
    pygame.draw.rect(screen, BLEU, (1300, 400, 120, 50))
    pygame.draw.rect(screen, BLEU, (1500, 400, 120, 50))
    pygame.draw.rect(screen, BLEU, (1300, 300, 50, 100))
    pygame.draw.rect(screen, BLEU, (1570, 300, 50, 100))

    # Conteneurs noirs
    for conteneur in conteneurs_noirs:
        pygame.draw.rect(screen, NOIR, conteneur["rect"])

    # Textes
    for i in range(len(texte)):
        text_surface = font.render(texte[i], True, NOIR)
        text_rect = text_surface.get_rect(center=(pos_texte[i][0], pos_texte[i][1]))
        screen.blit(text_surface, text_rect)

    # Texte vertical
    texte2 = "Article de sport"
    text_surface = font.render(texte2, True, NOIR)
    text_rotated = pygame.transform.rotate(text_surface, -90)
    rect_rotated = text_rotated.get_rect(center=(1270, 390))
    screen.blit(text_rotated, rect_rotated)

    # Bennes
    for benne in bennes:
        screen.blit(benne["surf"], benne["rect"])
        text_rect = font.render(benne["nom"], True, NOIR).get_rect(center=(benne["rect"].centerx, benne["rect"].top - 20))
        screen.blit(font.render(benne["nom"], True, NOIR), text_rect)

    # Bâtiments cliquables (optionnel)
    for batiment in batiments_cliquables:
        pygame.draw.rect(screen, BEIGE, batiment["rect"], 2)

    # Déplacement voiture
    if voiture_x < WIDTH/4:
        voiture_x += voiture_vitesse
    pygame.draw.rect(screen, VOITURE_COLOR, (voiture_x, voiture_y, voiture_width, voiture_height))

    # Bulle et mots draggable
    if voiture_x >= WIDTH/4:
        bulle_width, bulle_height = 200, max(80, len(mots_bulle)*25)
        bulle_x = voiture_x + voiture_width + 10
        bulle_y = voiture_y - 20
        pygame.draw.rect(screen, BLANC, (bulle_x, bulle_y, bulle_width, bulle_height), border_radius=10)
        pygame.draw.rect(screen, NOIR, (bulle_x, bulle_y, bulle_width, bulle_height), 2, border_radius=10)

        # Initialiser les mots s'ils n'ont pas encore de rects
        if not mots_rects:
            for j, mot in enumerate(mots_bulle):
                text_surface = font_bulle.render(mot, True, NOIR)
                text_rect = text_surface.get_rect(topleft=(bulle_x + 10, bulle_y + 10 + j*25))
                mots_rects.append({"mot": mot, "rect": text_rect, "surface": text_surface})

        # Afficher les mots
        for mot in mots_rects:
            screen.blit(mot["surface"], mot["rect"])

    # Gestion événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # Cliquer sur mots draggable
            for mot in mots_rects:
                if mot["rect"].collidepoint(pos):
                    dragging_mot = mot
                    offset_x_mot = mot["rect"].x - pos[0]
                    offset_y_mot = mot["rect"].y - pos[1]
                    break
            # Cliquer sur bennes
            for benne in bennes:
                if benne["rect"].collidepoint(pos):
                    print(f"Clic sur la benne {benne['nom']} !")
            # Cliquer sur conteneurs noirs
            for conteneur in conteneurs_noirs:
                if conteneur["rect"].collidepoint(pos):
                    print(f"Clic sur {conteneur['nom']} !")
            # Cliquer sur bâtiments
            for batiment in batiments_cliquables:
                if batiment["rect"].collidepoint(pos):
                    print(f"Clic sur le bâtiment {batiment['nom']} !")

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging_mot = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging_mot:
                dragging_mot["rect"].x = event.pos[0] + offset_x_mot
                dragging_mot["rect"].y = event.pos[1] + offset_y_mot

    pygame.display.flip()
    clock.tick(60)

pygame.quit()