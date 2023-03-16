import random
import time
import functions


class BoardOutException(Exception):
    """A point is out of board bounds"""


class ImpossibleShrimpException(Exception):
    """Shrimp's size doesn't make sense"""


class ShotAtDeadException(Exception):
    """Attempted to shoot a dead cell of a shrimp"""


class WrongCoordinateInputException(Exception):
    """Received coordinates do not match the standard"""


class ShrimpOnContourException(Exception):
    """Part of a shrimp is created too close to the other shrimp"""


class BadBoardException(Exception):
    """Impossible to complete filling up the board with shrimps"""


# Точка на поле игры. x - число колонки, y - число строки
class Dot:
    _x = 0
    _y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if 1 <= x <= 6:
            self._x = x
        else:
            raise BoardOutException

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if 1 <= y <= 6:
            self._y = y
        else:
            raise BoardOutException

    @property
    def tuple(self):
        return self.x, self.y


# Креветка, также известная как корабль
# size - возможный размер от 1 до 3
# space - расположение самой верхней и левой точки креветки
# is_horizontal - True: креветка расположена горизонтально на поле игры, False: вертикально
# lives - неповрежденные ячейки креветки, зависит от размера
class Shrimp:
    _size = 1
    _space = (1, 1)
    _is_horizontal = True
    _lives = 1

    def __init__(self, size, space, is_horizontal, lives):
        self.size = size
        self.space = space
        self.is_horizontal = is_horizontal
        self.lives = lives

        self.dots()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if 1 <= size <= 3:
            self._size = size
        else:
            raise ImpossibleShrimpException

    @property
    def space(self):
        return self._space

    @space.setter
    def space(self, space):
        if 1 <= space[0] <= 6 and 1 <= space[1] <= 6:
            self._space = space
        else:
            raise BoardOutException

    @property
    def is_horizontal(self):
        return self._is_horizontal

    @is_horizontal.setter
    def is_horizontal(self, is_horizontal):
        if isinstance(is_horizontal, bool):
            self._is_horizontal = is_horizontal
        else:
            raise TypeError("Variable is_horizontal is not boolean")

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, lives):
        if 0 <= lives <= self.size:
            self._lives = lives
        else:
            raise ValueError(f"Incorrect amount of lives: {lives}")

    # Возвращает лист из объектов Dot с координатами каждой ячейки
    def dots(self):
        dots_list = []

        for i in range(self.size):
            if self.is_horizontal:
                dots_list.append(Dot(self.space[0] + i, self.space[1]))
            else:
                dots_list.append(Dot(self.space[0], self.space[1] + i))

        return dots_list


# Поле игры
# grid - словарь, который содержит значения каждой ячейки игры в формате (1, 1): "-" или (3, 6): "■"
# shrimps - лист объектов Shrimp, все креветки на доске
# shrimps_alive - целое число, количество живых креветок
class Board:
    def __init__(self):
        self.grid = {}
        self.clean_board()
        self.shrimps = []
        self.shrimps_alive = 0

    # Очищает поле игры
    def clean_board(self):
        for x in range(1, 7):
            for y in range(1, 7):
                self.grid[x, y] = "-"

    # Добавляет новую креветку
    def add_shrimp(self, shrimp):
        # Вызывает ошибку если креветка слишком близко к другой креветке
        for dot in shrimp.dots():
            if dot in self.contour_all():
                raise ShrimpOnContourException

        # Добавляет все части креветки
        for dot in shrimp.dots():
            self.grid[dot.tuple] = "■"
        self.shrimps_alive += 1
        self.shrimps.append(shrimp)

    # Находит креветку по точке
    def find_shrimp(self, dot):
        for shrimp in self.shrimps:
            if dot in shrimp.dots():
                return shrimp

    # Топит креветку, обводит креветку вокруг
    def sink_shrimp(self, shrimp):
        for dot in self.contour(shrimp):
            self.grid[dot.tuple] = "T"
        self.shrimps_alive -= 1

    # Контур креветки, возвращает список объектов Dot
    @staticmethod
    def contour(shrimp):
        contour_list = []

        for dot in shrimp.dots():
            x = dot.x - 1
            y = dot.y - 1

            for i in range(3):
                for j in range(3):
                    try:
                        contour_dot = Dot(x + j, y + i)
                    except BoardOutException:
                        pass
                    else:
                        if (contour_dot not in shrimp.dots()) and (contour_dot not in contour_list):
                            contour_list.append(contour_dot)

        return contour_list

    # Контур всех креветок, возвращает список объектов Dot
    def contour_all(self):
        contour_list = []
        for shrimp in self.shrimps:
            contour_list += self.contour(shrimp)

        unique_list = []
        for dotdot in contour_list:
            if dotdot not in unique_list:
                unique_list.append(dotdot)

        return unique_list

    # Производит выстрел по заданной точке, возвращает True - при попадании в креветку, False - в другом случае
    def shot(self, dot):
        square = self.grid[dot.tuple]
        hit = False

        if square == "-":
            self.grid[dot.tuple] = "T"
        elif square == "■":
            hit = True
            self.grid[dot.tuple] = "╳"

            shrimp = self.find_shrimp(dot)
            shrimp.lives -= 1
            if shrimp.lives < 1:
                self.sink_shrimp(shrimp)
        elif square == "╳":
            raise ShotAtDeadException("Attempted to shoot at dead cell of a shrimp")
        elif square == "T":
            pass

        return hit


