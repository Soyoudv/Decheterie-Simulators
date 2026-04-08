import pygame, json, ctypes, platform
from pagedemarrage import ecran_demarrage
from pageFin import page_fin
from pause import menu_pause
from random import *

# --- Récupérer les déchets ---
with open("code/listeDechet.json", "r") as f:
    data = json.load(f)

# --- Initialisation Pygame + scaling Windows ---

if (platform.system() == "Windows"):
    ctypes.windll.user32.SetProcessDPIAware()

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h-60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# --- Résolution logique ---
WIDTH, HEIGHT = 1800, 1000
surface = pygame.Surface((WIDTH, HEIGHT))

pygame.display.set_caption("Décheterie Simulateur")
clock = pygame.time.Clock()

# --- Image ---
image = pygame.image.load("image/Yannick.png").convert_alpha()
image= pygame.transform.scale(image, (50, 50))

# --- Logo carré ---
carre = pygame.image.load("image/LundiAgglo.png").convert()
carre= pygame.transform.scale(carre, (150, 150))
# --- Logo rond ---
rond = pygame.image.load("image/LundiAggloRond.png").convert()
rond= pygame.transform.scale(rond, (200, 200))

conteneurs = pygame.image.load("image/conteneur_maritime.png").convert_alpha()
conteneurs= pygame.transform.scale(conteneurs, (100, 100))

conteneurs90 = pygame.image.load("image/conteneur_maritime_sim_90.png").convert_alpha()
conteneurs90= pygame.transform.scale(conteneurs90, (100, 100))

# --- Gardien ---
#personnes = ["Audrey","SuperVégéto","Anguille","Gipsy","Herbi"]
personnages_aide = [
    {"nom": "Agent Tri", "x": 700, "y": 500, "visible": False}  # apparaît via la salle de repos
]
# --- Variables supplémentaire ---
texte_visible = False
compteur_aide = 0
dejaAider = False

compteur_dechet = 0

# --- Couleurs ---
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
JAUNE = (255, 255, 0)
GRIS = (128, 128, 128)
BEIGE = (245, 245, 220)
BLEU = (0, 0, 153)
VOITURE_COLOR = (255,0,255)
VERT = (0, 200, 0)
ROUGE = (255, 0, 0)
GRISCLAIR =(200, 200, 200)
ListeColVoiture = [BLANC, JAUNE, BEIGE, BLEU, VERT, ROUGE, VOITURE_COLOR]

# --- Score ---
Score_joueur = 0

# --- Bennes ---
benne_width, benne_height = 140, 60
angles_bennes = -15
positions_bennes = [(20 + i*160, 760) for i in range(10)]
nomsBenne = list(data["dechets"].keys())[:9]
nomsBenne.append("Vegetaux")

# Charger UNE image de benne (avant la boucle)
benne_img = pygame.image.load("image/benne.png").convert_alpha()
benne_img = pygame.transform.scale(benne_img, (benne_width, benne_height))

