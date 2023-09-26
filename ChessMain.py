from os import listdir
from os.path import isfile, join
import pygame as p
import ChessEngine


WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}


imgs_folder = "images"
def loadImages():
    pieces = [f[:2] for f in listdir(imgs_folder) if isfile(join(imgs_folder, f))]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"{imgs_folder}/{piece}.png"),
            (SQUARE_SIZE, SQUARE_SIZE)
        )


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    loadImages()
    running = True
    square_selected = ()
    player_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                column = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE

                if square_selected == (row, column):
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (row, column)
                    player_clicks.append(square_selected)

                if len(player_clicks) == 2:
                    move = ChessEngine.Move(
                        player_clicks[0],
                        player_clicks[1],
                        game_state.board
                    )
                    print(move.getChessNotation())
                    game_state.makeMove(move)
                    square_selected = ()
                    player_clicks = []

        drawGameState(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, game_state):
    drawBoard(screen)
    drawPieces(screen, game_state.board)


COLORS_LIST = ["white", "gray"]
def drawBoard(screen):
    colors = [p.Color(c) for c in COLORS_LIST]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[(row + column) % 2]
            p.draw.rect(
                screen,
                color,
                p.Rect(
                    column * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
            )


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(
                    IMAGES[piece],
                    p.Rect(
                        column * SQUARE_SIZE,
                        row * SQUARE_SIZE,
                        SQUARE_SIZE,
                        SQUARE_SIZE
                    )
                )


if __name__ == "__main__":
    main()
