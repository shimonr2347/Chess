import tkinter as tk
from tkinter import ttk
import chess
import chess.pgn
import os
from pathlib import Path

class ChessSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game Viewer")
        self.root.geometry("900x600")
        
        # --- Data State ---
        self.board = chess.Board()
        self.moves = []
        self.move_index = 0
        self.base_dir = Path("splited_pgns")

        self.paned = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # --- Sidebar for Game List ---
        self.side_frame = tk.Frame(self.paned, width=250, bg="#f0f0f0")
        self.paned.add(self.side_frame)
        
        tk.Label(self.side_frame, text="Select Game:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=5)

        self.tree = ttk.Treeview(self.side_frame)
        self.tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        self.refresh_tree()
        
        # --- Main Board Area ---
        self.center_frame = tk.Frame(self.paned, bg="#ffffff")
        self.paned.add(self.center_frame)
        
        self.square_size = 50
        self.offset = 30
        self.canvas_size = self.square_size * 8 + self.offset * 2

        self.canvas = tk.Canvas(self.center_frame, width=self.canvas_size, height=self.canvas_size, bg="#ffffff")
        self.canvas.pack(pady=40)
        
        # --- Control Buttons ---
        self.btn_frame = tk.Frame(self.center_frame)
        self.btn_frame.pack(pady=0)

        btn_style = {
            "font": ("Arial", 11, "bold"),
            "width": 8,
            "bg": "#4a4a4a",
            "fg": "white",
            "activebackground": "#666666",
            "cursor": "hand2", # Changes mouse to a hand icon on hover
            "bd": 0,           # Removes the thick 3D border
            "pady": 5
        }
        
        tk.Button(self.btn_frame, text="Start", command=self.go_to_start, **btn_style).pack(side=tk.LEFT, padx=2)
        tk.Button(self.btn_frame, text="Prev", command=self.move_back, **btn_style).pack(side=tk.LEFT, padx=2)
        tk.Button(self.btn_frame, text="Next", command=self.move_forward, **btn_style).pack(side=tk.LEFT, padx=2)
        tk.Button(self.btn_frame, text="End", command=self.go_to_end, **btn_style).pack(side=tk.LEFT, padx=2)

        self.info_frame = tk.Frame(self.paned, width=250, bg="#f0f0f0")
        self.paned.add(self.info_frame)

        tk.Label(self.info_frame, text="Game Info:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=5)
        self.metadata_text = tk.Text(self.info_frame, height=15, width=30, state=tk.DISABLED, font=("Consolas", 9))
        self.metadata_text.pack(padx=10, pady=5)

        self.move_label = tk.Label(self.info_frame, text="Current Move 0/0:", font=("Arial", 15, "bold"), bg="#f0f0f0")
        self.move_label.pack(pady=10)        
        
        # tk.Label(self.info_frame, text="Current Move:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=0)
        self.current_move_text = tk.Label(self.info_frame, text="Select a game", font=("Consolas", 15), bg="#f0f0f0", wraplength=200, justify="center")
        self.current_move_text.pack(padx=10, pady=5)


        self.draw_board()

    def refresh_tree(self):
        """Finds all .pgn files in the directory."""
        base = Path(self.base_dir)

        if not base.exists():
            print(f"Directory '{self.base_dir}' not found.")
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        for folder in sorted([f for f in base.iterdir() if f.is_dir()]):
            node = self.tree.insert("", "end", text=folder.name, open=True)
            for pgn_file in sorted(folder.glob("*.pgn")):
                self.tree.insert(node, "end", text=pgn_file.name, values=(str(pgn_file.absolute()),))

    def on_tree_select(self, event):
        """Triggered when a user clicks a game in the list."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item, "values")
        if values:
            pgn_path = values[0]
            self.load_pgn(pgn_path)


    def load_pgn(self, path):
        try:
            path_obj = Path(path)
            with path_obj.open('r', encoding='utf-8') as f:
                game = chess.pgn.read_game(f)
                if game:
                    self.update_metadata_display(game.headers)
                    self.game_result = game.headers.get("Result", "*")
                    self.moves = list(game.mainline_moves())
                    self.board = game.board()
                    self.move_index = 0
                    self.update_ui()
        except Exception as e:
            print(f"Error loading PGN: {e}")

    def update_metadata_display(self, headers):
        self.metadata_text.config(state=tk.NORMAL)
        self.metadata_text.delete(1.0, tk.END)
        for key, value in headers.items():
            self.metadata_text.insert(tk.END, f"{key}: {value}\n")
        self.metadata_text.config(state=tk.DISABLED)

    def draw_board(self):
        self.canvas.delete("all")
        off = self.offset
        square = self.square_size # Square size

        for i in range(8):
            label_x = off + i * square + square // 2
            label_y = off + 8 * square + off // 2
            self.canvas.create_text(label_x, label_y, text=chess.FILE_NAMES[i], font=("Arial", 12, "bold"))

            num_x = off // 2
            num_y = off + (7 - i) * square + square // 2
            self.canvas.create_text(num_x, num_y, text=str(i + 1), font=("Arial", 12, "bold"))

        for r in range(8):
            for c in range(8):
                x1 = off + c * square
                y1 = off + r * square
                x2 = x1 + square
                y2 = y1 + square

                color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
                # Render piece symbol
                sqr = chess.square(c, 7-r)
                piece = self.board.piece_at(sqr)
                if piece:
                    self.canvas.create_text(x1 + (square // 2), y1 + (square // 2), text=piece.unicode_symbol(), font=("Arial", 30))

    def update_ui(self):
        self.draw_board()
        self.move_label.config(text=f"Current Move {self.move_index}/{len(self.moves)}:")
        if self.move_index == 0:
            self.current_move_text.config(text="", fg="black")
            return
        
        if self.move_index == len(self.moves):
            outcome_text = self.get_outcome_description()
            self.current_move_text.config(text=outcome_text, fg="red")
            return
        # self.current_move_text.config(text="")
        # self.current_move_text.config(state=tk.NORMAL)
        # self.current_move_text.delete(1.0, tk.END)
        # if self.move_index < len(self.moves):
        #     start, end = self.moves[self.move_index].uci()[:2], self.moves[self.move_index].uci()[2:]
        #     move = self.moves[self.move_index]
        #     piece = self.board.piece_at(move.from_square)
        #     self.current_move_text.insert(tk.END, f"Current Move: {start} → {end}, {piece.unicode_symbol()}")
        #     print(f"Current Move: {start} → {end}")
        # self.current_move_text.config(state=tk.DISABLED)

    def get_outcome_description(self):
        # Check board state first
        if self.board.is_checkmate():
            winner = "White" if self.board.turn == chess.BLACK else "Black"
            return f"CHECKMATE! {winner} wins."
        
        if self.board.is_stalemate():
            return "Draw by Stalemate"
        
        if self.board.is_insufficient_material():
            return "Draw by Insufficient Material"

        # If the board isn't in a terminal state but the moves ended, 
        # it's a resignation or an agreed draw based on the PGN header.
        if self.game_result == "1-0":
            return "White wins by Black Resignation"
        elif self.game_result == "0-1":
            return "Black wins by White Resignation"
        elif self.game_result == "1/2-1/2":
            return "Game Drawn by Agreement"
        
        return f"Game Over: {self.game_result}"


    def get_human_move(self, move):
        # 1. Identity of the piece
        piece = self.board.piece_at(move.from_square)
        if not piece: return "Unknown move" # Safety check
        
        piece_name = chess.piece_name(piece.piece_type).capitalize()
        color = "White" if piece.color == chess.WHITE else "Black"
        start = chess.square_name(move.from_square)
        end = chess.square_name(move.to_square)
        
        # 2. Check for special actions
        is_capture = self.board.is_capture(move)
        is_en_passant = self.board.is_en_passant(move)
        
        # 3. Handle Castling explicitly
        if piece.piece_type == chess.KING:
            # Kingside: White e1->g1 (6), Black e8->g8 (62)
            if move.from_square == chess.E1 and move.to_square == chess.G1:
                return f"White short castles Kingside"
            if move.from_square == chess.E8 and move.to_square == chess.G8:
                return f"Black short castles Kingside"
            # Queenside: White e1->c1 (2), Black e8->c8 (58)
            if move.from_square == chess.E1 and move.to_square == chess.C1:
                return f"White long castles Queenside"
            if move.from_square == chess.E8 and move.to_square == chess.C8:
                return f"Black long castles Queenside"

        # 4. Prepare for Check/Mate analysis
        # We apply the move to see the state of the board AFTER the move
        self.board.push(move)
        is_checkmate = self.board.is_checkmate()
        is_check = self.board.is_check()
        self.board.pop() # Return to current state

        # 5. Build the description
        verb = "captures" if is_capture or is_en_passant else "moves"
        description = f"{color} {piece_name} {verb} from {start} to {end}"

        # 6. Handle Promotions (e.g., Pawn to Queen)
        if move.promotion:
            promo_piece = chess.piece_name(move.promotion).capitalize()
            description += f" and promotes to a {promo_piece}"

        # 7. Add Status tags
        if is_checkmate:
            description += " - CHECKMATE!"
        elif is_check:
            description += " - Check!"

        return f"{description}"

    def move_forward(self):
        if self.move_index < len(self.moves):
            current_move = self.moves[self.move_index]
            readable_move = self.get_human_move(current_move)
            print(readable_move)
            self.current_move_text.config(text=readable_move, fg="black")
            self.board.push(current_move)
            self.move_index += 1
            self.update_ui()

    def move_back(self):
        if self.move_index > 0:
            self.move_index -= 1
            self.board.pop()

            if self.move_index > 0:
                prev_move = self.moves[self.move_index - 1]
                state_before = self.board.pop()
                readable_move = f"Back to: {self.get_human_move(prev_move)}"
                self.board.push(state_before) # Restore state after analysis
            else:
                readable_move = "Back to start"

            print(readable_move)
            self.current_move_text.config(text=readable_move, fg="black")
            self.update_ui()    

    def go_to_start(self):
        while self.move_index > 0:
            self.move_back()

    def go_to_end(self):
        while self.move_index < len(self.moves):
            self.move_forward()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessSimulator(root)
    root.mainloop()