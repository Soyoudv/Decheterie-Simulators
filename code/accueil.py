# en attente surement supprimé
import pygame, sys,os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")
    return os.path.join(base_path, relative_path)

def ecran_accueil(WIDTH, HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock):
    font_title = pygame.font.Font(resource_path("fonts/arial.ttf"), 80)
    font_fonct = pygame.font.Font(resource_path("fonts/arial.ttf"), 30)

    game_surface = pygame.Surface((WIDTH, HEIGHT))

    carre = pygame.transform.scale(
        pygame.image.load(resource_path("image/Logo/LenulAgglo.png")).convert(),
        (150, 150)
    )

    rond = pygame.transform.scale(
        pygame.image.load(resource_path("image/Logo/LenulAggloRond.png")).convert(),
        (200, 200)
    )
    clic_button = pygame.mixer.Sound(resource_path("audio/selectbutton.mp3"))

    running_start = True

    while running_start:
        game_surface.fill((50, 150, 200))

        game_surface.blit(carre, (160,60))


        textes = [
            ("Vous incarnez un agent qui découvre la nouvelle déchetterie de Telleville, gérée par Lenul Agglo.", 50, 500),
            ("Votre objectif est d’aider les visiteurs à trier correctement leurs déchets. Pour cela :", 50, 535),
            ("- Vous devrez vider les voitures des visiteurs.", 70, 570),
            ("- Placer les déchets dans les bonnes bennes rapporte des points.", 70, 605),
            ("- Se tromper vous fait perdre des points.", 70, 640)
        ]

        for texte, x, y in textes:
            surface = font_fonct.render(texte, True, (255, 255, 255))
            game_surface.blit(surface, (x, y - surface.get_height() // 2))

        # souris en coords logiques
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x *= WIDTH / SCREEN_WIDTH
        mouse_y *= HEIGHT / SCREEN_HEIGHT
        mouse_pos = (mouse_x, mouse_y)

        titre = font_title.render("Décheterie Simulator", True, (255, 255, 255))
        game_surface.blit(titre, (WIDTH//2 - titre.get_width()//2, HEIGHT//5))

        bouton_jouer = pygame.Rect(WIDTH//2 - 100, HEIGHT//2-200, 200, 60)

        couleur = (0, 255, 0) if bouton_jouer.collidepoint(mouse_pos) else (0, 200, 0)

        pygame.draw.rect(game_surface, couleur, bouton_jouer, border_radius=10)

        texte_bouton = font_fonct.render("JOUER", True, (255, 255, 255))
        game_surface.blit(
            texte_bouton,
            (bouton_jouer.centerx - texte_bouton.get_width()//2,
             bouton_jouer.centery - texte_bouton.get_height()//2)
        )

        # événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                mx *= WIDTH / SCREEN_WIDTH
                my *= HEIGHT / SCREEN_HEIGHT

                if bouton_jouer.collidepoint((mx, my)):
                    clic_button.play()
                    return 1

        # scaling final vers écran
        scaled = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled, (0, 0))

        pygame.display.flip()

        clock.tick(60)
