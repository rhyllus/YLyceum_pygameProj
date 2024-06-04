import pygame as pg


def main():
    screen = pg.display.set_mode((600, 450))
    font = pg.font.Font(None, 28)
    clock = pg.time.Clock()
    input_box = pg.Rect(5, 415, 520, 32)
    search = pg.Rect(527, 415, 69, 32)
    color_inactive = pg.Color('white')
    color_active = (230, 230, 230)
    color = color_inactive
    search_color_inactive = (255, 204, 0)
    search_color_active = (235, 172, 0)
    search_color = search_color_inactive
    active = False
    text = ''
    done = False
    hold = False
    button_hold = False
    back_hold = False
    tick = 0
    clock_tick = 15

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                elif search.collidepoint(event.pos):
                    button_hold = True
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pg.MOUSEBUTTONUP:
                if search.collidepoint(event.pos):
                    print(text)
                    text = ''
                    active = False
                    color = color_inactive
                button_hold = False
                search_color = search_color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        clock_tick = 25
                        if len(text) != 0:
                            text = text[:-1]
                        back_hold = True
                    else:
                        clock_tick = 25
                        text += event.unicode
                        hold = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_BACKSPACE:
                    back_hold = False
                else:
                    hold = False
                tick = 0
            if not search.collidepoint(pg.mouse.get_pos()) and button_hold:
                search_color = search_color_inactive
            elif search.collidepoint(pg.mouse.get_pos()) and button_hold:
                search_color = search_color_active
        if hold or back_hold:
            if hold:
                clock_tick = 25
            tick += 1
            if tick > 15:
                if hold:
                    if len(text) != 0:
                        text += text[-1]
                else:
                    if len(text) != 0:
                        text = text[:-1]
        screen.fill((30, 30, 30))
        if active and clock_tick in range(15, 30):
            txt_surface = font.render(text + '|', True, pg.Color('black'))
        else:
            txt_surface = font.render(text, True, pg.Color('black'))
        find_text = font.render('Найти', True, pg.Color('black'))
        pg.draw.rect(screen, color, input_box, 0)
        pg.draw.rect(screen, search_color, search, 0)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        screen.blit(find_text, (531, 421))
        pg.display.flip()
        if active:
            clock_tick += 1
        else:
            clock_tick = 15
        if clock_tick == 30:
            clock_tick = 0
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
