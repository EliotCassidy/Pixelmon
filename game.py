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

        # Génerer liste qui stock les collitions
        self.collitions = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.collitions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # Dessiner groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer=6)
        self.group.add(self.player)
        
        self.map = "world"
        # Défnir rect colision pour rentrer maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
        
        exit_house = tmx_data.get_object_by_name('enter_house_exit')
        self.exit_house_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)
        
    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z]:
            self.player.move_up()
            self.player.change_animation("up")
        elif pressed[pygame.K_s]:
            self.player.move_down()
            self.player.change_animation("down")
        elif pressed[pygame.K_q]:
            self.player.move_left()
            self.player.change_animation("left")
        elif pressed[pygame.K_d]:
            self.player.move_right()
            self.player.change_animation("right")

    def switch_house(self):
        # Load card (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("Map\house.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Génerer liste qui stock les collitions
        self.collitions = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.collitions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # Dessiner groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer=6)
        self.group.add(self.player)

        # Défnir rect colision pour rentrer maison
        enter_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # Récuperer spawn
        spawn_house_point = tmx_data.get_object_by_name("spawn_house")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20

    def switch_world(self):
        # Load card (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("Map\carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Génerer liste qui stock les collitions
        self.collitions = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.collitions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # Dessiner groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer=6)
        self.group.add(self.player)

        # Défnir rect colision pour rentrer maison
        exit_house = tmx_data.get_object_by_name('enter_house')
        self.exit_house_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)

        # Récuperer spawn
        enterpoint = tmx_data.get_object_by_name("enter_house_exit")
        self.player.position[0] = enterpoint.x
        self.player.position[1] = enterpoint.y + 20
    
   
    def update(self):
        self.group.update()
        
        if self.map == "world" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = "house"
        
        if self.map == "house" and self.player.feet.colliderect(self.exit_house_rect):
            self.switch_world()
            self.map = "world"
        
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.collitions) > -1:
                sprite.move_back()
        
    def run(self) -> None:
        clock = pygame.time.Clock()
        # Boucle du jeu
        running = True
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            # Verifie si on ferme la fenetre
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(30)
        pygame.quit
