import random
import time

from snake import Snake
from draw import Screen
from watcher import KeyWatcher

SNAKE_NODE_CHAR = '●'
SNAKE_FOOD_CHAR = '*'
EMPTY_CHAR = ' '


class Game:

    def __init__(self):
        self.food = None
        self._pause = False
        self._stop = False

        self.screen = Screen()
        if self.RIGHT < 50 or self.BOTTOM < 10:
            print('屏幕空间不足，无法启动游戏')
            self.exit()
            raise ValueError()

        self.screen.open()
        self.snake = Snake((10, 10), 0, 1)
        self.cmd_watcher = KeyWatcher(self)

    def get_snake_initial_pos(self):
        x, y = self.get_random_pos()

    def restore_state(self):
        chars = []
        for x, y in self.snake:
            chars.append((x, y, SNAKE_NODE_CHAR))

        if self.food:
            chars.append((self.food[0], self.food[1], SNAKE_FOOD_CHAR))

        self.screen.refresh()
        self.screen.draw_n(*chars)

    def exit(self):
        self.screen.close()

    def draw_snake(self, x, y):
        chars = [(x, y, EMPTY_CHAR)]
        for nx, ny in self.snake:
            chars.append((nx, ny, SNAKE_NODE_CHAR))

        self.screen.draw_n(*chars)

    def set_pause(self):
        flag = not bool(self._pause)
        if flag:
            self.screen.show_pad('已暂停')
        else:
            self.restore_state()

        self._pause = flag

    def stop(self):
        self._stop = True

    def is_stop(self):
        return self._stop

    @property
    def paused(self):
        return self._pause

    def get_random_pos(self):
        left = self.LEFT + 1
        if left % 2 != 0:
            left += 1

        x = random.randrange(left, self.RIGHT, 2)
        y = random.randint(self.TOP + 1, self.BOTTOM)
        return x, y

    def ready_food(self):
        while not self.food:
            x, y = self.get_random_pos()
            if (x, y) not in self.snake:
                self.food = x, y
                self.screen.draw(x, y, SNAKE_FOOD_CHAR)
                break

    @property
    def stdscr(self):
        return self.screen.get_stdscr()

    @property
    def LEFT(self):
        return self.screen.LEFT

    @property
    def RIGHT(self):
        return self.screen.RIGHT - 2

    @property
    def TOP(self):
        return self.screen.TOP

    @property
    def BOTTOM(self):
        return self.screen.BOTTOM - 1

    def turn_around(self, direction):
        if not self.paused and not self.is_stop():
            if not self.snake.turn_to(*direction):
                self.screen.warning()

    def run(self):
        self.cmd_watcher.watch()
        while not self._stop:
            if not self.paused:
                self.ready_food()

                last_pos = self.snake.slide(
                    self.LEFT, self.RIGHT, self.TOP, self.BOTTOM)

                if self.snake.alive:
                    if self.snake.head == self.food:
                        self.snake.eat(*self.food)
                        self.food = None

                    self.draw_snake(*last_pos)
                else:
                    break

            time.sleep(0.1)

        # self.screen.get_stdscr().getch()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()
        if exc_val:
            raise exc_val

        return not exc_val


if __name__ == '__main__':
    try:
        with Game() as g:
            g.run()
    except ValueError:
        pass
