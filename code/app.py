
"""
1) fin du jeu : faire en sorte que les dechets soient jetés dans les bonnes bennes, et que le joueur puisse cliquer sur les bennes pour voir les dechets qui s'y trouvent
2) rajouter les personnages qui peuvent aider a jeter les dechets dans les bonnes bennes (ex: un employé de la déchetterie,)
3) rajouter un systeme d'aide pour faire en sorte que si le joueur a besoin d'aide il clique sur la salle de repos pour faire apparaitre un agent du tri et avoir des conseils
4) rajouter un systeme de score pour faire en sorte que le joueur puisse gagner des points en jetant les dechets dans les bonnes bennes, et perdre des points en jetant les dechets dans les mauvaises bennes
5) rajouter des pieges (feraille,amiante, etc) pour faire en sorte que le joueur puisse perdre des points si il jette les dechets dans les bennes.
"""
import pygame, json
from random import *

# Récupérer les déchets dans le fichier JSON
with open("code/listeDechet.json", "r") as f:
    data = json.load(f)

# Initialisation Pygame + correction scaling Windows
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h-60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Résolution logique
WIDTH, HEIGHT = 1800, 1000
surface = pygame.Surface((WIDTH, HEIGHT))

pygame.display.set_caption("Déchet Simulator")
clock = pygame.time.Clock()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
JAUNE = (255, 255, 0)
GRIS = (128, 128, 128)
BEIGE = (245, 245, 220)
BLEU = (0, 0, 153)
VOITURE_COLOR = (255,0,255)
VERT = (0, 200, 0)
ROUGE = (255, 0, 0)

# Score
Score_joueur = 0

# Dimensions et rotation bennes
benne_width, benne_height = 120, 50
angles_bennes = -15

# Positions et noms des bennes
positions_bennes = [(20 + i*160, 760) for i in range(10)]
nomsBenne = list(data["dechets"].keys())[:10]

# Textes et positions
texte = ["ENTREE","Loge","Emmaus","DDS","Salle de repos","SORTIE",
         "Pneu","Bidons","Huile","Pile/Ampoule/Neon","Jouets","Verre","Papier"]
pos_texte = [[50,450],[25,330],[350,330],[500,330],[700,330],[WIDTH-50,450],
             [1350,460],[880,310],[950,310],[1050,310],[1180,310],[WIDTH-80,310],[WIDTH-80,340]]

# Créer surfaces et rects bennes
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
    {"rect": pygame.Rect(1280, 350, 10, 80), "nom": "Article de Sport"},
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

# Préparer mots draggables
font_bulle = pygame.font.SysFont(None, 20)
mots_rects = []
for i in range(randint(2,4)):
    categorie = choice(list(data["dechets"].keys()))
    objet = choice(data["dechets"][categorie])
    mots_rects.append({
        "mot": objet,
        "categorie": categorie,
        "rect": None,
        "surface": None,
        "couleur": NOIR,
        "placed": False
    })

# Drag variables
dragging_mot = None
offset_x_mot, offset_y_mot = 0, 0

