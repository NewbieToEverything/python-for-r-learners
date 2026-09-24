# Python 中的 `__init__`、类与实例

> 内容整理自笔记中的第一个 DeepSeek 分享链接。网页中的重复回答、图片占位符、复制/下载按钮和页面提示已去除。

## `__init__` 是什么

在 Python 中，`__init__` 是类中的特殊方法，也称为初始化方法。它会在创建类的新实例后自动调用，用来设置对象的初始属性，或执行其他必要的初始化操作。

严格来说，`__init__` 不是负责创建实例的方法；真正负责创建实例的是 `__new__`。`__init__` 负责初始化已经创建好的实例。

## 基本语法

```python
class MyClass:
    def __init__(self, 参数1, 参数2, ...):
        # 初始化代码
        self.属性1 = 参数1
        self.属性2 = 参数2
```

## 关键特点

1. **自动调用**：创建类的实例时，Python 会自动执行 `__init__`。
2. **`self` 参数**：第一个参数通常必须是 `self`，它代表实例本身。
3. **初始化属性**：可以通过 `self.属性 = 值` 设置对象的初始状态。
4. **不能返回其他值**：`__init__` 应该返回 `None`，不能返回其他对象。
5. **不是必须定义**：如果不需要初始化逻辑，可以省略 `__init__`，Python 会提供默认行为。

## 基本示例

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.greeting = f"大家好，我是{name}"

    def introduce(self):
        print(f"我叫{self.name}，今年{self.age}岁")


person1 = Person("Alice", 25)
print(person1.name)  # Alice
print(person1.age)   # 25
person1.introduce()  # 我叫Alice，今年25岁
```

创建 `Person` 实例时，`__init__` 会被自动调用，并把传入的参数用于初始化 `name`、`age` 和 `greeting`。

如果没有定义 `__init__`，对象仍然可以被创建：

```python
class SimpleClass:
    pass


obj = SimpleClass()
```

## 默认参数

`__init__` 可以接受带默认值的参数：

```python
class Person:
    def __init__(self, name, age=18):
        self.name = name
        self.age = age


person1 = Person("Bob")          # age 使用默认值 18
person2 = Person("Charlie", 30)  # age 被指定为 30
```

## 实际应用示例

### 银行账户

```python
class BankAccount:
    def __init__(self, account_number, owner, balance=0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"存入: {amount}")


account = BankAccount("123456", "李四", 1000)
account.deposit(500)
```

### 学生

```python
class Student:
    def __init__(self, name, student_id, major="未定"):
        self.name = name
        self.student_id = student_id
        self.major = major
        self.courses = []
        self.gpa = 0.0

    def enroll(self, course):
        self.courses.append(course)
        print(f"{self.name} 已选课: {course}")


student = Student("王五", "2023001", "计算机科学")
student.enroll("Python 编程")
```

## `__init__` 与 `__new__` 的区别

```python
class MyClass:
    def __new__(cls, *args, **kwargs):
        # 创建实例
        instance = super().__new__(cls)
        return instance

    def __init__(self, value):
        # 初始化已经创建的实例
        self.value = value
        print(f"初始化完成，value={self.value}")
```

- `__new__` 负责创建并返回实例对象。
- `__init__` 接收已经创建的实例，并设置它的初始状态。
- 日常开发中通常只需要定义 `__init__`。

## 使用类创建实例的好处

使用类和 `__init__` 创建实例，是面向对象编程的基础。它可以把相关的数据和操作组织在一起，并让多个对象共享相同的结构。

### 1. 代码组织与结构清晰

每个类可以代表一种实体，并集中定义它的属性和方法。

```python
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.orders = []

    def place_order(self, order):
        self.orders.append(order)
        print(f"{self.name} 下了一个订单：{order.order_id}")


class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price


class Order:
    def __init__(self, order_id, user, products):
        self.order_id = order_id
        self.user = user
        self.products = products
        self.total = sum(product.price for product in products)


user1 = User(1, "张三", "zhangsan@example.com")
product1 = Product(101, "手机", 2999)
product2 = Product(102, "耳机", 199)
order1 = Order(1001, user1, [product1, product2])
user1.place_order(order1)
```

相比把所有变量和函数散落在脚本中，这种结构更容易理解和维护。

### 2. 数据与行为封装

类可以把数据和操作数据的方法绑定起来，并限制外部对内部状态的直接修改。

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"存款成功，余额: {self.__balance}")
        else:
            print("存款金额必须大于 0")

    def get_balance(self):
        return self.__balance


account = BankAccount("张三", 1000)
account.deposit(500)
# account.__balance  # 不应直接访问私有属性
```

这样可以保护数据完整性，减少非法操作。

### 3. 代码复用

通过继承，子类可以复用父类的属性和方法。

```python
class Vehicle:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    def start(self):
        print(f"{self.brand} 启动")


class Car(Vehicle):
    def __init__(self, brand, color, doors):
        super().__init__(brand, color)
        self.doors = doors

    def honk(self):
        print(f"{self.brand} 鸣笛")


car = Car("Toyota", "红色", 4)
car.start()
car.honk()
```

