import numpy as np
import os
from colorama import Fore
from colorama import Style
from copy import deepcopy
import pygame
from pygame.constants import KEYDOWN
import bfs
import astar
import astar1

''' Timeout của mỗi map là 30 phút  '''
TIME_OUT = 1800
''' lấy path của folder testcases và checkpoints '''
path_board = os.getcwd() + '\\..\\Testcases'
path_checkpoint = os.getcwd() + '\\..\\Checkpoints'

''' lấy data từ các testcase để trả lại các bảng gồm các map'''
def get_boards():
    os.chdir(path_board)
    list_boards = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_board}/{file}"
            board = get_board(file_path)
            # print(file)
            list_boards.append(board)
    return list_boards

''' truyền data từ các file checkpoint để trả lại vị trí các checkpoint trong map'''
def get_check_points():
    os.chdir(path_checkpoint)
    list_check_point = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_checkpoint}/{file}"
            check_point = get_pair(file_path)
            list_check_point.append(check_point)
    return list_check_point

''' chuyển đổi các ký tự trong một hàng từ file TXT sang ký tự tượng trưng để hiện thị map trong game'''
def format_row(row):
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = '#'
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b':
            row[i] = '$'
        elif row[i] == 'c':
            row[i] = '%'

''' chuyển đổi ký tự checkpoint từ file txt sao chép sang một mảng '''
def format_check_points(check_points):
    result = []
    for check_point in check_points:
        result.append((check_point[0], check_point[1]))
    return result

''' trả về bản đồ dưới dạng một mảng NumPy, trong đó các ký tự đã được chuyển đổi thành các ký tự thể hiện các phần tử của bản đồ.'''
def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result

'''trả về checkpoints dưới dạng một mảng NumPy, trong đó các ký tự đã được chuyển đổi thành các ký tự thể hiện các phần tử của checkpoint. '''
def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result

'''
//========================//
//      DECLARE AND       //
//  INITIALIZE MAPS AND   //
//      CHECK POINTS      //
//========================//
'''
maps = get_boards()
check_points = get_check_points()


