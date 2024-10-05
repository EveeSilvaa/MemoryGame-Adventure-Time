import pygame
import random
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Initialize Pygame
pygame.init()

# colors // # Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)  # Light pink for card backs // # Rosa claro para versos de cartão

# screen dimensions // # dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Time Memory Game")

# Load background music // # Carrega música de fundo
pygame.mixer.music.load("Musica Hora.mpeg")

# Load images // # Carregar imagens
icon_paths = ["src/fin.jpg", "src/jake.jpg", "src/jujuba.jpg", "src/marcelinne.jpg", "src/princesa de fogo.jpg", "src/caroço.jpg", "src/Ricardio.jpg", "src/mordomo menta.jpg", "src/rei gelado.jpg", "src/canelinha.jpg", "src/gunther.jpg", "src/Angry lemongrab.jpg", "src/simon.webp", "src/rei da noitosfera.jpg", "src/lady iris.jpg"]
icons = [pygame.image.load(path) for path in icon_paths]

# Function to shuffle icons // # Função para embaralhar ícones
def shuffle_icons():
    icons_pair = icons * 2 
    random.shuffle(icons_pair)
    return icons_pair

class MemoryGame:
    def __init__(self, rows, cols, mode):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.selected = []
        self.matched = []
        self.mode = mode
        self.moves = 0
        self.start_time = pygame.time.get_ticks()
        self.card_width = SCREEN_WIDTH // self.cols - 10
        self.card_height = SCREEN_HEIGHT // self.rows - 10
        self.reset_grid()

    def reset_grid(self):
        shuffled_icons = shuffle_icons()
        index = 0
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = shuffled_icons[index]
                index += 1

    def draw_grid(self):
        screen.fill(WHITE)
        for i in range(self.rows):
            for j in range(self.cols):
                x = j * (self.card_width + 10) + 5
                y = i * (self.card_height + 10) + 5
                if (i, j) in self.matched or (i, j) in self.selected:
                    screen.blit(pygame.transform.scale(self.grid[i][j], (self.card_width, self.card_height)), (x, y))
                else:
                    pygame.draw.rect(screen, BLACK, (x, y, self.card_width, self.card_height))
                    pygame.draw.rect(screen, PINK, (x + 2, y + 2, self.card_width - 4, self.card_height - 4))  # Inner card color
        pygame.display.flip()

    def check_match(self):
        time.sleep(0.5)
        if len(self.selected) == 2:
            if self.grid[self.selected[0][0]][self.selected[0][1]] == self.grid[self.selected[1][0]][self.selected[1][1]]:
                self.matched.extend(self.selected)
            self.selected = []
            self.moves += 1

    def check_game_over(self):
        return len(self.matched) == self.rows * self.cols

    def game_loop(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if len(self.selected) < 2:
                        mouse_x, mouse_y = event.pos
                        row = (mouse_y - 5) // (self.card_height + 10)
                        col = (mouse_x - 5) // (self.card_width + 10)
                        if (row, col) not in self.selected and (row, col) not in self.matched:
                            self.selected.append((row, col))

            self.draw_grid()
            self.check_match()

            if self.check_game_over():
                self.end_game()
                running = False

            if self.mode == "time":
                elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
                if elapsed_time >= 60:  # Time limit of 60 seconds // # Limite de tempo de 60 segundos
                    self.end_game()
                    running = False

            clock.tick(30)

        pygame.quit()

    def end_game(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        result_message = f"Game Over!\nMoves: {self.moves}\nTime: {elapsed_time} seconds" if self.mode == "time" else f"Game Over!\nMoves: {self.moves}"
        messagebox.showinfo("Game Over", result_message)
        pygame.quit()
        main_menu()

def start_game(rows, cols, mode):
    pygame.mixer.music.play(0,5)
    game = MemoryGame(rows, cols, mode)
    game.game_loop()

def main_menu():
    root = tk.Tk()
    root.title("Adventure Time Memory Game")

    bg_img = Image.open("src/horaDaventura background.jpg")
    bg_img = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(relwidth=1, relheight=1)

    def on_start_click(level, mode):
        level_data = {
            0: (3, 4),  # Easy // # Fácil
            1: (4, 5),  # Medium // # Médio
            2: (5, 6)   # Hard // # Dificil
        }
        rows, cols = level_data.get(level, (3, 4))
        root.destroy()
        start_game(rows, cols, mode)

    def show_level_selection(mode):
        level_window = tk.Toplevel(root)
        level_window.title("Select Difficulty")

        tk.Label(level_window, text="Select Difficulty:", font=("Arial", 18)).pack(pady=20)
        
        tk.Button(level_window, text="Easy (3x4)", command=lambda: on_start_click(0, mode)).pack(pady=10)
        tk.Button(level_window, text="Medium (4x5)", command=lambda: on_start_click(1, mode)).pack(pady=10)
        tk.Button(level_window, text="Hard (5x6)", command=lambda: on_start_click(2, mode)).pack(pady=10)

    def show_mode_selection():
        mode_window = tk.Toplevel(root)
        mode_window.title("Select Mode")

        tk.Label(mode_window, text="Select Mode:", font=("Arial", 18)).pack(pady=20)

        tk.Button(mode_window, text="Practice Mode", command=lambda: show_level_selection("practice")).pack(pady=10)
        tk.Button(mode_window, text="Time Management", command=lambda: show_level_selection("time")).pack(pady=10)
        tk.Button(mode_window, text="Move Limit", command=lambda: show_level_selection("moves")).pack(pady=10)

    tk.Button(root, text="Start Game", command=show_mode_selection, height=2, width=20).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    main_menu()