bennes = []
for i, (x, y) in enumerate(positions_bennes):
    # rotation de l'image
    benne_tournee = pygame.transform.rotate(benne_img, angles_bennes)

    # garder le centre correct
    rect = benne_tournee.get_rect(center=(x + benne_width//2, y + benne_height//2))

    bennes.append({
        "rect": rect,
        "nom": nomsBenne[i],
        "surf": benne_tournee
    })


# --- Conteneurs noirs ---
conteneurs_noirs = [
    {"rect": pygame.Rect(860, 320, 40, 10), "nom": "Bidons"},
    {"rect": pygame.Rect(960, 320, 40, 10), "nom": "Huile"},
    {"rect": pygame.Rect(1090, 320, 40, 10), "nom": "Pile/Ampoule/Neon"},
    {"rect": pygame.Rect(1220, 320, 40, 10), "nom": "Jouets"},
    {"rect": pygame.Rect(1330, 470, 40, 10), "nom": "Pneu"},
    {"rect": pygame.Rect(1280, 350, 10, 80), "nom": "Article de Sport"},
    {"rect": pygame.Rect(WIDTH-100, 320, 40, 10), "nom": "Verre"},
    {"rect": pygame.Rect(WIDTH-100, 350, 40, 10), "nom": "Papier"},
]

# --- Bâtiments cliquables ---
batiments_cliquables = [
    {"rect": pygame.Rect(310, 310, 80, 80), "nom": "Emmaus"},
    {"rect": pygame.Rect(460, 310, 80, 80), "nom": "DDS"},
    {"rect": pygame.Rect(700, 310, 80, 80), "nom": "Salle de repos"},

]
taille_voiture = 0
# --- Voiture ---
voiture_width, voiture_height = 60, 30
voiture_x, voiture_y = 0, 520
voiture_vitesse = 2
coleur = VOITURE_COLOR

# --- Mots draggables ---
font_bulle = pygame.font.SysFont(None, 20)
mots_rects = []


# Fonction pour couleur arc-en-ciel selon score
def couleur_arc_en_ciel(score, max_score):
    import math
    # score normalisé [0,1]
    t = min(score / max_score, 1)
    r = int(127 * (math.sin(2*math.pi*t) + 1))
    g = int(127 * (math.sin(2*math.pi*t + 2) + 1))
    b = int(127 * (math.sin(2*math.pi*t + 4) + 1))
    return (r, g, b)

def trouver_categorie(objet, data):
    for categorie, objets in data["dechets"].items():
        if objet in objets:
            return categorie
    return None

def nouvelle_voiture():
    """Réinitialise la voiture et génère de nouveaux déchets"""
    global voiture_x, voiture_y, mots_rects, coleur
    voiture_x, voiture_y = 0, 520
    mots_rects = []
    coleur = choice(ListeColVoiture)
    for i in range(randint(2,4)):
        categorie = choice(list(data["dechets"].keys()))
        objet = choice(data["dechets"][categorie])
        surface_mot = font_bulle.render(objet, True, NOIR)
        rect_mot = surface_mot.get_rect(topleft=(0,0))  # initialisation
        mots_rects.append({
            "mot": objet,
            "categorie": categorie,
            "rect": rect_mot,
            "surface": surface_mot,
            "couleur": NOIR,
            "placed": False
        })

nouvelle_voiture()

# --- Drag variables ---
dragging_mot = None
offset_x_mot, offset_y_mot = 0, 0

# --- Paramètres barre ---
barre_x, barre_y = WIDTH//2-200, 100
barre_width, barre_height = 400, 30

# --- Jeu ---
score_max = ecran_demarrage(surface, 1800, 1000, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock)
running = True
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        menu_pause(surface, 1800, 1000, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock)
    surface.fill(BLANC)
    taille_voiture = len(mots_rects)


    font = pygame.font.SysFont(None, 20)

    # --- Déplacement voiture ---
    # Déplacement voiture
    if any(not mot["placed"] for mot in mots_rects):
        # Si au quart de l'écran, s'arrête
        if voiture_x < WIDTH/4:
            voiture_x += voiture_vitesse
            voiture_arretée = False
        else:
            voiture_arretée = True
    else:
        # Voiture reprend son mouvement si tous les mots sont placés
        voiture_arretée = False
        if voiture_x < WIDTH:
            voiture_x += 6
            texte_visible = False
        else:
            dejaAider = False
            
            nouvelle_voiture()

    # --- Sol et zones ---
    pygame.draw.rect(surface, GRISCLAIR, (0, 300, WIDTH, 550))
    pygame.draw.rect(surface, GRIS, (0, 500, WIDTH, 200))
    pygame.draw.rect(surface, BLANC, (0, 590, WIDTH, 20))
    pygame.draw.rect(surface, BEIGE, (0, 310, 50, 50))
    pygame.draw.rect(surface, BEIGE, (300, 310, 500, 80))
    surface.blit(carre, (160,60))
    surface.blit(conteneurs, (1299,375))
    surface.blit(conteneurs, (1490,375))
    surface.blit(conteneurs90, (1275,300))
    surface.blit(conteneurs90, (1516,300))

    # --- Conteneurs noirs ---
    for conteneur in conteneurs_noirs:
        pygame.draw.rect(surface, NOIR, conteneur["rect"])

    # --- Textes ---
    texte = ["ENTREE","Loge","Emmaus","DDS","Salle de repos","SORTIE","Pneu","Bidons","Huile","Pile/Ampoule/Neon","Jouets","Verre","Papier"]
    pos_texte = [[50,450],[25,330],[350,330],[500,330],[700,330],[WIDTH-50,450],[1350,460],[880,310],[980,310],[1110,310],[1240,310],[WIDTH-80,310],[WIDTH-80,340]]
    for i in range(len(texte)):
        text_surface = font.render(texte[i], True, NOIR)
        text_rect = text_surface.get_rect(center=(pos_texte[i][0], pos_texte[i][1]))
        surface.blit(text_surface, text_rect)
    texte2 = "Article de sport"
    text_surface = font.render(texte2, True, NOIR)
    text_rotated = pygame.transform.rotate(text_surface, -90)
    rect_rotated = text_rotated.get_rect(center=(1270, 390))
    surface.blit(text_rotated, rect_rotated)

    # --- Bennes ---
    for benne in bennes:
        surface.blit(benne["surf"], benne["rect"])
        text_rect = font.render(benne["nom"], True, NOIR).get_rect(center=(benne["rect"].centerx, benne["rect"].top - 20))
        surface.blit(font.render(benne["nom"], True, NOIR), text_rect)
    # --- Bâtiments cliquables ---
    for batiment in batiments_cliquables:
        pygame.draw.rect(surface, BEIGE, batiment["rect"], 2)

    # --- Voiture ---
    pygame.draw.rect(surface, coleur, (voiture_x, voiture_y, voiture_width, voiture_height))
    for p in personnages_aide:
        if p["nom"] == "Agent Tri" and p["visible"] and texte_visible:
            surface.blit(image, (p["x"] -20, p["y"]-50))
            advice = "Ah je vois que vous avez besoin d'aide !!!!\n"
            if "dernier_objet" in p:
                advice += f"{p['dernier_objet']}"
                benne_aide = trouver_categorie(p['dernier_objet'],data)
                advice += " va dans " + benne_aide
                compteur_aide +=1
            pygame.draw.rect(surface, BLANC, (p["x"] + 30, p["y"] - 40, 350, 60))
            pygame.draw.rect(surface, NOIR, (p["x"] + 30, p["y"] - 40, 350, 60), 2)
            # Affichage ligne par ligne
            lines = advice.split("\n")
            for i, line in enumerate(lines):
                surface.blit(font.render(line, True, NOIR), (p["x"] + 35, p["y"] - 35 + i*20))
            
    # --- Bulle et mots draggables ---
    if voiture_arretée and any(not mot["placed"] for mot in mots_rects):
        bulle_width, bulle_height = 200, max(80, len(mots_rects)*25)
        bulle_x = voiture_x + voiture_width + 10
        bulle_y = voiture_y - 20
        pygame.draw.rect(surface, BLANC, (bulle_x, bulle_y, bulle_width, bulle_height), border_radius=10)
        pygame.draw.rect(surface, NOIR, (bulle_x, bulle_y, bulle_width, bulle_height), 2, border_radius=10)

        for j, mot in enumerate(mots_rects):
            # ⚡ Position initiale seulement si jamais définie
            if mot["rect"].topleft == (0,0):
                mot["rect"].topleft = (bulle_x + 10, bulle_y + 10 + j*25)
            # Mettre à jour la couleur si changée
            mot["surface"] = font_bulle.render(mot["mot"], True, mot["couleur"])
            surface.blit(mot["surface"], mot["rect"])

    # --- Événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Drag start
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            scale_x, scale_y = WIDTH / SCREEN_WIDTH, HEIGHT / SCREEN_HEIGHT
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
                salle_repos = pygame.Rect(700, 310, 80, 80)

                # --- SALLE DE REPOS ---
                if dragging_mot["rect"].colliderect(salle_repos):
                    if not dejaAider:
                        dragging_mot["couleur"] = BLEU
                        texte_visible = True
                        dejaAider = True

                        for p in personnages_aide:
                            if p["nom"] == "Agent Tri":
                                p["dernier_objet"] = dragging_mot["mot"]
                                p["visible"] = True

                    dragging_mot = None
                    continue

                # --- Bennes ---
                for cible in bennes + conteneurs_noirs + batiments_cliquables:
                    if dragging_mot["rect"].colliderect(cible["rect"]):

                        if dragging_mot["categorie"] == cible["nom"]:
                            dragging_mot["couleur"] = VERT
                            dragging_mot["placed"] = True
                            Score_joueur += 1
                            compteur_dechet +=1
                            texte_visible = False
                            
                            
                        else:
                            dragging_mot["couleur"] = ROUGE
                            dragging_mot["placed"] = True
                            compteur_dechet +=1
                            

                        break

                dragging_mot = None
    
        # Drag motion
        elif event.type == pygame.MOUSEMOTION and dragging_mot and not dragging_mot["placed"]:
            pos = (event.pos[0] * scale_x, event.pos[1] * scale_y)
            dragging_mot["rect"].x = pos[0] + offset_x_mot
            dragging_mot["rect"].y = pos[1] + offset_y_mot
    if Score_joueur >= score_max:
        action_fin = page_fin(surface, 1800, 1000, Score_joueur, compteur_dechet, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock)
        if action_fin == "replay":
            Score_joueur = 0
            nouvelle_voiture()
            # éventuellement relancer l'écran de démarrage pour choisir la difficulté
            score_max = ecran_demarrage(surface, WIDTH, HEIGHT)

    # --- Affichage score ---
    # --- Barre de score ---
    pygame.draw.rect(surface, GRISCLAIR, (barre_x, barre_y, barre_width, barre_height))  # fond
    couleur_barre = couleur_arc_en_ciel(Score_joueur, score_max)
    pygame.draw.rect(surface, couleur_barre, (barre_x, barre_y, min(Score_joueur/score_max * barre_width, barre_width), barre_height))
    pygame.draw.rect(surface, NOIR, (barre_x, barre_y, barre_width, barre_height), 3)
    score_surf = font.render(f"Score : {Score_joueur}", True, NOIR)
    surface.blit(score_surf, (WIDTH//2 -10, 150))
    font2 = pygame.font.Font(None, 50)
    score2_surf = font2.render("Bienvenue dans la decheterie de Telleville géré par Lundi Agglo", True, NOIR)
    surface.blit(score2_surf, (WIDTH//2 - score2_surf.get_width()//2, 50))
    # --- Affichage final ---
    scaled_surface = pygame.transform.scale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()