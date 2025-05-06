"""
################################## THIS IS THE API BETWEEN THE GUI AND BACKEND #####################################
    if snake.move():  # If move returns True, a collision occurred
        print("Game Over!")
        running = False
    else:
        # Check if the snake has eaten the food
        if snake.head == snake.board.food:
            snake.growing = True
            snake.board.generate_food()
####################################################################################################################
"""

import random

class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.food = None

    def generate_food(self) -> None:
        self.food = random.randint(0, self.width - 1), random.randint(0, self.height - 1)

class Snake:
    def __init__(self, size, board_width, board_height):
        # self.body = [(i, 0) for i in range(size)]
        self.body = {(x, y): {} for x in range(board_width) for y in range(board_height)}
        self.direction = 'right'
        self.growing = False
        self.board = Board(board_width, board_height)
        self._head = (0, size -1)
        self._tail = (0, 0)

    @property
    def head(self):
        return self._head

    def move(self) -> bool:
        """
        Move the snake in the current direction.
        The direction is always in self.direction and it's updated from the main.
        self.growing is set to True when the snake eats the food from the main.
        :return: True if a collision occurred, False otherwise.
        """
        x, y = self.head

        if self.direction == 'up':
            new_head = (x, y + 1)
        elif self.direction == 'down':
            new_head = (x, y - 1)
        elif self.direction == 'left':
            new_head = (x - 1, y)
        else: # right
            new_head = (x + 1, y)

        if self._check_collision(new_head):
            return True

        #self.body.append(new_head)
        self._head = new_head
        self.body[new_head] = True

        if not self.growing:
            self._tail = self.body[self._tail]['next']
            self.body.[(self._tail)] = False

        self.growing = False
        return False


    def _check_collision(self, new_head) -> bool:
        """
        Check if the new head position results in a collision with the border or itself.
        :param new_head:
        :return: True if a collision occurred, False otherwise.
        """
        x, y = new_head

        if x <= 0 or x > self.board.width or y <= 0 or y > self.board.height:
            return True

        if new_head in self.body:
            return True

        return False

