import pygame, sys
from pygame.locals import *

#Game Variable
game_depth = 5
win_size = board_height = board_width = game_size = 3
FPS = 60
win_width = win_height = 400
box_size = 60
gap_size = 20
win_margin = (win_height - (box_size * board_height + gap_size * (board_height - 1))) / 2

# Value for each move
human_win = -1000
ai_win = 1000
tie = 1 
block = 999.5

# R G B
d_blue = (0, 0, 51)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

# Player
X = 1
O = -1
AI = X

# Game rule
assert game_size >= 3, "The size of the game is too small"
assert game_size *(box_size + gap_size) <= win_height, "The game size doesn't fit the display"
assert win_height <= 1000, "The size of the game is too big for the screen"


def draw_and_check(board):
    game_surf.fill(white)
    Draw_board(board)
    pygame.display.update()
    
    if G_Won(game_board, True) == 'won':
        pygame.time.wait(2000)
        return 1
    elif G_Won(game_board) == 'tie':
        pygame.time.wait(3000)
        return 1


class G_node: 
    def __init__(self, player, depth, g_board, position):
        self.player = player                      # player you know what I mean
        self.depth = depth                        # current depth of the game
        self.g_board = g_board                    # get the game board
        self.pos = position                       # get the cord of the move
        self.state, self.w_state = self.State()   # evaluate the each move for the next step
        self.n_moves = []                         # list for available moves
        print self.g_board                        # debug
        print 'x: {0[0]}, y: {0[1]} depth: {1} player: {2} world_state: {3}\n'.format(self.pos, self.depth, self.player, self.state)
        self.Next_move()                          # go to the next step of the game
    
    def Next_move(self):
        if (self.depth >= game_depth) or (G_Won(self.g_board) == 'won'):
            return 0
        if G_Won(self.g_board) == False:
            empty_b = M_left(self.g_board)
            for i in empty_b:
                x_pos, y_pos = i
                self.g_board[x_pos][y_pos] = -self.player
                n_node = G_node(-self.player, self.depth + 1, self.g_board, [x_pos, y_pos])
                self.g_board[x_pos][y_pos] = False
                self.n_moves.append(n_node)
    
    def State(self):
        if G_Won(self.g_board) == 'won':
            if self.player == O:
                print 'human won\n'
                return (human_win, 'won') 
            else:
                print 'computer won\n'
                print ai_win - self.depth
                return (ai_win - self.depth, 'won')
        elif G_Won == 'tie':
            return (tie, 'tie')
        if Block(self.g_board, self.pos[0], self.pos[1]):
            print 'block worked\n'
            return (block - self.depth, 'block')
        return (0, 'nothing')


def Block(board, x_cor, y_cor):
    print x_cor, y_cor
    #Vertical block
    for x in range(board_width):
        if (board[x][0] == board[x][1] == -AI) and (AI == board[x][2]) and (x_cor == x and y_cor == 2):
            return True
        elif (board[x][1] == board[x][2] == -AI) and (AI == board[x][0]) and (x_cor == x and y_cor == 0):
            return True
        elif (board[x][0] == board[x][2] == -AI) and (AI == board[x][1]) and (x == x_cor and y_cor == 1):
            return True
    
    #Side block 
    for y in range(board_height):
        if (board[0][y] == board[1][y] == -AI) and (AI == board[2][y]) and (x_cor == 2 and y_cor == y):
            return True
        elif (board[1][y] == board[2][y] == -AI) and (AI == board[0][y]) and (x_cor == 0 and y_cor == y):
            return True
        elif (board[0][y] == board[2][y] == -AI) and (AI == board[1][y]) and (x_cor == 1 and y_cor == y):
            return True
    
    #Diagonal
    if (board[0][0] == board[1][1] == -AI) and (AI == board[2][2]) and (x_cor == 2 and y_cor == 2):
        return True
    if (board[2][2] == board[1][1] == -AI) and (AI == board[0][0]) and (x_cor == 0 and y_cor == 0):
        return True
    if ((board[0][0] == board[2][2] == -AI) and (AI == board[1][1])) or ((board[2][0] == board[0][2] == -AI) and (AI == board[1][1])):
        return True
    return False


