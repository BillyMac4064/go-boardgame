import math
import pygame
import sys
import numpy as np
import copy

# Constants
num_rows = 19
num_cols = 19
turn = 0
captured = []
invalid_msg = "Sorry you cannot place a piece there"
over_msg = "Game is over... Counting points..."

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
OAK = (204, 153, 0)
MELLOW_APRICOT = (248, 184, 120)
dark_grey = (105,105,105)
light_grey = (211,211,211)
gainsboro = (230, 230, 230)
bright_green = (0,255,0)

pygame.init()

SQUARESIZE = 44

width = num_cols * SQUARESIZE
height = num_rows * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

# Images
background = pygame.image.load("Blank_Go_board.png")
background = pygame.transform.scale(background, (width, height))

intro_background = pygame.image.load("go_background.jpg")
intro_background = pygame.transform.scale(intro_background, (width, height))

black_piece = pygame.image.load("black_go_piece.png")
white_piece = pygame.image.load("white_go_piece.png")
black_piece = pygame.transform.scale(black_piece, (SQUARESIZE, SQUARESIZE))
white_piece = pygame.transform.scale(white_piece, (SQUARESIZE, SQUARESIZE))

def create_board():
    board = np.zeros((num_rows, num_cols))
    return board

def print_board(board):
    print(board)
    
def draw_board(board):
    screen.blit(background, (0,0))
    for c in range(num_cols):
        for r in range(num_rows):
            if board[r][c] == 1:
                if r < 9 and c < 9:
                    screen.blit(black_piece, ((c * SQUARESIZE) + 2,(r * SQUARESIZE) + 2))
                elif r < 9 and c == 9:
                    screen.blit(black_piece, ((c * SQUARESIZE),(r * SQUARESIZE) + 2))
                elif r < 9 and c > 9:
                    screen.blit(black_piece, ((c * SQUARESIZE) - 2,(r * SQUARESIZE) + 2))
                elif r == 9 and c < 9:
                    screen.blit(black_piece, ((c * SQUARESIZE) + 2,(r * SQUARESIZE)))
                elif r == 9 and c == 9:
                    screen.blit(black_piece, ((c * SQUARESIZE),(r * SQUARESIZE)))
                elif r == 9 and c > 9:
                    screen.blit(black_piece, ((c * SQUARESIZE) - 2,(r * SQUARESIZE)))
                elif r > 9 and c < 9:
                    screen.blit(black_piece, ((c * SQUARESIZE) + 2,(r * SQUARESIZE) - 2))
                elif r > 9 and c == 9:
                    screen.blit(black_piece, ((c * SQUARESIZE) ,(r * SQUARESIZE) - 2))
                elif r > 9 and c > 9:
                    screen.blit(black_piece, ((c * SQUARESIZE) - 2,(r * SQUARESIZE) - 2))
            elif board[r][c] == 2:
                if r < 9 and c < 9:
                    screen.blit(white_piece, ((c * SQUARESIZE) + 2,(r * SQUARESIZE) + 2))
                elif r < 9 and c == 9:
                    screen.blit(white_piece, ((c * SQUARESIZE),(r * SQUARESIZE) + 2))
                elif r < 9 and c > 9:
                    screen.blit(white_piece, ((c * SQUARESIZE) - 2,(r * SQUARESIZE) + 2))
                elif r == 9 and c < 9:
                    screen.blit(white_piece, ((c * SQUARESIZE) + 2,(r * SQUARESIZE)))
                elif r == 9 and c == 9:
                    screen.blit(white_piece, ((c * SQUARESIZE),(r * SQUARESIZE)))
                elif r == 9 and c > 9:
                    screen.blit(white_piece, ((c * SQUARESIZE) - 2,(r * SQUARESIZE)))
                elif r > 9 and c < 9:
                    screen.blit(white_piece, ((c * SQUARESIZE) + 2,(r * SQUARESIZE) - 2))
                elif r > 9 and c == 9:
                    screen.blit(white_piece, ((c * SQUARESIZE) ,(r * SQUARESIZE) - 2))
                elif r > 9 and c > 9:
                    screen.blit(white_piece, ((c * SQUARESIZE) - 2,(r * SQUARESIZE) - 2))                
    pygame.display.update()

# Initializing the initial board
board = create_board()
print_board(board)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

clock = pygame.time.Clock()

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_on_edge(board, row, col):
    if row == 0 or row == num_rows - 1 or col == 0 or col == num_cols - 1:
        return True

