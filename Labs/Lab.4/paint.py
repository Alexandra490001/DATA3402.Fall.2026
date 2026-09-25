
import math


class Canvas:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]

    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]

    def v_line(self, x, y, h, **kargs):
        for i in range(x, x + h):
            self.set_pixel(i, y, **kargs)

    def h_line(self, x, y, w, **kargs):
        for i in range(y, y + w):
            self.set_pixel(x, i, **kargs)

    def line(self, x1, y1, x2, y2, **kargs):
        slope = (x2 - x1) / (y2 - y1)

        for y in range(y1, y2):
            x = x1 + int(slope * (y - y1))
            self.set_pixel(x, y, **kargs)

    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


class Shape:

    def area(self):
        raise NotImplementedError

    def perimeter_points(self):
        raise NotImplementedError

    def contains(self, x, y):
        raise NotImplementedError

    def paint(self, canvas):
        raise NotImplementedError

    def overlaps(self, other):
        for x, y in self.perimeter_points():
            if other.contains(x, y):
                return True

        for x, y in other.perimeter_points():
            if self.contains(x, y):
                return True

        return False


class Rectangle(Shape):

    def __init__(self, length, width, x, y):
        self.__length = length
        self.__width = width
        self.__x = x
        self.__y = y

    def area(self):
        return self.__length * self.__width

    def perimeter_points(self):
        return [
            (self.__x, self.__y),
            (self.__x + self.__length, self.__y),
            (self.__x + self.__length, self.__y + self.__width),
            (self.__x, self.__y + self.__width)
        ]

    def contains(self, x, y):
        return (
            self.__x <= x <= self.__x + self.__length
            and
            self.__y <= y <= self.__y + self.__width
        )

    def paint(self, canvas):
        canvas.h_line(
            self.__x,
            self.__y,
            self.__width,
            char='*'
        )

        canvas.h_line(
            self.__x + self.__length - 1,
            self.__y,
            self.__width,
            char='*'
        )

        canvas.v_line(
            self.__x,
            self.__y,
            self.__length,
            char='*'
        )

        canvas.v_line(
            self.__x,
            self.__y + self.__width - 1,
            self.__length,
            char='*'
        )

    def __repr__(self):
        return (
            "Rectangle(" +
            repr(self.__length) + "," +
            repr(self.__width) + "," +
            repr(self.__x) + "," +
            repr(self.__y) +
            ")"
        )


class Circle(Shape):

    def __init__(self, radius, x, y):
        self.__radius = radius
        self.__x = x
        self.__y = y

    def area(self):
        return math.pi * self.__radius ** 2

    def perimeter_points(self):
        points = []

        for i in range(16):
            angle = 2 * math.pi * i / 16

            x = self.__x + self.__radius * math.cos(angle)
            y = self.__y + self.__radius * math.sin(angle)

            points.append((x, y))

        return points

    def contains(self, x, y):
        distance_squared = (
            (x - self.__x) ** 2 +
            (y - self.__y) ** 2
        )

        return distance_squared <= self.__radius ** 2

    def paint(self, canvas):
        for i in range(72):
            angle = 2 * math.pi * i / 72

            x = int(
                self.__x +
                self.__radius * math.cos(angle)
            )

            y = int(
                self.__y +
                self.__radius * math.sin(angle)
            )

            if 0 <= x < canvas.height and 0 <= y < canvas.width:
                canvas.set_pixel(x, y, char='*')

    def __repr__(self):
        return (
            "Circle(" +
            repr(self.__radius) + "," +
            repr(self.__x) + "," +
            repr(self.__y) +
            ")"
        )


class Triangle(Shape):

    def __init__(self, p1, p2, p3):
        self.__p1 = p1
        self.__p2 = p2
        self.__p3 = p3

    def distance(self, p1, p2):
        return math.sqrt(
            (p2[0] - p1[0]) ** 2 +
            (p2[1] - p1[1]) ** 2
        )

    def perimeter(self):
        side1 = self.distance(self.__p1, self.__p2)
        side2 = self.distance(self.__p2, self.__p3)
        side3 = self.distance(self.__p3, self.__p1)

        return side1 + side2 + side3

    def area(self):
        x1, y1 = self.__p1
        x2, y2 = self.__p2
        x3, y3 = self.__p3

        return abs(
            x1 * (y2 - y3)
            + x2 * (y3 - y1)
            + x3 * (y1 - y2)
        ) / 2

    def perimeter_points(self):
        return [
            self.__p1,
            self.__p2,
            self.__p3
        ]

    def contains(self, x, y):
        x1, y1 = self.__p1
        x2, y2 = self.__p2
        x3, y3 = self.__p3

        total_area = self.area()

        area1 = abs(
            x * (y2 - y3)
            + x2 * (y3 - y)
            + x3 * (y - y2)
        ) / 2

        area2 = abs(
            x1 * (y - y3)
            + x * (y3 - y1)
            + x3 * (y1 - y)
        ) / 2

        area3 = abs(
            x1 * (y2 - y)
            + x2 * (y - y1)
            + x * (y1 - y2)
        ) / 2

        return abs(
            total_area - (area1 + area2 + area3)
        ) < 0.0001

    def paint(self, canvas):
        self.draw_line(canvas, self.__p1, self.__p2)
        self.draw_line(canvas, self.__p2, self.__p3)
        self.draw_line(canvas, self.__p3, self.__p1)

    def draw_line(self, canvas, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        steps = max(
            abs(int(x2 - x1)),
            abs(int(y2 - y1))
        )

        if steps == 0:
            return

        for i in range(steps + 1):
            x = int(x1 + (x2 - x1) * i / steps)
            y = int(y1 + (y2 - y1) * i / steps)

            if 0 <= x < canvas.height and 0 <= y < canvas.width:
                canvas.set_pixel(x, y, char='*')


class CompoundShape(Shape):

    def __init__(self, shapes):
        self.__shapes = shapes

    def area(self):
        total = 0

        for shape in self.__shapes:
            total += shape.area()

        return total

    def perimeter_points(self):
        points = []

        for shape in self.__shapes:
            points.extend(shape.perimeter_points())

        return points

    def contains(self, x, y):
        for shape in self.__shapes:
            if shape.contains(x, y):
                return True

        return False

    def paint(self, canvas):
        for shape in self.__shapes:
            shape.paint(canvas)