# The algorith that run the AI
def Min_max(node, depth):
    if (node.w_state == 'block') and (depth == game_depth):
        return (node.state, node.pos)
    if (node.w_state == 'won') or (depth <= 0):
        return (node.state, node.pos)
    
    b_val = (human_win, [])
    for i in range(len(node.n_moves)):
        game_node = node.n_moves[i]
        n_val = Min_max(game_node, depth - 1)
        #print'n: {} b: {} depth: {}'.format(n_val[0], b_val[0], depth)  # debug
        if (n_val[0] >= b_val[0]):
            b_val = n_val
    return b_val


def M_left(board):
    empty_b = []
    for x_cor in range(board_width):
        for y_cor in range(board_height):
            if board[x_cor][y_cor] == False:
                empty_b.append((x_cor, y_cor))
    return empty_b


def Won_anime(x, y, win_size, won_type):
    x_pix, y_pix = Get_x_y_pixel(x, y)
    
    l_speed = box_size / 10
    half = box_size / 2
    l_width = gap_size / 8
    speed_rate = (box_size + gap_size) / l_speed
    
    for i in range(1, (win_size * speed_rate) + 1):
        if won_type == 'side':
            pygame.draw.line(game_surf, d_blue, (x_pix - gap_size, y_pix + half), (x_pix + (i * l_speed), y_pix + half), l_width)
        if won_type == 'vertical':
            pygame.draw.line(game_surf, d_blue, (x_pix + half, y_pix - gap_size), (x_pix + half, y_pix + (i * l_speed)), l_width)
        if won_type == 'diagonal_left':
            pygame.draw.line(game_surf, d_blue, (x_pix + half - (i * l_speed) / 2, y_pix + half - (i * l_speed) / 2), (x_pix + half + (i * l_speed) / 2, y_pix + half + (i * l_speed) / 2), l_width)
        if won_type == 'diagonal_right':
            pygame.draw.line(game_surf, d_blue, (x_pix + half - (i * l_speed) / 2, y_pix + half + (i * l_speed) / 2), (x_pix + half + (i * l_speed) / 2, y_pix + half - (i * l_speed) / 2), l_width)
        
        pygame.display.update()
        pygame.time.wait(22)    # Wait 22 milisecond for smoother animation 


def G_Won(board, ani = False):
    won_type = [False, False, [False,False]]
    # VERTICAL WIN
    for x_cor in range(board_width):
        if (board[x_cor][0] == board[x_cor][1] == board[x_cor][2]):
            if board[x_cor][0] != False:
                won_type = ['won','vertical',(x_cor, 0)]
    
    # SIDE WIN
    for y_cor in range(board_height):
        if (board[0][y_cor] == board[1][y_cor] == board[2][y_cor]):
            if board[0][y_cor] != False:
                won_type = ['won','side',(0, y_cor)]
    
    # DIAGONAL WIN
    if board[1][1] != False:
        # LEFT
        if (board[0][0] == board[1][1] == board[2][2]):
            won_type = ['won','diagonal_lef',(1,1)]
        # RIGHT
        if (board[2][0] == board[1][1] == board[0][2]):
            won_type = ['won','diagonal_right',(1, 1)]
        
    
    if (won_type[0] == 'won') and (ani == True):
        Won_anime(won_type[2][0], won_type[2][1], win_size, won_type[1])
        return 'won'
    elif (won_type[0] == 'won'):
        return 'won'
    
    for x in range(board_width):
        for y in range(board_height):
            if board[x][y] == False:
                return False
    return 'tie'


def Make_2d_list(board):
    # transform a list to the game coordinate
    n_list = []
    for x_cor in range(0, len(board), game_size):
        n_list.append(board[x_cor:(x_cor + game_size)])
    return n_list