def is_corner(board, row, col):
    if row == 0 and col == 0 or row == 0 and col == num_cols - 1 or row == num_rows - 1 and col == 0 or row == num_rows - 1 and col == num_cols - 1:
        return True

def is_valid_location(board, row, col, piece):    
    # Valid positions
    if board[row][col] == 0:
        if is_corner(board, row, col):
            if row == 0 and col == 0:
                if board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row][col + 1] == 0 or board[row][col + 1] == piece:
                    return True
                else:
                    return False
            elif row == 0 and col == num_cols - 1:
                if board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row][col - 1] == 0 or board[row][col - 1] == piece:
                    return True
                else:
                    return False  
            elif row == num_rows - 1 and col == 0:
                if board[row - 1][col] == 0 or board[row - 1][col] == piece or board[row][col + 1] == 0 or board[row][col + 1] == piece:
                    return True
                else:
                    return False
            elif row == num_rows - 1 and col == num_cols - 1:
                if board[row - 1][col] == 0 or board[row - 1][col] == piece or board[row][col - 1] == 0 or board[row][col - 1] == piece:
                    return True
                else:
                    return False
        elif is_on_edge(board, row, col):
            if row == 0:
                if board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row][col + 1] == 0 or board[row][col + 1] == piece or board[row][col - 1] == 0 or board[row][col - 1] == piece:
                    return True
                else:
                    return False
            elif row == num_rows - 1:
                if board[row - 1][col] == 0 or board[row - 1][col] == piece or board[row][col + 1] == 0 or board[row][col + 1] == piece or board[row][col - 1] == 0 or board[row][col - 1] == piece:
                    return True
                else:
                    return False
            elif col == 0:
                if board[row][col + 1] == 0 or board[row][col + 1] == piece or board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row - 1][col] == 0 or board[row - 1][col] == piece:
                    return True
                else:
                    return False
            elif col == num_cols - 1:
                if board[row][col - 1] == 0 or board[row][col - 1] == piece or board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row - 1][col] == 0 or board[row - 1][col] == piece:
                    return True
                else:
                    return False        
        else:
            if board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row - 1][col] == 0 or board[row - 1][col] == piece or board[row][col + 1] == 0 or board[row][col + 1] == piece or board[row][col - 1] == 0 or board[row][col - 1] == piece:
                return True
            else:
                return False                
    else:
        return False

def is_still_valid(board, row, col, piece):
    if is_corner(board, row, col):
        if row == 0 and col == 0:
            if board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row][col + 1] == 0 or board[row][col + 1] == piece:
                return True
            else:
                return False
        elif row == 0 and col == num_cols - 1:
            if board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row][col - 1] == 0 or board[row][col - 1] == piece:
                return True
            else:
                return False  
        elif row == num_rows - 1 and col == 0:
            if board[row - 1][col] == 0 or board[row - 1][col] == piece or board[row][col + 1] == 0 or board[row][col + 1] == piece:
                return True
            else:
                return False
        elif row == num_rows - 1 and col == num_cols - 1:
            if board[row - 1][col] == 0 or board[row - 1][col] == piece or board[row][col - 1] == 0 or board[row][col - 1] == piece:
                return True
            else:
                return False
    elif is_on_edge(board, row, col):
        if row == 0:
            if board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row][col + 1] == 0 or board[row][col + 1] == piece or board[row][col - 1] == 0 or board[row][col - 1] == piece:
                return True
            else:
                return False
        elif row == num_rows - 1:
            if board[row - 1][col] == 0 or board[row - 1][col] == piece or board[row][col + 1] == 0 or board[row][col + 1] == piece or board[row][col - 1] == 0 or board[row][col - 1] == piece:
                return True
            else:
                return False
        elif col == 0:
            if board[row][col + 1] == 0 or board[row][col + 1] == piece or board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row - 1][col] == 0 or board[row - 1][col] == piece:
                return True
            else:
                return False
        elif col == num_cols - 1:
            if board[row][col - 1] == 0 or board[row][col - 1] == piece or board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row - 1][col] == 0 or board[row - 1][col] == piece:
                return True
            else:
                return False        
    else:
        if board[row + 1][col] == 0 or board[row + 1][col] == piece or board[row - 1][col] == 0 or board[row - 1][col] == piece or board[row][col + 1] == 0 or board[row][col + 1] == piece or board[row][col - 1] == 0 or board[row][col - 1] == piece:
            return True
        else:
            return False              
    
def update_board(board):
    for c in range(num_cols):
        for r in range(num_rows):
            if is_still_valid(board, r, c, board[r][c]) == False:
                captured.append(board[r][c])
                board[r][c] = 0

