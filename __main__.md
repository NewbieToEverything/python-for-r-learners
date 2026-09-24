# Python 中的 `__main__`

> 内容整理自 Python 学习笔记中的 DeepSeek 分享页。重复回答和网页占位符已清理。

当一个 Python 文件被直接执行时，解释器会把这个模块的 `__name__` 设置为字符串 `"__main__"`。当文件被其他模块导入时，`__name__` 则是模块名。

## 常见写法

```python
def main():
    print("主程序执行中...")


if __name__ == "__main__":
    main()
```

这表示：只有直接运行当前文件时才调用 `main()`；如果当前文件被导入，则不会执行入口代码。

## 直接运行和导入的区别

`my_module.py`：

```python
def my_function():
    print("这是一个函数")


def main():
    print("主程序执行中...")
    my_function()


if __name__ == "__main__":
    main()
```

直接运行：

```bash
python my_module.py
```

此时 `__name__ == "__main__"`，入口代码会执行。

另一个文件导入：

```python
import my_module

my_module.my_function()
```

此时 `my_module.__name__ == "my_module"`，入口代码不会执行，但函数可以被调用。

## 为什么需要这个模式

它让一个文件同时具备两种用途：

- 作为脚本直接运行。
- 作为模块被其他代码导入。

导入时不会意外执行测试代码、命令行逻辑或其他只应该在脚本启动时执行的代码。

## 示例：模块既可运行又可导入

```python
# calculator.py
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


if __name__ == "__main__":
    print("测试加法:", add(5, 3))
    print("测试减法:", subtract(5, 3))
```

## `__main__.py` 与 `-m`

包中可以放置 `__main__.py`，这样包可以直接作为脚本运行：

```text
app/
├── __main__.py
└── app.py
```

```python
# app/__main__.py
import app


if __name__ == "__main__":
    app.run()
```

运行：

```bash
python -m app
```

`-m` 表示按模块运行，而不是把路径当成普通脚本文件运行。

## 获取主模块

```python
import sys
import __main__

print(__main__.__file__)
print(sys.modules["__main__"])
```

## 最佳实践

1. 把可执行代码放进 `if __name__ == "__main__":` 中。
2. 定义 `main()` 函数，使入口逻辑清晰。
3. 将可复用的函数和类放在入口代码之外。
4. 命令行参数可以在 `main()` 中通过 `argparse` 解析。

```python
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="World")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()
```

## 总结

`__main__` 机制使 Python 模块能够根据运行方式表现出不同的行为：直接运行时执行程序入口，被导入时只提供可复用的定义。这是 Python 模块化编程的重要基础。
