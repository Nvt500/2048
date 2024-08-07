import curses
import random


class Numbers:
    
    nums = []
    
    def __init__(self, number):
        
        self.nums.append(number)

class Number(Numbers):
    
    def __init__(self, num: int) -> None:
        
        super().__init__(self)
        self.num = num
        
    
    def __repr__(self) -> str:
        
        return str(self.num) + " " * (4 - len(str(self.num)))
    
    
    def __str__(self) -> str:
        
        return str(self.num) + " " * (4 - len(str(self.num)))
    
    
    def merge(self, other) -> bool:
        
        if self.num == other.num:
            self.num = self.num * 2
            return True
        else:
            return False

    
def up(board) -> list:
    
    row_num = 1
    for row in board[1:]:
        for col_num, col in enumerate(row):
            if isinstance(col, Number):
                for i in range(1, 1 + row_num):
                    if isinstance(board[row_num - i][col_num], Number):
                        if not board[row_num - i + 1][col_num].merge(board[row_num - i][col_num]):
                            break
                    board[row_num - i][col_num] = col
                    board[row_num - i + 1][col_num] = "    "
        row_num += 1
                
    return board
    

def down(board) -> list:
    
    row_num = 2
    for row in board[:-1][::-1]:
        for col_num, col in enumerate(row):
            if isinstance(col, Number):
                for i in range(1, 4 - row_num):
                    if isinstance(board[row_num + i][col_num], Number):
                        if not board[row_num + i - 1][col_num].merge(board[row_num + i][col_num]):
                            break
                    board[row_num + i][col_num] = col
                    board[row_num + i - 1][col_num] = "    "
        row_num -= 1
                
    return board
    

def left(board) -> list:
    
    for row_num, row in enumerate(board):
        col_num = 1
        for col in row[1:]:
            if isinstance(col, Number):
                for i in range(1, 1 + col_num):
                    if isinstance(board[row_num][col_num - i], Number):
                        if not board[row_num][col_num - i + 1].merge(board[row_num][col_num - i]):
                            break
                    board[row_num][col_num - i] = col
                    board[row_num][col_num - i + 1] = "    "
            col_num += 1
                
    return board
    

def right(board) -> list:
    
    for row_num, row in enumerate(board):
        col_num = 2
        for col in row[:-1][::-1]:
            if isinstance(col, Number):
                for i in range(1, 4 - col_num):
                    if isinstance(board[row_num][col_num + i], Number):
                        if not board[row_num][col_num + i - 1].merge(board[row_num][col_num + i]):
                            break
                    board[row_num][col_num + i] = col
                    board[row_num][col_num + i - 1] = "    "
            col_num -= 1
                
    return board
    
    
def check_win(window) -> bool:
    
    if 2048 in [i.num for i in Numbers.nums]:
        window.addstr("YOU WIN!")
        if window.getkey():
            
            return True
    return False


def check_lose(window, board) -> bool:

    b = [[e for e in i] for i in board] #IM REFERENCING IT BUT .COPY DOESNT WORK CAUSE IT 2d LIST FUCK!

    for row in b:
        for col in row:
            if not isinstance(col, Number):
                return False
    
    if up(b) != board or down(b) != board or left(b) != board or right(b) != board:
        return False

    window.addstr("YOU LOSE!")
    if window.getkey():
        return True


def main(window) -> None:
    
    window.keypad(True)
    window.nodelay(False)
    #window.scrollok(True)
    curses.noecho()
    curses.cbreak()
    #curses.start_color()
    #curses.use_default_colors()
    curses.curs_set(0)
    
    board = [
        [
            "    " for i in range(4)
        ] for e in range(4)
    ]
    
    while True:

        for row in board:
            window.addstr("  |")
            for col in row:
                window.addstr(str(col) + "|", curses.A_UNDERLINE)
            window.addstr("\n")
        
        window.refresh()
        
        if check_win(window):
            break
            
        if check_lose(window, board):
            break
        
        
        key = window.getkey()
        
        if key == "q":
            break
        elif key == "w" or key == "KEY_UP":
            board = up(board)
        elif key == "s" or key == "KEY_DOWN":
            board = down(board)
        elif key == "a" or key == "KEY_LEFT":
            board = left(board)
        elif key == "d" or key == "KEY_RIGHT":
            board = right(board)
        if key:
            can = False
            for i in range(len(board)):
                for e in range(len(board[i])):
                    if not isinstance(board[i][e], Number):
                        can = True
            while can:
                r, c = random.randint(0, 3), random.randint(0, 3)
                if not isinstance(board[r][c], Number):
                    board[r][c] = Number(2)
                    break
            
        window.clear()
    
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()

    
try:
    curses.wrapper(main)
except AttributeError as e:
    print("\n" + str(e))
    curses.endwin()
