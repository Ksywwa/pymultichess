import socket, pickle
import pygame as pg
from time import time
pg.init()

#создание экрана игры
screenSize = (1200, 700)
screen = pg.display.set_mode(screenSize)
pg.display.set_caption("Multiplayer Chess")
clock = pg.time.Clock()

#определение различных цветов, использованных в игре
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
BLUE     = (  0,   0, 255)
GREEN    = (  0, 255,   0)
BROWN    = (165,  42,  42)
ORANGE   = (255, 165,   0)
YELLOW   = (255, 255,   0)

tileSize = 60
border = 25
#шрифты
pieceFont = pg.font.Font("freesansbold.ttf", 30)
subtitleFont = pg.font.Font("freesansbold.ttf", 25)
notationFont = pg.font.Font("freesansbold.ttf", 15)
#история ходов
moveNotation = list()
alertMessage = None
class button(pg.sprite.Sprite):
    def __init__(self, topLeft, bottomRight, colour, name):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface( (bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]) )
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.topleft = topLeft

        self.name = name
    def display(self):
        screen.blit(self.image, self.rect)
        if self.name != None:
            text = pieceFont.render(self.name, True, ORANGE)
            textRect = text.get_rect()
            textRect.center = ((self.rect.left + self.rect.right)/2, (self.rect.bottom + self.rect.top)/2)
            screen.blit(text, textRect)

    #сыгранные ходы
    def displayMoves(self, moveNotation):

        screen.blit(self.image, self.rect)

        #белые ходы
        text = subtitleFont.render("White Moves", True, BLACK)
        textRect = text.get_rect()
        textRect.center = (self.rect.left + 1/4*(self.rect.right - self.rect.left), self.rect.top + 20)
        screen.blit(text, textRect)

        #чёрные ходы
        text = subtitleFont.render("Black Moves", True, BLACK)
        textRect = text.get_rect()
        textRect.center = (self.rect.left + 3/4*(self.rect.right - self.rect.left), self.rect.top + 20)
        screen.blit(text, textRect)

        #если для отображения требуется слишком много ходов, первые несколько ходов не отображаются
        moveNum = 1
        while 16 * (len(moveNotation[2*(moveNum - 1):]) + 1)/2 + 61 > self.rect.bottom:
            moveNum += 1

        #Чередует отображение перемещения с левой стороны и с правой
        num = 1
        for move in moveNotation[2*(moveNum - 1):]:

            if num % 2 == 1:
                text = notationFont.render(str(moveNum) + ". " + move, True, BLACK)
                textRect = text.get_rect()
                textRect.topleft = (self.rect.left + 5, border + (num + 1)/2 * 16 + 20)

            elif num % 2 == 0:
                text = notationFont.render(move, True, BLACK)
                textRect = text.get_rect()
                textRect.topleft = (self.rect.left + 1/2*(self.rect.right - self.rect.left) + 5, border + num * 8 + 20)

                moveNum += 1

            screen.blit(text, textRect)
            num += 1
    def displayAlert(self, alertMessage):

        screen.blit(self.image, self.rect)
        
        if alertMessage != None:
            if alertMessage == "Game Drawn":
                msg = "Game Drawn"
                
            elif alertMessage[0] == WHITE:
                msg = "White " + alertMessage[1]
            else:
                msg = "Black " + alertMessage[1]
                
            text = pieceFont.render(msg, True, WHITE)
            textRect = text.get_rect()
            textRect.midleft = (self.rect.left + 10, (self.rect.top + self.rect.bottom)/2)
            screen.blit(text, textRect)

    def clicked(self, mousePos):
        if self.rect.left < mousePos[0] and self.rect.right > mousePos[0]:
            if self.rect.top < mousePos[1] and self.rect.bottom > mousePos[1]:
                return True

