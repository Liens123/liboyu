# 🐾 桌面宠物 & 番茄钟

一个可爱的桌面宠物应用和番茄钟工具集合。

## 📦 项目内容

### 🐱 桌面宠物 (desktop-pet)

一个基于 Python 的桌面宠物应用，可以在桌面上显示可爱的宠物角色。

**功能特点：**
- 可爱的宠物角色显示
- 桌面互动功能
- 支持自定义配置
- 可打包为独立 exe 文件

**使用方法：**
```bash
cd desktop-pet
python main.py
```

**打包为 exe：**
```bash
cd desktop-pet
build.bat
```

### ⏱️ 番茄钟 (pomodoro.html)

一个简洁美观的番茄钟网页应用。

**功能特点：**
- 25 分钟番茄工作计时
- 5 分钟短休息
- 15 分钟长休息
- 简洁美观的界面

**使用方法：**
直接在浏览器中打开 `pomodoro.html` 文件即可。

## 🛠️ 技术栈

- **桌面宠物：** Python, Tkinter
- **番茄钟：** HTML, CSS, JavaScript

## 📁 项目结构

```
├── desktop-pet/          # 桌面宠物项目
│   ├── main.py           # 主程序入口
│   ├── pet.py            # 宠物核心逻辑
│   ├── renderer.py       # 渲染器
│   ├── ui.py             # 用户界面
│   ├── config.py         # 配置管理
│   ├── persistence.py    # 数据持久化
│   ├── build.bat         # 打包脚本
│   └── DesktopPet.spec   # PyInstaller 配置
└── pomodoro.html         # 番茄钟网页应用
```

## 📝 更新日志

- 2026-05-18：初始版本上传

## 👤 作者

**Liens123**
- GitHub: [@Liens123](https://github.com/Liens123)

## 📄 许可证

本项目仅供学习交流使用。