### 4. 创建多个相似对象

类可以用来批量创建结构相同、数据不同的对象。

```python
class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def display_info(self):
        print(f"产品: {self.name}, 价格: ¥{self.price}")


products = [
    Product("iPhone", 6999, "手机"),
    Product("MacBook", 12999, "电脑"),
    Product("iPad", 3299, "平板"),
]

for product in products:
    product.display_info()
```

### 5. 状态保持与维护

每个实例都可以保存自己独立的状态，并在调用方法后继续保留更新后的状态。

```python
class GameCharacter:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.inventory = []
        self.position = (0, 0)

    def move(self, x, y):
        self.position = (x, y)
        print(f"{self.name} 移动到 {self.position}")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"获得物品: {item}")


hero = GameCharacter("勇者")
hero.move(10, 5)
hero.add_item("宝剑")
hero.add_item("药水")
print(f"当前位置: {hero.position}")
print(f"背包: {hero.inventory}")
```

### 6. 灵活性与可扩展性

通过继承和多态，可以在不修改调用代码的情况下替换具体实现。

```python
class PaymentMethod:
    def __init__(self, method_name):
        self.method_name = method_name

    def process_payment(self, amount):
        pass


class CreditCard(PaymentMethod):
    def __init__(self, card_number, expiry_date):
        super().__init__("信用卡")
        self.card_number = card_number
        self.expiry_date = expiry_date

    def process_payment(self, amount):
        print(f"使用信用卡支付 ¥{amount}")


class PayPal(PaymentMethod):
    def __init__(self, email):
        super().__init__("PayPal")
        self.email = email

    def process_payment(self, amount):
        print(f"使用 PayPal 支付 ¥{amount}")


def checkout(payment_method, amount):
    payment_method.process_payment(amount)


credit_card = CreditCard("1234-5678", "12/25")
paypal = PayPal("user@example.com")
checkout(credit_card, 100)
checkout(paypal, 200)
```

### 7. 现实世界建模

类可以直观地表示现实世界中的实体及其关系。

```python
class LibrarySystem:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)
        return book

    def register_member(self, name):
        member = Member(name)
        self.members.append(member)
        return member


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False


class Member:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []


library = LibrarySystem()
book1 = library.add_book("Python 编程", "张三")
member1 = library.register_member("李四")
```

### 8. 团队协作与维护

类可以拆分到不同模块中，由不同成员负责不同的功能。

```python
# person.py
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


# employee.py
class Employee(Person):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)
        self.employee_id = employee_id


# department.py
class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []


# main.py
from person import Person
from employee import Employee
from department import Department
```

### 9. 数据验证与错误处理

初始化时可以验证输入数据，并在数据无效时抛出异常。

```python
class Email:
    def __init__(self, address):
        if self._is_valid_email(address):
            self.address = address
        else:
            raise ValueError("无效的邮箱地址")

    def _is_valid_email(self, address):
        import re

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, address) is not None


try:
    email1 = Email("user@example.com")
    email2 = Email("invalid-email")
except ValueError as error:
    print(f"错误: {error}")
```

### 10. 便于测试

类的行为可以被单独测试。

```python
class Calculator:
    def __init__(self, precision=2):
        self.precision = precision

    def add(self, a, b):
        return round(a + b, self.precision)

    def multiply(self, a, b):
        return round(a * b, self.precision)


calc = Calculator()
assert calc.add(0.1, 0.2) == 0.3
assert calc.multiply(2, 3) == 6
```

## 面向对象与面向过程的对比

### 面向过程

```python
student_name = "张三"
student_age = 20
student_courses = ["数学", "物理"]
student_grades = {"数学": 90, "物理": 85}
```

### 面向对象

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.courses = []
        self.grades = {}


student = Student("张三", 20)
```

面向对象的写法把相关的数据和行为组织到对象中，更适合需要维护状态、创建多个相似对象或封装复杂逻辑的场景。

## 总结对比表

| 维度 | 面向对象 | 面向过程 |
| :--- | :--- | :--- |
| 数据封装 | 数据和操作绑定 | 数据与方法分离 |
| 代码复用 | 继承、组合 | 需要复制或导入 |
| 状态管理 | 实例保持状态 | 需要全局变量或参数传递 |
| 可维护性 | 模块化，易修改 | 逻辑可能分散各处 |
| 团队协作 | 接口明确，分工清晰 | 更容易产生冲突 |
| 扩展性 | 继承、多态 | 可能需要大量修改 |

## 何时使用类

1. 需要表示现实世界实体。
2. 需要维护对象状态。
3. 需要创建多个相似对象。
4. 需要封装复杂逻辑。
5. 正在开发需要良好架构的大型项目。

## 何时使用简单函数

1. 简单脚本。
2. 一次性任务。
3. 纯数学计算。
4. 数据处理管道。

总体来说，类和实例是面向对象编程的核心工具，特别适合中大型项目、复杂系统和团队协作。
