# demarrage.py
import pygame, sys


def ecran_demarrage(surface, WIDTH, HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock):
    font_title = pygame.font.Font(None, 80)
    font_text = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 30)
    font_fonct = pygame.font.Font(None, 25)
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # --- Logo carré ---
    carre = pygame.image.load("image/LundiAgglo.png").convert()
    carre= pygame.transform.scale(carre, (150, 150))
    # --- Logo rond ---
    rond = pygame.image.load("image/LundiAggloRond.png").convert()
    rond= pygame.transform.scale(rond, (200, 200))

    score_max = 20
    user_input = ''
    etape = 1
    

    running_start = True
    while running_start:
        ### PARTIE AFFICHAGE JEU###



        surface.fill((50, 150, 200))
        surface.blit(carre, (160,60))

        # --- Titre ---
        titre = font_title.render("Décheterie Simulator", True, (255, 255, 255))
        surface.blit(titre, (WIDTH//2 - titre.get_width()//2, HEIGHT//5))

        fonctionnement = font_fonct.render("Vous incarnez un agent qui découvre la nouvelle déchetterie de Telleville, gérée par Lundi Agglo.",True,(255, 255, 255))
        surface.blit(fonctionnement, (50 , 300 - fonctionnement.get_height()//2))

        fonctionnement2 = font_fonct.render("Votre objectif est d’aider les visiteurs à trier correctement leurs déchets. Pour cela :",True,(255, 255, 255))
        surface.blit(fonctionnement2, (50 , 325 - fonctionnement2.get_height()//2))

        fonctionnement3 = font_fonct.render("- Vous devrez vider les voitures des visiteurs.",True,(255, 255, 255))
        surface.blit(fonctionnement3, (70 , 350 - fonctionnement3.get_height()//2))

        fonctionnement4 = font_fonct.render("- Placer les déchets dans les bonnes bennes rapporte des points.",True,(255, 255, 255))
        surface.blit(fonctionnement4, (70 , 375 - fonctionnement4.get_height()//2))

        fonctionnement5 = font_fonct.render("- Se tromper vous fait perdre des points.",True,(255, 255, 255))
        surface.blit(fonctionnement5, (70 , 400 - fonctionnement5.get_height()//2))
        if etape == 1:
            texte = font_text.render("Choisissez la difficulté :", True, (255, 255, 255))
            surface.blit(texte, (WIDTH//2 - texte.get_width()//2, HEIGHT//2 - 60))
            options = ["1 - Facile", "2 - Moyen", "3 - Difficile", "4 - Perso"]
            for i, option in enumerate(options):
                opt_surf = font_small.render(option, True, (255, 255, 0))
                surface.blit(opt_surf, (WIDTH//2 - opt_surf.get_width()//2, HEIGHT//2 + i*40))

        elif etape == 2:
            texte = font_text.render("Entrez le score max désiré :", True, (255, 255, 255))
            surface.blit(texte, (WIDTH//2 - texte.get_width()//2, HEIGHT//2 - 60))
            input_surf = font_text.render(user_input, True, (255, 255, 0))
            surface.blit(input_surf, (WIDTH//2 - input_surf.get_width()//2, HEIGHT//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if etape == 1:
                    if event.key == pygame.K_1:
                        score_max = 20
                        running_start = False
                    elif event.key == pygame.K_2:
                        score_max = 40
                        running_start = False
                    elif event.key == pygame.K_3:
                        score_max = 60
                        running_start = False
                    elif event.key == pygame.K_4:
                        etape = 2
                elif etape == 2:
                    if event.key == pygame.K_RETURN and user_input.isdigit():
                        score_max = int(user_input)
                        running_start = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit():
                        user_input += event.unicode

        scaled_surface = pygame.transform.scale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen = pygame.display.get_surface()
        screen.blit(scaled_surface, (0,0))
        pygame.display.flip()
        clock.tick(60)

    return score_max