def flood_fill_acc(board, row, col, piece, potential, checked):
    if [row, col] in checked and board[row][col] == piece:
        for p in potential:
            board[p[0]][p[1]] = piece
        return None
    elif [row, col] in checked:
        return None
    if board[row][col] == 0:
        checked.append([row, col])
        for p in potential:
            board[p[0]][p[1]] = piece
        return None
    if board[row][col] == piece:
        potential.append([row, col])
        board[row][col] = 0
        checked.append([row, col])    
    elif board[row][col] != piece:
        checked.append([row, col])
        return None    
    # Recursive calls
    if is_corner(board, row, col):
        if row == 0 and col == 0:
            flood_fill_acc(board, row + 1, col, piece, potential, checked)
            flood_fill_acc(board, row, col + 1, piece, potential, checked)
        elif row == 0 and col == num_cols - 1:
            flood_fill_acc(board, row + 1, col, piece, potential, checked)
            flood_fill_acc(board, row, col - 1, piece, potential, checked)
        elif row == num_rows - 1 and col == 0:
            flood_fill_acc(board, row - 1, col, piece, potential, checked)
            flood_fill_acc(board, row, col + 1, piece, potential, checked)
        elif row == num_rows - 1 and col == num_cols - 1:
            flood_fill_acc(board, row - 1, col, piece, potential, checked)
            flood_fill_acc(board, row, col - 1, piece, potential, checked)
    elif is_on_edge(board, row, col):
        if row == 0:
            flood_fill_acc(board, row + 1, col, piece, potential, checked)
            flood_fill_acc(board, row, col + 1, piece, potential, checked)
            flood_fill_acc(board, row, col - 1, piece, potential, checked)
        elif row == num_rows - 1:
            flood_fill_acc(board, row - 1, col, piece, potential, checked)
            flood_fill_acc(board, row, col + 1, piece, potential, checked)
            flood_fill_acc(board, row, col - 1, piece, potential, checked)   
        elif col == 0:
            flood_fill_acc(board, row, col + 1, piece, potential, checked)
            flood_fill_acc(board, row + 1, col, piece, potential, checked)
            flood_fill_acc(board, row - 1, col, piece, potential, checked)
        elif col == num_cols - 1:
            flood_fill_acc(board, row, col - 1, piece, potential, checked)
            flood_fill_acc(board, row + 1, col, piece, potential, checked)
            flood_fill_acc(board, row - 1, col, piece, potential, checked)  
    else:
        flood_fill_acc(board, row + 1, col, piece, potential, checked)
        flood_fill_acc(board, row - 1, col, piece, potential, checked)
        flood_fill_acc(board, row, col + 1, piece, potential, checked)
        flood_fill_acc(board, row, col - 1, piece, potential, checked)

def flood_fill(board, row, col, piece):
    flood_fill_acc(board, row, col, piece, [], [])

# Check for is_corner and is_on_edge again    
def group_capture(board, piece):
    for c in range(num_cols):
        for r in range(num_rows):
            flood_fill(board, r, c, piece)

def is_valid_for_exception(board, row, col, piece):
    pass

# Exception where you my place where it is usually not a valid location but placing there will group capture the other player
def exception(board, row, col, piece, other):
    if is_still_valid(board, row, col, piece) == False:
        #Two copies to compare
        board_copy1 = copy.copy(board)
        board_copy2 = copy.copy(board)
        board_copy1[row][col] = piece
        board_copy2[row][col] = piece
        group_capture(board_copy1, other)
        if (board_copy1 == board_copy2).all():
            return False
        else:
            return True
                                                            
def ending_move(board, piece):
    # Check that all spaces are filled on the board
    # Check that all unfilled spaces (zeros) are not valid locations
    for c in range(num_cols):
        for r in range(num_rows):
            if turn == 0 and is_valid_location(board, r, c, 1):
                return False
            elif turn == 1 and is_valid_location(board, r, c, 2):
                return False
    return True

