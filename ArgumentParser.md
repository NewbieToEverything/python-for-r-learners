# `ArgumentParser`：解析命令行参数

> 内容整理自 Python 学习笔记中的 DeepSeek 分享页。重复回答和网页界面占位符已合并清理。

`argparse` 是 Python 标准库中用于构建命令行接口的模块。`ArgumentParser` 负责定义程序接受哪些参数，`add_argument()` 负责添加参数规则，`parse_args()` 负责解析用户实际输入的参数。

## 基本用法

```python
import argparse

parser = argparse.ArgumentParser(description="这是一个示例程序")
parser.add_argument("--input", type=str, help="输入文件路径")
parser.add_argument("--output", type=str, help="输出文件路径")
parser.add_argument("--verbose", action="store_true", help="详细模式")

args = parser.parse_args()

if args.verbose:
    print("详细模式已开启")
if args.input:
    print(f"输入文件: {args.input}")
if args.output:
    print(f"输出文件: {args.output}")
```

运行方式：

```bash
python script.py --input input.txt --output output.txt --verbose
python script.py -h
```

## `add_argument()` 的常用参数

- `name or flags`：参数名称，例如 `"--input"`、`"-i"`，也可以同时提供短选项和长选项。
- `type`：转换类型，例如 `int`、`float`、`str`。
- `help`：帮助信息。
- `default`：未提供参数时使用的默认值。
- `action`：参数出现时执行的动作。
- `choices`：允许的取值。
- `required`：是否必须提供，默认是 `False`。
- `dest`：解析后保存到命名空间中的属性名。
- `nargs`：接受的值的数量。

### 位置参数和可选参数

```python
parser.add_argument("filename", help="输入文件名")
parser.add_argument("--output", "-o", default="result.txt", help="输出文件")
```

位置参数没有 `-` 或 `--`，通常是必需的；可选参数带有选项名，可以提供默认值。

### 类型、默认值和选择范围

```python
parser.add_argument("--count", type=int, help="整数参数")
parser.add_argument("--price", type=float, help="浮点数参数")
parser.add_argument("--mode", choices=["train", "test", "predict"], default="train")
parser.add_argument("--config", required=True, help="必需的配置文件")
```

### `action`

```python
parser.add_argument("--debug", action="store_true", help="开启调试模式")
parser.add_argument("--no-cache", action="store_false", help="禁用缓存")
parser.add_argument("-v", action="count", help="统计详细级别")
parser.add_argument("--add", action="append", help="允许多次添加")
```

`store_true` 在参数出现时得到 `True`，否则为 `False`；`append` 会把多次出现的值收集到列表中。

### 多值参数

```python
parser.add_argument("--point", nargs=2, type=float, help="x y 坐标")
parser.add_argument("files", nargs="*", help="零个或多个文件")
parser.add_argument("inputs", nargs="+", help="至少一个输入")
parser.add_argument("--opt", nargs="?", const="default_value", help="零个或一个值")
```

## 完整示例

```python
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="文件处理工具",
        epilog="示例: python script.py input.txt --output out.txt",
    )
    parser.add_argument("input", help="输入文件路径")
    parser.add_argument("-o", "--output", default="output.txt", help="输出文件路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")
    parser.add_argument("--size", type=int, choices=[1, 2, 4, 8], default=1)
    parser.add_argument("--coordinates", nargs=2, type=float, metavar=("X", "Y"))

    args = parser.parse_args()
    print(f"输入文件: {args.input}")
    print(f"输出文件: {args.output}")
    print(f"详细模式: {args.verbose}")
    print(f"处理大小: {args.size}")


if __name__ == "__main__":
    main()
```

## 自定义 `parse_args()` 函数

`ArgumentParser` 有一个实例方法 `parser.parse_args()`。同时，用户也可以定义一个名为 `parse_args()` 的普通函数，用来集中创建解析器、添加参数并调用实例方法。两者属于不同作用域，不会冲突。

```python
import argparse


def parse_args(args_list=None):
    parser = argparse.ArgumentParser(description="模型测试工具")
    parser.add_argument("--model", required=True)
    parser.add_argument("--data_file", required=True)

    if args_list is None:
        return parser.parse_args()
    return parser.parse_args(args_list)


def main():
    args = parse_args()
    print(args.model)


if __name__ == "__main__":
    main()
```

这种封装可以让主函数更清晰，也便于测试：

```python
def test_parse_args():
    args = parse_args(["--model", "test_model", "--data_file", "test.json"])
    assert args.model == "test_model"
    assert args.data_file == "test.json"
```

更明确的命名可以是 `get_args()`、`parse_arguments()` 或 `configure_and_parse_args()`。

## 不使用命令行参数

可以改用硬编码、配置文件、环境变量、函数参数、GUI、Web 界面或数据库。

### JSON 配置

```python
import json


def load_config():
    with open("config.json", "r", encoding="utf-8") as file:
        return json.load(file)


config = load_config()
input_file = config.get("input_file", "data.txt")
```

### 环境变量

```python
import os

input_file = os.getenv("INPUT_FILE", "input.txt")
verbose = os.getenv("VERBOSE", "false").lower() == "true"
size = int(os.getenv("SIZE", "1"))
```

### 函数调用

```python
def process_file(input_file, output_file, verbose=False, size=1):
    print(input_file, output_file, verbose, size)


process_file("input.txt", "output.txt", verbose=True, size=4)
```

选择建议：简单脚本可使用函数参数或硬编码；复杂配置使用 JSON/YAML；容器化部署常用 `.env`；桌面或 Web 应用可以使用 GUI 或 Web 表单。
