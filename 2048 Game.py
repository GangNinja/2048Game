import random
import os

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.board[r][c] = 2 if random.random() < 0.9 else 4

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (self.size - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(self.size - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0
                self.score += row[i]
        return row

    def move_left(self):
        moved = False
        for i in range(self.size):
            compressed = self.compress(self.board[i])
            merged = self.merge(compressed)
            compressed = self.compress(merged)
            if self.board[i] != compressed:
                moved = True
            self.board[i] = compressed
        if moved:
            self.add_new_tile()

    def move_right(self):
        self.board = [row[::-1] for row in self.board]
        self.move_left()
        self.board = [row[::-1] for row in self.board]

    def move_up(self):
        self.board = list(map(list, zip(*self.board)))
        self.move_left()
        self.board = list(map(list, zip(*self.board)))

    def move_down(self):
        self.board = list(map(list, zip(*self.board)))
        self.move_right()
        self.board = list(map(list, zip(*self.board)))

    def is_game_over(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return False
                if c < self.size - 1 and self.board[r][c] == self.board[r][c + 1]:
                    return False
                if r < self.size - 1 and self.board[r][c] == self.board[r + 1][c]:
                    return False
        return True

    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\033[1;33m2048 GAME\033[0m")
        print(f"\033[1;34mScore: {self.score}\033[0m\n")
        for row in self.board:
            print(" | ".join(f"\033[1;32m{num:4}\033[0m" if num != 0 else "    " for num in row))
            print("-" * (self.size * 6))

    def play(self):
        while not self.is_game_over():
            self.display()
            move = input("\033[1;36mEnter move (W/A/S/D): \033[0m").strip().upper()
            if move == 'W':
                self.move_up()
            elif move == 'A':
                self.move_left()
            elif move == 'S':
                self.move_down()
            elif move == 'D':
                self.move_right()
            else:
                print("\033[1;31mInvalid move! Use W/A/S/D.\033[0m")
        
        self.display()
        print("\033[1;31mGame Over! Final Score:\033[0m", self.score)

if __name__ == "__main__":
    game = Game2048()
    game.play()

