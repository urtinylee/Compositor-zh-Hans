# Compositor 简体中文补丁

[下载安装包](https://github.com/urtinylee/Compositor-zh-Hans/releases/latest) · [中文安装指南](docs/INSTALL.zh-CN.md) · [问题反馈](https://github.com/urtinylee/Compositor-zh-Hans/issues)

基于 [robbietilton/Compositor](https://github.com/robbietilton/Compositor) **1.4.8** 的第三方简体中文汉化副本。主要菜单、工具、图层面板、滤镜及常用对话框加入中文，也支持中文命令搜索。

## 安装

**要求：macOS 26.0+、Apple silicon（M 系列芯片）。**

1. 在 Releases 下载 `Compositor-1.4.8-zh-Hans.pkg`。
2. 退出已有的 **Compositor 简体中文**，双击 PKG，按提示安装。
3. 在“应用程序”中打开 **Compositor 简体中文**。

无需先安装原版，无需 Xcode 或 Python。安装包将完整的中文应用安装到 `/Applications/Compositor 简体中文.app`。原版 `/Applications/Compositor.app` 可继续使用。

本发行版采用本地 ad-hoc 应用签名，**PKG 未使用 Developer ID Installer 签名，也未经过 Apple 公证**。从互联网下载后可能出现 macOS 安全提示，请先阅读 [安装指南](docs/INSTALL.zh-CN.md#macos-拦截安装或首次启动时)，确认来源与 SHA-256。此项目不是原作者的官方中文版。

可选的 `Compositor-1.4.8-zh-Hans-app.zip` 支持解压后拖入“应用程序”安装；两个安装版本包含同一应用。

## 范围和限制

- 简体中文覆盖主要菜单、工具、面板、滤镜名称、命令搜索和常用对话框；少量提示可能仍为英文。
- 原来的文件格式、英文枚举标识、快捷键、用户已有图层名称与图片内容保留。
- 中文副本使用独立 bundle ID `com.wonderassembly.compositor.zhHans`，设置与原版分开。
- 中文副本关闭官方自动更新；新版需从本项目 Releases 获取对应的汉化版本。
- 发布程序已在 Apple silicon Mac 上启动并检查过画布创建、导入、保存、PNG 导出、混合模式和中文搜索。PKG 的结构、路径及所含应用签名已检查；尚未在全新 macOS 环境中完成下载安装全过程验证，也未运行完整自动化 UI 测试集。

## 源码与重建

本仓库包含汉化后的完整源码。上游基线为提交 `22c7b8d5b23bb1e27a5746912061b23757c4f554`（Compositor 1.4.8）。

译文源：`localization/translations.tsv`。标准资源：`Compositor/zh-Hans.lproj/Localizable.strings`。动态文案入口：`Compositor/Localization.swift`。

本机已验证的构建环境是 Command Line Tools 的 Swift 6.4 与 macOS 26.5 SDK；构建脚本目前固定使用该 SDK。其他工具链尚未验证。为取得同版本编译后的图标资源，源码重建需要先将官方 1.4.8 安装到 `/Applications/Compositor.app`。普通用户使用发行安装包不需要这一步。

```sh
python3 scripts/build-zh-hans.py
python3 scripts/package-release.py
```

第一条重新编译完整 Swift / C 源码并构建中文应用，第二条生成 PKG、应用 ZIP 与安装指南。安装器打包使用系统自带的 `pkgbuild` / `productbuild`。

如只需从官方 1.4.8 源码应用差异，可在原项目基线提交上运行：

```sh
git apply /path/to/Compositor-1.4.8-zh-Hans-source.patch
```

这里的 `.patch` 是源码补丁，不是普通用户的安装入口。PKG/ZIP 包含完整应用，是因为部分显示文案需要重新编译源码。

## 回退

退出中文版，将且仅将 `/Applications/Compositor 简体中文.app` 拖入废纸篓，再打开原版。项目文件请保留。详见 [安装指南](docs/INSTALL.zh-CN.md#卸载与回退)。

## 上游与许可

原项目 Copyright (c) 2026 Wonder Assembly LLC，采用 [MIT 许可证](LICENSE)。新增汉化和打包代码亦按 MIT 许可证提供。原始 README 保存在 [docs/UPSTREAM-README.md](docs/UPSTREAM-README.md)。

这是独立的社区汉化发布，与原作者无关联；所有原项目版权声明均保留。
