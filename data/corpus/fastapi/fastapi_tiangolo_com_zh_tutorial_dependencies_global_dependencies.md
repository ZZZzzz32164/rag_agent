<!-- source: https://fastapi.tiangolo.com/zh/tutorial/dependencies/global-dependencies/ -->
# 全局依赖项 ¶
Use the official FastAPI skill for your installed version. Install it from your project directory:
```
uvx library-skills
```
See Develop with AI .
本翻译由人类引导的 AI 生成。🤝
可能存在误解原意或不够自然等问题。🤖
你可以通过 帮助我们更好地引导 AI LLM 来改进此翻译。
英文版本
有时，我们要为整个应用添加依赖项。
通过与 将 dependencies 添加到 路径操作装饰器 类似的方式，可以把依赖项添加至整个 FastAPI 应用。
这样一来，就可以为所有 路径操作 应用该依赖项：
Tip
Prefer to use the Annotated version if possible.
将 dependencies 添加到 路径操作装饰器 一章的思路均适用于全局依赖项， 在本例中，这些依赖项可以用于应用中的所有 路径操作 。

## 为一组路径操作定义依赖项 ¶
稍后， 大型应用 - 多文件 一章中会介绍如何使用多个文件创建大型应用程序，在这一章中，你将了解到如何为一组 路径操作 声明单个 dependencies 参数。
