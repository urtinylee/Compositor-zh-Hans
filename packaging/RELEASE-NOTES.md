# Compositor 1.4.8 简体中文补丁 · zh1

适用于 **macOS 26.0+、Apple silicon（M 系列芯片）**。

## 下载哪个文件

- **`Compositor-1.4.8-zh-Hans.pkg`：推荐，双击按提示安装。**
- `Compositor-1.4.8-zh-Hans-app.zip`：解压后将中文应用拖入“应用程序”。
- `INSTALL.zh-CN.md`：离线中文安装指南。
- `Compositor-1.4.8-zh-Hans-source.patch`：开发者使用的源码补丁。
- `SHA256SUMS.txt`：下载完整性校验值。
- `LICENSE.txt`：MIT 许可证和原版权声明。

## 安装

退出已有的中文版，双击 PKG，按安装器提示操作。完成后从“应用程序”打开 **Compositor 简体中文**。无需先安装原版，无需 Xcode 或 Python。

安装位置为 `/Applications/Compositor 简体中文.app`。保留原版 `/Applications/Compositor.app`；如已有同一中文副本，安装器将更新它。

[完整安装指南](https://github.com/urtinylee/Compositor-zh-Hans/blob/main/docs/INSTALL.zh-CN.md)

## 发布状态

本发行版不是官方中文版。应用使用本地 ad-hoc 签名，**PKG 未使用 Developer ID Installer 签名，且未经过 Apple 公证**。下载后可能被 macOS 拦截；仅在确认来源与 SHA-256 后，按照安装指南中的 Apple 官方说明为该文件授权。

主要菜单、工具、图层面板、滤镜、常用对话框和命令搜索加入简体中文；少量罕见提示可能仍为英文。中文副本关闭官方自动更新。

源码基于 Compositor 1.4.8 的 `22c7b8d5b23bb1e27a5746912061b23757c4f554`，MIT 许可证；原版权声明保留。

## 核验范围

已在 Apple silicon Mac 上运行中文版并检查画布创建、PNG 导入、项目保存、PNG 导出、中文混合模式和中文命令搜索。发行 PKG 的结构、安装路径及内含应用签名已检查。尚未在全新 macOS 环境中完成互联网下载后的全过程安装验证，未运行完整自动化 UI 测试集。
