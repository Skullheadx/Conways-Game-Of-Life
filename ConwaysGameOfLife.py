from setup import *
from game import Game

scene = Game()
delta = 1000 // fps

# Main loop
is_running = True
while is_running:
    # Check if the window is closed
    if pygame.event.peek(pygame.QUIT):
        is_running = False

    scene.update(delta)
    # print(scene)
    scene.draw(screen)

    # Update the window and find delta
    pygame.display.update()
    delta = clock.tick(fps)

# Exit pygame
pygame.quit()
