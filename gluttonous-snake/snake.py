
class SnakeDead(Exception):
    pass


class Snake:

    def __init__(self, pos, x_direction, y_direction):
        self.body = [pos]
        self._alive = True
        self.x_direction = x_direction
        self.y_direction = y_direction

    @property
    def alive(self):
        return self._alive

    def iter(self):
        for n in self.body:
            yield n

    def __iter__(self):
        return self.iter()

    def __contains__(self, item):
        return item in self.body

    @property
    def head(self):
        return self.body[-1]

    @property
    def tail(self):
        return self.body[0]

    def __len__(self):
        return len(self.body)

    @property
    def length(self):
        return len(self)

    @staticmethod
    def compare_direction(a, b):
        return a != b and abs(a) != abs(b)

    def kill(self):
        self._alive = False

    def turn_to(self, x_direction, y_direction):
        if not (self.compare_direction(self.x_direction, x_direction)
                and self.compare_direction(self.y_direction, y_direction)):
            return False

        self.x_direction = x_direction
        self.y_direction = y_direction
        return True

    def slide(self, ls, rs, ts, bs):
        if not self.alive:
            raise SnakeDead()

        x, y = self.head
        x += self.x_direction
        y += self.y_direction

        self._alive = (x, y) not in self and ls < x < rs and ts < y < bs

        self.eat(x, y)
        return self.body.pop(0)

    def eat(self, x, y):
        self.body.append((x, y))

    def __str__(self):
        return str(self.body)
