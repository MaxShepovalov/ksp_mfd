import pygame

def main():
    pygame.init()
    DISPLAY = pygame.display.set_mode((1000,500),0,32)
    WHITE = (255,255,255)
    blue = (0,0,255)
    DISPLAY.fill(WHITE)
    pygame.mouse.set_visible(False)
    pygame.draw.rect(DISPLAY, blue,(480,200,50,250))
    pygame.display.update()
    pygame.mouse.set_pos(480, 200)
    pos = [0, 0]
    run = True
    while run:
        for event in pygame.event.get():
            strpos = "--"
            if "pos" in dir(event):
                strpos = event.pos
            print("{} @ {}".format(pygame.event.event_name(event.type), strpos))
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                pos = event.pos
            pygame.draw.rect(DISPLAY, blue, (pos[0]-25,pos[1], 50, 250))
            pygame.display. update()
            DISPLAY.fill(WHITE)
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    run = False 
main()