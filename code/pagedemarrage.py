# demarrage.py
import pygame, sys
from accueil import ecran_accueil


def ecran_demarrage(surface, WIDTH, HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock):
    val = ecran_accueil( WIDTH, HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock)
    if val == 1:
        font_title = pygame.font.Font("fonts/arial.ttf", 80)
        font_text = pygame.font.Font("fonts/arial.ttf", 40)
        font_small = pygame.font.Font("fonts/arial.ttf", 30)
        

        # --- Logo carré ---
        carre = pygame.image.load("image/LenulAgglo.png").convert()
        carre= pygame.transform.scale(carre, (150, 150))
        # --- Logo rond ---
        rond = pygame.image.load("image/LenulAggloRond.png").convert()
        rond= pygame.transform.scale(rond, (200, 200))

        score_max = 20
        user_input = ''
        etape = 1
        

        running_start = True
        while running_start:
            surface.fill((50, 150, 200))
            surface.blit(carre, (160,60))

            # --- Titre ---
            titre = font_title.render("Décheterie Simulator", True, (255, 255, 255))
            surface.blit(titre, (WIDTH//2 - titre.get_width()//2, HEIGHT//5))
            if etape == 1:
                boutons = {
                    "facile": pygame.Rect(WIDTH//2 - 120, HEIGHT//2, 240, 50),
                    "moyen": pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 60, 240, 50),
                    "difficile": pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 120, 240, 50),
                    "perso": pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 180, 240, 50),
                }
                mouse_pos = pygame.mouse.get_pos()

                # scaling souris (IMPORTANT si tu gardes ton système)
                mouse_pos = (mouse_pos[0] * WIDTH / SCREEN_WIDTH,
                            mouse_pos[1] * HEIGHT / SCREEN_HEIGHT)

                labels = {
                    "facile": ("Facile - 20 pts", 20),
                    "moyen": ("Moyen - 40 pts", 40),
                    "difficile": ("Difficile - 60 pts", 60),
                    "perso": ("Personnalisé", None),
                }

                for key, rect in boutons.items():
                    color = (0, 200, 0)

                    if rect.collidepoint(mouse_pos):
                        color = (0, 255, 0)

                    pygame.draw.rect(surface, color, rect, border_radius=10)

                    text = font_small.render(labels[key][0], True, (255, 255, 255))
                    surface.blit(
                        text,
                        (rect.centerx - text.get_width()//2,
                        rect.centery - text.get_height()//2)
                    )


                texte = font_text.render("Choisissez la difficulté :", True, (255, 255, 255))
                surface.blit(texte, (WIDTH//2 - texte.get_width()//2, HEIGHT//2 - 60))

            elif etape == 2:
                texte = font_text.render("Entrez le score max désiré :", True, (255, 255, 255))
                surface.blit(texte, (WIDTH//2 - texte.get_width()//2, HEIGHT//2 - 60))
                input_surf = font_text.render(user_input, True, (255, 255, 0))
                surface.blit(input_surf, (WIDTH//2 - input_surf.get_width()//2, HEIGHT//2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos

                    mx = mx * WIDTH / SCREEN_WIDTH
                    my = my * HEIGHT / SCREEN_HEIGHT

                    for key, rect in boutons.items():
                        if rect.collidepoint((mx, my)):

                            if key == "facile":
                                score_max = 20
                                running_start = False

                            elif key == "moyen":
                                score_max = 40
                                running_start = False

                            elif key == "difficile":
                                score_max = 60
                                running_start = False

                            elif key == "perso":
                                etape = 2
                elif event.type == pygame.KEYDOWN:
                    if etape == 2:
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