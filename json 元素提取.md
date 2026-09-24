# Python 中的 JSON 长度与元素提取

> 内容整理自 Python 学习笔记中的 DeepSeek 分享页。重复内容和网页占位符已清理。

JSON 字符串解析后通常变成 Python 的 `dict` 或 `list`。因此，长度和元素提取要根据解析后的类型处理。

## 检测 JSON 长度

```python
import json

json_str = '{"name": "John", "age": 30, "city": "New York"}'
data = json.loads(json_str)

print(len(data))       # 字典的键值对数量
print(len(json_str))   # JSON 字符串的字符数
```

字典返回键值对数量，列表返回元素数量：

```python
json_array = '[{"id": 1}, {"id": 2}, {"id": 3}]'
data = json.loads(json_array)
print(len(data))
```

从文件读取：

```python
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
print(len(data))
```

对于嵌套 JSON，`len(data)` 通常只计算顶层长度。如果要递归统计元素，可以定义函数：

```python
def count_json_elements(value):
    if isinstance(value, dict):
        total = len(value)
        for child in value.values():
            total += count_json_elements(child)
        return total
    if isinstance(value, list):
        total = len(value)
        for child in value:
            total += count_json_elements(child)
        return total
    return 1
```

处理超大 JSON 时可以使用 `ijson` 流式解析，避免一次性载入全部内容：

```python
import ijson


def count_large_json_elements(file_path):
    count = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for _, event, _ in ijson.parse(file):
            if event in ("string", "number", "boolean", "null", "start_map", "start_array"):
                count += 1
    return count
```

## 直接按键和索引提取

```python
json_data = {
    "user": {
        "name": "张三",
        "age": 25,
        "address": {"city": "北京"},
        "hobbies": ["篮球", "读书", "编程"],
    },
    "status": "active",
}

print(json_data["user"]["name"])
print(json_data["user"]["address"]["city"])
print(json_data["user"]["hobbies"][0])
```

列表使用整数索引：

```python
json_array = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]

print(json_array[0]["name"])
print(json_array[-1]["name"])
print(json_array[1:])
```

不确定键是否存在时，可以使用 `get()`：

```python
name = json_data.get("user", {}).get("name")
missing = json_data.get("missing", "默认值")
```

## 按路径安全提取

```python
def safe_get(data, keys, default=None):
    current = data
    for key in keys:
        try:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int):
                current = current[key]
            else:
                return default
        except (KeyError, IndexError, TypeError):
            return default
    return current


print(safe_get(json_data, ["user", "address", "city"]))
print(safe_get(json_data, ["user", "hobbies", 0]))
print(safe_get(json_data, ["user", "missing"], "默认值"))
```

也可以使用点号路径：

```python
def extract_by_path(data, path, separator="."):
    current = data
    for key in path.split(separator):
        if key.isdigit():
            key = int(key)

        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
            current = current[key]
        else:
            return None
    return current


print(extract_by_path(json_data, "user.address.city"))
print(extract_by_path(json_data, "user.hobbies.0"))
```

## 通用路径函数

```python
def extract_element(data, path):
    current = data
    for step in path:
        if isinstance(step, str) and isinstance(current, dict):
            current = current.get(step)
        elif isinstance(step, int) and isinstance(current, list) and 0 <= step < len(current):
            current = current[step]
        else:
            return None

        if current is None:
            return None
    return current
```

例如：

```python
path = ["store", "book", 0, "author"]
author = extract_element(data, path)
```

## JSONPath

复杂查询可以使用 `jsonpath-ng`：

```bash
pip install jsonpath-ng
```

```python
from jsonpath_ng import parse

expression = parse("$.store.book[*].author")
matches = [match.value for match in expression.find(data)]
print(matches)
```

常用表达式：

| 表达式 | 含义 | 示例 |
| :--- | :--- | :--- |
| `$` | 根对象 | `$.store` |
| `.` 或 `[]` | 子元素 | `$.store.book` |
| `*` | 所有元素 | `$.store.book[*]` |
| `..` | 递归查找 | `$..author` |
| `[0]` | 下标 | `$.store.book[0]` |
| `[start:end]` | 切片 | `$.store.book[0:2]` |
| `[?()]` | 过滤 | `$.store.book[?(@.price < 10)]` |

## 从 API 响应中提取

```python
import requests
from jsonpath_ng import parse


def extract_from_api(url, expression_text):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        expression = parse(expression_text)
        return [match.value for match in expression.find(data)]
    except requests.RequestException as error:
        print(f"请求失败: {error}")
        return []
    except ValueError as error:
        print(f"JSON 解析失败: {error}")
        return []
```

## 总结

- 顶层字典或列表：使用 `len()`。
- 固定路径：使用键和索引直接访问。
- 不确定路径：使用 `get()`、`try-except` 或安全访问函数。
- 复杂查询：使用 `jsonpath-ng`。
- 批量字段提取：可转换为 DataFrame。
- 大型 JSON：使用流式解析，避免内存溢出。
