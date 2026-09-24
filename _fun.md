# Python 中以下划线开头的函数

> 内容整理自 Python 学习笔记中的 DeepSeek 分享页。重复回答和网页占位符已清理。

Python 中以单个下划线 `_` 开头的函数，通常表示“内部使用”。这是一种命名约定，不是语法层面的访问控制。外部代码仍然可以调用它，但调用者应理解这不是稳定的公共接口。

## 什么时候使用单下划线

### 模块内部辅助函数

```python
def _internal_helper():
    """仅在模块内部使用的函数"""
    return "raw data"


def public_api():
    data = _internal_helper()
    return data.upper()
```

### 辅助或工具函数

```python
def _format_data(data):
    return data.strip().lower()
```

### 内部测试函数

```python
def _test_specific_feature():
    pass
```

### 避免名称冲突

更常见的是使用尾部下划线，例如 `class_`、`type_`：

```python
def class_(name):
    return name


def type_(value):
    return value
```

## 公共函数不需要下划线

如果函数是模块对外提供的接口，或是希望用户直接调用的方法，就使用普通名称：

```python
def calculate_total(price, tax):
    return price * (1 + tax)


def get_user_info(user_id):
    pass
```

## 导入行为

使用 `from module import *` 时，以下划线开头的名称通常不会被导入：

```python
# mymodule.py
def public_api():
    return "public"


def _fetch_data():
    return "internal"
```

```python
from mymodule import *

public_api()
# _fetch_data()  # 通常不会被星号导入
```

但显式导入仍然可以访问：

```python
import mymodule

mymodule.public_api()
mymodule._fetch_data()  # 可以，但不推荐作为外部依赖
```

如果模块定义了 `__all__`，则星号导入的范围由 `__all__` 决定。

## 类中的单下划线方法

```python
class MyClass:
    def __init__(self):
        self.public_variable = 10
        self._private_variable = 20

    def public_method(self):
        return "public"

    def _private_method(self):
        return "internal"
```

`_private_method()` 通常只在类内部或子类中使用，但 Python 不会阻止外部调用：

```python
instance = MyClass()
instance.public_method()
instance._private_method()  # 可以调用，但不符合约定
```

## 单下划线、双下划线与尾部下划线

### 单下划线开头：`_function`

表示内部使用的约定，不会强制阻止访问。

### 双下划线开头：`__function`

在类中会触发名称改写（name mangling）：

```python
class MyClass:
    def __private(self):
        return "private"


instance = MyClass()
# instance.__private()  # AttributeError
instance._MyClass__private()  # 可以访问，但不推荐
```

它的主要作用是减少子类覆盖同名方法的风险，而不是提供绝对安全的私有机制。

### 单下划线结尾：`function_`

通常用于避免与关键字或内置名称冲突：

```python
def class_(name):
    pass


def type_(value):
    pass
```

## 主要区别

| 维度 | `_function` | `function` |
| :--- | :--- | :--- |
| 语义 | 暗示内部实现 | 公共接口 |
| 访问限制 | 没有真正限制 | 正常公开访问 |
| `from module import *` | 默认不导入 | 默认导入 |
| 文档定位 | 通常不是公共 API | 可以作为公共 API |
| 适用场景 | 辅助逻辑、实现细节 | 用户直接调用的功能 |

## 模块示例

```python
# mymodule.py
def public_api():
    data = _fetch_data()
    return _process(data)


def _fetch_data():
    return "raw data"


def _process(data):
    return data.upper()
```

使用者应该调用 `public_api()`，而不是依赖 `_fetch_data()` 或 `_process()`。这样模块作者以后可以修改内部实现，而不必保证内部函数的兼容性。

## 最佳实践

1. 模块内部使用的辅助函数使用单下划线前缀。
2. 对外稳定提供的函数使用普通名称。
3. 类中用 `_method()` 表示受保护的约定，用 `__method()` 避免名称冲突，用 `method()` 表示公共方法。
4. 不要把单下划线误解为真正的权限控制。
5. 遵循 PEP 8 的命名约定，并在文档中清楚说明公共 API。

核心原则是：单下划线是在告诉其他开发者“这是实现细节，除非你明确知道自己在做什么，否则不要直接依赖”。
