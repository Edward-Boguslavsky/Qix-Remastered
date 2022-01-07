import pygame
import random
from entity import Entity



class Sparx(Entity):
    """
    A class representing the Sparx in the game.

    Attributes:
        x (int): x coordinate of the entity on the field
        y (int): y coordinate of the entity on the field
        icon (str): the file path containing the image representing this entity
    """
    x: int
    y: int
    icon: pygame.Surface

    def __init__(self, x: int, y: int, direction: bool) -> None:
        """
        Initialize the Player with the  <icon_file> and given <x> and <y> position on the game.
        """

        super().__init__(x, y)
        self.set_icon("resources/sprite_sparx.png")
        # Spawn the Sparx with a clockwise or counter-clockwise direction traversing the <game.map.perimeter> list
        self.clockwise = direction
        if self.clockwise:
            self.x_direction, self.y_direction = 1, 0
        else:
            self.x_direction, self.y_direction = -1, 0

    def move(self, game: 'Game') -> None:
        """
        The Sparx is spawned on the edge of the field and its movement its restricted to its edge. If the Sparx comes
        into contact with the <Player> its movement is then reversed.
        """
        if game.map.wires:
            if (self.x, self.y) == game.map.wire_coordinates[0]:
                game.lose_live()
                game.player.x, game.player.y = game.map.wire_coordinates[0][0], game.map.wire_coordinates[0][1]
                game.map.wires = []
                game.map.wire_coordinates = []
                self.x_direction *= -1
                self.y_direction *= -1
                pygame.time.wait(100)
                self.x += self.x_direction
                self.y += self.y_direction
        if (self.x, self.y) == (game.player.x, game.player.y):
            game.lose_live()
            self.x_direction *= -1
            self.y_direction *= -1
            pygame.time.wait(100)

        if (self.x, self.y) not in game.map.perimeter:
            (self.x, self.y) = random.choice(game.map.perimeter)

        if (self.x + self.x_direction, self.y + self.y_direction) not in game.map.perimeter:
            if self.x_direction:
                self.x_direction = 0
                if (self.x, self.y - 1) in game.map.perimeter:
                    self.y_direction = -1
                else:
                    self.y_direction = 1
            else:
                self.y_direction = 0
                if (self.x - 1, self.y) in game.map.perimeter:
                    self.x_direction = -1
                else:
                    self.x_direction = 1
        self.x += self.x_direction
        self.y += self.y_direction