#класс для каждой шахматной плитки
class chessTile(pg.sprite.Sprite):

    def __init__(self, coordinate):
        pg.sprite.Sprite.__init__(self)

        #проверка цвета плитки
        if (coordinate[0] + coordinate[1]) % 2 == 0:
            self.colour = WHITE
        else:
            self.colour = BLACK

        self.image = pg.Surface((tileSize, tileSize))
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()
        self.rect.topleft = (2*border + coordinate[0]*tileSize, 2*border + coordinate[1]*tileSize)

        self.coordinate = coordinate

    def clicked(self, mousePos):
        if self.rect.left < mousePos[0] and self.rect.right > mousePos[0]:
            if self.rect.top < mousePos[1] and self.rect.bottom > mousePos[1]:
                return True

    #отображает кнопку, фигуру на ней, а также то, нажата ли она и/или возможен ли шахматный ход
    def display(self, legalMoves):

        #изменяет цвет плитки в зависимости от того, выбрана ли фигура или возможный ход
        if len(legalMoves) == 0:
            self.image.fill(self.colour)

        elif self.coordinate == legalMoves[0][:2]:
            self.image.fill(GREEN)

        else:
            for coord in legalMoves[1:]:
                if self.coordinate == coord[:2]:
                    self.image.fill(RED)
                    break

        screen.blit(self.image, self.rect)
        if pieceDict[ self.coordinate ] != None:

            if pieceDict[ self.coordinate ][0] == WHITE:
                text = pieceFont.render( pieceDict[self.coordinate][1], True, BLUE )
            else:
                text = pieceFont.render( pieceDict[self.coordinate][1], True, ORANGE )

            textRect = text.get_rect()
            textRect.center = ( 2*border + tileSize*(self.coordinate[0] + 0.5), 2*border + tileSize*(self.coordinate[1] + 0.5) )
            
            screen.blit(text, textRect)

#определение сети, которая будет подключаться к серверу
class Network:
    #создание сокета, который подключается к определённому адресу
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = input("Введите IP адрес сервера")
        self.port = 5555
        self.addr = (self.server, self.port)

    #подключение сокета к серверу, возвращая цвет пользователя
    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads( self.client.recv(1024) )
        except:
            pass

    #отправляет информацию на сервер и получает ответ обратно
    def send(self, data):
        try:
            self.client.send( pickle.dumps(data) )
            return pickle.loads( self.client.recv(1024) )
        except socket.error as e:
            print(e)
connection = Network()
pieceDict, msg = connection.connect()
print (msg)

#создание шахматной доски
tiles = pg.sprite.Group()
for coordinate in pieceDict.keys():
    tiles.add(chessTile(coordinate))  

#создание истории перемещений и виджет таймера
moveHistory = button( (4*border + 8*tileSize, border), (screenSize[0] - border, 8*tileSize - border),  ORANGE, None)
length = screenSize[0] - (5*border + 8*tileSize)

#кнопки оформления, рисования и отмены
resign = button( (4*border + 8*tileSize,              8*tileSize - border), ( 4*border + 8*tileSize + 1/3*length, 8*tileSize + 3*border),    RED, "Resign")
draw   = button( (4*border + 8*tileSize + 1/3*length, 8*tileSize - border), ( 4*border + 8*tileSize + 2/3*length, 8*tileSize + 3*border), YELLOW,   "Draw")
undo   = button( (4*border + 8*tileSize + 2/3*length, 8*tileSize - border), ( screenSize[0] - border,             8*tileSize + 3*border),  BLACK,   "Undo")
alerts = button( (border, 8*tileSize + 4*border), (screenSize[0] - border, screenSize[1] - border), BLACK, None)

#обновление экрана
def update_screen(legalMoves):

    #заполняет экран белым цветом
    screen.fill(WHITE)

    #отображение фона шахматной доски
    pg.draw.rect(screen, BROWN, (border, border, 8*tileSize + 2*border, 8*tileSize + 2*border))

    #отображение шахматной плитки
    for tile in tiles:
        tile.display(legalMoves)

    moveHistory.displayMoves(moveNotation)
    resign.display()
    draw.display()
    undo.display()
    alerts.displayAlert(alertMessage)

    #обновление отображения
    pg.display.flip()

    #время обновления
    clock.tick(15)

#ввод пользователя
def userInput(legalMoves):
    global pieceDict, moveNotation, alertMessage

    for event in pg.event.get():

        #если пользователь закрывает, программа завершается
        if event.type == pg.QUIT:
            pg.display.quit()
            pg.quit()
            quit()

        #если пользователь нажимает кнопку мыши
        elif event.type == pg.MOUSEBUTTONDOWN:
            mousePos = pg.mouse.get_pos()
            if resign.clicked(mousePos):
                alertMessage = connection.send("Resign")
                
            elif draw.clicked(mousePos):
                alertMessage = connection.send("Draw")
                
            elif undo.clicked(mousePos):
                alertMessage = connection.send("Undo")
                
            else:
                for tile in tiles:
                    if tile.clicked(mousePos):
                        data = connection.send(tile.coordinate)
                        if data != "Wrong Turn":
                            alertMessage, legalMoves, pieceDict, moveNotation = data

                        break

    return legalMoves

legalMoves = list()
start = time()
while 1:
    legalMoves = userInput(legalMoves)
    update_screen(legalMoves)
    
    #обновление экрана каждые 0,25 секунды в зависимости от действий другого игрока
    if time() - start > 0.25:
        alertMessage, pieceDict, moveNotation = connection.send("Update")
        start = time()
            