'''
//========================//
//         PYGAME         //
//     INITIALIZATIONS    //
//                        //
//========================//
'''
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Sokoban')
clock = pygame.time.Clock()
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
'''
GET SOME ASSETS
'''
assets_path = os.getcwd() + "\\..\\Assets"
os.chdir(assets_path)
player = pygame.image.load(os.getcwd() + '\\player.png')
wall = pygame.image.load(os.getcwd() + '\\wall.png')
box = pygame.image.load(os.getcwd() + '\\box.png')
point = pygame.image.load(os.getcwd() + '\\point.png')
space = pygame.image.load(os.getcwd() + '\\space.png')
arrow_left = pygame.image.load(os.getcwd() + '\\arrow_left.png')
arrow_right = pygame.image.load(os.getcwd() + '\\arrow_right.png')
init_background = pygame.image.load(os.getcwd() + '\\init_background.png')
loading_background = pygame.image.load(os.getcwd() + '\\loading_background.png')
notfound_background = pygame.image.load(os.getcwd() + '\\notfound_background.png')
found_background = pygame.image.load(os.getcwd() + '\\found_background.png')
'''
RENDER THE MAP FOR GAMEPLAY
'''
def renderMap(board):
	width = len(board[0])
	height = len(board)
	indent = (640 - width * 32) / 2.0
	for i in range(height):
		for j in range(width):
			screen.blit(space, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '#':
				screen.blit(wall, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '$':
				screen.blit(box, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '%':
				screen.blit(point, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '@':
				screen.blit(player, (j * 32 + indent, i * 32 + 250))

			
'''
VARIABLES INITIALIZATIONS
'''
#Map level
mapNumber = 0
#Algorithm to solve the game
algorithm = "Euclidean Distance Heuristic"
#Your scene states, including: 
#init for choosing your map and algorithm
#loading for displaying "loading scene"
#executing for solving problem
#playing for displaying the game
sceneState = "init"
loading = False

''' SOKOBAN FUNCTION '''
def sokoban():
	running = True
	global sceneState
	global loading
	global algorithm
	global list_board
	global mapNumber
	stateLenght = 0
	currentState = 0
	found = True

	

	while running:
		screen.blit(init_background, (0, 0))
		if sceneState == "init":
			#Choose map and display
			initGame(maps[mapNumber])

		if sceneState == "executing":
			#Choose map
			list_check_point = check_points[mapNumber]

			#Choose between BFS or Hill Climbing
			if algorithm == "Euclidean Distance Heuristic":
				print("EDH")
				list_board = astar1.AStar_Search1(maps[mapNumber], list_check_point)
			elif algorithm == "Manhattan Distance Heuristic":
				print("MDH")
				list_board = astar.AStar_Search(maps[mapNumber], list_check_point)
			else:
				print("BFS")
				list_board = bfs.BFS_search(maps[mapNumber], list_check_point)

			if len(list_board) > 0:
				sceneState = "playing"
				stateLenght = len(list_board[0])
				currentState = 0
			else:
				sceneState = "end"
				found = False
		if sceneState == "loading":
			loadingGame()
			sceneState = "executing"
		if sceneState == "end":
			if found:
				foundGame(list_board[0][stateLenght - 1])
			else:
				notfoundGame()
		if sceneState == "playing":
			clock.tick(2)
			renderMap(list_board[0][currentState])
			currentState = currentState + 1
			if currentState == stateLenght:
				sceneState = "end"
				found = True
		#Check event when you press key board
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				
				#Press arrow key board to change level map
				if event.key == pygame.K_RIGHT and sceneState == "init":
					if mapNumber < len(maps) - 1:
						mapNumber = mapNumber + 1
				if event.key == pygame.K_LEFT and sceneState == "init":
					if mapNumber > 0:
						mapNumber = mapNumber - 1
				#Press ENTER key board to select level map and algorithm
				if event.key == pygame.K_RETURN:
					if sceneState == "init":
						sceneState = "loading"
					if sceneState == "end":
						sceneState = "init"
				#Press SPACE key board to switch algorithm
				if event.key == pygame.K_SPACE and sceneState == "init":
					if algorithm == "Euclidean Distance Heuristic":
						algorithm = "Manhattan Distance Heuristic"
					elif algorithm == "Manhattan Distance Heuristic":
						algorithm = "BFS" 
					else:
						algorithm = "Euclidean Distance Heuristic"
		pygame.display.flip()
	pygame.quit()

''' DISPLAY MAIN SCENE '''
#DISPLAY INITIAL SCENE
def initGame(map):
	titleSize = pygame.font.Font('gameFont.ttf', 60)
	titleText = titleSize.render('Sokoban(Nhóm 10)', True, WHITE)
	titleRect = titleText.get_rect(center=(320, 80))
	screen.blit(titleText, titleRect)

	desSize = pygame.font.Font('gameFont.ttf', 20)
	desText = desSize.render('Chọn map:', True, WHITE)
	desRect = desText.get_rect(center=(320, 140))
	screen.blit(desText, desRect)
	
	desSize = pygame.font.Font('gameFont.ttf', 20)
	desText = desSize.render('Nhấn SPACE để đổi thuật toán', True, WHITE)
	desRect = desText.get_rect(center=(320, 550))
	screen.blit(desText, desRect)

	mapSize = pygame.font.Font('gameFont.ttf', 30)
	mapText = mapSize.render(" Map: " + str(mapNumber + 1) + " ", True, WHITE)
	mapRect = mapText.get_rect(center=(320, 200))
	screen.blit(mapText, mapRect)

	screen.blit(arrow_left, (240, 188))
	screen.blit(arrow_right, (376, 188))

	algorithmSize = pygame.font.Font('gameFont.ttf', 30)
	algorithmText = algorithmSize.render(str(algorithm), True, WHITE)
	algorithmRect = algorithmText.get_rect(center=(320, 600))
	screen.blit(algorithmText, algorithmRect)
	renderMap(map)

''' LOADING SCENE '''
#DISPLAY LOADING SCENE
def loadingGame():
	screen.blit(loading_background, (0, 0))

	fontLoading_1 = pygame.font.Font('gameFont.ttf', 40)
	text_1 = fontLoading_1.render('LOADING', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 60))
	screen.blit(text_1, text_rect_1)

	fontLoading_2 = pygame.font.Font('gameFont.ttf', 20)
	text_2 = fontLoading_2.render('Đang tìm lời giải............', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 100))
	screen.blit(text_2, text_rect_2)

def foundGame(map):
	screen.blit(found_background, (0, 0))

	font_1 = pygame.font.Font('gameFont.ttf', 30)
	text_1 = font_1.render('Yeah! Đã tìm thấy lời giải!!!', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 100))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 20)
	text_2 = font_2.render('Nhấn ENTER để tiếp tục', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 600))
	screen.blit(text_2, text_rect_2)

	renderMap(map)

def notfoundGame():
	screen.blit(notfound_background, (0, 0))

	font_1 = pygame.font.Font('gameFont.ttf', 40)
	text_1 = font_1.render('Không thể tìm ra lời giải', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 100))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 20)
	text_2 = font_2.render('Nhấn ENTER để tiếp tục', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 600))
	screen.blit(text_2, text_rect_2)

	

def main():
	sokoban()

if __name__ == "__main__":
	main()

