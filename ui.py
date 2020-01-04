import curses
import json
import shutil
import time

term_cols, term_rows = shutil.get_terminal_size()


class UI:
    def __init__(self, state):
        self.state = state
        self.curpos = (0, 0)
        self.selected_line = 0

        self.headers = ["thing 1", "thing 2", "thing 3", "etc"]
        self.songlist = ["song 1", "song 2", "song 3", "etc"]

        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

        # ## views
        self.left_box = curses.newwin(24, 24, 4, 1)
        self.listscr = curses.newwin(20, curses.COLS - 4, 4, 27)
        self.status_line = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)

        curses.noecho()
        curses.cbreak()

    def write_left_box(self):
        self.left_box.addstr(1, 0, "-----------------------")
        for y in range(2, 12):
            s = "|                     |"
            self.left_box.addstr(y, 0, s)
        self.left_box.addstr(11, 0, "-----------------------")

    def write_list(self):
        for i in range(len(self.songlist)):
            if i == self.selected_line:
                color = curses.color_pair(2)
            else:
                color = curses.color_pair(1)
            self.listscr.addstr(i, 0, self.songlist[i], color)

    def write_status_line(self):
        self.status_line.addstr(
            0, 0, f"the current time is: {str(time.ctime())}", curses.color_pair(1)
        )
        self.status_line.addstr(0, 0, json.dumps(self.state), curses.color_pair(1))

    def write_frame(self):
        self.write_left_box()
        self.left_box.refresh()

        self.write_list()
        self.listscr.refresh()

        self.write_status_line()
        self.status_line.refresh()

    def move_selected_line(self, direc):
        if direc == 2:
            self.selected_line += 1
        elif direc == 3:
            self.selected_line = max(0, self.selected_line - 1)


if __name__ == "__main__":
    u = UI({"term_cols": term_cols})
    u.write_frame()