# Класс игрока
class Player:
    def __init__(self, own_board, rival_board):
        self.own_board = own_board
        self.rival_board = rival_board

    def ask(self):
        pass

    def move(self):
        pass


# Класс пользователя
class User(Player):
    # Обработка ввода пользователя
    def ask(self):
        choice = input("Ваш ход: ").lower()
        letter_list = ["а", "б", "в", "г", "д", "е"]
        num_list = ["1", "2", "3", "4", "5", "6"]

        if len(choice) != 2:
            raise WrongCoordinateInputException
        elif choice[0] in letter_list and choice[1] in num_list:
            x = letter_list.index(choice[0]) + 1
            y = int(choice[1])
        elif choice[0] in num_list and choice[1] in letter_list:
            x = letter_list.index(choice[1]) + 1
            y = int(choice[0])
        else:
            raise WrongCoordinateInputException

        if self.rival_board.grid[x, y] == "╳":
            raise ShotAtDeadException

        return x, y

    # Обработка хода игрока. Возвращает True если есть попадание
    def move(self):
        # Случайный пример ввода координат
        str_random_coord = random.choice(["1", "2", "3", "4", "5", "6", "7"]) + \
                           random.choice(["а", "б", "в", "г", "д", "е"])
        if random.choice([True, False]):
            str_random_coord.upper()

        if random.choice([True, False]):
            letter1, letter2 = str_random_coord[0], str_random_coord[1]
            str_random_coord = letter2 + letter1

        functions.print_grid(own_grid=self.own_board.grid,
                             rival_grid=self.rival_board.grid,
                             low_line="Введите координаты, например " + str_random_coord)

        # Петля, пока игрок не введет все правильно
        while True:
            try:
                x, y = self.ask()
            except WrongCoordinateInputException:
                functions.print_grid(self.own_board.grid,
                                     self.rival_board.grid,
                                     low_line="Введите координаты, например " + str_random_coord,
                                     message="Ввели что-то неправильно, попробуйте еще раз")
            except ShotAtDeadException:
                functions.print_grid(self.own_board.grid,
                                     self.rival_board.grid,
                                     low_line="Введите координаты, например " + str_random_coord,
                                     message="Вы пытаетесь выстрелить в мертвую часть креветки, с вами все в порядке?")
            else:
                break

        return self.rival_board.shot(Dot(x, y))


