import pygame

pygame.init()


# Colors var
yellow_color = (227, 224, 18)
black_color = (0, 0, 0)
blue_color = (0, 0, 255)

# Room/screen var
room_width = 1280
room_height = 720
screen = pygame.display.set_mode((room_width, room_height), 0)
# Scenario var
retangle_sample = screen.set_at((int(room_width/4), int(room_height/4)), blue_color)

# Char var
xx = 30
yy = 30
xspd = .2
yspd = .2
radius = 15
char_mouth = [(radius/2, radius/2), (radius, radius), (radius, radius/2)]
while True:
    # Rules
    xx += xspd
    if xx + radius> room_width:
        xspd = -xspd
    if xx - radius < 0:
        xspd = -xspd
    yy += yspd
    if yy + radius> room_height:
        yspd = -yspd
    if yy - radius< 0:
        yspd = -yspd

    # Color
    screen.fill((black_color))
    pygame.draw.circle(screen, yellow_color, (xx, yy), radius, 0)
    pygame.display.update()
    # Events

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

