import random
import pygame
from entity import Entity
from settings import *


class Qix(Entity):
    """
    A class representing the Qix in the game

    Attributes:
        x (int): x coordinate of the entity on the field
        y (int): y coordinate of the entity on the field
        x_direction (int): velocity of entity in the x-axis
        y_direction (int): velocity of entity in the y-axis
        icon (str): the file path containing the image representing this entity]
    """
    x: int
    y: int
    x_direction: int
    y_direction: int
    icon: pygame.Surface

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the Player with the  <icon_file> and given <x> and <y> position on the game.
        """
        super().__init__(x, y)
        self.set_icon("resources/sprite_qix.png")
        # Spawn the Qix with a random velocity of -1 or 1 in x and y direction
        self.x_direction, self.y_direction = random.choice([-1, 1]), random.choice([-1, 1])

    def move(self, game: 'Game') -> None:
        """
        A Qix is spawned randomly in the inner field and has a random velocity. Once it contacts the outer field it
        "bounces" in the opposite direction.
        """
        # Collision detection with wires or player
        if game.map.wires:
            if (self.x, self.y) in game.map.wire_coordinates or (self.x, self.y) == (game.player.x, game.player.y):
                game.lose_live()
                game.player.x, game.player.y = game.map.wire_coordinates[0][0], game.map.wire_coordinates[0][1]
                game.map.wires = []
                game.map.wire_coordinates = []
                pygame.time.wait(100)

        # 1/6 chance for the qix velocity to change
        if random.randrange(6) == 0:
            self.x_direction, self.y_direction = random.choice([-1, 1]), random.choice([-1, 1])

        # Spawn Qix in a first location available iteratively
        if game.map.is_captured(self.x, self.y):
            found = False
            for i in range(game.map.size):
                for j in range(game.map.size):
                    if not game.map.tiles[j][i].captured:
                        self.x, self.y = game.map.tiles[j][i].x, game.map.tiles[j][i].y
                        found = True
                        break
                if found:
                    break

        # Checks if next tile in its path is captured and if it is, it "bounces" off in the opposite direction
        if game.map.is_captured(self.x + self.x_direction, self.y):
            self.x_direction *= -1
        if game.map.is_captured(self.x, self.y + self.y_direction):
            self.y_direction *= -1

        # Update the x and y position
        self.x += self.x_direction
        self.y += self.y_direction
