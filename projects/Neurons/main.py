import random
import time
from enum import Enum
from shutil import get_terminal_size


TICKS_PER_SECOND = 60


class Direction(Enum):
    """Mapping of direction to int."""#Enum 是 Python 的枚举类。它的作用是：把一组具有固定含义的值组织起来。

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Empty(str):
    """String subclass to return character representing empty space."""

    CHAR = "  "

    def __new__(cls) -> str:
        return str.__new__(cls, cls.CHAR)


class Neuron(str):
    """String subclass to return character representing a neuron."""

    CHAR = "██"
    CHANCE_OF_DEATH = 35

    def __new__(cls) -> str:
        return str.__new__(cls, cls.CHAR)


class Grid:
    """Class to store grid."""

    def __init__(self, width, height) -> None:
        """Initialise the grid with empty cells."""#创建一个 width长height高的数组
        self._grid = [[Empty() for _ in range(width)] for _ in range(height)]#_ 是一个普通变量名，只不过 Python 程序员习惯用它表示：这个循环变量我不需要使用，只需要循环指定次数即可
        #self指向这个类对应对象，是个形参，相当于是初始化了这个类的对象有_grid这个属性
    
    def __str__(self) -> str:#__str__(self)用来规定一个对象转换成字符串时应该呈现什么内容
        """Return the string representation of the grid."""
        return "\n".join(["".join(row) for row in self._grid])#遍历列表时，变量每次拿到的是列表中的一个直接元素。

    @property
    def neurons(self) -> tuple[tuple[Neuron, tuple[int, int]]]:    #neurons 的作用是获取当前网格中的神经元信息，它更像一个数据属性，而不是一个需要用户主动执行的操作，加上@property后.neurons调用这个方法不用加括号
        """Return 2D tuple of Neurons."""
        return tuple(
            (element, (x, y))
            for y, row in enumerate(self._grid) #enumerate(self._grid)会同时返回每一行的索引和这一行的内容，每一行列表。
            for x, element in enumerate(row)    #这个地方相当于是返回每一行每个元素的索引，和对应元素
            if isinstance(element, Neuron)      #isinstance() 是 Python 内置函数，用于判断对象是否属于某个类
        )                                       #Python 的一种固定语法规则：列表推导式和生成器表达式中的 if 是筛选条件，前面的表达式是筛选通过后要生成的数据

    def set_neuron(self, x, y) -> None:
        """Set x, y to a Neuron."""
        self._grid[y][x] = Neuron()             #把原来占位的enpty()对象换成Neuron()

    def tick(self) -> None:
        """Randomly kill or move all Neurons."""
        for neuron_data in self.neurons:
            neuron = neuron_data[0]
            x, y = neuron_data[1]

            if random.randint(1, 100) <= Neuron.CHANCE_OF_DEATH:
                self._grid[y][x] = Empty()
                continue

            direction = random.choice(list(Direction))#list(Direction)把枚举类中的四个成员转换成列表,random.choice(...)从列表中随机选择一个元素
            if direction == Direction.UP:
                y -= 1
            elif direction == Direction.RIGHT:
                x += 1
            elif direction == Direction.DOWN:
                y += 1
            elif direction == Direction.LEFT:
                x -= 1
            try:
                self._grid[y][x] = Neuron()
            except IndexError:
                pass
"""Python 的二维列表采用 [行索引][列索引] 的方式访问：
     第一维 y：控制行，越往下索引越大。
     第二维 x：控制列，越往右索引越大"""

def main() -> None:
    """Run the program with two example Neurons."""
     # 将网格大小按终端比例设置
    width, height = get_terminal_size()
    grid = Grid(width // len(Neuron.CHAR), height)
    grid.set_neuron(15, 15)  # Example placement
    grid.set_neuron(35, 35)
    while grid.neurons:
        print(grid)  # 输出网格的字符串表示
        grid.tick()
        time.sleep(1 / TICKS_PER_SECOND)


if __name__ == "__main__":
    while True:
        main()
