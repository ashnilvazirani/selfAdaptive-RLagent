import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as timeDisplay
import time
SPM_SCALE_PARAM = 10
SEARCH_LENGTH_SCALE_PARAM = 4
POSSIBLE_MOVES = 4
NUMBER_OF_EPISODES = 10
SEARCH_PARAM = 200
moveX = []
timeY=[]
thingX = []
thingTimeY=[]
from gameRules import initialize_game, oneRandomStep,\
                            actionDOWN, actionLEF,\
                            actionRIGHT, actionUP,\
                            isEnd, placeNewTile
f = open('movesFile.txt', 'r+')
f.truncate(0)

f = open('timeForExecution.txt', 'r+')
f.truncate(0)

def get_search_params(moveNumber):
    numberOfSearches = SPM_SCALE_PARAM * (1+(moveNumber // SEARCH_PARAM))
    lengthOfSearch = SEARCH_LENGTH_SCALE_PARAM * (1+(moveNumber // SEARCH_PARAM))
    return numberOfSearches, lengthOfSearch

def agentStep(board, numberOfSearches, lengthOfSearch):
    # FILENAME_TO_WRITE = "TestWith_"+str()+""+".txt"
    FILE_OBJECT = open("movesFile.txt", "a")
    TIME_FILE = open("timeForExecution.txt", "a")
    idealMoves = [actionLEF, actionUP, actionDOWN, actionRIGHT]
    moveScores = np.zeros(POSSIBLE_MOVES)
    start = time.time()
    for first_move_index in range(POSSIBLE_MOVES):
        first_move_function =  idealMoves[first_move_index]
        board_with_first_move, first_move_made, first_move_score = first_move_function(board)
        if first_move_made:
            board_with_first_move = placeNewTile(board_with_first_move)
            moveScores[first_move_index] += first_move_score
        else:
            continue
        for _ in range(numberOfSearches):
            moveNumber = 1
            currentBoard = np.copy(board_with_first_move)
            game_valid = True
            while game_valid and moveNumber < lengthOfSearch:
                currentBoard, game_valid, score = oneRandomStep(currentBoard)
                if game_valid:
                    currentBoard = placeNewTile(currentBoard)
                    moveScores[first_move_index] += score
                    moveNumber += 1
    bestMoveInd = np.argmax(moveScores)
    moveSelected = idealMoves[bestMoveInd]
    currentBoard, game_valid, score = moveSelected(board)
    endTime = time.time()-start;
    print(currentBoard)
    text = str(idealMoves[bestMoveInd])
    text = text.split(' ')[1].strip(' ')
    out = str("("+text+","+str(score)+") \n")
    FILE_OBJECT.write(out)
    print(out)
    print("ITERATION TIME: ", endTime)
    return currentBoard, game_valid, endTime

def agentLearn(board):
    moveNumber = 0
    continueGame = True
    while continueGame:
        moveNumber += 1
        numberOfSearches, lengthOfSearch = get_search_params(moveNumber)
        board, continueGame,endTime = agentStep(board, numberOfSearches, lengthOfSearch)
        # board, continueGame, endTime = agentStep(board, 40, 30)
        if continueGame:
            board = placeNewTile(board)
        if isEnd(board):
            continueGame = False
        print(board)
        print(moveNumber)
        moveX.append(moveNumber)
        timeY.append(endTime)
    print(board)
    return np.amax(board)

def agentLearnOPT(board):
    moveNumber = 0
    continueGame = True
    while continueGame:
        moveNumber += 1
        board, continueGame, endTime = agentStep(board, 40, 30)
        if continueGame:
            board = placeNewTile(board)
        if isEnd(board):
            continueGame = False
        print(board)
        print(moveNumber)
        moveX.append(moveNumber)
        timeY.append(endTime)
    print(board)
    return np.amax(board)


def plotAnalysis():
    tick_locations = np.arange(1, 12)
    final_scores = []
    thingStartTime = time.time()
    for itr in range(NUMBER_OF_EPISODES):
        print('thing is ', itr)
        board = initialize_game()
        game_is_win = agentLearn(board)
        final_scores.append(game_is_win)
        thingEndTime = time.time() - thingStartTime
        print(f"thing time for {itr}: ", thingEndTime)
        thingX.append(itr)
        thingTimeY.append(thingEndTime)
    all_counts = np.zeros(11)
    unique, counts = np.unique(np.array(final_scores), return_counts=True)
    unique = np.log2(unique).astype(int)
    index = 0

    for tick in tick_locations:
        if tick in unique:
            all_counts[tick-1] = counts[index]
            index += 1
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    ax1.bar(tick_locations, all_counts)
    ax1.set_xticks(tick_locations, minor=False)
    ax1.set_xticklabels(np.power(2, tick_locations), fontdict=None, minor=False)
    # ax1.xticks(tick_locations, np.power(2, tick_locations))
    # ax1.xlabel("Score of Game", fontsize = 24)
    # ax1.ylabel(f"Frequency per {NUMBER_OF_EPISODES} runs", fontsize = 24)
    ax1.set_xlabel("Number Of iterations")
    ax1.set_ylabel("Result")
    ax2.scatter(moveX, timeY)
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Iteration Time")
    ax3.scatter(thingX, thingTimeY)
    ax3.set_xlabel("Thing")
    ax3.set_ylabel("Thing Time")
    plt.show()
    # ax2.show() 
    # ax1.show()
    # ax2.show()


def plotConAnalysis():
    tick_locations = np.arange(1, 12)
    final_scores = []
    thingStartTime = time.time()
    for itr in range(NUMBER_OF_EPISODES):
        print('thing is ', itr)
        board = initialize_game()
        game_is_win = agentLearnOPT(board)
        final_scores.append(game_is_win)
        thingEndTime = time.time() - thingStartTime
        print(f"thing time for {itr}: ", thingEndTime)
        thingX.append(itr)
        thingTimeY.append(thingEndTime)
    all_counts = np.zeros(11)
    unique, counts = np.unique(np.array(final_scores), return_counts=True)
    unique = np.log2(unique).astype(int)
    index = 0

    for tick in tick_locations:
        if tick in unique:
            all_counts[tick-1] = counts[index]
            index += 1
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    ax1.bar(tick_locations, all_counts)
    ax1.set_xticks(tick_locations, minor=False)
    ax1.set_xticklabels(np.power(2, tick_locations), fontdict=None, minor=False)
    # ax1.xticks(tick_locations, np.power(2, tick_locations))
    # ax1.xlabel("Score of Game", fontsize = 24)
    # ax1.ylabel(f"Frequency per {NUMBER_OF_EPISODES} runs", fontsize = 24)
    ax1.set_xlabel("Number Of iterations")
    ax1.set_ylabel("Result")
    ax2.scatter(moveX, timeY)
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Iteration Time")
    ax3.scatter(thingX, thingTimeY)
    ax3.set_xlabel("Thing")
    ax3.set_ylabel("Thing Time")
    plt.show()
    # ax2.show() 
    # ax1.show()
    # ax2.show()

	
