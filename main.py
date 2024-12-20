#Требуется разработать компьютерную игру «крестики-нолики».
#Минимальные требования:
#1.Графичекский интерфейс (использовать внутреннюю библиотеку питона  tkinter).
#2.Игра с приложением (приложение не должно проигрывать)
#3. Минимальный комплект программной документации в соответствии с ГОСТ 19 группы:
#  1.1.Техническое задание
#  1.2.Пояснительная записка
#  1.3.Руководство программиста
#4. Тестовая документация:
#  2.1. Mind map
#  2.2. Чек-лист
#  2.3. Набор тест-кейсов

import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.current_player = None
        self.ai_player = None
        self.board = [""] * 9
        self.buttons = []
        self.player_choices = {}  # Словарь для хранения выбора игрока

        self.create_start_screen()

    def create_start_screen(self):
        self.clear_window()

        # Запрос игроку о выборе за кого играть
        label = tk.Label(self.root, text="Выбери за кого играть:", font=("Arial", 14))
        label.pack(pady=20)

        x_button = tk.Button(self.root, text="Крестики (X)", font=("Arial", 12), command=lambda: self.start_game("X"))
        x_button.pack(side=tk.LEFT, padx=50)

        o_button = tk.Button(self.root, text="Нолики (O)", font=("Arial", 12), command=lambda: self.start_game("O"))
        o_button.pack(side=tk.RIGHT, padx=50)


    def start_game(self, player_choice):
        self.player_choices['player'] = player_choice
        self.ai_player = "O" if player_choice == "X" else "X"
        self.current_player = "X"
        self.create_board()
        if self.current_player == self.ai_player:
          self.ai_move()


    def clear_window(self):
      for widget in self.root.winfo_children():
        widget.destroy()

    def create_board(self):
        self.clear_window()
        for i in range(9):
            button = tk.Button(self.root, text="", font=("Arial", 40), width=3, height=1,
                             command=lambda i=i: self.player_move(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def player_move(self, position):
      if self.board[position] == "":
          self.board[position] = self.current_player
          self.buttons[position].config(text=self.current_player)
          if self.check_winner(self.current_player):
            self.game_over(f"Игрок ({self.current_player}) победил!")
            return
          if self.check_draw():
            self.game_over("Ничья!")
            return
          self.current_player = self.ai_player
          self.ai_move()

    def ai_move(self):
      best_move = self.minimax(self.board, self.ai_player)[1]
      self.board[best_move] = self.ai_player
      self.buttons[best_move].config(text=self.ai_player)
      if self.check_winner(self.ai_player):
            self.game_over(f"ИИ ({self.ai_player}) победил!")
            return
      if self.check_draw():
            self.game_over("Ничья!")
            return
      self.current_player = self.player_choices['player']

    def minimax(self, board, player):
        available_moves = [i for i, x in enumerate(board) if x == ""]

        if self.check_winner(self.ai_player, board):
            return 1, None
        if self.check_winner(self.player_choices['player'], board):
            return -1, None
        if not available_moves:
            return 0, None
        
        if player == self.ai_player:
            best_score = -float('inf')
            best_move = None
            for move in available_moves:
                board[move] = player
                score = self.minimax(board, self.player_choices['player'])[0]
                board[move] = ""
                if score > best_score:
                  best_score = score
                  best_move = move
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for move in available_moves:
                board[move] = player
                score = self.minimax(board, self.ai_player)[0]
                board[move] = ""
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    def check_winner(self, player, board = None):
        if board is None:
          board = self.board

        winning_combinations = [
          [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтали
          [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикали
          [0, 4, 8], [2, 4, 6]  # Диагонали
          ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
              return True
        return False

    def check_draw(self):
      return all(cell != "" for cell in self.board)

    def game_over(self, message):
      messagebox.showinfo("Игра окончена", message)
      self.ask_play_again()

    def ask_play_again(self):
      answer = messagebox.askyesno("Игра окончена", "Хотите сыграть еще раз?")
      if answer:
          self.board = [""] * 9
          self.buttons = []
          self.create_start_screen()
      else:
          self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()