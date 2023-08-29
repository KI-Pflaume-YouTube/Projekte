#Tik Tak Toe

import tkinter as tk
from tkinter import messagebox, simpledialog

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = [' '] * 9
        self.current_sign = 'X'
        self.vs_computer = messagebox.askyesno("Wahl des Gegners", "Möchtest du gegen den Computer spielen?")
        self.buttons = [tk.Button(root, text=" ", font='Arial 20', width=5, height=2, command=lambda i=i: self.make_move(i)) for i in range(9)]
        for i, button in enumerate(self.buttons):
            row = i // 3
            col = i % 3
            button.grid(row=row, column=col)

    def is_winner(self, sign):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combination in winning_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] == sign:
                return True
        return False

    def is_full(self):
        return ' ' not in self.board

    def change_player(self):
        self.current_sign = 'X' if self.current_sign == 'O' else 'O'

    def make_move(self, position):
        if self.vs_computer and self.current_sign == 'O':
            return
        if self.board[position] == ' ':
            self.board[position] = self.current_sign
            self.buttons[position].config(text=self.current_sign)
            if self.is_winner(self.current_sign):
                self.end_game(f"Spieler {self.current_sign} gewinnt!")
                return
            elif self.is_full():
                self.end_game("Unentschieden!")
                return
            self.change_player()
            if self.vs_computer and self.current_sign == 'O':
                self.computer_move()

    def computer_move(self):
        best_score = float('-inf')
        best_move = None
        for i, spot in enumerate(self.board):
            if spot == ' ':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        self.board[best_move] = 'O'
        self.buttons[best_move].config(text='O')
        if self.is_winner('O'):
            self.end_game("Der Computer gewinnt!")
        elif self.is_full():
            self.end_game("Unentschieden!")
        else:
            self.change_player()

    def minimax(self, board, depth, is_maximizing):
        if self.is_winner('O'):
            return 10 - depth
        if self.is_winner('X'):
            return depth - 10
        if self.is_full():
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for i, spot in enumerate(board):
                if spot == ' ':
                    board[i] = 'O'
                    evaluation = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    max_eval = max(max_eval, evaluation)
            return max_eval
        else:
            min_eval = float('inf')
            for i, spot in enumerate(board):
                if spot == ' ':
                    board[i] = 'X'
                    evaluation = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    min_eval = min(min_eval, evaluation)
            return min_eval

    def end_game(self, message):
        messagebox.showinfo("Spiel beendet", message)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    if game.vs_computer and game.current_sign == 'O':
        game.computer_move()
    root.mainloop()
