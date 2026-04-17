import pygame, json, ctypes, platform,os,sys
from pagedemarrage import ecran_demarrage
from pageFin import page_fin
from pause import menu_pause
from random import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")
    return os.path.join(base_path, relative_path)


# --- Récupérer les déchets ---
with open(resource_path("code/listeDechet.json"), "r", encoding="utf-8") as f:
    data = json.load(f)
# --- Initialisation Pygame + scaling Windows ---

if (platform.system() == "Windows"):
    ctypes.windll.user32.SetProcessDPIAware()

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h-60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# --- Résolution logique ---
WIDTH, HEIGHT = 1800, 1000
surface = pygame.Surface((WIDTH, HEIGHT))

pygame.display.set_caption("Décheterie Simulateur")
clock = pygame.time.Clock()

# --- Audio --- #
gameover = pygame.mixer.Sound(resource_path("audio/gameover.mp3"))

moteur = pygame.mixer.Sound(resource_path("audio/moteur.mp3"))
moteur.set_volume(0.5)# regler le soucis du bruit du moteur

bip = pygame.mixer.Sound(resource_path("audio/bipentree.mp3"))

correct = pygame.mixer.Sound(resource_path("audio/correct.mp3"))
correct.set_volume(0.4)

fond = pygame.mixer.Sound(resource_path("audio/fond.mp3"))
fond.set_volume(0.2)
fond.play(-1)

# --- Variables --- #

voiture_width, voiture_height = 120, 110
texte_visible = False
compteur_aide = 0
dejaAider = False
compteur_dechet = 0
Score_joueur = 0
# --- Couleurs ---
BLEUFONCE = (0, 0, 100)
VERTFONCE = (0, 100, 0)
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






# --- Image ---
image = pygame.image.load(resource_path("image/Agent/Yannick.png")).convert_alpha()
image= pygame.transform.scale(image, (50, 50))

voiture = pygame.image.load(resource_path("image/Voiture/voiture1.png")).convert_alpha()
voiture= pygame.transform.scale(voiture, (voiture_width, voiture_height))

voiture2 = pygame.image.load(resource_path("image/Voiture/voiture2.png")).convert_alpha()
voiture2= pygame.transform.scale(voiture2, (voiture_width, voiture_height))

voiture3 = pygame.image.load(resource_path("image/Voiture/voiture3.png")).convert_alpha()
voiture3= pygame.transform.scale(voiture3, (voiture_width, voiture_height))

"""
voiture4 = pygame.image.load(resource_path("image/Voiture/voiture4.png")).convert_alpha()
voiture4= pygame.transform.scale(voiture4, (voiture_width, voiture_height))

voiture5 = pygame.image.load(resource_path("image/Voiture/voiture5.png")).convert_alpha()
voiture5= pygame.transform.scale(voiture5, (voiture_width, voiture_height))

voiture6 = pygame.image.load(resource_path("image/Voiture/voiture6.png")).convert_alpha()
voiture6= pygame.transform.scale(voiture6, (voiture_width, voiture_height))

voiture7 = pygame.image.load(resource_path("image/Voiture/voiture7.png")).convert_alpha()
voiture7= pygame.transform.scale(voiture7, (voiture_width, voiture_height))
"""

# --- Logo carré ---
carre = pygame.image.load(resource_path("image/Logo/LenulAgglo.png")).convert()
carre= pygame.transform.scale(carre, (150, 150))
# --- Logo rond ---
rond = pygame.image.load(resource_path("image/Logo/LenulAggloRond.png")).convert()
rond= pygame.transform.scale(rond, (200, 200))

conteneurs = pygame.image.load(resource_path("image/Dessin/conteneur_maritime.png")).convert_alpha()
conteneurs= pygame.transform.scale(conteneurs, (100, 100))

conteneurs90 = pygame.image.load(resource_path("image/Dessin/conteneur_maritime_sim_90.png")).convert_alpha()
conteneurs90= pygame.transform.scale(conteneurs90, (100, 100))

batimentpng = pygame.image.load(resource_path("image/Dessin/batiment.png")).convert_alpha()
batimentpng= pygame.transform.scale(batimentpng, (150, 110))

