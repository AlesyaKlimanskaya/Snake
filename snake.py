import random
from tkinter import *

# Создаем константы
WIDTH = 800   # ширина окна
HEIGHT = 600  # высота окна
BG_Color = 'black' # цвет фона
S_size = 20     # размер клетки поля
food_color = 'red' # цвет еды
head_color = 'turquoise' # цвет головы змеи
body_color = 'green' # цвет туловища змеи
Snake_length = 3 # длина змейки изначальная
speed = 130 #скорость движения

# создаем окно, в котором мы зададим его название и размер
window = Tk() # переменная отвечает за наше окно
window.title("GAME SNAKE on Python") # имя окна
window.resizable(False, False) #не дает пользователю изменить размер окна путем его растягивая
window.wm_attributes('-topmost', 1) # показывает окно приложения по верху всех открытых программ

score = 0 # счетчик счета
route = 'down' # изначально заданое направление змейки

# создаем надпись отражающую подсчет очков
l_score = Label(window, text='Score: {}'.format(score), font=('Arial',25))
l_score.pack()
# создаем поле с областью в которой будут проходить основные действия
c = Canvas(window, width=WIDTH, height=HEIGHT, bg=BG_Color)
c.pack()

# создаем класс змейка
class Snake():
    def __init__(self):
        self.snake_l = Snake_length # задаем длину змейке
        self.coord = [(0,0)]*3 # задаем матрицу координат 2 на 3
        self.squares = [] # задаем массив для отрисовки самой змейки

# создаем квадратик который будет телом нашей змеи, задаем ему цвет
# квадрат добавляем в массив
        for x, y in self.coord:
            square = c.create_rectangle(x, y, x + S_size, y + S_size, fill=body_color)
            self.squares.append(square)

# создаем класс для еды
class Food():
    def __init__(self):
# еда имеет 2-ва значения по х и у, она может появляться в любом месте. Посчитаем сколько клеток поместиться по х и по у,
# для этого ширину и высоту мы делим на размер заданной клетки поля и отнимаем 1(так мы установили диапозон с 0).
# чтобы перевести обратно в пиксели умножаем на размер клетки поля. Запускаем генератор random в вычесленном диапазоне
        x = random.randint(0, (WIDTH/S_size)-1)* S_size #800/20 = 40
        y = random.randint(0, (HEIGHT/S_size)-1)* S_size #600/20 = 30
        self.coord = [x, y] # заносим данные координаты в массив
# создаем овал с начальными координатами в точке х,у а также х и у + наше пространство, а также задаем цвет нашей еды
        c.create_oval(x, y, x + S_size, y + S_size, fill=food_color)

# создаем функцию движения в которую передаем змейку и еду. Задача функции при каждом
# нажатии кнопки изменять координаты и совершать ровно одно движение
def move(snake, food):
    for x, y in snake.coord:
        square = c.create_rectangle(x, y, x + S_size, y + S_size, fill=body_color)

    x, y = snake.coord[0]

    if route == 'down':
        y += S_size
    elif route == 'up':
        y -= S_size
    elif route == 'left':
        x -= S_size
    elif route == 'right':
        x += S_size

    snake.coord.insert(0, (x, y)) # в первую ячейку массива будем вставлять кординаты головы
    square = c.create_rectangle(x, y, x + S_size, y + S_size, fill=head_color)# отрисовываем голову, для этого создаем прямоугольник
# созданный прямоугольник мы добавляем в массив в ячейку с индексом равным 0 так как это голова,
# таким образом мы соединяем голову со всей змейкой
    snake.squares.insert(0, square)
# пропишем подсчет съеденных яблок и появления нового на игровом поле
    if x == food.coord[0] and y == food.coord[1]:
        global score
        score +=1
        l_score.config(text='Score: {}'.format(score))
        c.delete('food')
        food = Food()
    else:
        x, y = snake.coord[-1] # убираем хвост после каждого хода головы
        square = c.create_rectangle(x, y, x + S_size, y + S_size, fill= BG_Color)
        del snake.coord[-1]
        c.delete(snake.squares[-1]) # удаляем отрисовку квадрата
        del snake.squares[-1]
# пропишем проверку на столкновение
    if check_clashes(snake):
        game_over()
    else:
        window.after(speed, move, snake, food) # Данный метод снова запускаем отрисовку через заданное количество
# милисекунд.

# функция изменения направления движения
def change_route(new_route):
    global route

    if new_route == 'down':
        if route != 'up':
            route = new_route
    if new_route == 'up':
        if route != 'down':
            route = new_route
    if new_route == 'left':
        if route != 'right':
            route = new_route
    if new_route == 'right':
        if route != 'left':
            route = new_route

# функция отвечающая за отслеживание выхода змейки за координаты игрового поля
def check_clashes(snake):
    x, y = snake.coord[0]
    if x < 0 or x >= WIDTH:
        return True
    elif y < 0 or y >= HEIGHT:
        return True
    for snake_l in snake.coord[1:]:
        if x == snake_l[0] and y == snake_l[1]:
            return True
# функция окончания игры
def game_over():
    c.delete(ALL)
    c.create_text(c.winfo_width()/2, c.winfo_height()/2, font=('Cambria', 50), text='Game over\n\n Try again', fill='white')

# привязка клавиш направления движения в нашем окне
window.bind('<Down>', lambda event: change_route('down'))
window.bind('<Up>', lambda event: change_route('up'))
window.bind('<Left>', lambda event: change_route('left'))
window.bind('<Right>', lambda event: change_route('right'))

# создаем объекты нашего класса
snake = Snake()
food = Food()

# вызываем функцию
move(snake,food)

# создаем кнопку для запуска игры
btn = Button(window, text = "START", width=29, height = 1, font = 'Arial 35', fg='red', bg = 'yellow')
btn.pack()

#запускаем окно с помощюь функции mainloop
window.mainloop()

