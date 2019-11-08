from random import choice


class ball():
    def __init__(self, canv, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.live = 1
        self.time = 0
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def time_live(self, balls, canv):
        """Время жизни мяча во время раунда

        Метод удаляет мяч по прошествии 1 секунды
        """
        if self.vx == 0 and self.vy == 0 and self.time >= 1020:
            canv.delete(self.id)
            balls.remove(self)
        else:
            self.time += 30

    def set_coords(self, canv):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self, canv):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy += 2
        if self.x + self.vx >= 780:
            self.x = 1560 - self.x - self.vx
            self.vx = - self.vx
        elif self.x + self.vx <= 20:
            self.x = 40 - self.x - self.vx
            self.vx = - self.vx
        else:
            self.x += self.vx
        if self.y + self.vy >= 550:
            self.y = 550 - (2 / 3) * (self.y + self.vy - 550)
            self.vy = - self.vy / 1.5
            self.vx = self.vx / 1.5
        else:
            self.y += self.vy
        if self.vx ** 2 + self.vy ** 2 < 2:
            self.vy = 0
            self.vx = 0
            self.y = 550
        self.set_coords(canv)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (obj.x - self.x) ** 2 + (obj.y - self.y) ** 2 <= (obj.r + self.r) ** 2:
            return True
        else:
            return False
