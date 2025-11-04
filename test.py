import pygame as pg

pg.init()
screen = pg.display.set_mode((600, 400))
pg.display.set_caption("Zone de texte")

font = pg.font.Font(None, 36)
clock = pg.time.Clock()

# --- Variables ---
input_box = pg.Rect(200, 150, 200, 40)
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
color = color_inactive
active = False
text = ""

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            # Active la zone si on clique dedans
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive

        if event.type == pg.KEYDOWN and active:
            if event.key == pg.K_RETURN:
                print("Texte entré :", text)
                text = ""  # Réinitialise
            elif event.key == pg.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode

    # --- Affichage ---
    screen.fill((30, 30, 30))
    txt_surface = font.render(text, True, color)
    # Ajuste la taille si le texte dépasse
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pg.draw.rect(screen, color, input_box, 2)

    pg.display.flip()
    clock.tick(30)

pg.quit()