# Класс ИИ
class AI(Player):
    # ИИ выбирает случайную клетку
    def ask(self):
        empty_dots = []
        grid = self.rival_board.grid

        for x, y in grid:
            if grid[x, y] == "-" or grid[x, y] == "■":
                empty_dots.append((x, y))

        return random.choice(empty_dots)

    # Обработка хода, в основном для визуализации и паузы. Возвращает True если есть попадание
    def move(self):
        functions.print_grid(own_grid=self.rival_board.grid,
                             rival_grid=self.own_board.grid,
                             low_line="Ваш противник отдает приказы")
        time.sleep(2)
        x, y = self.ask()

        hit = self.rival_board.shot(Dot(x, y))
        if hit:
            functions.print_grid(own_grid=self.rival_board.grid,
                                 rival_grid=self.own_board.grid,
                                 low_line="Противник подбил вашу креветку!")
        else:
            functions.print_grid(own_grid=self.rival_board.grid,
                                 rival_grid=self.own_board.grid,
                                 low_line="Ваш противник промахнулся")
        time.sleep(2)
        return hit


# Класс игры. user - игрок, user_board - поле игры, ai - ИИ, ai_board - поле ИИ
class Game:
    user = None
    user_board = None
    ai = None
    ai_board = None

    # Возвращает случайное заполненное креветками поле игры
    @staticmethod
    def random_board():
        def create_board():
            board = Board()
            allowed_dots = []  # Лист Dot которые можно использовать для установки креветки

            for coord in board.grid.keys():
                allowed_dots.append(Dot(coord[0], coord[1]))

            def refresh_allowed_dots():
                nonlocal allowed_dots, board

                # Исключение каждой Dot вокруг креветок
                for contour_dot in board.contour_all():
                    if contour_dot in allowed_dots:
                        allowed_dots.remove(contour_dot)

                # Исключение Dot самих креветок
                for shrimp in board.shrimps:
                    for shrimp_dot in shrimp.dots():
                        if shrimp_dot in allowed_dots:
                            allowed_dots.remove(shrimp_dot)

            # Создание креветки по размеру и количеству
            def shrimp_factory(size, amount):
                nonlocal allowed_dots, board

                tries = 0
                for i in range(amount):
                    while True:
                        if tries > 1000:
                            raise BadBoardException
                        try:
                            board.add_shrimp(Shrimp(
                                size=size,
                                space=random.choice(allowed_dots).tuple,
                                is_horizontal=random.choice([True, False]),
                                lives=size
                            ))
                        except BoardOutException:
                            tries += 1
                        except ShrimpOnContourException:
                            tries += 1
                        except IndexError:
                            tries += 1
                        else:
                            refresh_allowed_dots()
                            break

            shrimp_factory(size=3, amount=1)
            shrimp_factory(size=2, amount=2)
            shrimp_factory(size=1, amount=4)

            return board

        return_board = None
        while return_board is None:
            try:
                return_board = create_board()
            except BadBoardException:
                pass

        return return_board

    # Вывод приветствия
    @staticmethod
    def greet():
        functions.clean_screen()
        print(" -=BattleShrimp=-")
        print()
        print("Игра 'Креветочный Бой' - тоже что и 'Морской Бой', только с боевыми морепродуктами.")
        print("Поле игры размером 6х6. У каждого игрока есть: 1 Лобстер ■ ■ ■, 2 Креветки ■ ■ и 4 Краба ■.")
        print("Если игрок попадет в цель, то может сделать ход еще раз")
        print("Выбор клетки осуществляется вводом символов - цифры и буквы, где буква - это колонка, а цифра - строка.")
        print("Например: А1 или е3 или 4Д. Порядок и регистр значения не имеют.")
        print()
        print("Попутного ветра!")
        print()
        print("Нажмите Enter чтобы продолжить...")
        input("Ваш ввод: ")

    # Инициация игры
    def start(self):
        self.user_board = self.random_board()
        self.ai_board = self.random_board()
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

        self.greet()

        self.loop()

    # Игровой цикл
    def loop(self):
        player_turn = True
        while self.user_board.shrimps_alive > 0 and self.ai_board.shrimps_alive > 0:
            if player_turn:
                player_turn = self.user.move()
            else:
                player_turn = not self.ai.move()

        # Вывод победителя
        if self.user_board.shrimps_alive < 1:
            functions.print_grid(own_grid=self.user_board.grid,
                                 rival_grid=self.ai_board.grid,
                                 low_line="Победил ваш противник!")
        else:
            functions.print_grid(own_grid=self.user_board.grid,
                                 rival_grid=self.ai_board.grid,
                                 low_line="Вы победили!")
