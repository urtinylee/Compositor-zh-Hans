# Compositor 1.4.8 简体中文补丁安装指南

## 下载与系统要求

从 [本项目 Releases](https://github.com/urtinylee/Compositor-zh-Hans/releases/latest) 下载：

- **推荐：`Compositor-1.4.8-zh-Hans.pkg`** — macOS 图形安装器。
- `Compositor-1.4.8-zh-Hans-app.zip` — 可选的拖放安装版本。
- `Compositor-1.4.8-zh-Hans-source.patch` — 供开发者使用的源码差异，普通用户不需要。
- `SHA256SUMS.txt` — 上述文件的完整性校验值。

需要 **macOS 26.0 或更高版本、Apple silicon（M 系列芯片）**。不支持 Intel Mac 或更早的 macOS。无需先安装原版，也无需安装 Xcode、Python。

这是基于开源 Compositor 1.4.8 的第三方汉化副本。为使源码中的动态菜单和提示一并显示中文，安装包包含完整的已编译中文应用，而非直接修改原版的资源补丁。

## 方式一：PKG 安装（推荐）

1. 退出正在运行的 **Compositor 简体中文**。
2. 双击 `Compositor-1.4.8-zh-Hans.pkg`，阅读安装器说明。
3. 按“继续”与“安装”，按 macOS 提示输入本机管理员密码。
4. 安装完成后，在“应用程序”文件夹打开 **Compositor 简体中文**。

安装位置是 `/Applications/Compositor 简体中文.app`。若该路径已有同一中文版，安装器会更新它；若是其他应用或符号链接，会停止安装。安装器只支持当前启动磁盘，且不会自动退出任何应用。

原版 `/Applications/Compositor.app` 可继续使用。中文副本使用独立应用标识，设置与原版分开；项目格式、快捷键及已有图层名称沿用原来的值。

## 方式二：ZIP 拖放安装

1. 下载并解压 `Compositor-1.4.8-zh-Hans-app.zip`。
2. 将其中的 **Compositor 简体中文.app** 拖到“应用程序”文件夹。
3. 若同名旧版存在，先退出旧版并将它移入废纸篓，再拖入新版。
4. 双击中文版启动。

ZIP 内提供的应用与 PKG 内的应用相同。向“应用程序”文件夹写入时也可能需要管理员授权。

## macOS 拦截安装或首次启动时

**发布状态：应用采用 ad-hoc 本地签名；PKG 没有 Developer ID Installer 签名；两者均未经过 Apple 公证。** 因此从 GitHub 下载后，macOS 可能阻止安装器或应用首次运行。这不是“已公证的官方中文版”。

只在确认下载来自本项目 Releases、且文件校验一致时，按照 [Apple 官方说明：在 Mac 上安全地打开 App](https://support.apple.com/zh-cn/102445) 为这个文件授权：先尝试打开，然后到“系统设置 → 隐私与安全性”查看对应项目的“仍要打开”，并确认打开。安装器和应用可能分别需要确认。

如果你的 Mac 被组织管理，或系统没有显示授权选项，请遵守设备管理员的限制。不要关闭整个系统的 Gatekeeper，也不要运行来源不明的解除限制命令。若系统提示恶意软件、证书撤销或风险，请停止，并提交具体提示供排查。

## 核对文件

在终端进入下载目录，运行：

```sh
shasum -a 256 Compositor-1.4.8-zh-Hans.pkg
```

将输出与本次 Release 附带的 `SHA256SUMS.txt` 中对应文件的一行比较。应逐字相同；不同则重新下载并暂缓安装。校验值用于确认下载完整性，不代替 Apple 公证。

## 汉化范围与更新

主要菜单、工具、图层面板、滤镜名称、命令搜索及常用保存/导出对话框已加入简体中文。少量罕见动态提示、第三方或系统文案可能仍为英文。

此副本关闭了官方自动更新，以免汉化被官方版本覆盖。请通过本项目 Releases 下载匹配版本的新版汉化包。不要将这个包作为其他 Compositor 版本的原位补丁使用。

## 卸载与回退

1. 退出 **Compositor 简体中文**。
2. 将 `/Applications/Compositor 简体中文.app` 拖入废纸篓。
3. 打开原版 **Compositor.app**；若未安装原版，可从 [原项目 Releases](https://github.com/robbietilton/Compositor/releases) 获取。

安装器不删除你的项目文件。自己的 `.comp` 项目与图片请自行保留。为了可回退，安装器也不清理中文版的个人偏好设置；卸载应用不会自动删除这些设置。

## 常见问题

- **提示先退出中文版：** 用中文版菜单“退出”或 ⌘Q 退出，再运行安装器。
- **提示安装位置被占用：** 检查“应用程序”中的同名项目，不要让安装器覆盖其他软件。
- **提示系统或芯片不支持：** 本包只支持 macOS 26+ 的 Apple silicon Mac。
- **原版更新后还能用吗：** 原版与本中文副本各自独立；中文副本仍基于 1.4.8。
- **需要编译吗：** 普通安装不需要；源码构建方法见仓库 README。

反馈入口：[GitHub Issues](https://github.com/urtinylee/Compositor-zh-Hans/issues)。提交截图或日志前，请移除自己的文件路径、项目内容等私人信息。

## 版权与许可

原项目：[robbietilton/Compositor](https://github.com/robbietilton/Compositor)，Copyright (c) 2026 Wonder Assembly LLC，MIT 许可证。

本项目保留原版权声明，新增汉化与打包代码也按 MIT 许可证发布。完整许可见仓库和发布附件中的 `LICENSE` / `LICENSE.txt`。
