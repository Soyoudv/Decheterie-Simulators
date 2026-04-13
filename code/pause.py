# pause.py
import pygame, sys



def menu_pause(surface, WIDTH, HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock):
    font_title = pygame.font.Font(None, 80)
    font_text = pygame.font.Font(None, 40)
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # --- Logo carré ---
    carre = pygame.image.load("image/LenulAgglo.png").convert()
    carre= pygame.transform.scale(carre, (150, 150))
    # --- Logo rond ---
    rond = pygame.image.load("image/LenulAggloRond.png").convert()
    rond= pygame.transform.scale(rond, (200, 200))
        

    running_pause = True
    while running_pause:
        surface.fill((50, 50, 50))  # fond sombre semi-transparent
        surface.blit(carre, (160,60))

        # Titre
        titre = font_title.render("PAUSE", True, (255, 255, 0))
        surface.blit(titre, (WIDTH//2 - titre.get_width()//2, HEIGHT//4))

        # Options
        options = [
            "R - Reprendre le jeu",
            "Q - Quitter le jeu"
        ]
        for i, opt in enumerate(options):
            texte_surf = font_text.render(opt, True, (255, 255, 255))
            surface.blit(texte_surf, (WIDTH//2 - texte_surf.get_width()//2, HEIGHT//2 + i*50))

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # reprendre
                    running_pause = False
                    return "resume"
                elif event.key == pygame.K_q:  # quitter
                    pygame.quit()
                    sys.exit()

        # Affichage final
        scaled_surface = pygame.transform.scale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)