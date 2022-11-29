import pygame


# 0 is grass, 1 is dirt 2 is sand

grid = [
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
]

TILE_SIZE = 128

# define images for our background
grass = pygame.image.load("images/grass.png")
dirt = pygame.image.load("images/dirt.png")
track = pygame.image.load("images/greentrack.png")

soils = [grass,dirt,track]

# grab the dimension of our tile rectangle
tile_rect = grass.get_rect()


def draw_background(bg_size):
    bg = pygame.Surface(bg_size)
    # draw each tile onto our background
    for r, grid_list in enumerate(grid):
        for c, grid_element in enumerate(grid_list):
            # blit the correc tile onto our screen
            bg.blit(soils[grid_element], (c*TILE_SIZE, r*TILE_SIZE))
    return bg