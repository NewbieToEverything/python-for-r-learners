# Python 的 f-string 与字符串格式化

> 内容整理自 Python 学习笔记中的 DeepSeek 分享页。重复回答和网页占位符已清理。

字符串前面的 `f` 表示格式化字符串字面值（f-string）。它允许在字符串中直接嵌入表达式，表达式会在运行时求值。

```python
name = "Alice"
age = 25
message = f"Hello, {name}. You are {age} years old."
```

传统写法包括 `%` 格式化和 `str.format()`，但现代 Python 通常推荐 f-string：

```python
message1 = "Hello, %s. You are %d years old." % (name, age)
message2 = "Hello, {}. You are {} years old.".format(name, age)
message3 = f"Hello, {name}. You are {age} years old."
```

## 文件名示例

```python
import os

out_dir = "/output"
file_idx = 7
out_path = os.path.join(out_dir, f"health_info_{file_idx:04d}.jsonl")
```

`file_idx:04d` 表示按十进制整数格式化，最小宽度为 4，不足时用 `0` 填充。因此 `7` 会变成 `0007`。

```python
f"{1:04d}"      # "0001"
f"{12:04d}"     # "0012"
f"{123:04d}"    # "0123"
f"{1234:04d}"   # "1234"
```

## 常见格式说明符

```python
price = 19.99999
percentage = 0.854321
distance = 1234567.89

print(f"价格: ¥{price:.2f}")
print(f"完成度: {percentage:.1%}")
print(f"距离: {distance:,.2f} 米")
```

- `.2f`：保留两位小数。
- `.1%`：按百分比显示并保留一位小数。
- `,`：使用千位分隔符。
- `04d`：宽度为 4，不足补零。

## 对齐和表达式

```python
name = "张三"
print(f"|{name:<10}|")  # 左对齐
print(f"|{name:>10}|")  # 右对齐
print(f"|{name:^10}|")  # 居中

a, b = 5, 3
print(f"{a} + {b} = {a + b}")

items = ["苹果", "香蕉", "橙子"]
print(f"水果列表: {', '.join(items)}")

person = {"name": "李四", "age": 30}
print(f"姓名: {person['name']}, 年龄: {person['age']}")
```

花括号内可以放表达式：

```python
x = 10
print(f"{x + 5}")
```

如果要输出花括号本身，需要使用双花括号：

```python
print(f"{{这是花括号}}")
```

## 为什么要格式化字符串

字符串格式化可以：

1. 动态插入变量和表达式。
2. 控制数字、日期、百分比和货币的显示形式。
3. 控制文本宽度、对齐和填充。
4. 生成规律、易排序的文件名。
5. 避免大量字符串拼接，提高可读性和可维护性。
6. 适应日志、报告、配置文件和 API 响应等场景。

## 对比字符串拼接

```python
user_name = "张三"
date = "2024-01-15"
amount = 99.5

message = f"用户{user_name}在{date}消费了{amount:.2f}元"
```

相比下面的写法，f-string 的文本结构更直观：

```python
message = "用户" + user_name + "在" + date + "消费了" + str(amount) + "元"
```

## 表格输出

```python
data = [
    ("张三", 95, 1200.5),
    ("李四", 88, 950.0),
    ("王五", 92, 1100.75),
]

print(f"{'姓名':<6} {'分数':>4} {'薪资':>10}")
print("-" * 25)
for name, score, salary in data:
    print(f"{name:<6} {score:>4}分 ¥{salary:>8.2f}")
```

## 文件和日期格式化

```python
from datetime import datetime

for index in range(1, 4):
    filename = f"data_{index:04d}.csv"
    print(filename)

now = datetime.now()
log_file = f"app_{now:%Y%m%d_%H%M%S}.log"
```

## 实际应用

日志：

```python
user_id = "U1001"
action = "login"
timestamp = datetime.now()
log_message = f"[{timestamp:%Y-%m-%d %H:%M:%S}] 用户 {user_id} 执行了 {action} 操作"
```

配置生成：

```python
config_template = """
APP_NAME = "{app_name}"
DEBUG = {debug}
PORT = {port}
"""

config_content = config_template.format(
    app_name="MyApp",
    debug=True,
    port=8080,
)
```

## 总结

f-string 的核心形式是 `f"文本{表达式}"`。在 `f"health_info_{file_idx:04d}.jsonl"` 中，`f` 开启格式化，`file_idx` 提供变量值，`:04d` 控制编号格式。它简洁、清晰，适合动态文本、文件名、日志和报告。
