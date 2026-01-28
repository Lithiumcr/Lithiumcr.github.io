# Jekyll 本地开发环境指南

本文档说明如何在 macOS Sequoia 15.5 上配置和使用 Jekyll 本地开发环境。

## 环境要求

- **操作系统**：macOS Sequoia 15.5（或更高版本）
- **Ruby 版本**：3.3.x（通过 rbenv 管理）
- **依赖工具**：
  - Homebrew（macOS 包管理器）
  - Xcode Command Line Tools
  - rbenv + ruby-build（Ruby 版本管理）
  - Bundler（Ruby gem 包管理器）

## 已完成的安装步骤

✅ 以下环境已配置完成，无需重复安装：

### 1. 系统工具
```bash
# Homebrew - 已安装
brew --version  # Homebrew 5.0.8

# Xcode Command Line Tools - 已安装
xcode-select -p  # /Library/Developer/CommandLineTools
```

### 2. Ruby 环境
```bash
# rbenv - 已通过 Homebrew 安装
rbenv --version  # rbenv 1.3.2

# Ruby 3.3.10 - 已安装并设为全局版本
ruby -v  # ruby 3.3.10 (2025-10-23 revision 343ea05002) [arm64-darwin24]

# shell 配置 - 已在 ~/.zshrc 添加 rbenv 初始化
# eval "$(rbenv init - zsh)"
```

### 3. 项目依赖
```bash
# Bundler - 已安装
bundle --version  # Bundler version 4.0.4

# Jekyll 及插件 - 已通过 bundle install 安装
# - jekyll (4.4.1)
# - jekyll-feed
# - jekyll-remote-theme
# - jekyll-seo-tag
# - jekyll-paginate
# - jekyll-sitemap
```

## 快速开始

### 启动本地开发服务器

```bash
# 1. 进入项目目录
cd /Users/administrator/work/Lithiumcr.github.io

# 2. 启动 Jekyll 服务器
bundle exec jekyll serve

# 服务器启动成功后，终端会显示：
# Server address: http://127.0.0.1:4000
# Server running... press ctrl-c to stop.
```

### 访问本地博客

在浏览器中打开：**http://localhost:4000**

你会看到博客首页，包含：
- 标题"北辕记"
- 文章列表
- 与线上版本一致的样式（远程主题已正确加载）

### 停止开发服务器

在运行 Jekyll 服务器的终端窗口按：**Ctrl + C**

## 开发工作流

### 编辑博客内容

1. **修改现有文章**：编辑 `_posts/` 目录下的 Markdown 文件
2. **添加新文章**：在 `_posts/` 目录创建新的 `.md` 文件，遵循命名规范：`YYYY-MM-DD-标题.md`
3. **修改配置**：编辑 `_config.yml`（修改后需要重启服务器）

### 实时预览

- **自动重新生成**：修改文章后，Jekyll 会自动检测变化并重新生成站点
- **终端提示**：看到 "Regenerating..." 和 "...done in X.XX seconds" 表示重新生成完成
- **浏览器刷新**：重新生成完成后，刷新浏览器即可看到更新内容
- **配置文件例外**：修改 `_config.yml` 需要手动重启服务器（Ctrl+C 后重新运行 `bundle exec jekyll serve`）

## 高级用法

### 自定义端口

如果端口 4000 被占用，可以指定其他端口：

```bash
bundle exec jekyll serve --port 4001
# 访问 http://localhost:4001
```

### 增量构建（加快重新生成速度）

```bash
bundle exec jekyll serve --incremental
# 仅重新生成变更的文件，适合大型博客
```

### 草稿预览

查看 `_drafts/` 目录中的草稿文章：

```bash
bundle exec jekyll serve --drafts
```

### 详细日志输出

查看详细的构建日志（用于调试）：

```bash
bundle exec jekyll serve --verbose
```

## 常见问题排查

### 问题 1：端口 4000 被占用

**错误信息**：
```
Address already in use - bind(2) for 127.0.0.1:4000
```

**解决方案**：

方法一：查找并关闭占用端口的进程
```bash
lsof -i :4000
# 找到 PID，然后 kill [PID]
```

方法二：使用其他端口
```bash
bundle exec jekyll serve --port 4001
```

### 问题 2：gem 安装失败（native extension 编译错误）

**错误信息**：
```
ERROR: Failed to build gem native extension
```

**解决方案**：

