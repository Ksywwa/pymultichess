import socket, pickle
#уникальная библиотека которая содержит функции для определения допустимых ходов, которые может делать шахматная фигура
import chess
# необходим для обмена данными между несколькими клиентами одновременно
from _thread import *
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

#преобразование букв в цифры
Num2Letter = {0 : "a", 1 : "b", 2 : "c", 3 : "d", 4 : "e", 5 : "f", 6 : "g", 7 : "h"}

#словарь со всеми исходными позициями шахматных фигур и их цветами
pieceDict = {
            (0, 0) : (BLACK, "R"), (1, 0) : (BLACK, "N"), (2, 0) : (BLACK, "B"), (3, 0) : (BLACK, "Q"), (4, 0) : (BLACK, "K"), (5, 0) : (BLACK, "B"), (6, 0) : (BLACK, "N"), (7, 0) : (BLACK, "R"),
            (0, 1) : (BLACK, "P"), (1, 1) : (BLACK, "P"), (2, 1) : (BLACK, "P"), (3, 1) : (BLACK, "P"), (4, 1) : (BLACK, "P"), (5, 1) : (BLACK, "P"), (6, 1) : (BLACK, "P"), (7, 1) : (BLACK, "P"),
            (0, 2) :         None, (1, 2) :         None, (2, 2) :         None, (3, 2) :         None, (4, 2) :         None, (5, 2) :         None, (6, 2) :         None, (7, 2) :         None,
            (0, 3) :         None, (1, 3) :         None, (2, 3) :         None, (3, 3) :         None, (4, 3) :         None, (5, 3) :         None, (6, 3) :         None, (7, 3) :         None,
            (0, 4) :         None, (1, 4) :         None, (2, 4) :         None, (3, 4) :         None, (4, 4) :         None, (5, 4) :         None, (6, 4) :         None, (7, 4) :         None,
            (0, 5) :         None, (1, 5) :         None, (2, 5) :         None, (3, 5) :         None, (4, 5) :         None, (5, 5) :         None, (6, 5) :         None, (7, 5) :         None,
            (0, 6) : (WHITE, "P"), (1, 6) : (WHITE, "P"), (2, 6) : (WHITE, "P"), (3, 6) : (WHITE, "P"), (4, 6) : (WHITE, "P"), (5, 6) : (WHITE, "P"), (6, 6) : (WHITE, "P"), (7, 6) : (WHITE, "P"),
            (0, 7) : (WHITE, "R"), (1, 7) : (WHITE, "N"), (2, 7) : (WHITE, "B"), (3, 7) : (WHITE, "Q"), (4, 7) : (WHITE, "K"), (5, 7) : (WHITE, "B"), (6, 7) : (WHITE, "N"), (7, 7) : (WHITE, "R")
            }

#определение текущее положения белого и чёрного королей
kingPositions = {WHITE : (4, 7), BLACK : (4, 0)}
currentTurn = WHITE
moveList = list(); lastMove = None
moveNotation = list()

#список допустимых ходов, в котором хранятся все возможные ходы, которые может сделать фигура
#первым пунктом в списке допустимых ходов всегда является выбранная фигура
legalMoves = list()
alertMsg = None

#устанановка IP-адреса и порт сервера
#сервер должен быть изменён в зависимости от локальной сети
server = socket.gethostbyname(socket.gethostname())
port = 5555
#создание сокета и привязка этого сокета к определенному IP-адресу и порту
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen(2)
print("Сервер запустился")
print("IP адрес сервера:", server)

