# 秦羲子的网站

用 Astro 搭的静态站。文章都是 Markdown，改完推上去就自动重新生成。

## 本地跑

```powershell
$env:PATH = "C:\Users\Qxiz\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin;" + $env:PATH
$env:ASTRO_TELEMETRY_DISABLED = "1"
$env:XDG_CONFIG_HOME = "C:\Workarea\.config"

cd C:\Workarea\qinxi-site
node node_modules/astro/bin/astro.mjs dev --port 4321
```

浏览器开 <http://127.0.0.1:4321/>。改文件会自动刷新。

想生成静态文件（部署用）：

```powershell
node node_modules/astro/bin/astro.mjs build
```

产物在 `dist/`。

## 加一篇文章

在 `src/content/texts/` 下对应目录新建 `.md`：

- `fiction/` —— 小说、同人
- `longform/` —— 考据、长论文
- `essay/` —— 随笔、日记

文件开头得有这一段：

```markdown
---
title: "关灯"
slug: "guandeng"
kind: fiction
category: "短篇"
date: 2026-11-20
summary: "一句话摘要，列表里会显示。"
draft: false
---
```

- `title` 标题
- `slug` 网址用的英文名，`guandeng` 就是 `/guandeng/`
- `kind` 三选一：`fiction` / `longform` / `essay`
- `category` 栏目内再分组用的名字，随便起
- `date` 写 `2026-11-20` 这种格式
- `summary` 可以省略
- `order` 可选，数字越小排越前（日记用不上，默认按日期倒序）
- `draft: true` 就先不发布

正文就是普通 Markdown。图片放 `public/images/` 下面，正文里写：

```markdown
<figure>
  <img src="/images/qin-hesheng/01-koryuji-romon.jpg" alt="広隆寺楼门" loading="lazy" />
  <figcaption>图注写这里</figcaption>
</figure>
```

## 目录

```
src/
  content/texts/   文章（fiction / longform / essay）
  pages/           首页、各栏目列表、详情页
  layouts/Base.astro
  components/Entry.astro
  styles/global.css   所有样式都在里面
  lib/texts.ts     读取和排序
  content.config.ts   文章字段定义
public/
  images/          文章配图
  favicon.svg
tools/             导入和压缩图片的脚本
```

## 部署

`.github/workflows/deploy.yml` 已经写好了。第一次推上 GitHub 之后：

1. 仓库 Settings → Pages → Source 选 **GitHub Actions**
2. push 到 `main`，Actions 里会自己跑

`astro.config.mjs` 里的 `site` 现在是占位地址，等知道正式的 GitHub 用户名了要改成 `https://<用户名>.github.io` 或者 `https://<用户名>.github.io/<仓库名>`（如果是项目仓库，还要加 `base`）。

## 现在还没做的

- 日记只放了两篇样本，等你圈完哪些能公开再批量导
- `秦造河胜`（东方同人）正文还没校对过排版
- 搜索、标签、暗色模式切换按钮都还没加