def Find_pos(x, y):
    for x_cor in range(board_width):
        for y_cor in range(board_height):
            x_pix, y_pix = Get_x_y_pixel(x_cor, y_cor)
            x_y_check = pygame.Rect(x_pix, y_pix, box_size, box_size)
            if x_y_check.collidepoint(x, y):
                return (x_cor, y_cor)
    return (None, None)


def Draw_board(board):
    half = gap_size / 2
    # Draw gap first then draw x o, you don't need to read this mess
    for x_cor in range(1, board_width):
        pygame.draw.line(game_surf, black, ((win_margin + x_cor * (box_size + gap_size)) - half, win_margin), ((win_margin + x_cor * (box_size + gap_size)) - half, win_height - win_margin), half - 8)
    for y_cor in range(1, board_height):
        pygame.draw.line(game_surf, black, (win_margin,(win_margin + y_cor * (box_size + gap_size)) - half), (win_width - win_margin, (win_margin + y_cor * (box_size + gap_size)) - half), half - 8)
    for x_cor in range(board_width):
        for y_cor in range(board_height):
            if board[x_cor][y_cor] == O:
                Draw_x_o(O, x_cor, y_cor)
            elif board[x_cor][y_cor] == X:
                Draw_x_o(X, x_cor, y_cor)


def Create_board():
    board = []
    for x in range(board_width):
        for y in range(board_height):
            board.append(False)
    board = Make_2d_list(board)
    return board


def Get_x_y_pixel(x, y): # transform the game coordinate to pixel co...
    x_pix_cor = x * (box_size + gap_size) + win_margin
    y_pix_cor = y * (box_size + gap_size) + win_margin
    return (x_pix_cor, y_pix_cor)


def Draw_x_o(sign, x, y):
    x_pix, y_pix = Get_x_y_pixel(x,y)
    half = box_size / 2
    
    if sign == X:
        pygame.draw.line(game_surf, black, (x_pix, y_pix),(x_pix + box_size, y_pix + box_size))
        pygame.draw.line(game_surf, black, (x_pix, y_pix + box_size),(x_pix + box_size, y_pix))
    elif sign == O:
        pygame.draw.circle(game_surf, red, (x_pix + half, y_pix + half), half, 2)


if __name__ == '__main__':
    pygame.init()
    global game_surf
    game_fps = pygame.time.Clock()
    game_board = Create_board()
    mousex = 0
    mousey = 0
    
    game_surf = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('TIC TAC TOE')
    
    while True:
        if draw_and_check(game_board): # Must alway check the game
            game_board = Create_board()
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                x_pos, y_pos = Find_pos(mousex, mousey)
                
                if x_pos != None and y_pos != None and game_board[x_pos][y_pos] == False:
                    game_board[x_pos][y_pos] = -AI
                    
                    empty_place = M_left(game_board)
                    x_moves = []
                    
                    if draw_and_check(game_board): # Check if AI should take the move
                        game_board = Create_board()
                        continue
                    
                    # AI play the game
                    for x, y in empty_place:
                        game_board[x][y] = AI
                        #print game_board # debug
                        print 'x: {}, y: {} depth: {} player: {}\n'.format(x, y, game_depth, X)
                        g_nod = G_node(AI, 0, game_board, [x, y])
                        game_board[x][y] = False
                        x_moves.append(g_nod) 
                    best_val = (human_win, [])
                    # Evaluate the game
                    for i in range(len(x_moves)):
                        game_node = x_moves[i]
                        normal_move = Min_max(game_node, game_depth)
                        print 'normal move:{}  best val:{}'.format(normal_move, best_val)
                        if (normal_move[0] >= best_val[0]) and (normal_move[1] != []):
                            best_val = normal_move
                    
                    best_move = best_val
                    if best_move[1] == []:
                        continue
                    print 'X chooses', best_move[1]
                    game_board[best_move[1][0]][best_move[1][1]] = X
        game_fps.tick(FPS)
