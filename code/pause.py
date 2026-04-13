import pygame
import sys

def draw_button(surface, rect, text, font, mouse_pos):
    # Couleur selon survol
    if rect.collidepoint(mouse_pos):
        color = (200, 200, 200)
    else:
        color = (100, 100, 100)

    pygame.draw.rect(surface, color, rect, border_radius=10)

    # Texte centré
    txt = font.render(text, True, (0, 0, 0))
    surface.blit(txt, (
        rect.x + rect.width // 2 - txt.get_width() // 2,
        rect.y + rect.height // 2 - txt.get_height() // 2
    ))

def menu_pause(surface, WIDTH, HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, screen, clock):
    font_title = pygame.font.Font("fonts/arial.ttf", 80)
    font_button = pygame.font.Font("fonts/arial.ttf", 40)

    carre = pygame.image.load("image/LenulAgglo.png").convert()
    carre = pygame.transform.scale(carre, (150, 150))

    # Boutons
    btn_resume = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 60, 300, 60)
    btn_restart = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 20, 300, 60)
    btn_quit = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 100, 300, 60)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        surface.fill((50, 50, 50))
        surface.blit(carre, (160, 60))

        # Titre
        titre = font_title.render("PAUSE", True, (255, 255, 0))
        surface.blit(titre, (WIDTH//2 - titre.get_width()//2, HEIGHT//4))

        # Dessin boutons
        draw_button(surface, btn_resume, "Reprendre", font_button, mouse_pos)
        draw_button(surface, btn_restart, "Rejouer", font_button, mouse_pos)
        draw_button(surface, btn_quit, "Quitter", font_button, mouse_pos)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_resume.collidepoint(mouse_pos):
                    return "resume"

                if btn_restart.collidepoint(mouse_pos):
                    return "replay"

                if btn_quit.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Affichage
        scaled_surface = pygame.transform.scale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)