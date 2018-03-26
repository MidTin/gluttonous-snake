import curses
import threading

UP_DIRECTION = (0, -1)
DOWN_DIRECTION = (0, 1)
LEFT_DIRECTION = (-2, 0)
RIGHT_DIRECTION = (2, 0)

ACTION_TURN_AROUND = 'turn_around'
ACTION_SET_PAUSE = 'set_pause'
ACTION_STOP = 'stop'

KEY_MAP = {
    curses.KEY_UP: (ACTION_TURN_AROUND, (UP_DIRECTION, )),
    curses.KEY_DOWN: (ACTION_TURN_AROUND, (DOWN_DIRECTION, )),
    curses.KEY_LEFT: (ACTION_TURN_AROUND, (LEFT_DIRECTION, )),
    curses.KEY_RIGHT: (ACTION_TURN_AROUND, (RIGHT_DIRECTION, )),
    ord('P'): (ACTION_SET_PAUSE, ()),
    ord('p'): (ACTION_SET_PAUSE, ()),
    ord('q'): (ACTION_STOP, ()),
    ord('Q'): (ACTION_STOP, ()),
}


class KeyWatcher:

    def __init__(self, game):
        self.game = game
        self.stdscr = game.stdscr
        self._thread = None

    def _watch(self):
        while True:
            cmd = self.stdscr.getch()
            try:
                action_name, args = KEY_MAP[cmd]
                action = getattr(self.game, action_name)
                action(*args)
            except (KeyError, AttributeError):
                pass

    def watch(self):
        if not self._thread:
            self._thread = threading.Thread(target=self._watch)
            self._thread.daemon = True
            self._thread.start()
