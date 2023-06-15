BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

#все возможные ходы пешки
def pawnMoves(currentTurn, startPos, pieceDict, lastMove, kingPos):

    #список доступных ходов
    legalMoves = list()
    legalMoves.append(startPos)

    #проверяет, движется ли пешка вверх/вниз (зависит от её цвета)
    if currentTurn == WHITE:
        vertical = -1
    else:
        vertical = 1
    print(lastMove)
    if lastMove != None and lastMove[1][1] == "P" and abs( lastMove[2][1] - lastMove[0][1] ) == 2:

        if ( startPos[0] + 1, startPos[1] ) == lastMove[2]:
            if inCheck( startPos, (startPos[0] + 1, startPos[1] + vertical), pieceDict, kingPos, currentTurn ):
                legalMoves.append( ( startPos[0] + 1, startPos[1] + vertical, "ep") )

        elif ( startPos[0] - 1, startPos[1] ) == lastMove[2]:
            if inCheck( startPos, (startPos[0] - 1, startPos[1] + vertical), pieceDict, kingPos, currentTurn ):
                legalMoves.append( ( startPos[0] - 1, startPos[1] + vertical, "ep") )

    #перемещение пешки на 1 или 2 хода вперёд
    if pieceDict[ (startPos[0], startPos[1] + vertical) ] == None:

        if inCheck( startPos, (startPos[0], startPos[1] + vertical), pieceDict, kingPos, currentTurn ):
            legalMoves.append( (startPos[0], startPos[1] + vertical) )


        if inCheck( startPos, (startPos[0], startPos[1] + vertical * 2), pieceDict, kingPos, currentTurn ):

            if (vertical == 1 and startPos[1] == 1) or (vertical == -1 and startPos[1] == 6):

                if pieceDict[ (startPos[0], startPos[1] + 2 * vertical) ] == None:

                    legalMoves.append( (startPos[0], startPos[1] + 2 * vertical) )

    #диагональные ходы
    try:
        if inCheck( startPos, (startPos[0] - 1, startPos[1] + vertical), pieceDict, kingPos, currentTurn ):
            if pieceDict[ (startPos[0] - 1, startPos[1] + vertical) ] != None:
                if pieceDict[ startPos ][0] not in pieceDict[ (startPos[0] - 1, startPos[1] + vertical) ]:
                    legalMoves.append( (startPos[0] - 1, startPos[1] + vertical) )
    except:
        pass

    try:
        if inCheck( startPos, (startPos[0] + 1, startPos[1] + vertical), pieceDict, kingPos, currentTurn ):
            if pieceDict[ (startPos[0] + 1, startPos[1] + vertical) ] != None:
                if pieceDict[ startPos ][0] not in pieceDict[ (startPos[0] + 1, startPos[1] + vertical) ]:
                    legalMoves.append( (startPos[0] + 1, startPos[1] + vertical) )
    except:
        pass
    return legalMoves

#все возможные ходы конём
def knightMoves(currentTurn, startPos, pieceDict, kingPos):

    #список доступных ходов
    legalMoves = list()
    legalMoves.append(startPos)

    knightMoves = (
                  (startPos[0] + 1, startPos[1] + 2), (startPos[0] - 1, startPos[1] + 2),
                  (startPos[0] + 1, startPos[1] - 2), (startPos[0] - 1, startPos[1] - 2),
                  (startPos[0] + 2, startPos[1] + 1), (startPos[0] - 2, startPos[1] + 1),
                  (startPos[0] + 2, startPos[1] - 1), (startPos[0] - 2, startPos[1] - 1)
                  )

    for knightMove in knightMoves:
        try:
            if ( pieceDict[ knightMove ] == None or pieceDict[ knightMove ][0] != currentTurn ) and inCheck(startPos, knightMove, pieceDict, kingPos, currentTurn):
                legalMoves.append( knightMove )
        except:
            pass

    return legalMoves

