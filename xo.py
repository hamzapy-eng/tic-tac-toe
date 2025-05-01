import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QGridLayout, 
                            QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, 
                            QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe - Neo Edition")
        self.setFixedSize(350, 450)
        self.current_player = "X"  # Human is X, AI is O
        self.board = [""] * 9
        self.difficulty = "medium"  # Default difficulty

        # Set neo-style palette
        self.set_neo_style()
        self.init_ui()

    def set_neo_style(self):
        # Dark color scheme with green accents
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(10, 15, 20))
        dark_palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
        dark_palette.setColor(QPalette.Base, QColor(20, 25, 30))
        dark_palette.setColor(QPalette.AlternateBase, QColor(30, 35, 40))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 255, 0))
        dark_palette.setColor(QPalette.ToolTipText, QColor(10, 15, 20))
        dark_palette.setColor(QPalette.Text, QColor(0, 255, 0))
        dark_palette.setColor(QPalette.Button, QColor(20, 25, 30))
        dark_palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(0, 150, 0))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(dark_palette)
        
        # Set font
        self.setFont(QFont("Courier New", 10))

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("NEO TIC TAC TOE")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Courier New", 16, QFont.Bold))
        title.setStyleSheet("color: #00ff00;")
        layout.addWidget(title)

        # Difficulty selection
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel("DIFFICULTY:")
        difficulty_label.setFont(QFont("Courier New", 10, QFont.Bold))
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["EASY", "MEDIUM", "HARD"])
        self.difficulty_combo.setFont(QFont("Courier New", 10))
        self.difficulty_combo.setStyleSheet("""
            QComboBox {
                background-color: #141e26;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.difficulty_combo.currentTextChanged.connect(self.set_difficulty)
        
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        layout.addLayout(difficulty_layout)

        # Game status
        self.status_label = QLabel(f"PLAYER {self.current_player}'S TURN")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Courier New", 12, QFont.Bold))
        self.status_label.setStyleSheet("color: #00ff00;")
        layout.addWidget(self.status_label)

        # Game board
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)
        self.buttons = []

        for i in range(9):
            btn = QPushButton("")
            btn.setFixedSize(80, 80)
            btn.setFont(QFont("Courier New", 24, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #141e26;
                    color: #00ff00;
                    border: 2px solid #00ff00;
                    border-radius: 0px;
                }
                QPushButton:hover {
                    background-color: #1e2b37;
                    border: 2px solid #00ff88;
                }
                QPushButton:pressed {
                    background-color: #0f151a;
                }
            """)
            btn.clicked.connect(lambda _, index=i: self.handle_click(index))
            self.grid_layout.addWidget(btn, i // 3, i % 3)
            self.buttons.append(btn)

        layout.addLayout(self.grid_layout)

        # Reset Button
        reset_layout = QHBoxLayout()
        self.reset_button = QPushButton("RESET MATRIX")
        self.reset_button.setFont(QFont("Courier New", 10, QFont.Bold))
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #141e26;
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 8px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #1e2b37;
                border: 2px solid #00ff88;
            }
            QPushButton:pressed {
                background-color: #0f151a;
            }
        """)
        self.reset_button.clicked.connect(self.reset_game)
        reset_layout.addStretch()
        reset_layout.addWidget(self.reset_button)
        reset_layout.addStretch()

        layout.addLayout(reset_layout)

        self.setLayout(layout)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty.lower()
        self.reset_game()

    def handle_click(self, index):
        if self.board[index] != "" or self.current_player == "O":
            return  # already played or AI's turn

        self.make_move(index, "X")
        
        if not self.check_game_over():
            self.ai_move()  # AI makes its move after player

    def make_move(self, index, player):
        self.board[index] = player
        color = "#00ffff" if player == "X" else "#ff00ff"  # Cyan for X, Magenta for O
        self.buttons[index].setText(player)
        self.buttons[index].setStyleSheet(f"""
            QPushButton {{
                background-color: #141e26;
                color: {color};
                border: 2px solid {color};
                border-radius: 0px;
            }}
        """)
        
        if self.check_win():
            winner = "HUMAN" if player == "X" else "SYSTEM"
            self.show_neo_message("MATRIX TERMINATED", f"{winner} VICTORY")
            self.disable_buttons()
        elif "" not in self.board:
            self.show_neo_message("MATRIX STALEMATE", "DRAW DETECTED")
            self.disable_buttons()
        else:
            self.current_player = "O" if player == "X" else "X"
            self.status_label.setText(f"PLAYER {self.current_player}'S TURN")

    def show_neo_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(f"<font color='#00ff00'>{message}</font>")
        msg.setFont(QFont("Courier New", 10))
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #141e26;
            }
            QLabel {
                color: #00ff00;
            }
            QPushButton {
                background-color: #141e26;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1e2b37;
                border: 1px solid #00ff88;
            }
        """)
        msg.exec_()

    def ai_move(self):
        if "" not in self.board:
            return

        if self.difficulty == "easy":
            move = self.easy_ai()
        elif self.difficulty == "medium":
            move = self.medium_ai()
        else:  # hard
            move = self.hard_ai()

        self.make_move(move, "O")

    def easy_ai(self):
        # Random moves
        empty_spots = [i for i, spot in enumerate(self.board) if spot == ""]
        return random.choice(empty_spots)

    def medium_ai(self):
        # Try to win, block opponent, or make random move
        empty_spots = [i for i, spot in enumerate(self.board) if spot == ""]
        
        # Check if AI can win
        for spot in empty_spots:
            self.board[spot] = "O"
            if self.check_win():
                self.board[spot] = ""
                return spot
            self.board[spot] = ""
        
        # Check if player can win and block
        for spot in empty_spots:
            self.board[spot] = "X"
            if self.check_win():
                self.board[spot] = ""
                return spot
            self.board[spot] = ""
        
        # Otherwise random
        return random.choice(empty_spots)

    def hard_ai(self):
        # Minimax algorithm - unbeatable AI
        best_score = -float('inf')
        best_move = None
        
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move

    def minimax(self, board, depth, is_maximizing):
        # Check terminal states
        if self.check_win_with_board(board, "O"):
            return 10 - depth
        if self.check_win_with_board(board, "X"):
            return depth - 10
        if "" not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def check_win_with_board(self, board, player):
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for a, b, c in combos:
            if board[a] == board[b] == board[c] == player:
                return True
        return False

    def check_win(self):
        return self.check_win_with_board(self.board, self.current_player)

    def check_game_over(self):
        return self.check_win() or "" not in self.board

    def disable_buttons(self):
        for btn in self.buttons:
            btn.setEnabled(False)

    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        for btn in self.buttons:
            btn.setText("")
            btn.setEnabled(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #141e26;
                    color: #00ff00;
                    border: 2px solid #00ff00;
                    border-radius: 0px;
                }
                QPushButton:hover {
                    background-color: #1e2b37;
                    border: 2px solid #00ff88;
                }
            """)
        self.status_label.setText(f"PLAYER {self.current_player}'S TURN")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicTacToe()
    window.show()
    sys.exit(app.exec_())