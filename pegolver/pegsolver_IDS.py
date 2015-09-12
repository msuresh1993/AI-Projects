from queue import PriorityQueue
import time
import fileinput


class PegSolver:
    def __init__(self, pegboard):
        self.pegboard = pegboard
        self.solution_found = False
        self.count = 0
        self.nodesexpanded = 0
        for row in range(7):
            for column in range(7):
                if pegboard[row][column] == 1:
                    self.count += 1

    def display_board(self):
        print('\n'.join([' '.join(['{0:3}'.format(item) for item in row])for row in self.pegboard]))
        print('\n')

    def solved(self):
        if self.count == 1 and self.pegboard[3][3] == 1:
            return True

    def iterative_deepning(self, current_depth, max_depth):
        self.nodesexpanded += 1
        if self.solved():
            self.solution_found = True
            print("NODES EXPANDED:", self.nodesexpanded)
            self.display_board()
            return
        if current_depth > max_depth:
            return
        for row in range(7):
            for column in range(7):

                    if 0 != column and column != 6 and self.pegboard[row][column-1] == 0 and self.pegboard[row][column+1] == 1 and self.pegboard[row][column] == 1:

                        self.pegboard[row][column - 1] = 1
                        self.pegboard[row][column + 1] = 0
                        self.pegboard[row][column] = 0
                        self.count -= 1
                        self.iterative_deepning(current_depth + 1, max_depth)

                        self.count += 1
                        self.pegboard[row][column - 1] = 0
                        self.pegboard[row][column + 1] = 1
                        self.pegboard[row][column] = 1
                        if self.solution_found is True:
                            self.display_board()
                            return
                    if column != 0 and column != 6 and self.pegboard[row][column-1] == 1 and self.pegboard[row][column+1] == 0 and self.pegboard[row][column] == 1:
                        self.pegboard[row][column - 1] = 0
                        self.pegboard[row][column + 1] = 1
                        self.pegboard[row][column] = 0
                        self.count -= 1
                        self.iterative_deepning(current_depth + 1, max_depth)

                        self.count += 1
                        self.pegboard[row][column - 1] = 1
                        self.pegboard[row][column + 1] = 0
                        self.pegboard[row][column] = 1
                        if self.solution_found is True:
                            self.display_board()
                            return
                    if row != 0 and row != 6 and self.pegboard[row-1][column] == 0 and self.pegboard[row+1][column] == 1 and self.pegboard[row][column] == 1:
                        self.pegboard[row - 1][column] = 1
                        self.pegboard[row + 1][column] = 0
                        self.pegboard[row][column] = 0
                        self.count -= 1
                        self.iterative_deepning(current_depth + 1, max_depth)

                        self.count += 1
                        self.pegboard[row - 1][column] = 0
                        self.pegboard[row + 1][column] = 1
                        self.pegboard[row][column] = 1
                        if self.solution_found is True:
                            self.display_board()
                            return
                    if row != 0 and row != 6 and self.pegboard[row - 1][column] == 1 and self.pegboard[row + 1][column] == 0 and self.pegboard[row][column] == 1:
                        self.pegboard[row - 1][column] = 0
                        self.pegboard[row + 1][column] = 1
                        self.pegboard[row][column] = 0
                        self.count -= 1
                        self.iterative_deepning(current_depth + 1, max_depth)

                        self.count += 1
                        self.pegboard[row - 1][column] = 1
                        self.pegboard[row + 1][column] = 0
                        self.pegboard[row][column] = 1
                        if self.solution_found is True:
                            self.display_board()
                            return
        return



def display_board(pegboard):
        print('\n'.join([' '.join(['{0:3}'.format(item) for item in row])for row in pegboard]))
        print('\n')

def main():
    check = input("Do you want default Board. Answer y or n\n")
    if check == 'y':
        input1 = [[9, 9, 0, 0, 0, 9, 9],
                 [9, 9, 0, 1, 0, 9, 9],
                 [0, 0, 1, 1, 1, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0],
                 [9, 9, 0, 0, 0, 9, 9],
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


    pegs = PegSolver(input1)
    x = time.clock()
    #for i in range(32):
    pegs.iterative_deepning(0,12)
    #    if pegs.solution_found is True:
    #        break
    y = time.clock()
    print("TIME TAKEN:", y-x, " Seconds")

if __name__ == '__main__':
    main()

