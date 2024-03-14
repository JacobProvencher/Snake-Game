import pygame
from random import choice
from itertools import product

class cube:

    rows = 20
    width = 500

    def __init__(self, position, direction=(1, 0), color=(255, 0, 0)):
        self.position = position
        self.direction = direction
        self.color = color

    def move(self, direction):

        self.direction = direction
        row, line = self.position
        i, j = direction
        self.position = (row + i, line + j)

    def draw(self, surface, eyes=False):

        sizeBtwn = self.width // self.rows
        row, line = self.position
        position, dimension = (sizeBtwn*row, sizeBtwn*line), (sizeBtwn, sizeBtwn)
        pygame.draw.rect(surface, self.color, (position, dimension))

class snake:

    bodyparts = []
    turns = {}

    def __init__(self, color, position):
        self.color = color
        self.head = cube(position)
        self.bodyparts.append(self.head)
        self.vector = {'right': (1, 0), 'left': (-1, 0),'up': (0, -1), 'down': (0, 1), 'statique': (0, 0)}

    def move(self, direction):

        self.turns[self.head.position[:]] = self.vector[direction]

        for index, part in enumerate(self.bodyparts):
            position = part.position[:]
            if position in self.turns:
                i, j = self.turns[position]
                part.move((i, j))
                if index == len(self.bodyparts)-1:
                    self.turns.pop(position)
            else:
                part.move(part.direction)

    def addCube(self):
        tail = self.bodyparts[-1]
        row, line = tail.position
        i, j = tail.direction

        addedCube = cube((row + (0 if i == 0 else -i), line + (0 if j == 0 else -j)))
        self.bodyparts.append(addedCube)

        self.bodyparts[-1].direction = tail.direction

    def draw(self, surface):

        for index, part in enumerate(self.bodyparts):
            if index == 0:
                part.draw(surface, eyes=True)
            else:
                part.draw(surface)

class apple:

    def __init__(self):
        self.spawnPossible = set(product(range(1, 20), range(1, 20)))

    def spawn(self, snake):
        snakePositions = set(snake.bodyparts)
        spawnCoordinate = choice(list(self.spawnPossible - snakePositions))
        print(spawnCoordinate)

        return spawnCoordinate

class window:

    def __init__(self, dimension, rows):

        self.width, self.height = dimension
        self.rows = rows
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.snake = snake((255, 0, 0), (10, 10))
        self.apple = cube(apple().spawn(self.snake), color=(0, 255, 0))
        self.running = True
        self.clock = pygame.time.Clock()

    def drawGrid(self):

        sizeBtwn = self.width // self.rows
        for n in range(0, self.width, sizeBtwn):
            pygame.draw.line(self.screen, (105, 105, 105), (n, 0), (n, self.width))
            pygame.draw.line(self.screen, (105, 105, 105), (0, n), (self.width, n))

    def redrawWindow(self):

        self.screen.fill((0, 0, 0))
        self.drawGrid()
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)
        pygame.display.update()

    def mainloop(self):

        direction = 'statique'

        while self.running:
            pygame.time.delay(50)
            self.clock.tick(8)
            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if keys[pygame.K_LEFT]:
                direction = 'left'
            elif keys[pygame.K_RIGHT]:
                direction = 'right'
            elif keys[pygame.K_UP]:
                direction = 'up'
            elif keys[pygame.K_DOWN]:
                direction = 'down'

            self.snake.move(direction)

            if self.snake.bodyparts[0].position == self.apple.position:
                self.snake.addCube()
                self.apple = cube(apple().spawn(self.snake), color=(0, 255, 0))

            self.redrawWindow()

game = window((500, 500), 20)
game.mainloop()

pygame.quit()