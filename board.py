import random
import numpy as np

SIZE = 20



class Board:
    def __init__(self):
        self.snakes = []
        self.matrix = np.zeros((SIZE, SIZE), dtype=bool)

        start = [random.randrange(10), random.randrange(10)] 
        start2 = [19 - start[0], 19 - start[1]]
        print(start, start2)
        #TOD0 lag metode som passer på at start og start_dir passer sammen
        start_dir = random.randrange(4) # N = 0, E = 1, S = 2, W  = 3
        start_dir2 = (start_dir + 2) % 4

        self.snakes.append(Snake(start, len(self.snakes)+1, start_dir))
        self.snakes.append(Snake(start2, len(self.snakes)+1, start_dir2))
        self.vinner = 0

        self.gen = self.game()

    def restart(self):
        self.__init__()




    def checkCrash(self, snake):
        if snake.x < 0 or snake.x >= SIZE:
            return True
        if snake.y < 0 or snake.y >= SIZE:
            return True
        if self.matrix[snake.y][snake.x]:
            return True
        return False

    def printBoard(self):
        for y in range(SIZE):
            for x in range(SIZE):
                if self.matrix[y][x]:
                    print(" S ", end = "")
                else:
                    print(" * ", end = "")
            print("\n")



    def game(self):
        while self.vinner == 0:
            player = 0
            for snake in self.snakes:
                player += 1
                if snake.dir == 0:
                    snake.y -= 1
                if snake.dir == 1:
                    snake.x += 1
                if snake.dir == 2:
                    snake.y += 1
                if snake.dir == 3:
                    snake.x -= 1
                
                if self.checkCrash(snake):
                    print("ferdig")
                    if self.vinner == 0:
                        self.vinner = 3-player
                    else:
                        self.vinner = 3     
                    print(f"{self.vinner} har vunnet")
                    raise StopIteration()
                else:
                    self.matrix[snake.y][snake.x] = True   
            yield self.matrix                 


class Snake:
    def __init__(self, start, player, dir):
        self.y = start[0]
        self.x = start[1]
        #if player == 2:
            #self.x += 10
        self.dir = dir

if __name__ == "__main__":
    game = Board()
    game.game()