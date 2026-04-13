# en attente surement supprimé
# demarrage.py
import pygame, sys

def ecran_accueil(WIDTH, HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock):
    font_title = pygame.font.Font("fonts/arial.ttf", 80)
    font_fonct = pygame.font.Font("fonts/arial.ttf", 30)

    game_surface = pygame.Surface((WIDTH, HEIGHT))

    carre = pygame.transform.scale(
        pygame.image.load("image/LenulAgglo.png").convert(),
        (150, 150)
    )

    rond = pygame.transform.scale(
        pygame.image.load("image/LenulAggloRond.png").convert(),
        (200, 200)
    )

    running_start = True

    while running_start:
        game_surface.fill((50, 150, 200))

        game_surface.blit(carre, (160,60))

        fonctionnement = font_fonct.render("Vous incarnez un agent qui découvre la nouvelle déchetterie de Telleville, gérée par Lenul Agglo.",True,(255, 255, 255))
        game_surface.blit(fonctionnement, (50 , 500 - fonctionnement.get_height()//2))

        fonctionnement2 = font_fonct.render("Votre objectif est d’aider les visiteurs à trier correctement leurs déchets. Pour cela :",True,(255, 255, 255))
        game_surface.blit(fonctionnement2, (50 , 535 - fonctionnement2.get_height()//2))

        fonctionnement3 = font_fonct.render("- Vous devrez vider les voitures des visiteurs.",True,(255, 255, 255))
        game_surface.blit(fonctionnement3, (70 , 570 - fonctionnement3.get_height()//2))

        fonctionnement4 = font_fonct.render("- Placer les déchets dans les bonnes bennes rapporte des points.",True,(255, 255, 255))
        game_surface.blit(fonctionnement4, (70 , 605 - fonctionnement4.get_height()//2))

        fonctionnement5 = font_fonct.render("- Se tromper vous fait perdre des points.",True,(255, 255, 255))
        game_surface.blit(fonctionnement5, (70 , 640 - fonctionnement5.get_height()//2))

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
                    return 1

        # scaling final vers écran
        scaled = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled, (0, 0))

        pygame.display.flip()

        clock.tick(60)