def manual_end(board, piece, other):
    p1_points = 0
    p2_points = 0
    for c in range(num_cols):
        for r in range(num_rows):
            if is_corner(board, r, c) and board[r][c] == 0:
                if r == 0 and c == 0:
                    if board[r + 1][c] == piece or board[r][c + 1] == piece:
                        p1_points += 1
                    elif board[r + 1][c] == other or board[r][c + 1] == other:
                        p2_points += 1
                elif r == 0 and c == num_cols - 1:
                    if board[r + 1][c] == piece or board[r][c - 1] == piece:
                        p1_points += 1
                    elif board[r + 1][c] == other or board[r][c - 1] == other:
                        p2_points += 1
                elif r == num_rows - 1 and c == 0:
                    if board[r - 1][c] == piece or board[r][c + 1] == piece:
                        p1_points += 1
                    elif board[r - 1][c] == other or board[r][c + 1] == other:
                        p2_points += 1
                elif r == num_rows - 1 and c == num_cols - 1:
                    if board[r - 1][c] == piece or board[r][c - 1] == piece:
                        p1_points += 1
                    elif board[r - 1][c] == other or board[r][c - 1] == other:
                        p2_points += 1
            elif is_on_edge(board, r, c) and board[r][c] == 0:
                if r == 0:
                    if board[r + 1][c] == piece or board[r][c + 1] == piece or board[r][c - 1] == piece:
                        p1_points += 1
                    elif board[r + 1][c] == other or board[r][c + 1] == other or board[r][c - 1] == other:
                        p2_points += 1
                elif r == num_rows - 1:
                    if board[r - 1][c] == piece or board[r][c + 1] == piece or board[r][c - 1] == piece:
                        p1_points += 1
                    elif board[r - 1][c] == other or board[r][c + 1] == other or board[r][c - 1] == other:
                        p2_points += 1
                elif c == 0:
                    if board[r][c + 1] == piece or board[r + 1][c] == piece or board[r - 1][c] == piece:
                        p1_points += 1
                    elif board[r][c + 1] == other or board[r + 1][c] == other or board[r - 1][c] == other:
                        p2_points += 1
                elif c == num_cols - 1:
                    if board[r][c - 1] == piece or board[r + 1][c] == piece or board[r - 1][c] == piece:
                        p1_points += 1 
                    elif board[r][c - 1] == other or board[r + 1][c] == other or board[r - 1][c] == other:
                        p2_points += 1
            elif board[r][c] == 0:
                if (board[r+1][c] or board[r-1][c] or board[r][c+1] or board[r][c-1]) == piece:
                    p1_points += 1
                elif (board[r+1][c] or board[r-1][c] or board[r][c+1] or board[r][c-1]) == other:
                    p2_points += 1
    
# After game is over
def calculate_points(board, piece):
    points = 0
    for c in range(num_cols):
        for r in range(num_rows):
            if is_corner(board, r, c) and board[r][c] == 0:
                if r == 0 and c == 0:
                    if board[r + 1][c] == piece or board[r][c + 1] == piece:
                        points += 1
                elif r == 0 and c == num_cols - 1:
                    if board[r + 1][c] == piece or board[r][c - 1] == piece:
                        points += 1
                elif r == num_rows - 1 and c == 0:
                    if board[r - 1][c] == piece or board[r][c + 1] == piece:
                        points += 1
                elif r == num_rows - 1 and c == num_cols - 1:
                    if board[r - 1][c] == piece or board[r][c - 1] == piece:
                        points += 1         
            elif is_on_edge(board, r, c) and board[r][c] == 0:
                if r == 0:
                    if board[r + 1][c] == piece or board[r][c + 1] == piece or board[r][c - 1] == piece:
                        points += 1
                elif r == num_rows - 1:
                    if board[r - 1][c] == piece or board[r][c + 1] == piece or board[r][c - 1] == piece:
                        points += 1
                elif c == 0:
                    if board[r][c + 1] == piece or board[r + 1][c] == piece or board[r - 1][c] == piece:
                        points += 1
                elif c == num_cols - 1:
                    if board[r][c - 1] == piece or board[r + 1][c] == piece or board[r - 1][c] == piece:
                        points += 1                              
            elif board[r][c] == 0:
                if (board[r+1][c] or board[r-1][c] or board[r][c+1] or board[r][c-1]) == piece:
                    points += 1
    return points

# Determine winner
def winner(p1, p2):
    if p1 > p2:
        return 1
    else:
        return 2

# Intro Screen
def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            print(event)
        #screen.blit(intro_background, (0,0))
        screen.fill(WHITE)
        
        #pygame.draw.rect(screen, light_grey, (218, 75, 418, 120)) 
        
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("GO", large_text)
        TextRect.center = ((width / 2), (height / 6))
        screen.blit(TextSurf, TextRect)        
        
        # A Chinese Board Game
        caption = pygame.font.Font('freesansbold.ttf', 30)
        textSurf, textRect = text_objects("A Chinese Board Game", caption)
        textRect.center = ((width / 2), (height / 3))
        screen.blit(textSurf, textRect)
        
        button("Play",318,600,200,60,light_grey,gainsboro,game_loop)
        #BOARD 9 13 19
        #Handicap 
        #Komi
        
        pygame.display.update()
        clock.tick(15)