1. 确保 Xcode Command Line Tools 已安装：
```bash
xcode-select --install
```

2. 如果问题依然存在，尝试重新安装相关 gem：
```bash
bundle clean --force
bundle install
```

### 问题 3：远程主题加载失败

**错误信息**：
```
Could not find remote theme...
```

**解决方案**：

1. 检查网络连接（主题从 GitHub 加载）
2. 验证 `jekyll-remote-theme` 插件已安装：
```bash
bundle list | grep jekyll-remote-theme
```
3. 如果插件未安装，运行：
```bash
bundle install
```

### 问题 4：Ruby 版本不匹配

**错误信息**：
```
requires ruby version >= X.X.X
```

**解决方案**：

1. 检查当前 Ruby 版本：
```bash
ruby -v
which ruby  # 应该显示 ~/.rbenv/shims/ruby
```

2. 如果使用的是系统 Ruby（/usr/bin/ruby），重新加载 shell 配置：
```bash
source ~/.zshrc
```

3. 验证 rbenv 已正确初始化：
```bash
rbenv versions  # 应该显示 * 3.3.10
```

### 问题 5：bundle 命令找不到或使用旧版本

**错误信息**：
```
Could not find 'bundler' (X.X.X) required by your Gemfile.lock
```

**解决方案**：

1. 确保使用 rbenv 的 Ruby 环境：
```bash
source ~/.zshrc
which bundle  # 应该显示 ~/.rbenv/shims/bundle
```

2. 重新生成 rbenv shims：
```bash
rbenv rehash
```

3. 如果问题依然存在，重新安装 Bundler：
```bash
gem install bundler
```

### 问题 6：文件编码问题（中文文件名）

**错误信息**：
```
invalid byte sequence in UTF-8
```

**解决方案**：

确保文件以 UTF-8 编码保存。如果使用的编辑器不支持 UTF-8，考虑使用以下编辑器：
- VS Code（推荐）
- Sublime Text
- Atom

## 文件结构说明

```
Lithiumcr.github.io/
├── _config.yml          # Jekyll 配置文件（修改后需重启服务器）
├── _posts/              # 博客文章目录（YYYY-MM-DD-标题.md）
├── _drafts/             # 草稿目录（不会发布到线上）
├── _data/               # 数据文件（如 social.yml）
├── _includes/           # 可复用的页面片段
├── _layouts/            # 页面布局模板
├── image/               # 图片资源目录
├── Gemfile              # Ruby 依赖声明文件
├── Gemfile.lock         # 锁定依赖版本（自动生成）
├── .gitignore           # Git 忽略文件配置
└── README-DEV.md        # 本文档
```

### 本地生成的文件（已被 git 忽略）

以下文件由 Jekyll 本地生成，**不会**提交到 Git 仓库：

- `_site/` - Jekyll 生成的静态站点文件
- `.jekyll-cache/` - Jekyll 缓存目录
- `.jekyll-metadata` - Jekyll 元数据文件
- `.bundle/` - Bundler 本地配置
- `vendor/` - Bundler 安装的 gem 目录（如果使用 `--path vendor/bundle`）

## 与 GitHub Pages 的区别

### 相同点
- 博客内容和配置完全一致
- 使用相同的主题和插件
- 最终渲染效果应该一致

### 不同点
- **本地**：Jekyll 版本为最新（4.4.1），gem 版本由 Gemfile 控制
- **GitHub Pages**：使用固定的 Jekyll 版本和插件白名单

### 建议
如果需要确保本地环境与 GitHub Pages 完全一致，可以在 Gemfile 中添加：

```ruby
gem "github-pages", group: :jekyll_plugins
```

然后运行 `bundle update`。这会安装与 GitHub Pages 相同版本的 Jekyll 和插件。

## 更新依赖

### 更新所有 gem 到最新版本

```bash
bundle update
```

### 更新特定 gem

```bash
bundle update jekyll
```

### 查看过时的 gem

```bash
bundle outdated
```

## 联系与支持

如果遇到本文档未涵盖的问题：

1. 查看 Jekyll 官方文档：https://jekyllrb.com/docs/
2. 查看主题文档：https://github.com/ngzhio/jekyll-theme-hamilton
3. 查看 rbenv 文档：https://github.com/rbenv/rbenv

---

**环境配置完成日期**：2026-01-28
**Ruby 版本**：3.3.10
**Jekyll 版本**：4.4.1
**macOS 版本**：Sequoia 15.5
