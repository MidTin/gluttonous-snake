import curses


class Screen:

    DEFAULT_PAD_HEIGHT = 5
    DEFAULT_PAD_WIDTH = 10

    def __init__(self):
        self.main = curses.initscr()

        self.BOTTOM = curses.LINES - 2
        self.TOP = 0
        self.RIGHT = curses.COLS
        self.LEFT = 0

        self.background = self.main.subwin(self.BOTTOM, self.RIGHT, 0, 0)
        self.menu = self.main.subwin(1, self.RIGHT, self.BOTTOM, 0)

        self.pad = self.main.subwin(self.BOTTOM - 2, self.RIGHT - 2, 1, 1)

        curses.noecho()  # 不输出键盘输入
        curses.cbreak()  # 立刻响应键盘输入
        curses.curs_set(0)

        self.background.keypad(True)

    def show_pad(self, msg):
        self.pad.erase()
        length = len(msg)
        x = (self.RIGHT - length) // 2 if self.RIGHT > length else 0
        y = (self.BOTTOM // 2)

        self.pad.addstr(y, x, msg)
        self.pad.refresh()

    def ready_menu(self):
        self.menu.addstr('(Q) 停止    (P) 暂停/恢复')
        self.menu.refresh()

    def ready_background(self):
        self.background.border()
        self.background.refresh()

    def warning(self):
        pass

    def get_stdscr(self):
        return self.background

    def draw(self, x, y, char):
        self.background.addstr(y, x, char)
        self.background.refresh()

    def draw_n(self, *args):
        for x, y, char in args:
            self.background.addstr(y, x, char)

        self.background.refresh()

    def refresh(self):
        self.background.clear()
        self.ready_background()

    def open(self):
        self.ready_menu()
        self.ready_background()

    def close(self):
        self.background.keypad(False)

        curses.nocbreak()
        curses.curs_set(1)
        curses.echo()

        curses.endwin()
