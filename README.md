# Waline 到 Twikoo 评论数据迁移工具 🔄

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/Horean0574/waline2twikoo)

> 🚀 **将 Waline 评论数据无缝迁移至 Twikoo 系统**  
> 保留博主标识、评论层级、时间戳等所有关键信息

## 📋 项目简介

本项目是一个轻量级的 Python 工具，用于将 Waline 评论系统导出的 JSON 数据转换为 Twikoo 评论系统可导入的格式。无需复杂的配置，一行命令即可完成迁移。

## ✨ 功能特点

| 特性 | 说明 |
|------|------|
| ✅ **博主标识保留** | 自动识别博主评论，在 Twikoo 中显示「博主」标签 |
| ✅ **评论层级完整** | PID/RID 关系完美保留，父子评论不乱序 |
| ✅ **自动创建目录** | 输出路径不存在时自动创建，无需手动建文件夹 |
| ✅ **Markdown 转 HTML** | 评论内容自动渲染，代码块、粗体等格式完美保留 |
| ✅ **垃圾评论标记** | 保留 Waline 的审核状态，spam 评论自动标记 |
| ✅ **置顶状态保留** | sticky > 0 的评论自动转为置顶评论 |
| ✅ **UUID 重映射** | 所有 ID 重新生成，避免冲突 |
| ✅ **时间戳精准** | ISO 8601 转 Unix 毫秒时间戳 |

## 🔧 环境要求

- **Python**: 3.8 或更高版本
- **依赖包**: 
  ```bash
  pip install click markdown

## 📦 安装与配置
### 1. 克隆仓库
```bash
git clone https://github.com/Horean0574/waline2twikoo.git
cd waline2twikoo
```

### 2. 创建虚拟环境（推荐）
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

## 🚀 快速上手
### 基础使用（交互式）
```bash
python main.py
```

#### 运行示例：
```text
Program started.

你的站点域名: blog.demo.site
你（博主）有在新的Twikoo评论系统上评论过吗？(y/N): 
原 Waline 评论数据文件路径（相对路径，JSON文件）: ./test_input.json
新的 Twikoo 评论数据文件存储路径（相对路径，JSON文件）: ./output/twikoo.json

读取 Waline 评论数据中……  完成✅
映射建立中……  完成✅

1/9: 正在转换来自 [张三] 的评论……  完成✅
2/9: 正在转换来自 [李四] 的评论……  完成✅
...
写入文件中……  完成✅

Program ended.
```

## 📖 详细使用指南
### 场景一：博主从未评论过
```bash
你的站点域名: example.com
你（博主）有在新的Twikoo评论系统上评论过吗？(y/N): [直接回车]
原 Waline 评论数据文件路径: ./input/waline.json
新的 Twikoo 评论数据文件存储路径: ./output/twikoo.json
```

### 场景二：博主已有 Twikoo 评论（需保留博主标识）
```bash
你的站点域名: example.com
你（博主）有在新的Twikoo评论系统上评论过吗？(y/N): y
你的电子邮件: admin@example.com
你的 Twikoo UID: 51fa62a9deed478544da9e60663434d8
原 Waline 评论数据文件路径: ./input/waline.json
新的 Twikoo 评论数据文件存储路径: ./output/twikoo.json
```

> 💡 如何获取 Twikoo UID？
> 1. 在 Twikoo 后台导出评论数据
> 2. 打开导出的 JSON 文件
> 3. 找到你自己的评论，复制 `_id` 字段的值

## 🧪 测试数据
项目内置了完整的测试用例：
| 文件 | 用途 |
|------|------|
| `test_input.json` | Waline 格式的测试输入数据 |
| `test_expected_output.json` | 预期转换后的 Twikoo 格式数据 |

**测试数据类型覆盖：**
- ✅ 普通评论
- 💬 嵌套回复（测试 PID/RID）
- 👑 博主评论（测试 master 标识）
- 🚫 垃圾评论（测试 isSpam）
- ⏳ 待审核评论
- 📝 Markdown 格式评论
- 📌 置顶评论

## 📁 项目结构
```text
waline2twikoo/
├── .gitignore                 # Git 忽略配置
├── requirements.txt           # Python 依赖
├── README.md                 # 项目文档（你正在阅读）
├── main.py                   # 主程序 ✨
├── test_input.json           # 测试输入数据
└── test_expected_output.json # 预期输出数据
```

## 🔄 数据映射关系


## ❓ 常见问题
### Q1: 转换失败怎么办？
**检查以下几点：**
- ✅ 输入文件是否存在且为有效 JSON
- ✅ JSON 结构是否为 `{"data": {"Comment": [...]}}`
- ✅ 是否包含必要的字段（nick, mail, url, comment 等）
- ✅ 目标路径是否有写入权限

### Q2: 如何中断程序？
按 `Ctrl + C` 即可安全退出，会显示 `Aborted!`。

### Q3: 输出文件路径有什么限制？
无任何限制！支持：
- 相对路径：./output/data.json
- 绝对路径：/home/user/backups/twikoo.json
- Windows 路径：D:\迁移数据\twikoo.json
- 深层嵌套：./a/b/c/d/e/f/g/data.json

**所有不存在的父目录都会自动创建！**

### Q4: 支持批量转换吗？
目前每次转换一个文件，但可以多次运行，每次指定不同的输入输出路径。

## 📄 开源协议
MIT License © 2026

## ⭐ 支持项目
如果你觉得这个工具有用，欢迎给项目点一个 Star ⭐️

这能帮助更多人发现这个项目！

## 📮 联系方式
- 提交 Issue：[GitHub Issues](https://github.com/Horean0574/waline2twikoo/issues)
- 个人博客：[https://blog.hxrch.top](https://blog.hxrch.top)

Made with ❤️ for Waline → Twikoo migration

如果遇到问题，请仔细阅读本文档或提交 Issue。
