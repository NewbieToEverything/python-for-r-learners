# DeepSeek API 笔记

> 内容整理自 Python 学习笔记中的 DeepSeek 分享页。页面中的重复问答和图片占位符已合并清理。

DeepSeek API 提供兼容 OpenAI 风格的 Chat Completions 接口。典型调用方式如下：

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-deepseek-api-key",
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个专业的 Python 助手。"},
        {"role": "user", "content": "如何用 Python 读取文件？"},
    ],
    temperature=0.7,
    max_tokens=200,
)

print(response.choices[0].message.content)
```

## `messages` 中的角色

每个消息通常包含 `role` 和 `content`：

| 角色 | 作用 |
| :--- | :--- |
| `system` | 设置助手的角色、行为规则和回答风格，通常放在开头 |
| `user` | 用户的问题或指令 |
| `assistant` | 助手此前的回复，用于维护多轮上下文 |

单轮对话：

```python
messages = [
    {"role": "system", "content": "你是一个乐于助人的助手。"},
    {"role": "user", "content": "解释列表和元组的区别。"},
]
```

多轮对话需要把历史消息继续放在 `messages` 中：

```python
messages = [
    {"role": "system", "content": "你是一个数学老师。"},
    {"role": "user", "content": "什么是勾股定理？"},
    {"role": "assistant", "content": "勾股定理描述直角三角形三边的关系。"},
    {"role": "user", "content": "能举个实际例子吗？"},
]
```

每次 API 调用都需要携带希望模型理解的历史消息，并注意上下文长度限制。

## `temperature` 和 `top_p`

- `temperature=0`：输出更确定，适合代码和事实性回答。
- `temperature` 较高：输出更有随机性，适合创意写作。
- `top_p`：核采样参数，限制候选 token 的累计概率范围。

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "写一个故事开头。"}],
    temperature=0.8,
    top_p=0.9,
    max_tokens=300,
)
```

## `do_sample` 是否存在

分享页中的结论是：DeepSeek 官方的 OpenAI 兼容 API 不应依赖 Hugging Face 风格的 `do_sample` 参数。官方接口通常使用 `temperature` 和 `top_p` 控制随机性。

`do_sample` 在 Transformers 或本地模型推理中常见：

- `do_sample=False` 通常对应贪心解码。
- `do_sample=True` 通常表示从概率分布中采样。

但调用 DeepSeek 官方 API 时，建议使用兼容接口支持的参数：

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "生成一段 Python 代码。"}],
    temperature=0,
    max_tokens=100,
)
```

如果传入不支持的 `do_sample`，可能会收到参数错误。始终以最新官方文档为准。

## `num_return_sequences` 和 `n`

`num_return_sequences` 常见于 Hugging Face Transformers，而不是 OpenAI 风格的 Chat Completions。兼容接口中可能使用 `n` 请求多个候选回复，但是否支持应以 DeepSeek 当前 API 文档为准。

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "写一句问候语。"}],
    n=3,
    max_tokens=50,
)

for index, choice in enumerate(response.choices, start=1):
    print(f"回复 {index}: {choice.message.content}")
```

如果接口不支持 `n` 或需要更明确地控制多个变体，可以多次调用：

```python
import asyncio


async def generate_multiple(prompt, count=3):
    tasks = []
    for _ in range(count):
        tasks.append(
            client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=100,
            )
        )
    results = await asyncio.gather(*tasks)
    return [result.choices[0].message.content for result in results]
```

## 流式输出

流式输出会逐块返回内容：

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "写一个长篇故事的开头。"}],
    stream=True,
    max_tokens=300,
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## 多轮对话封装

```python
class ChatAssistant:
    def __init__(self, system_prompt=None):
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def get_response(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            temperature=0.7,
            max_tokens=500,
        )
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})

        # 保留系统提示和最近若干条消息
        if len(self.messages) > 20:
            self.messages = [self.messages[0]] + self.messages[-18:]
        return reply
```

## 实践建议

- 代码生成、数学问题：使用较低的 `temperature`。
- 创意写作：使用 `temperature=0.7` 到 `0.9`。
- 需要可重复结果：使用 `temperature=0`，并确认接口是否支持 `seed`。
- 多轮对话：管理历史消息，避免超过上下文长度。
- 参数是否支持：以 DeepSeek 最新官方 API 文档为准，不要直接套用 Transformers 参数。