batimentpngrepos = pygame.image.load(resource_path("image/Dessin/batiment.png")).convert_alpha()
batimentpngrepos= pygame.transform.scale(batimentpngrepos, (220, 110))

benne_width, benne_height = 140, 60
benne_img = pygame.image.load(resource_path("image/Dessin/benne.png")).convert_alpha()
benne_img = pygame.transform.scale(benne_img, (benne_width, benne_height))

poubellenoir = pygame.image.load(resource_path("image/Dessin/poubelle.png")).convert_alpha()
poubellenoir = pygame.transform.scale(poubellenoir, (50, 25))

poubellevert = pygame.image.load(resource_path("image/Dessin/poubelle_v.png")).convert_alpha()
poubellevert = pygame.transform.scale(poubellevert, (50, 25))

poubellebleu = pygame.image.load(resource_path("image/Dessin/poubelle_b.png")).convert_alpha()
poubellebleu = pygame.transform.scale(poubellebleu, (50, 25))

poubellenoirR = pygame.image.load(resource_path("image/Dessin/poubelle_r.png")).convert_alpha()
poubellenoirR = pygame.transform.scale(poubellenoirR, (25, 50))

# --- Gardien ---
personnages_aide = [
    {"nom": "Agent Tri", "x": 700, "y": 500, "visible": False}  # apparaît via la salle de repos
]

# --- Choix Voiture ---
#,voiture4,voiture5,voiture6,voiture7
#attente de voiture
listevoiture = [voiture2,voiture,voiture3]

# --- Bennes ---

angles_bennes = -15
positions_bennes = [(20 + i*160, 760) for i in range(10)]
nomsBenne = list(data["dechets"].keys())[:9]
nomsBenne.append("Vegetaux")



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

# --- Décor fixe ---
herbes_haut = [(randint(0, WIDTH), randint(155, 300)) for _ in range(150)]
herbes_bas = [(randint(0, WIDTH), randint(860, HEIGHT)) for _ in range(150)]

fleurs = [(randint(0, WIDTH), randint(150, 300)) for _ in range(30)]
cailloux = [(randint(0, WIDTH), randint(150, 300)) for _ in range(20)]
arbres = [(randint(0, WIDTH), randint(150, 250)) for _ in range(10)]
fissures = [(randint(0, WIDTH), randint(300, 850)) for _ in range(30)]


# --- Conteneurs noirs ---
conteneurs_noirs = [
    {"rect": pygame.Rect(855, 315, 40, 10), "nom": "Bidons"},
    {"rect": pygame.Rect(955, 315, 40, 10), "nom": "Huile"},
    {"rect": pygame.Rect(1085, 315, 40, 10), "nom": "Pile/Ampoule/Neon"},
    {"rect": pygame.Rect(1215, 315, 40, 10), "nom": "Jouets"},
    {"rect": pygame.Rect(1325, 465, 40, 10), "nom": "Pneu"},
    {"rect": pygame.Rect(1275, 360, 10, 80), "nom": "Article de Sport"},
    {"rect": pygame.Rect(WIDTH-103, 320, 40, 10), "nom": "Verre"},
    {"rect": pygame.Rect(WIDTH-105, 400, 40, 10), "nom": "Papier"},
]

# --- Bâtiments cliquables ---
batiments_cliquables = [
    {"rect": pygame.Rect(300, 300, 143,112), "nom": "Emmaus"},
    {"rect": pygame.Rect(439, 300, 145, 112), "nom": "DDS"},
    {"rect": pygame.Rect(584, 300, 216, 112), "nom": "Salle de repos"},

]
taille_voiture = 0
# --- Voiture ---

voiture_x, voiture_y = 0, 520
voiture_vitesse = 2
bipused = False
choixvoiture = choice(listevoiture)

# --- Mots draggables ---
font_bulle = pygame.font.Font(resource_path("fonts/arial.ttf"), 17)
mots_rects = []