#многопоточный клиент
def threaded_client(conn, currentPlayer):
    #позволяет функции изменять эти переменные
    global currentTurn, pieceDict, kingPositions, moveList, lastMove, moveNotation, legalMoves, alertMsg

    #при подключении к клиенту сервер сообщает ему, каким игроком он является
    #белый - это игрок, который подключается первым, а чёрный - это игрок, который подключается после
    if currentPlayer == WHITE:
        conn.sendall( pickle.dumps( (pieceDict, "You are white") ) )
    else:
        conn.sendall( pickle.dumps( (pieceDict, "You are black") ) )
    while 1:
        try:
            #получение данных от клиента
            data = pickle.loads( conn.recv(1024) )

            #если клиент ничего не отправляет, соединение разрывается, и поток завершается
            if not data:
                print("Disconnected")
                break

            #если игра окончена, дальнейший ввод данных от клиентов не принимается
            elif (lastMove != None and (lastMove == "stalemate" or lastMove == "checkmate")) or (alertMsg != None and (alertMsg == "Game Drawn" or alertMsg[1] == "resigns.")):
                pass

            elif data == "Resign":
                alertMsg = (currentPlayer, "resigns.")
                conn.sendall( pickle.dumps(alertMsg) )

            elif data == "Draw":

                if alertMsg == None  or alertMsg[1] != "proposes a draw.":
                    alertMsg = (currentPlayer, "proposes a draw.")

                elif alertMsg[0] == currentPlayer:
                    alertMsg = None

                else:
                    alertMsg = "Game Drawn"
                conn.sendall( pickle.dumps(alertMsg) )

            elif data == "Undo":

                if lastMove == None:
                    alertMsg = None

                elif alertMsg == None or alertMsg[1] != "wishes to undo.":
                    alertMsg = (currentPlayer, "wishes to undo.")
                elif alertMsg[0] == currentPlayer:
                    alertMsg = None
                else:

                    alertMsg = None

                    #отменяет последний ход, изменяя историю ходов пользователей
                    pieceDict[lastMove[0]] = lastMove[1]
                    pieceDict[lastMove[2]] = lastMove[3]

                    #особые случаи
                    if lastMove[-1] == "ep":
                        pieceDict[lastMove[2]] = (currentTurn, "P")
                    elif lastMove[-1] == "O-O":
                        pieceDict[(7, lastMove[0][1])] = (currentTurn, "P")
                    elif lastMove[-1] == "O-O-O":
                        pieceDict[(0, lastMove[0][1])] = (currentTurn, "P")

                    moveList.pop(-1)
                    moveNotation.pop(-1)


                    if len(moveList) == 0:
                        lastMove = None
                    else:
                        lastMove = moveList[-1]

                    if currentTurn == WHITE:
                        currentTurn = BLACK
                    else:
                        currentTurn = WHITE

                conn.sendall( pickle.dumps(alertMsg) )

            #если клиент запрашивает обновление, отправка необходимой информации
            elif data == "Update":
                conn.sendall( pickle.dumps( (alertMsg, pieceDict, moveNotation) ) )

            elif currentPlayer == currentTurn:

                if not len(legalMoves):

                    if pieceDict[data] == (currentTurn, "P"):
                        legalMoves = chess.pawnMoves(currentTurn, data, pieceDict, lastMove, kingPositions[currentTurn])

                    elif pieceDict[data] == (currentTurn, "N"):
                        legalMoves = chess.knightMoves(currentTurn, data, pieceDict, kingPositions[currentTurn])

                    elif pieceDict[data] == (currentTurn, "R"):
                        legalMoves = chess.rookMoves(currentTurn, data, pieceDict, kingPositions[currentTurn])

                    elif pieceDict[data] == (currentTurn, "B"):
                        legalMoves = chess.bishopMoves(currentTurn, data, pieceDict, kingPositions[currentTurn])

                    elif pieceDict[data] == (currentTurn, "Q"):
                        legalMoves = chess.queenMoves(currentTurn, data, pieceDict, kingPositions[currentTurn])

                    elif pieceDict[data] == (currentTurn, "K"):
                        legalMoves = chess.kingMoves(currentTurn, data, pieceDict, moveList)


                    conn.sendall( pickle.dumps( (alertMsg, legalMoves, pieceDict, moveNotation) ) )

                else:

                    legal = False
                    for potMove in legalMoves[1:]:


                        if data == potMove[:2]:

                            if len( potMove ) == 3:
                                special = potMove[2]
                            else:
                                special = None

                            legal = True
                            break

                    if legal:
                        moveList.append( [ legalMoves[0], pieceDict[ legalMoves[0] ], data, pieceDict[ data ], special ] )

                        if pieceDict[legalMoves[0]][1] == "K":
                            kingPositions[currentTurn] = data

                        if special == "ep" and currentTurn == WHITE:
                            pieceDict[ (data[0], data[1] + 1) ] = None

                        elif special == "ep" and currentTurn == BLACK:
                            pieceDict[ (data[0], data[1] - 1) ] = None

                        elif special == "O-O":
                            pieceDict[ (data[0] - 1, data[1] ) ] = (currentTurn, "R")
                            pieceDict[ (7, data[1]) ] = None

                        elif special == "O-O-O":
                            pieceDict[ (data[0] + 1, data[1]) ] = (currentTurn, "R")
                            pieceDict[ (0, data[1]) ] = None

                        if pieceDict[ data ] == (WHITE, "P") and data[1] == 0:
                            pieceDict[ data ] = (WHITE, "Q")

                        elif pieceDict[ data ] == (BLACK, "P") and data[1] == 7:
                            pieceDict[ data ] = (BLACK, "Q")
                        

                        #изменение очереди хода
                        if currentTurn == WHITE:
                            currentTurn = BLACK
                        else:
                            currentTurn = WHITE


                        if not chess.inCheck(legalMoves[0], data[:2], pieceDict, kingPositions[currentTurn], currentTurn):

                            pieceDict[ data[:2] ] = pieceDict[ legalMoves[0] ]
                            pieceDict[ legalMoves[0] ] = None

                            checkmate = True


                            for coord, piece in pieceDict.items():
                                if piece != None and piece[0] == currentTurn:
                                    if pieceDict[ coord ][1] == "P" and len( chess.pawnMoves(currentTurn, coord, pieceDict, lastMove, kingPositions[currentTurn]) ) > 1:
                                        checkmate = False
                                        break

                                    elif pieceDict[ coord ][1] == "N" and len( chess.knightMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        checkmate = False
                                        break

                                    elif pieceDict[ coord ][1] == "R" and len( chess.rookMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        checkmate = False
                                        break

                                    elif pieceDict[ coord ][1] == "B" and len( chess.bishopMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        checkmate = False
                                        break

                                    elif pieceDict[ coord ][1] == "Q" and len( chess.queenMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        checkmate = False
                                        break

                                    elif pieceDict[ coord ][1] == "K" and len( chess.kingMoves(currentTurn, coord, pieceDict, moveList) ) > 1:
                                        checkmate = False
                                        break


                            if checkmate:
                                moveList[-1].append("checkmate")

                            else:
                                moveList[-1].append("check")


                        else:

                            pieceDict[ data[:2] ] = pieceDict[ legalMoves[0] ]
                            pieceDict[ legalMoves[0] ] = None
                            stalemate = True
                            for coord, piece in pieceDict.items():
                                if piece != None and piece[0] == currentTurn:
                                    if pieceDict[ coord ][1] == "P" and len( chess.pawnMoves(currentTurn, coord, pieceDict, lastMove, kingPositions[currentTurn]) ) > 1:
                                        stalemate = False
                                        break

                                    elif pieceDict[ coord ][1] == "N" and len( chess.knightMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        stalemate = False
                                        break

                                    elif pieceDict[ coord ][1] == "R" and len( chess.rookMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        stalemate = False
                                        break

                                    elif pieceDict[ coord ][1] == "B" and len( chess.bishopMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        stalemate = False
                                        break

                                    elif pieceDict[ coord ][1] == "Q" and len( chess.queenMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        stalemate = False
                                        break

                                    elif pieceDict[ coord ][1] == "K" and len( chess.kingMoves(currentTurn, coord, pieceDict, moveList) ) > 1:
                                        stalemate = False
                                        break


                            if stalemate:
                                moveList[-1].append("stalemate")

                            else:
                                moveList[-1].append(None)

                        lastMove = moveList[-1]

                        #определение правильного обозначения для последнего перемещения

                        if lastMove[4] == "O-O":
                            if lastMove[5] == None:
                                moveNotation.append("O-O")

                            if lastMove[5] == "check":
                                moveNotation.append("O-O+")

                            elif lastMove[5] == "checkmate":
                                moveNotation.append("O-O#")

                            elif lastMove[5] == "stalemate":
                                moveNotation.append("O-O1/2")

                        elif lastMove[4] == "O-O-O":

                            if lastMove[5] == None:
                                moveNotation.append("O-O-O")

                            if lastMove[5] == "check":
                                moveNotation.append("O-O-O+")

                            elif lastMove[5] == "checkmate":
                                moveNotation.append("O-O-O#")

                            elif lastMove[5] == "stalemate":
                                moveNotation.append("O-O-O1/2")

                        else:

                            notation = Num2Letter[ lastMove[0][0] ] + str(lastMove[0][1] + 1) + lastMove[1][1]
                            
                            if lastMove[3] != None:
                                notation += "x"
                                
                            notation += Num2Letter[ lastMove[2][0] ] + str(lastMove[2][1] + 1)
                            
                            if lastMove[4] == "ep":
                                notation += "e.p."

                            if lastMove[5] == "check":
                                notation += "+"

                            elif lastMove[5] == "checkmate":
                                notation += "#"

                            elif lastMove[5] == "stalemate":
                                notation += "1/2"

                            moveNotation.append( notation )

                        alertMsg = None; legalMoves = list()

                        conn.sendall( pickle.dumps( (alertMsg, legalMoves, pieceDict, moveNotation) ) )
                    else:

                        legalMoves = list()
                        conn.sendall( pickle.dumps( (alertMsg, legalMoves, pieceDict, moveNotation) ) )

            else:
                
                #очередь ещё не наступила
                conn.sendall( pickle.dumps("Wrong Turn") )
        
        except:
            break

    print("Потеряно соединение", currentPlayer)
    conn.close()
        

currentPlayer = WHITE
while 1:
    conn, addr = s.accept()
    print ("Подключено к:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer = BLACK
