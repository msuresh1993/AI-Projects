import time
from queue import PriorityQueue

class PegSolverHeuristic:
    def __init__(self, pegboard):
        self.priqueue = PriorityQueue()
        self.open = {}
        self.close = {}
        self.prev = {}
        self.costnode = {}
        self.prioritycost = {}
        self.nodesexpanded = 0
        self.prev[conv_string(pegboard)] = ""
        self.totalones = count_ones(pegboard)
        self.prioritycost[conv_string(pegboard)] = self.totalones
        #print(self.totalones)
        self.priqueue.put((self.totalones,conv_string(pegboard)) )
        self.costnode[conv_string(pegboard)] = 0
        self.done = False
        #self.f = open("pegsolver_heuristic1.txt", "w")
         #_put(conv_string(pegboard), count_ones(pegboard)).
        self.prevHeuristic = self.totalones
        self.prevboard = []
    def total_ones(self,pegboard):
        for row in range(7):
            for col in range(7):
                if pegboard[row][col] == 1:

                    self.totalones += 1

    def conv_array(self,str):
        i =0
        arr = [[9 for row in range(7)] for col in range(7)]
        for row in range(7):
            for col in range(7):
                arr[row][col] = int(str[i])
                i += 1
        return arr

    def add_next(self,board):

        prevstr = conv_string(board)
        for row in range(7):
            for column in range(7):
                #move possible from the right side
                if column != 0 and column != 6 and board[row][column-1] == 0 and board[row][column+1] == 1 and board[row][column] == 1:
                    board[row][column - 1] = 1
                    board[row][column + 1] = 0
                    board[row][column] = 0
                    #make the board into a string tostore in priority queue
                    checkstr = conv_string(board)
                    if checkstr not in self.close:
                        #increase the f(n) value.
                        self.costnode[checkstr] = self.costnode[prevstr] + 1
                        cost = self.costnode[checkstr]+count_ones(board)#count_ones is the heuristic calculating function.
                        self.priqueue.put((cost,checkstr))
                        self.prioritycost[checkstr] = cost
                        self.nodesexpanded +=1
                    if is_done(board):
                        self.done = True
                        display_board(board)
                        return True
                    board[row][column - 1] = 0
                    board[row][column + 1] = 1
                    board[row][column] = 1
                    self.prev[checkstr] = prevstr
                #move possible from the left side
                if column != 0 and column != 6 and board[row][column-1] == 1 and board[row][column+1] == 0 and board[row][column] == 1:
                    board[row][column - 1] = 0
                    board[row][column + 1] = 1
                    board[row][column] = 0
                    checkstr = conv_string(board)
                    if checkstr not in self.close:                                                                      #checking if the board position has not already been seen before.
                        self.costnode[checkstr] = self.costnode[prevstr] + 1                                            #f(n) for the new board position is 1 more than the previous board since one more peg has been removed
                        cost = self.costnode[checkstr]+count_ones(board)                                                #finds the heuristic value associated with the board positon the heuristic calculating function is count_ones
                        self.priqueue.put((cost,checkstr))                                                              #add to priority queue
                        self.prioritycost[checkstr] = cost
                        self.nodesexpanded +=1
                    if is_done(board):
                        self.done = True
                        display_board(board)
                        return True
                    board[row][column - 1] = 1
                    board[row][column + 1] = 0
                    board[row][column] = 1
                    self.prev[checkstr] = prevstr
                #move possible fro bottom
                if row != 0 and row != 6 and board[row-1][column] == 0 and board[row+1][column] == 1 and board[row][column] == 1:
                    board[row-1][column] = 1
                    board[row+1][column] = 0
                    board[row][column] = 0
                    checkstr = conv_string(board)
                    if checkstr not in self.close:
                        self.costnode[checkstr] = self.costnode[prevstr] + 1
                        cost = self.costnode[checkstr]+count_ones(board)
                        self.priqueue.put((cost,checkstr))
                        self.prioritycost[checkstr] = cost
                        self.nodesexpanded +=1
                    if is_done(board):
                        self.done = True
                        display_board(board)
                        return True

                    board[row-1][column] = 0
                    board[row+1][column] = 1
                    board[row][column] = 1
                    self.prev[checkstr] = prevstr
                #move possible from the top
                if row != 0 and row != 6 and board[row - 1][column] == 1 and board[row + 1][column] == 0 and board[row][column] == 1:
                    board[row-1][column] = 0
                    board[row+1][column] = 1
                    board[row][column] = 0
                    checkstr = conv_string(board)
                    if checkstr not in self.close:
                        self.costnode[checkstr] = self.costnode[prevstr] + 1
                        cost = self.costnode[checkstr]+count_ones(board)
                        self.priqueue.put((cost,checkstr))
                        self.prioritycost[checkstr] = cost
                        self.nodesexpanded +=1
                    if is_done(board):
                        self.done = True
                        display_board(board)
                        return True

                    board[row-1][column] = 1
                    board[row+1][column] = 0
                    board[row][column] = 1
                    self.prev[checkstr] = prevstr
        return False
