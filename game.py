import pygame
import pytmx
import pyscroll

from player import player


class Game:
    def __init__(self) -> None:
        # Creer la fenetre
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Pokémon")
        logo = pygame.image.load("Image\pokeball.png").convert_alpha()
        pygame.display.set_icon(logo)

        # Load card (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("Map\carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        # Générer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = player(player_position.x, player_position.y)

        # Dessiner groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer=5)
        self.group.add(self.player)


    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z]:
            self.player.move_up()
        elif pressed[pygame.K_s]:
            self.player.move_down()
        elif pressed[pygame.K_q]:
            self.player.move_left()
        elif pressed[pygame.K_d]:
            self.player.move_right()

    def run(self) -> None:
        clock = pygame.time.Clock()
        # Boucle du jeu
        running = True
        while running:
            self.handle_input()
            self.group.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            # Verifie si on ferme la fenetre
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
        pygame.quit
