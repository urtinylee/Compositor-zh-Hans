import AppKit
import Foundation

/// Display strings only. Never use the translated result as a persisted identifier.
nonisolated private enum ChineseLocalization {
    static let bundle: Bundle? = Bundle.main.path(forResource: "zh-Hans", ofType: "lproj").flatMap(Bundle.init(path:))
}

nonisolated func zh(_ text: String) -> String {
    guard let bundle = ChineseLocalization.bundle else { return text }
    let value = bundle.localizedString(forKey: text, value: text, table: "Localizable")
    if value != text { return value }
    // Dynamic command titles are composed at runtime. Their persisted action names stay English.
    for (prefix, translated) in [("Last Filter: ", "上次滤镜："), ("Undo ", "撤销"), ("Redo ", "重做"),
                                  ("Delete ", "删除"), ("Hide ", "隐藏"), ("Show ", "显示"),
                                  ("Align ", "对齐：")] where text.hasPrefix(prefix) {
        return translated + zh(String(text.dropFirst(prefix.count)))
    }
    for direction in ["Left", "Right", "Up", "Down"] {
        for amount in [1, 10] {
            if text == "Nudge \(direction) \(amount) px" { return "向" + zh(direction) + "微移 \(amount) 像素" }
            if text == "Move selected pixels \(direction) \(amount) px" { return "向" + zh(direction) + "移动所选像素 \(amount) 像素" }
        }
    }
    for digit in 0...9 where text == "Opacity digit \(digit) (type two for exact %)" {
        return "不透明度数字 \(digit)（输入两位数字可精确设置百分比）"
    }
    if text.hasSuffix(" by 10") { return zh(String(text.dropLast(6))) + "（步长 10）" }
    return text
}

@MainActor
enum ChinesePatch {
    static func showInformation() {
        let alert = NSAlert()
        alert.messageText = "Compositor 简体中文补丁"
        alert.informativeText = "基于 Compositor 1.4.8 的本地汉化副本。官方原版可从应用程序文件夹单独打开。\n\n此副本已关闭官方自动更新；新版需要重新应用汉化补丁。"
        alert.addButton(withTitle: "确定")
        alert.runModal()
    }
}

extension EditorSession {
    var toolInstructions: String {
        let selection = "Shift 添加 · Option 减去 · 拖动选区内部移动 · Delete 清除 · ⌘D 取消选择"
        let brush = "[ ] 调整大小 · Shift-[ ] 调整硬度 · 1–0 调整不透明度 · 空格平移"
        switch tool {
        case .marquee:
            return (marqueeKind == .ellipse ? "拖动绘制椭圆 · 拖动中再次按 Shift 限制为圆形" : "拖动绘制矩形 · 拖动中再次按 Shift 限制为正方形 · ⌘拖动移动像素") + " · " + selection
        case .wand:
            return (wandMode == .object ? "点击对象以选择轮廓 · Tab 切换魔棒" : "点击选择相似颜色 · Tab 切换对象选择") + " · " + selection
        case .lasso:
            return lassoKind == .freehand ? "拖动绘制选区 · ⌥⌫ / ⌘⌫ 填充 · " + selection : "点击添加顶点 · 点击起点、双击或 Enter 闭合 · Delete 移除顶点 · Esc 取消"
        case .brush:
            return (brushMode == .erase ? "拖动擦除" : "拖动绘画") + " · " + brush + " · Esc 取消"
        case .blur:
            return (blurMode == .blur ? "拖动柔化" : blurMode == .smudge ? "拖动涂抹" : "拖动推动像素") + " · [ ] 大小 · Shift-[ ] 硬度 · 1–0 强度 · 空格平移"
        case .cloneStamp: return "Option 点击设置取样来源 · 拖动仿制 · " + brush
        case .spotHealing: return "在瑕疵上拖动以修复 · " + brush + " · Esc 取消"
        case .type: return "拖动创建文本框 · 点击文字编辑 · 拖动控制点调整大小 · ⌘Return 完成 · Esc 取消"
        case .shape:
            let constraint = shapeKind == .line ? "45°" : shapeKind == .rectangle ? "正方形" : "圆形"
            return "拖动在新图层绘制形状 · Shift 限制为" + constraint + " · Option 从中心绘制 · Shift-U 或 Tab 切换形状 · Esc 取消 · 空格平移"
        case .gradient: return "拖动绘制渐变 · 拖动端点调整 · Shift 限制 45° · 1–0 不透明度 · Enter 应用 · Esc 取消"
        case .crop: return "拖动裁剪 · Enter 应用 · Esc 取消 · 空格平移"
        case .move: return "拖动移动 · 控制点缩放 · 圆点旋转 · 1–0 图层不透明度 · 空格平移"
        case .hand: return "拖动平移 · 双指捏合缩放"
        case .idle: return "未选择工具 · 按工具快捷键选择 · 空格平移"
        case .eyedropper: return "点击取样颜色 · 空格平移"
        case .zoom: return "点击放大 · Option 点击缩小 · 左右拖动平滑缩放 · 空格平移"
        }
    }
}