# Actual Game
def game_loop():
    game_over = False
    turn = 0 
    draw_board(board)
    print_board(board)    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:                   
                if turn == 0:
                    posx = event.pos[0]
                    posy = event.pos[1]
                    r_coord = int(math.floor(posy / SQUARESIZE))
                    c_coord = int(math.floor(posx / SQUARESIZE))
                    
                    if r_coord >= num_rows or c_coord >= num_cols:
                        print(invalid_msg)
                        
                    elif is_valid_location(board, r_coord, c_coord, 1):
                        drop_piece(board, r_coord, c_coord, 1)
                        update_board(board)
                        group_capture(board, 2)
                        group_capture(board, 1)                    
                        turn += 1
                        turn = turn % 2
                        
                        if ending_move(board, 1):                      
                            game_over = True
        
                    elif exception(board, r_coord, c_coord, 1, 2) and board[r_coord][c_coord] == 0:
                        drop_piece(board, r_coord, c_coord, 1)
                        group_capture(board, 2)  
                        turn += 1
                        turn = turn % 2
                        
                        if ending_move(board, 1):
                            game_over = True
        
                    else:
                        print(invalid_msg)
                    
                    draw_board(board)
                    print_board(board)
                    
                elif turn == 1:
                    posx = event.pos[0]
                    posy = event.pos[1]
                    r_coord = int(math.floor(posy / SQUARESIZE))
                    c_coord = int(math.floor(posx / SQUARESIZE))
                    
                    if r_coord >= num_rows or c_coord >= num_cols:
                        print(invalid_msg)
                        
                    elif is_valid_location(board, r_coord, c_coord, 2):
                        drop_piece(board, r_coord, c_coord, 2)
                        update_board(board)
                        group_capture(board, 1)
                        group_capture(board, 2)
                        turn += 1
                        turn = turn % 2
                        
                        if ending_move(board, 2):
                            game_over = True
                        
                    elif exception(board, r_coord, c_coord, 2, 1) and board[r_coord][c_coord] == 0:
                        drop_piece(board, r_coord, c_coord, 2)
                        group_capture(board, 1)
                        turn += 1
                        turn = turn % 2
                        
                        if ending_move(board, 2):
                            game_over = True
                            
                    else:
                        print(invalid_msg)                
                                   
                    draw_board(board)
                    print_board(board)
                
    # Wait 3 seconds before closing screen
    if game_over:
        #over_text = pygame.font.Font('freesansbold.ttf', 60)
        #textsurf, textrect = text_objects(over_msg, over_text)
        #textrect.center = ((width / 2), (height / 2))      
        #screen.blit(textsurf, textrect)       
        pygame.time.wait(3000)
        end_game()


def end_game():
    end = True
    # Calculations after game is over to determine winner
    captured_p1 = captured.count(2)
    captured_p2 = captured.count(1)
    
    score_p1 = calculate_points(board, 1) + captured_p1
    score_p2 = calculate_points(board, 2) + captured_p2
    
    final_winner = winner(score_p1, score_p2)    
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(WHITE)
        regular_text = pygame.font.Font('freesansbold.ttf', 20)
        TextSurf, TextRect = text_objects("Player 1 ended with {0} points and Player 2 ended with {1} points.".format(score_p1, score_p2), regular_text)
        TextRect.center = ((width / 2), (height / 6))
        screen.blit(TextSurf, TextRect)
        
        # A Chinese Board Game
        winner_text = pygame.font.Font('freesansbold.ttf', 50)
        textSurf, textRect = text_objects("The winner is Player {0}!!!".format(final_winner), winner_text)
        textRect.center = ((width / 2), (height / 2))
        screen.blit(textSurf, textRect)
        
        button("Play Again",318,600,200,60,light_grey,gainsboro,game_loop)
        #BOARD 9 13 19
        #Handicap 
        #Komi
        
        pygame.display.update()
        clock.tick(15)       
    
game_intro()
game_loop()
end_game()
pygame.quit()
quit()

# ISSUES
# Ending game function is still messed up
# Add intro screen with GO, handicap, komi, and play button
# Change end game so it will end if it cannot place in spaces made by other player so you dont need to fill up all your own life spaces before 
# game ends.