#все возможные ходы ладьи
def rookMoves(currentTurn, startPos, pieceDict, kingPos):
    legalMoves = list()
    legalMoves.append(startPos)

    #доступные ходы вправо
    for xPos in range(startPos[0] + 1, 8, 1):
        if pieceDict[ (xPos, startPos[1]) ] == None:
            if inCheck(startPos, (xPos, startPos[1]), pieceDict, kingPos, currentTurn):
                legalMoves.append( (xPos, startPos[1]) )

        elif pieceDict[ startPos ][0] != pieceDict[ (xPos, startPos[1]) ][0]:
            if inCheck(startPos, (xPos, startPos[1]), pieceDict, kingPos, currentTurn):
                legalMoves.append( (xPos, startPos[1]) )
                break

        else:
            break

    #доступные ходы влево
    for xPos in range(startPos[0] - 1, -1, -1):
        if pieceDict[ (xPos, startPos[1]) ] == None:
            if inCheck(startPos, (xPos, startPos[1]), pieceDict, kingPos, currentTurn):
                legalMoves.append( (xPos, startPos[1]) )

        elif pieceDict[ startPos ][0] != pieceDict[ (xPos, startPos[1]) ][0]:
            if inCheck(startPos, (xPos, startPos[1]), pieceDict, kingPos, currentTurn):
                legalMoves.append( (xPos, startPos[1]) )
                break

        else:
            break

    #доступные ходы вниз
    for yPos in range(startPos[1] + 1, 8, 1):
        if pieceDict[ (startPos[0], yPos) ] == None:
            if inCheck(startPos, (startPos[0], yPos), pieceDict, kingPos, currentTurn):
                legalMoves.append( (startPos[0], yPos) )

        elif pieceDict[ startPos ][0] != pieceDict[ (startPos[0], yPos) ][0]:
            if inCheck(startPos, (startPos[0], yPos), pieceDict, kingPos, currentTurn):
                legalMoves.append( (startPos[0], yPos) )
                break

        else:
            break

    #доступные ходы вверх
    for yPos in range(startPos[1] - 1, -1, -1):
        if pieceDict[ (startPos[0], yPos) ] == None:
            if inCheck(startPos, (startPos[0], yPos), pieceDict, kingPos, currentTurn):
                legalMoves.append( (startPos[0], yPos) )

        elif pieceDict[ startPos ][0] != pieceDict[ (startPos[0], yPos) ][0]:
            if inCheck(startPos, (startPos[0], yPos), pieceDict, kingPos, currentTurn):
                legalMoves.append( (startPos[0], yPos) )
                break

        else:
            break

    return legalMoves

#все возможные ходы слона
def bishopMoves(currentTurn, startPos, pieceDict, kingPos):

    legalMoves = list()
    legalMoves.append(startPos)

    #верхняя правая диагональ
    testCoordinate = (startPos[0] + 1, startPos[1] + 1)
    while testCoordinate in pieceDict.keys():

        if pieceDict[testCoordinate] == None:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)

        elif pieceDict[startPos][0] != pieceDict[testCoordinate][0]:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)
                break

        else:
            break

        testCoordinate = (testCoordinate[0] + 1, testCoordinate[1] + 1)

    #нижняя правая диагональ
    testCoordinate = (startPos[0] + 1, startPos[1] - 1)
    while testCoordinate in pieceDict.keys():

        if pieceDict[testCoordinate] == None:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)

        elif pieceDict[startPos][0] != pieceDict[testCoordinate][0]:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)
                break

        else:
            break

        testCoordinate = (testCoordinate[0] + 1, testCoordinate[1] - 1)

    #нижняя левая диагональ
    testCoordinate = (startPos[0] - 1, startPos[1] + 1)
    while testCoordinate in pieceDict.keys():
        if pieceDict[testCoordinate] == None:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)

        elif pieceDict[startPos][0] != pieceDict[testCoordinate][0]:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)
                break

        else:
            break

        testCoordinate = (testCoordinate[0] - 1, testCoordinate[1] + 1)

    #верхняя левая диагональ
    testCoordinate = (startPos[0] - 1, startPos[1] - 1)
    while testCoordinate in pieceDict.keys():
        if pieceDict[testCoordinate] == None:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)

        elif pieceDict[startPos][0] != pieceDict[testCoordinate][0]:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)
                break

        else:
            break

        testCoordinate = (testCoordinate[0] - 1, testCoordinate[1] - 1)

    return legalMoves

