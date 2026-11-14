<!-- source: https://fastapi.tiangolo.com/zh/tutorial/cookie-param-models/ -->
# Cookie 参数模型 ¶
Use the official FastAPI skill for your installed version. Install it from your project directory:
```
uvx library-skills
```
See Develop with AI .
本翻译由人类引导的 AI 生成。🤝
可能存在误解原意或不够自然等问题。🤖
你可以通过 帮助我们更好地引导 AI LLM 来改进此翻译。
英文版本
如果你有一组相关的 cookie ，你可以创建一个 Pydantic 模型 来声明它们。🍪
这将允许你在 多个地方 能够 重用模型 ，并且可以一次性声明所有参数的验证方式和元数据。😎
注意
自 FastAPI 版本 0.115.0 起支持此功能。🤓
提示
此技术同样适用于 Query 、 Cookie 和 Header 。😎

## 带有 Pydantic 模型的 Cookie ¶
在 Pydantic 模型中声明所需的 cookie 参数，然后将参数声明为 Cookie ：
```
from typing import Annotated from fastapi import Cookie , FastAPI from pydantic import BaseModel app = FastAPI () class Cookies ( BaseModel ): session_id : str fatebook_tracker : str | None = None googall_tracker : str | None = None @app . get ( "/items/" ) async def read_items ( cookies : Annotated [ Cookies , Cookie ()]): return cookies
```
Tip
Prefer to use the Annotated version if possible.
```
from fastapi import Cookie , FastAPI from pydantic import BaseModel app = FastAPI () class Cookies ( BaseModel ): session_id : str fatebook_tracker : str | None = None googall_tracker : str | None = None @app . get ( "/items/" ) async def read_items ( cookies : Cookies = Cookie ()): return cookies
```
FastAPI 将从请求中接收到的 cookie 中 提取 出 每个字段 的数据，并提供你定义的 Pydantic 模型。

## 查看文档 ¶
你可以在文档 UI 的 /docs 中查看定义的 cookie：
注意
请记住，由于 浏览器 以特殊方式 处理 cookie ，并在后台进行操作，因此它们 不会 轻易允许 JavaScript 访问这些 cookie。
如果你访问 /docs 的 API 文档 UI ，你将能够查看你 路径操作 的 cookie 文档 。
但是即使你 填写数据 并点击“执行”，由于文档界面使用 JavaScript ，cookie 将不会被发送。而你会看到一条 错误 消息，就好像你没有输入任何值一样。

## 禁止额外的 Cookie ¶
在某些特殊使用情况下（可能并不常见），你可能希望 限制 你想要接收的 cookie。
你的 API 现在可以控制自己的 cookie 同意 。🤪🍪
你可以使用 Pydantic 的模型配置来禁止（ forbid ）任何额外（ extra ）字段：
```
from typing import Annotated from fastapi import Cookie , FastAPI from pydantic import BaseModel app = FastAPI () class Cookies ( BaseModel ): model_config = { "extra" : "forbid" } session_id : str fatebook_tracker : str | None = None googall_tracker : str | None = None @app . get ( "/items/" ) async def read_items ( cookies : Annotated [ Cookies , Cookie ()]): return cookies
```
Tip
Prefer to use the Annotated version if possible.
```
from fastapi import Cookie , FastAPI from pydantic import BaseModel app = FastAPI () class Cookies ( BaseModel ): model_config = { "extra" : "forbid" } session_id : str fatebook_tracker : str | None = None googall_tracker : str | None = None @app . get ( "/items/" ) async def read_items ( cookies : Cookies = Cookie ()): return cookies
```
如果客户端尝试发送一些 额外的 cookie ，他们将收到 错误 响应。
可怜的 cookie 通知条，费尽心思为了获得你的同意，却被 API 拒绝了 。🍪
例如，如果客户端尝试发送一个值为 good-list-please 的 santa_tracker cookie，客户端将收到一个 错误 响应，告知他们 santa_tracker cookie 是不允许的 ：
```
{ "detail" : [ { "type" : "extra_forbidden" , "loc" : [ "cookie" , "santa_tracker" ], "msg" : "Extra inputs are not permitted" , "input" : "good-list-please" , } ] }
```

## 组合参数模型 ¶
你可以将多个 cookie 参数模型与单独的 cookie 参数及依赖项组合使用。每个模型都会独立提取和验证，具体说明请参阅 查询参数模型 。
每个模型的 extra 配置适用于所有 cookie 参数，包括在其他模型或依赖项中声明的参数。使用 extra="forbid" 时，该模型之外的任何 cookie 都会被拒绝。使用 extra="allow" 时，这些 cookie 会作为模型的额外字段包含在内。

## 可选 Cookie 参数模型 ¶
使用 | None 并将默认值设为 None 来声明 cookie 参数模型，即可将这组参数设为可选。
```
from typing import Annotated from fastapi import Cookie , FastAPI from pydantic import BaseModel app = FastAPI () class Preferences ( BaseModel ): theme : str locale : str @app . get ( "/items/" ) async def read_items ( preferences : Annotated [ Preferences | None , Cookie ()] = None ): return preferences
```
Tip
Prefer to use the Annotated version if possible.
```
from fastapi import Cookie , FastAPI from pydantic import BaseModel app = FastAPI () class Preferences ( BaseModel ): theme : str locale : str @app . get ( "/items/" ) async def read_items ( preferences : Preferences | None = Cookie ( default = None )): return preferences
```
如果既未发送 theme 也未发送 locale ，则 preferences 为 None 。如果发送了其中任意一个，FastAPI 就会验证模型，并要求两个字段都存在。
默认值、额外字段和 OpenAPI 的规则与 可选查询参数模型 相同。

## 总结 ¶
你可以使用 Pydantic 模型 在 FastAPI 中声明 cookie 。😎