# Début jeu
running = True
while running:
    surface.fill(BLANC)
    font = pygame.font.SysFont(None, 20)

    # Sol et zones
    pygame.draw.rect(surface, GRIS, (0, 300, WIDTH, 550))
    pygame.draw.rect(surface, NOIR, (0, 500, WIDTH, 200))
    pygame.draw.rect(surface, BLANC, (0, 590, WIDTH, 20))
    pygame.draw.rect(surface, BEIGE, (0, 310, 50, 50))
    pygame.draw.rect(surface, BEIGE, (300, 310, 550, 80))
    pygame.draw.rect(surface, BLEU, (1300, 400, 120, 50))
    pygame.draw.rect(surface, BLEU, (1500, 400, 120, 50))
    pygame.draw.rect(surface, BLEU, (1300, 300, 50, 100))
    pygame.draw.rect(surface, BLEU, (1570, 300, 50, 100))

    # Conteneurs noirs
    for conteneur in conteneurs_noirs:
        pygame.draw.rect(surface, NOIR, conteneur["rect"])

    # Textes
    for i in range(len(texte)):
        text_surface = font.render(texte[i], True, NOIR)
        text_rect = text_surface.get_rect(center=(pos_texte[i][0], pos_texte[i][1]))
        surface.blit(text_surface, text_rect)

    # Texte vertical
    texte2 = "Article de sport"
    text_surface = font.render(texte2, True, NOIR)
    text_rotated = pygame.transform.rotate(text_surface, -90)
    rect_rotated = text_rotated.get_rect(center=(1270, 390))
    surface.blit(text_rotated, rect_rotated)

    # Bennes
    for benne in bennes:
        surface.blit(benne["surf"], benne["rect"])
        text_rect = font.render(benne["nom"], True, NOIR).get_rect(center=(benne["rect"].centerx, benne["rect"].top - 20))
        surface.blit(font.render(benne["nom"], True, NOIR), text_rect)

    # Bâtiments cliquables
    for batiment in batiments_cliquables:
        pygame.draw.rect(surface, BEIGE, batiment["rect"], 2)

    # Déplacement voiture
    if voiture_x < WIDTH/4:
        voiture_x += voiture_vitesse
    pygame.draw.rect(surface, VOITURE_COLOR, (voiture_x, voiture_y, voiture_width, voiture_height))

    # Bulle et mots draggable
    if voiture_x >= WIDTH/4:
        bulle_width, bulle_height = 200, max(80, len(mots_rects)*25)
        bulle_x = voiture_x + voiture_width + 10
        bulle_y = voiture_y - 20
        pygame.draw.rect(surface, BLANC, (bulle_x, bulle_y, bulle_width, bulle_height), border_radius=10)
        pygame.draw.rect(surface, NOIR, (bulle_x, bulle_y, bulle_width, bulle_height), 2, border_radius=10)

        # Initialiser mots
        for j, mot in enumerate(mots_rects):
            if mot["rect"] is None:
                mot["surface"] = font_bulle.render(mot["mot"], True, mot["couleur"])
                mot["rect"] = mot["surface"].get_rect(topleft=(bulle_x + 10, bulle_y + 10 + j*25))
            mot["surface"] = font_bulle.render(mot["mot"], True, mot["couleur"])
            surface.blit(mot["surface"], mot["rect"])

    # Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Drag start
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            scale_x = WIDTH / SCREEN_WIDTH
            scale_y = HEIGHT / SCREEN_HEIGHT
            pos = (event.pos[0] * scale_x, event.pos[1] * scale_y)
            for mot in mots_rects:
                if not mot["placed"] and mot["rect"].collidepoint(pos):
                    dragging_mot = mot
                    offset_x_mot = mot["rect"].x - pos[0]
                    offset_y_mot = mot["rect"].y - pos[1]
                    break

        # Drag end
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if dragging_mot:
                placed = False

                # Bennes
                for benne in bennes:
                    if dragging_mot["rect"].colliderect(benne["rect"]):
                        if dragging_mot["categorie"] == benne["nom"]:
                            dragging_mot["couleur"] = VERT
                            dragging_mot["placed"] = True
                            Score_joueur += 1
                        else:
                            dragging_mot["couleur"] = ROUGE
                            Score_joueur -= 1
                        placed = True

                # Conteneurs noirs
                for conteneur in conteneurs_noirs:
                    if dragging_mot["rect"].colliderect(conteneur["rect"]):
                        if dragging_mot["categorie"] == conteneur["nom"]:
                            dragging_mot["couleur"] = VERT
                            dragging_mot["placed"] = True
                            Score_joueur += 1
                        else:
                            dragging_mot["couleur"] = ROUGE
                            Score_joueur -= 1
                        placed = True

                # Bâtiments (DDS, Emmaus)
                for batiment in batiments_cliquables:
                    if dragging_mot["rect"].colliderect(batiment["rect"]):
                        if dragging_mot["categorie"] == batiment["nom"]:
                            dragging_mot["couleur"] = VERT
                            dragging_mot["placed"] = True
                            Score_joueur += 1
                        else:
                            dragging_mot["couleur"] = ROUGE
                            Score_joueur -= 1
                        placed = True

            dragging_mot = None

        # Drag motion
        elif event.type == pygame.MOUSEMOTION and dragging_mot and not dragging_mot["placed"]:
            pos = (event.pos[0] * scale_x, event.pos[1] * scale_y)
            dragging_mot["rect"].x = pos[0] + offset_x_mot
            dragging_mot["rect"].y = pos[1] + offset_y_mot

    # Affichage score
    score_surf = font.render(f"Score : {Score_joueur}", True, NOIR)
    surface.blit(score_surf, (50, 50))

    # Affichage final
    scaled_surface = pygame.transform.scale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()