#ходы королевы
def queenMoves(currentTurn, startPos, pieceDict, kingPos):
    return rookMoves(currentTurn, startPos, pieceDict, kingPos) + bishopMoves(currentTurn, startPos, pieceDict, kingPos)[1:]

#ходы короля
def kingMoves(currentTurn, startPos, pieceDict, moveList):
    legalMoves = list()
    legalMoves.append(startPos)

    #рокировка
    if currentTurn == WHITE:
        rank = 7
    else:
        rank = 0

    #если прошлый ход не поставил короля под шах
    if len(moveList) > 0:
        if len(moveList[-1]) == 5 or moveList[-1][5] == None:

            #проверка, возможна ли рокировка короля или королевы
            kingCastle = True; queenCastle = True
            for move in moveList:
                if move[1] == (currentTurn, "K"):
                    kingCastle = False; queenCastle = False
                    break

                elif move[0] == (7, rank) or move[2] == (7, rank):
                    kingCastle = False

                elif move[0] == (0, rank) or move[2] == (0, rank):
                    queenCastle = False

            #рокировка на стороне короля
            if kingCastle and pieceDict[ (5, rank) ] == None and pieceDict[ (6, rank) ] == None:
                if inCheck(startPos, (5, rank), pieceDict, (5, rank), currentTurn) and inCheck(startPos, (6, rank), pieceDict, (6, rank), currentTurn):
                    legalMoves.append( (6, rank, "O-O") )

            #рокировка на стороне королевы
            if queenCastle and pieceDict[ (3, rank) ] == None and pieceDict[ (2, rank) ] == None and pieceDict[ (1, rank) ] == None:

                if inCheck(startPos, (5, rank), pieceDict, (3, rank), currentTurn) and inCheck(startPos, (6, rank), pieceDict, (2, rank), currentTurn):
                    legalMoves.append( (2, rank, "O-O-O") )

    #обычные ходы короля
    kingMoves = (
                (startPos[0] - 1, startPos[1] - 1), (startPos[0], startPos[1] - 1),
                (startPos[0] + 1, startPos[1] - 1), (startPos[0] - 1, startPos[1]),
                (startPos[0] + 1, startPos[1]), (startPos[0] - 1, startPos[1] + 1),
                (startPos[0], startPos[1] + 1), (startPos[0] + 1, startPos[1] + 1)
                )

    #Добавляет ход короля к разрешённым ходам, если это не приводит к тому, что король находится в шахе, или к тому, что король покидает шахматную доску
    for kingMove in kingMoves:
        try:
            if pieceDict[ kingMove ] == None or pieceDict[ kingMove ][0] != currentTurn:
                if inCheck(startPos, kingMove, pieceDict, kingMove, currentTurn):
                    legalMoves.append( kingMove )
        except:
            pass

    return legalMoves

