from random import randrange as rnd, choice
import tkinter as tk
import math
import time
from class_ball import ball

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball(canv)
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an) * (-1)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class mega_gun(gun):
    def __init__(self):
        self.id_line = canv.create_line(20, 450, 50, 420, width=1)
        super().__init__()

    def targetting(self, event=0):
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )
        canv.coords(self.id_line, 20, 450,
                    20 + 1000 * math.cos(self.an),
                    450 + 1000 * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 150:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='red')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self, number):
        self.number = number
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 750)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(20, 40)
        self.vx = rnd(5, 15) * choice([-1, 1])
        self.vy = rnd(5, 15) * choice([-1, 1])
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def move(self):
        if self.live == 1:

            if self.x + self.r + self.vx >= 800:
                self.x = 1600 - self.x - 2 * self.r - self.vx
                self.vx = - self.vx
            elif self.x - self.r + self.vx <= 400:
                self.x = 800 - self.x + 2 * self.r - self.vx
                self.vx = - self.vx
            else:
                self.x += self.vx
            if self.y + self.r + self.vy >= 550:
                self.y = 1100 - self.y - 2 * self.r - self.vy
                self.vy = - self.vy
            elif self.y - self.r + self.vy <= 0:
                self.y = - self.y + 2 * self.r - self.vy
                self.vy = - self.vy
            else:
                self.y += self.vy

            self.set_coords()

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def hit(self):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)


class points():
    """Подсчет очков в левом верхнем углу поля."""

    def __init__(self):
        self.points = 0
        self.id_points = canv.create_text(30, 30, text=self.points, font='28')

    def hit(self, points=1):
        self.points += points
        canv.itemconfig(self.id_points, text=self.points)


n = 3  # количесвто целей
easy = True  # Режим игры
targets = []
for i in range(n):
    targets.append(target(i))
screen1 = canv.create_text(400, 300, text='', font='28')
if easy:
    g1 = mega_gun()
else:
    g1 = gun()
bullet = 0
balls = []
points = points()


def new_game(event=''):
    global screen1, balls, bullet, points, targets
    for t in targets:
        t.new_target()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    k = 0
    z = 0.03
    for t in targets:
        t.live = 1
    round = True
    while round or balls:
        for t in targets:
            t.move()
        for b in balls:
            b.move(canv)
            for t in targets:
                if t.live and b.hittest(t):
                    t.live = 0
                    k += 1
                    t.hit()
                    points.hit()
                if k == n:
                    round = False
            if not round:
                g1.f2_on = 0
                g1.f2_power = 10
                canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
            b.time_live(balls, canv)
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    root.after(750, new_game)


new_game()

tk.mainloop()