def collision_avec_padding(rect1, rect2, padding=20):
    return rect1.inflate(padding, padding).colliderect(rect2)
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
    global voiture_x, voiture_y, mots_rects, choixvoiture, bipused
    voiture_x, voiture_y = -70, 520
    mots_rects = []
    choixvoiture = choice(listevoiture)
    bipused = False
    i = randint(2,4)
    
    while i!=0:
        categorie = choice(list(data["dechets"].keys()))
        objet = choice(data["dechets"][categorie])
        if object not in [mot["mot"] for mot in mots_rects]:  # éviter les doublons
            surface_mot = font_bulle.render(objet, True, NOIR)
            rect_mot = surface_mot.get_rect(topleft=(0,0))
            i-=1  # initialisation
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
    
    pygame.draw.rect(surface, (80,160,80), (0, 0, WIDTH, 300))



    pygame.draw.rect(surface, (80,160,80), (0, 620, WIDTH, HEIGHT-620))
    pygame.draw.rect(surface, (135,206,235), (0, 0, WIDTH, 150))#bleu
    pygame.draw.rect(surface, GRISCLAIR, (0, 300, WIDTH, 550))
    pygame.draw.rect(surface, (90,90,90), (0, 500, WIDTH, 200))

    y_grillage = HEIGHT -50

    for i in range(0, WIDTH, 40):
        pygame.draw.rect(surface, (120,120,120), (i, y_grillage, 5, 30))

    # barre horizontale
    pygame.draw.line(surface, (120,120,120), (0, y_grillage), (WIDTH, y_grillage), 4)
    pygame.draw.line(surface, (120,120,120), (0, y_grillage+15), (WIDTH, y_grillage+15), 2)

    
    for i in range(0, WIDTH, 80):
        pygame.draw.rect(surface, (255,255,255), (i, 590, 40, 5))
    for x, y in herbes_haut:
        pygame.draw.line(surface, (60,140,60), (x, y), (x, y - 10), 2)

    for x, y in herbes_bas:
        pygame.draw.line(surface, (60,140,60), (x, y), (x, y - 10), 2)


    for x, y in fleurs:
        pygame.draw.circle(surface, (255,255,0), (x, y), 3)
        pygame.draw.circle(surface, (255,0,0), (x+3, y), 2)
        pygame.draw.circle(surface, (255,0,0), (x-3, y), 2)
    for x, y in cailloux:
        pygame.draw.circle(surface, (120,120,120), (x,y), 3)
    for x, y in arbres:
        pygame.draw.rect(surface, (100,70,40), (x, y, 10, 20))
        pygame.draw.circle(surface, (50,150,50), (x+5, y), 15)

    for i in range(0, WIDTH, 40):
        pygame.draw.rect(surface, (120,120,120), (i,170, 5, 30))
        pygame.draw.line(surface, (120,120,120), (0, 170), (WIDTH, 170), 4)
        pygame.draw.line(surface, (120,120,120), (0, 185), (WIDTH, 185), 2)
    for i in range(0, WIDTH, 200):
        pygame.draw.line(surface, (255,255,0), (i, 500), (i+100, 500), 4)
        pygame.draw.line(surface, (255,255,0), (i, 700), (i+100, 700), 4)



    font = pygame.font.Font(resource_path("fonts/arial.ttf"), 18)

    # --- Déplacement voiture ---
    # Déplacement voiture
    if any(not mot["placed"] for mot in mots_rects):
        # Si au quart de l'écran, s'arrête
        if not bipused:
            bip.play()
            bipused = True
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
            moteur.play()

    # --- Sol et zones ---
    
    pygame.draw.rect(surface, BEIGE, (0, 310, 50, 50))
    #pygame.draw.rect(surface, BEIGE, (300, 310, 500, 80))
    surface.blit(carre, (10,60))
    surface.blit(conteneurs, (1299,375))
    surface.blit(conteneurs, (1490,375))
    surface.blit(conteneurs90, (1275,300))
    surface.blit(conteneurs90, (1516,300))
    surface.blit(batimentpng, (300,300))
    surface.blit(batimentpng, (440,300))
    surface.blit(batimentpngrepos, (580,300))
    # --- Conteneurs noirs ---
    for conteneur in conteneurs_noirs:
        if conteneur["nom"] in ["Papier"]:
            surface.blit(poubellebleu, conteneur["rect"].topleft)
        elif conteneur["nom"] in ["Verre"]:
            surface.blit(poubellevert, conteneur["rect"].topleft)
        elif conteneur["nom"] in ["Article de Sport"]:
            surface.blit(poubellenoirR, conteneur["rect"].topleft)
        else:
            surface.blit(poubellenoir, conteneur["rect"].topleft)

    # --- Textes ---
    texte = ["Entree","Loge","Emmaus","DDS","Salle de repos","Sortie","Pneu","Bidons","Huile","Pile/Ampoule/Neon","Jouets","Verre","Papier"]
    pos_texte = [[50,450],[25,330],[350,330],[500,330],[700,330],[WIDTH-50,450],[1350,460],[880,310],[980,310],[1110,310],[1240,310],[WIDTH-80,310],[WIDTH-80,390]]
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
        pygame.draw.rect(surface, GRISCLAIR, batiment["rect"], 1)

    # --- Voiture ---
    surface.blit(choixvoiture,(voiture_x,voiture_y-35))
    
    for p in personnages_aide:
        if p["nom"] == "Agent Tri" and p["visible"] and texte_visible:
            surface.blit(image, (p["x"] -20, p["y"]-50))
            advice = "Ah je vois que vous avez besoin d'aide !\n"
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
        bulle_width, bulle_height = 250, max(50, len(mots_rects)*30)
        bulle_x = voiture_x + voiture_width + 10
        bulle_y = voiture_y - 20
        pygame.draw.rect(surface, BLANC, (bulle_x, bulle_y, bulle_width, bulle_height), border_radius=10)
        pygame.draw.rect(surface, NOIR, (bulle_x, bulle_y, bulle_width, bulle_height), 2, border_radius=10)

        for j, mot in enumerate(mots_rects):
            # ⚡ Position initiale seulement si jamais définie
            if mot["rect"].topleft == (0,0):
                mot["rect"].topleft = (bulle_x + 10, bulle_y + 10 + j*27)
            # Mettre à jour la couleur si changée
            mot["surface"] = font_bulle.render(mot["mot"], True, mot["couleur"])
            surface.blit(mot["surface"], mot["rect"])
            pygame.draw.rect(surface, NOIR, (mot["rect"].x-5, mot["rect"].y-4, mot["rect"].width+10, mot["rect"].height+7), 2, border_radius=10)

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
                    if collision_avec_padding(dragging_mot["rect"], cible["rect"]):

                        if dragging_mot["categorie"] == cible["nom"]:
                            dragging_mot["couleur"] = VERT
                            dragging_mot["placed"] = True
                            Score_joueur += 1
                            compteur_dechet +=1
                            texte_visible = False
                            correct.play()
                            
                            
                        else:
                            dragging_mot["couleur"] = ROUGE
                            dragging_mot["placed"] = True
                            compteur_dechet +=1
                            gameover.play()
                            

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
            score_max = ecran_demarrage(surface, 1800, 1000, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock)

    # --- Affichage score ---
    # --- Barre de score ---
    pygame.draw.rect(surface, GRISCLAIR, (barre_x, barre_y, barre_width, barre_height))  # fond
    couleur_barre = couleur_arc_en_ciel(Score_joueur, score_max)
    pygame.draw.rect(surface, couleur_barre, (barre_x, barre_y, min(Score_joueur/score_max * barre_width, barre_width), barre_height))
    pygame.draw.rect(surface, NOIR, (barre_x, barre_y, barre_width, barre_height), 3)
    score_surf = font.render(f"Score : {Score_joueur}", True, NOIR)
    surface.blit(score_surf, (WIDTH//2 -10, 150))
    font2 = pygame.font.Font(resource_path("fonts/arial.ttf"), 50)
    score2_surf = font2.render("Bienvenue dans la decheterie de Telleville géré par Lenul Agglo", True, NOIR)
    surface.blit(score2_surf, (WIDTH//2 - score2_surf.get_width()//2, 20))
    # --- Affichage final ---
    scaled_surface = pygame.transform.scale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()