#Start of the Heuristic function
    def heuristic(self):
        iden = 0
        print("started")
        while self.priqueue.empty() is not True:
            presentTuple =self.priqueue.get() #gets the next element from the priority queue
            present = presentTuple[1]  #the priority queue stores the board state as well as the cost of the node
            presentVal = presentTuple[0]
            iden = iden + 1  #the iteration number
            #self.f.write('{0},{1}\n'.format(str(iden), str(presentVal)))  #stores the values in a file
            self.nodesexpanded += 1
            currentboard = self.conv_array(present) #board stored as string
            self.prevHeuristic = presentVal
            self.prevBoard = currentboard
            #display_board(currentboard)
            #print(self.prioritycost[present])
            #inputstr = input()
            if self.add_next(currentboard) is True: #function that develops the f(n) + h(n) value also if the final state is reached returns true.
                break
            self.close[present] = self.prev[present] #otherwise adds the present node to the close list.
        current = present
        while self.prev[current] is not "" and self.done is True:  #display the board if solution is found
            display_board(self.conv_array(current))
            current = self.prev[current]
        if self.done is True:
            display_board(self.conv_array(current))
            print("nodes Expanded:"+str(self.nodesexpanded))


def is_done(pegboard):
    check = 0
    if pegboard[3][3] == 0:
        return False
    for row in range(7):
        for col in range(7):
            if(pegboard[row][col] is 1):
                if check is 1:
                    return False
                if check is 0:
                    check = 1

    return True

#FUNCTION TO CALCULATE THE HEURISTIC VALUE
def count_ones(pegboard):
    count = 0
    for row in range(7):
        for col in range(7):
            if(pegboard[row][col] == 1):
                #heuristic 1: positional bais : Simply put it adds 2 more cost to elements present in the four side boxes compared to being present in the center.
                tempcount = 1
                if row <2 or col <2:
                    tempcount = tempcount+4
                count= count +tempcount
    return count

def display_board(pegboard):
        print('\n'.join([' '.join(['{0:3}'.format(item) for item in row])for row in pegboard]))
        print('\n')

def conv_string(arr):
    arrayStr = ""
    for row in range(7):
        for col in range(7):
            arrayStr = arrayStr + str(arr[row][col])

    return arrayStr

def main():
    # input1 = [[9, 9, 1, 1, 1, 9, 9],
    #          [9, 9, 1, 1, 0, 9, 9],
    #          [1, 1, 1, 1, 0, 1, 1],
    #          [1, 1, 1, 1, 1, 1, 1],
    #          [1, 1, 1, 1, 1, 0, 1],
    #          [9, 9, 1, 0, 0, 9, 9],
    #          [9, 9, 0, 0, 0, 9, 9]]
    # input2 = [[9, 9, 1, 1, 1, 9, 9],
    #          [9, 9, 1, 1, 1, 9, 9],
    #          [1, 1, 1, 1, 1, 1, 1],
    #          [1, 1, 1, 0, 1, 1, 1],
    #          [1, 1, 1, 1, 1, 1, 1],
    #          [9, 9, 1, 1, 1, 9, 9],
    #          [9, 9, 1, 1, 1, 9, 9]]
    check = input("Do you want default Board. Answer y or n\n")
    if check == 'y':
        input1 = [[9, 9, 1, 1, 1, 9, 9],
             [9, 9, 1, 1, 0, 9, 9],
             [1, 1, 1, 1, 0, 1, 1],
             [1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 0, 1],
             [9, 9, 1, 0, 0, 9, 9],
             [9, 9, 0, 0, 0, 9, 9]]
    else:
        while(1):
            board_string = input("Enter the board as a string separated by space example first row will be - - 0 0 0 - - - - 0 1 0 - - 0 0 1 1 1 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 - - 0 0 0 - - - - 0 0 0 - -\n")
            board_list = board_string.split()
            if len(board_list) != 49:
                print("INVALID BOARD")
                continue
            input1 = [[9 for row in range(7)] for col in range(7)]
            for i in range(7):
                for j in range(7):
                    if board_list[i*7 + j] == '-':
                        input1[i][j] = 9
                    elif board_list[i*7 + j] == '1':
                        input1[i][j] = 1
                    elif board_list[i*7 + j] == '0':
                        input1[i][j] = 0
                    else:
                        continue
            break

    pegs2 = PegSolverHeuristic(input1)
    x  = time.clock()
    pegs2.heuristic()
    y = time.clock()
    print("TIME TAKEN:", y - x," Seconds" )

if __name__ == '__main__':
    main()

