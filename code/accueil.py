# en attente surement supprimé
# demarrage.py
import pygame, sys


def ecran_accueil(surface, WIDTH, HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock):
    font_title = pygame.font.Font(None, 80)

    font_fonct = pygame.font.Font(None, 25)
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # --- Logo carré ---
    carre = pygame.image.load("image/LenulAgglo.png").convert()
    carre= pygame.transform.scale(carre, (150, 150))
    # --- Logo rond ---
    rond = pygame.image.load("image/LenulAggloRond.png").convert()
    rond= pygame.transform.scale(rond, (200, 200))
    

    running_start = True
    while running_start:
        ### PARTIE AFFICHAGE JEU###



        surface.fill((50, 150, 200))
        surface.blit(carre, (160,60))

        # --- Titre ---
        titre = font_title.render("Décheterie Simulator", True, (255, 255, 255))
        surface.blit(titre, (WIDTH//2 - titre.get_width()//2, HEIGHT//5))

        fonctionnement = font_fonct.render("Vous incarnez un agent qui découvre la nouvelle déchetterie de Telleville, gérée par Lenul Agglo.",True,(255, 255, 255))
        surface.blit(fonctionnement, (50 , 300 - fonctionnement.get_height()//2))

        fonctionnement2 = font_fonct.render("Votre objectif est d’aider les visiteurs à trier correctement leurs déchets. Pour cela :",True,(255, 255, 255))
        surface.blit(fonctionnement2, (50 , 325 - fonctionnement2.get_height()//2))

        fonctionnement3 = font_fonct.render("- Vous devrez vider les voitures des visiteurs.",True,(255, 255, 255))
        surface.blit(fonctionnement3, (70 , 350 - fonctionnement3.get_height()//2))

        fonctionnement4 = font_fonct.render("- Placer les déchets dans les bonnes bennes rapporte des points.",True,(255, 255, 255))
        surface.blit(fonctionnement4, (70 , 375 - fonctionnement4.get_height()//2))

        fonctionnement5 = font_fonct.render("- Se tromper vous fait perdre des points.",True,(255, 255, 255))
        surface.blit(fonctionnement5, (70 , 400 - fonctionnement5.get_height()//2))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # reprendre
                    running_start= False
                    return 1

        scaled_surface = pygame.transform.scale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen = pygame.display.get_surface()
        screen.blit(scaled_surface, (0,0))
        pygame.display.flip()
        clock.tick(60)

    