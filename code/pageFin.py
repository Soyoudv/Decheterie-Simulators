# fin.py
import pygame, sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")
    return os.path.join(base_path, relative_path)


def page_fin(surface, WIDTH, HEIGHT, Score_joueur, nbdechets, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock):
    font_title = pygame.font.Font(resource_path("fonts/arial.ttf"), 80)
    font_text = pygame.font.Font(resource_path("fonts/arial.ttf"), 40)
    
    # --- Logo carré ---
    carre = pygame.image.load(resource_path("image/Logo/LenulAgglo.png")).convert()
    carre= pygame.transform.scale(carre, (150, 150))
    # --- Logo rond ---
    rond = pygame.image.load(resource_path("image/Logo/LenulAggloRond.png")).convert()
    rond= pygame.transform.scale(rond, (200, 200))
    winning = pygame.mixer.Sound(resource_path("audio/winning.mp3"))
    winning.set_volume(0.1)
    winning.play()

    running_fin = True
    while running_fin:
        surface.fill((20, 20, 50))  # fond sombre
        surface.blit(carre, (160,60))
        
        

        # Titre
        titre = font_title.render("Félicitations !", True, (255, 255, 0))
        surface.blit(titre, (WIDTH//2 - titre.get_width()//2, HEIGHT//4))

        # Score final
        texte_score = font_text.render(f"Score final : {Score_joueur}", True, (255, 255, 255))
        surface.blit(texte_score, (WIDTH//2 - texte_score.get_width()//2, HEIGHT//2 - 100))

        stats = font_text.render(f"Nombre de déchets déposés : {nbdechets}", True, (255, 255, 255))
        surface.blit(stats, (WIDTH//2 - stats.get_width()//2, 450))

        if nbdechets > 0:
            pourcentage = (Score_joueur / nbdechets) * 100
        else:
            pourcentage = 0
        stats2 = font_text.render(f"Pourcentage de réussite : {pourcentage:.1f}%", True, (255, 255, 255))
        surface.blit(stats2, (WIDTH//2 - stats2.get_width()//2, 500))

        # Instructions
        texte_rejouer = font_text.render("Appuyez sur R pour rejouer ou Q pour quitter", True, (200, 200, 255))
        surface.blit(texte_rejouer, (WIDTH//2 - texte_rejouer.get_width()//2, HEIGHT//2 + 60))

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # rejouer
                    running_fin = False
                    return "replay"
                elif event.key == pygame.K_q:  # quitter
                    pygame.quit()
                    sys.exit()
        # Affichage final
        scaled_surface = pygame.transform.scale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)