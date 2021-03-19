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

        self.snakes.append(Snake(start, len(self.snakes)+1, start_dir, self.matrix, self))
        self.snakes.append(Snake(start2, len(self.snakes)+1, start_dir2, self.matrix, self))
        self.vinner = 0

        self.gen = self.game()
        self.message = ""

    def restart(self):
        message = self.message
        self.__init__()
        self.message = message




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
                if   snake.dir == 0: snake.y -= 1
                elif snake.dir == 1: snake.x += 1
                elif snake.dir == 2: snake.y += 1
                elif snake.dir == 3: snake.x -= 1
                
                if self.checkCrash(snake):
                    self.message += "ferdig, "
                    if self.vinner == 0:
                        self.vinner = 3-player
                    else:
                        self.vinner = 3     
                    self.message += f"{self.vinner} har vunnet\n"
                    return
                else:
                    self.matrix[snake.y][snake.x] = True   
            yield self.matrix                 


class Snake:
    def __init__(self, start, player, dir, matrix, game):
        self.y = start[0]
        self.x = start[1]
        #if player == 2:
            #self.x += 10
        self.__dir = dir
        self.ai = RandomAI(self, matrix)
        self.game = game
        self.player = player
    
    @property
    def dir(self):
        return self.__dir
    
    @dir.setter
    def dir(self, new_dir):
        if not new_dir in range(4):
            raise ValueError("illegal direction")
        if (2 + new_dir) % 4 == self.dir:
            return
        self.__dir = new_dir 


class RandomAI:
    def __init__(self, snake, matrix):
        self.snake = snake
        self.matrix = matrix
        self.gen = self.generator()

    def generator(self):
        while True:
            choices = [-1, -1,  (self.snake.dir + 1) % 4, (self.snake.dir + 3) % 4]
            while choices:
                choice_index = random.randrange(len(choices))
                choice = choices[choice_index]
                bad_choice = False
                x, y = self.snake.x, self.snake.y
                dir = self.snake.dir if choice == -1 else choice
                if   dir == 0: y -= 1
                elif dir == 1: x += 1
                elif dir == 2: y += 1
                elif dir == 3: x -= 1
                try:
                    if self.matrix[y, x]:
                        bad_choice = True
                except IndexError:
                    bad_choice = True
                if bad_choice:
                    del choices[choice_index]
                    self.snake.game.message += f"player {self.snake.player}: "
                    self.snake.game.message += f"sletta {choice_index}, "
                    self.snake.game.message += f"gjenværende {choices}\n"
                    continue
                yield choice
                break
            if not choices:
                self.snake.game.message += f"player {self.snake.player} will lose\n"
                yield -1

if __name__ == "__main__":
    game = Board()
    game.game()