#проверка, которая возвращает true, если король не находится в шахе и false в противном случае
#проверка, может ли какая-либо фигура взять короля, если сделан ход
def inCheck(startPos, newPos, pieceDict, kingPos, currentTurn):

    potDict = dict(pieceDict)
    potDict[newPos] = potDict[startPos]; potDict[startPos] = None
    knightCoords = (
                   (kingPos[0] + 1, kingPos[1] + 2), (kingPos[0] - 1, kingPos[1] + 2),
                   (kingPos[0] + 1, kingPos[1] - 2), (kingPos[0] - 1, kingPos[1] - 2),
                   (kingPos[0] + 2, kingPos[1] + 1), (kingPos[0] - 2, kingPos[1] + 1),
                   (kingPos[0] + 2, kingPos[1] - 1), (kingPos[0] - 2, kingPos[1] - 1)
                   )

    for coord in knightCoords:
        if coord[0] > -1 and coord[0] < 8 and coord[0] > - 1 and coord[1] > -1 and coord[1] < 8:
            if potDict[coord] == None:
                pass

            elif potDict[coord][0] == currentTurn:
                pass

            elif potDict[coord][1] == "N":
                return False

    if kingPos[0] + 1 != 8:
        if potDict[ (kingPos[0] + 1, kingPos[1]) ] == None:

            for x in range(kingPos[0] + 1, 8):
                if potDict[(x, kingPos[1])] == None:
                    pass

                elif potDict[(x, kingPos[1])][0] == currentTurn:
                    break

                elif potDict[ (x, kingPos[1]) ][1] == "R" or potDict[ (x, kingPos[1]) ][1] == "Q":
                    return False

                else:
                    break

        elif potDict[ (kingPos[0] + 1, kingPos[1]) ][0] != currentTurn:
            if potDict[ (kingPos[0] + 1, kingPos[1]) ][1] == "K" or potDict[ (kingPos[0] + 1, kingPos[1]) ][1] == "R" or potDict[ (kingPos[0] + 1, kingPos[1]) ][1] == "Q":
                return False

    if kingPos[0] - 1 != -1:
        if potDict[ (kingPos[0] - 1, kingPos[1]) ] == None:

            for x in range(kingPos[0] - 1, -1, -1):
                if potDict[(x, kingPos[1])] == None:
                    pass

                elif potDict[(x, kingPos[1])][0] == currentTurn:
                    break

                elif potDict[(x, kingPos[1])][1] == "R" or potDict[ (x, kingPos[1]) ][1] == "Q":
                    return False

                else:
                    break

        elif potDict[ (kingPos[0] - 1, kingPos[1]) ][0] != currentTurn:
            if potDict[ (kingPos[0] - 1, kingPos[1]) ][1] == "K" or potDict[ (kingPos[0] - 1, kingPos[1]) ][1] == "R" or potDict[ (kingPos[0] - 1, kingPos[1]) ][1] == "Q":
                return False

    if kingPos[1] + 1 != 8:
        if potDict[ (kingPos[0], kingPos[1] + 1) ] == None:

            for y in range(kingPos[1] + 1, 8):
                if potDict[(kingPos[0], y)] == None:
                    pass

                elif potDict[(kingPos[0], y)][0] == currentTurn:
                    break

                elif potDict[(kingPos[0], y)][1] == "R" or potDict[(kingPos[0], y)][1] == "Q":
                    return False

                else:
                    break

        elif potDict[ (kingPos[0], kingPos[1] + 1) ][0] != currentTurn:
            if potDict[ (kingPos[0], kingPos[1] + 1) ][1] == "K" or potDict[ (kingPos[0], kingPos[1] + 1) ][1] == "R" or potDict[ (kingPos[0], kingPos[1] + 1) ][1] == "Q":
                return False

    if kingPos[1] - 1 != -1:
        if potDict[ (kingPos[0], kingPos[1] - 1) ] == None:

            for y in range(kingPos[1] - 2, -1, -1):
                if potDict[(kingPos[0], y)] == None:
                    pass

                elif potDict[(kingPos[0], y)][0] == currentTurn:
                    break

                elif potDict[(kingPos[0], y)][1] == "R" or potDict[(kingPos[0], y)][1] == "Q":
                    return False

                else:
                    break

        elif potDict[ (kingPos[0], kingPos[1] - 1) ][0] != currentTurn:
            if potDict[ (kingPos[0], kingPos[1] - 1) ][1] == "K" or potDict[ (kingPos[0], kingPos[1] - 1) ][1] == "R" or potDict[ (kingPos[0], kingPos[1] - 1) ][1] == "Q":
                return False

    if kingPos[0] + 1 < 8 and kingPos[1] + 1 < 8:
        if potDict[ (kingPos[0] + 1, kingPos[1] + 1) ] != None:
            if potDict[ (kingPos[0] + 1, kingPos[1] + 1) ][0] != currentTurn and ( potDict[ (kingPos[0] + 1, kingPos[1] + 1) ][1] == "P" or potDict[ (kingPos[0] + 1, kingPos[1] + 1) ][1] == "K" or potDict[ (kingPos[0] + 1, kingPos[1] + 1) ][1] == "B" or potDict[ (kingPos[0] + 1, kingPos[1] + 1) ][1] == "Q"):
                return False

        else:
            num = 2
            while kingPos[0] + num < 8 and kingPos[1] + num < 8:

                if potDict[ (kingPos[0] + num, kingPos[1] + num) ] == None:
                    pass

                elif potDict[ (kingPos[0] + num, kingPos[1] + num) ][0] == currentTurn:
                    break

                elif potDict[ (kingPos[0] + num, kingPos[1] + num) ][1] == "B" or potDict[ (kingPos[0] + num, kingPos[1] + num) ][1] == "Q":
                    return False

                else:
                    break

                num += 1

    if kingPos[0] + 1 < 8 and kingPos[1] - 1 > -1:
        if potDict[ (kingPos[0] + 1, kingPos[1] - 1) ] != None:
            if potDict[ (kingPos[0] + 1, kingPos[1] - 1) ][0] != currentTurn and ( potDict[ (kingPos[0] + 1, kingPos[1] - 1) ][1] == "P" or potDict[ (kingPos[0] + 1, kingPos[1] - 1) ][1] == "K" or potDict[ (kingPos[0] + 1, kingPos[1] - 1) ][1] == "B" or potDict[ (kingPos[0] + 1, kingPos[1] - 1) ][1] == "Q"):
                return False

        else:
            num = 2
            while kingPos[0] + num < 8 and kingPos[1] - num > -1:

                if potDict[ (kingPos[0] + num, kingPos[1] - num) ] == None:
                    pass

                elif potDict[ (kingPos[0] + num, kingPos[1] - num) ][0] == currentTurn:
                    break

                elif potDict[ (kingPos[0] + num, kingPos[1] - num) ][1] == "B" or potDict[ (kingPos[0] + num, kingPos[1] - num) ][1] == "Q":
                    return False

                else:
                    break

                num += 1

    if kingPos[0] - 1 > -1 and kingPos[1] + 1 < 8:
        if potDict[ (kingPos[0] - 1, kingPos[1] + 1) ] != None:
            if potDict[ (kingPos[0] - 1, kingPos[1] + 1) ][0] != currentTurn and ( potDict[ (kingPos[0] - 1, kingPos[1] + 1) ][1] == "P" or potDict[ (kingPos[0] - 1, kingPos[1] + 1) ][1] == "K" or  potDict[ (kingPos[0] - 1, kingPos[1] + 1) ][1] == "B" or potDict[ (kingPos[0] - 1, kingPos[1] + 1) ][1] == "Q"):
                return False

        else:
            num = 2
            while kingPos[0] - num > -1 and kingPos[1] + num < 8:

                if potDict[ (kingPos[0] - num, kingPos[1] + num) ] == None:
                    pass

                elif potDict[ (kingPos[0] - num, kingPos[1] + num) ][0] == currentTurn:
                    break

                elif potDict[ (kingPos[0] - num, kingPos[1] + num) ][1] == "B" or potDict[ (kingPos[0] - num, kingPos[1] + num) ][1] == "Q":
                    return False

                else:
                    break

                num += 1

    if kingPos[0] - 1 > -1 and kingPos[1] - 1 > -1:
        if potDict[ (kingPos[0] - 1, kingPos[1] - 1) ] != None:
            if potDict[ (kingPos[0] - 1, kingPos[1] - 1) ][0] != currentTurn and ( potDict[ (kingPos[0] - 1, kingPos[1] - 1) ][1] == "P" or potDict[ (kingPos[0] - 1, kingPos[1] - 1) ][1] == "K" or potDict[ (kingPos[0] - 1, kingPos[1] - 1) ][1] == "B" or potDict[ (kingPos[0] - 1, kingPos[1] - 1) ][1] == "Q"):
                return False
        else:
            num = 2
            while kingPos[0] - num > -1 and kingPos[1] - num > -1:

                if potDict[ (kingPos[0] - num, kingPos[1] - num) ] == None:
                    pass

                elif potDict[ (kingPos[0] - num, kingPos[1] - num) ][0] == currentTurn:
                    break

                elif potDict[ (kingPos[0] - num, kingPos[1] - num) ][1] == "B" or potDict[ (kingPos[0] - num, kingPos[1] - num) ][1] == "Q":
                    return False

                else:
                    break

                num += 1

    return True
