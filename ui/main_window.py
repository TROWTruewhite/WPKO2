# -*- coding: utf-8 -*-
import sys
import math
import json
import os
import copy

from PySide6.QtCore import (
    Qt, Signal, Property, QPointF, QRectF, QRect, QSize, QPoint,
    QPropertyAnimation, QEasingCurve,
    QParallelAnimationGroup, QSequentialAnimationGroup,
    QVariantAnimation, QAbstractAnimation, QTimer, QProcess,
)
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QStackedWidget, QGraphicsDropShadowEffect, QMessageBox,
    QGraphicsOpacityEffect, QInputDialog, QScrollArea,
    QTextBrowser, QFrame, QMenu,
    QDialog, QLineEdit, QTextEdit, QBoxLayout,
    QSizePolicy, QLayout,
)
from PySide6.QtGui import (
    QColor, QPainter, QRadialGradient, QLinearGradient, QPen,
    QFont, QFontDatabase, QPainterPath, QFontMetrics,
)


# ==================== 全局常量 ====================
TOPBAR_HEIGHT = 108
FOOTER_HEIGHT = 40
BUTTON_MARGIN = 108
AMP_SIZE = 40
GAP_AROUND_AMP = (BUTTON_MARGIN - AMP_SIZE) // 2

FONT_CANDIDATES = [
    "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC",
    "Noto Sans CJK SC", "WenQuanYi Micro Hei",
]

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "config.json"
)


def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


# ==================== 语言表 ====================
LANGUAGES = {
    "zh": {
        "tab_character_short": "CHA",
        "tab_character_full": "角色管理",
        "tab_config_short": "CON",
        "tab_config_full": "板子管理",
        "tab_logger_short": "LOG",
        "tab_logger_full": "游戏记录",
        "tab_runner_short": "RUN",
        "tab_runner_full": "游戏模拟",
        "tab_more_short": "...",
        "action_add": "添加角色",
        "action_edit": "编辑角色",
        "action_delete": "删除角色",
        "no_character_title": "未选择角色",
        "no_character_desc": "请从左侧列表选择一个角色，或点击 + 添加新角色。",
        "camp_label": "阵营",
        "coming_soon": "即将推出…",
        "edit_dialog_title": "编辑角色",
        "edit_dialog_label": "角色名称：",
        "new_character_name": "新角色 {n}",
        "new_character_camp": "未知",
        "new_character_desc": "请编辑以填写角色描述。",
        "settings_title": "设置",
        "settings_language": "语言",
        "restart_title": "重启应用",
        "restart_text": "修改语言需要重启应用才能生效。\n是否立即重启？",
        "restart_confirm": "重启",
        "exit_title": "退出应用",
        "exit_message": "确定要退出 WPKO2 吗？",
        "exit_confirm": "退出",
        "delete_title": "删除角色",
        "delete_message": "确定要删除「{name}」吗？此操作不可撤销。",
        "delete_confirm": "删除",
        "tag_attack": "攻击牌",
        "tag_heal": "治疗牌",
        "tag_open_eye": "睁眼牌",
        "tag_close_eye": "闭眼牌",
        "tag_day": "白天牌",
        "tag_night": "黑夜牌",
        "tag_info": "信息牌",
        "tag_protect": "保护牌",
        "editor_title_new": "创建角色",
        "editor_title_edit": "编辑角色",
        "editor_name_label": "角色名称",
        "editor_camp_label": "阵营",
        "editor_desc_label": "角色描述",
        "editor_tags_label": "标签",
        "editor_name_placeholder": "输入角色名称",
        "editor_camp_placeholder": "例如：好人阵营 / 狼人阵营",
        "editor_desc_placeholder": "描述该角色的技能和玩法……",
        "editor_cancel": "取消",
        "editor_save": "保存",
    },
    "en": {
        "tab_character_short": "CHA",
        "tab_character_full": "Character Manager",
        "tab_config_short": "CON",
        "tab_config_full": "Config Manager",
        "tab_logger_short": "LOG",
        "tab_logger_full": "Game Logger",
        "tab_runner_short": "RUN",
        "tab_runner_full": "Game Runner",
        "tab_more_short": "...",
        "action_add": "Add Character",
        "action_edit": "Edit Character",
        "action_delete": "Delete Character",
        "no_character_title": "No Character",
        "no_character_desc": "Pick a character from the list, or click + to add one.",
        "camp_label": "Camp",
        "coming_soon": "Coming soon...",
        "edit_dialog_title": "Edit Character",
        "edit_dialog_label": "Name:",
        "new_character_name": "New Character {n}",
        "new_character_camp": "Unknown",
        "new_character_desc": "Edit to fill in the description.",
        "settings_title": "Settings",
        "settings_language": "Language",
        "restart_title": "Restart",
        "restart_text": "Changing language requires a restart.\nRestart now?",
        "restart_confirm": "Restart",
        "exit_title": "Quit",
        "exit_message": "Are you sure you want to quit WPKO2?",
        "exit_confirm": "Quit",
        "delete_title": "Delete Character",
        "delete_message": "Delete \"{name}\"? This cannot be undone.",
        "delete_confirm": "Delete",
        "tag_attack": "Attack",
        "tag_heal": "Heal",
        "tag_open_eye": "Open Eye",
        "tag_close_eye": "Close Eye",
        "tag_day": "Day",
        "tag_night": "Night",
        "tag_info": "Info",
        "tag_protect": "Protect",
        "editor_title_new": "New Character",
        "editor_title_edit": "Edit Character",
        "editor_name_label": "Name",
        "editor_camp_label": "Camp",
        "editor_desc_label": "Description",
        "editor_tags_label": "Tags",
        "editor_name_placeholder": "Enter character name",
        "editor_camp_placeholder": "e.g. Village / Wolf",
        "editor_desc_placeholder": "Describe the role's abilities and playstyle...",
        "editor_cancel": "Cancel",
        "editor_save": "Save",
    },
}

_current_lang = "zh"


def set_language(code):
    global _current_lang
    if code in LANGUAGES:
        _current_lang = code


def tr(key, **kwargs):
    text = LANGUAGES.get(_current_lang, LANGUAGES["zh"]).get(key, key)
    return text.format(**kwargs) if kwargs else text


TAG_DEFS = [
    {"id": "attack"},
    {"id": "heal"},
    {"id": "open_eye"},
    {"id": "close_eye"},
    {"id": "day"},
    {"id": "night"},
    {"id": "info"},
    {"id": "protect"},
]

TAG_COLORS = {
    "attack": "#d13b3f",
    "heal": "#3a9e5c",
    "open_eye": "#5b8def",
    "close_eye": "#7a7f8a",
    "day": "#e0a030",
    "night": "#4a4e69",
    "info": "#8e6bbf",
    "protect": "#2d9c8f",
}

SCROLL_STYLE = """
QScrollArea {
    background: transparent;
    border: none;
}
QScrollArea > QWidget > QWidget {
    background: transparent;
}
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 4px 2px 4px 0px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: rgba(0, 0, 0, 45);
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(0, 0, 0, 85);
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}
QScrollBar:horizontal {
    background: transparent;
    height: 0px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background: transparent;
    min-width: 0;
}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: transparent;
}
"""


class FlowLayout(QLayout):
    """从左到右排列，放不下自动换行；用于标签胶囊"""

    def __init__(self, parent=None, margin=0, hspacing=6, vspacing=6):
        super().__init__(parent)
        self._items = []
        self._hspacing = hspacing
        self._vspacing = vspacing
        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        self._items.append(item)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        m = self.contentsMargins()
        size += QSize(m.left() + m.right(), m.top() + m.bottom())
        return size

    def _do_layout(self, rect, test_only):
        m = self.contentsMargins()
        effective = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        x = effective.x()
        y = effective.y()
        line_height = 0

        for item in self._items:
            widget = item.widget()
            if widget is None:
                continue
            next_x = x + item.sizeHint().width() + self._hspacing
            if next_x - self._hspacing > effective.right() and line_height > 0:
                x = effective.x()
                y = y + line_height + self._vspacing
                next_x = x + item.sizeHint().width() + self._hspacing
                line_height = 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y() + m.bottom()


class _ContentHost(QWidget):
    """内容宿主：强制 minimumSizeHint 为 0，避免 QScrollArea 被内容撑宽"""

    def minimumSizeHint(self):
        return QSize(0, 0)

    def sizeHint(self):
        return QSize(0, 0)


def tag_name(tag_id):
    return tr("tag_" + tag_id)


TOP_BTN_QSS = """
QPushButton {
    color: #cfd6e0;
    background: rgba(255, 255, 255, 22);
    border: none;
    outline: none;
    border-radius: 10px;
    padding: 0;
}
QPushButton:hover {
    background: rgba(255, 255, 255, 60);
    color: #ffffff;
}
QPushButton:pressed {
    background: rgba(255, 255, 255, 32);
}
QPushButton#danger:hover {
    background: rgba(179, 34, 43, 230);
    color: #ffffff;
}
"""


def pick_font(candidates, fallback="sans-serif"):
    families = set(QFontDatabase.families())
    for name in candidates:
        if name in families:
            return name
    return fallback


def passthrough(widget):
    widget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
    return widget


# ==================== 窗口背景 ====================
class WindowBackground(QWidget):
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, QColor("#1b202b"))
        grad.setColorAt(1.0, QColor("#12151c"))
        p.fillRect(self.rect(), grad)
        p.end()


# ==================== 图标按钮 ====================
class IconButton(QPushButton):
    def __init__(self, icon_type: str, tooltip: str,
                 danger: bool = False, parent=None):
        super().__init__(parent)
        self._icon_type = icon_type
        self.setFixedSize(44, 44)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)
        self.setToolTip(tooltip)
        self.setStyleSheet(TOP_BTN_QSS)
        if danger:
            self.setObjectName("danger")

    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        color = QColor("#ffffff") if self.underMouse() else QColor("#cfd6e0")
        pen = QPen(color)
        pen.setWidthF(1.8)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)

        size = 24.0
        cx, cy = self.width() / 2, self.height() / 2
        r = QRectF(cx - size / 2, cy - size / 2, size, size)

        if self._icon_type == "about":
            self._draw_about(p, r)
        elif self._icon_type == "account":
            self._draw_account(p, r)
        elif self._icon_type == "settings":
            self._draw_settings(p, r)
        elif self._icon_type == "exit":
            self._draw_exit(p, r)
        p.end()

    def _draw_about(self, p, r):
        x, y, w, h = r.x(), r.y(), r.width(), r.height()
        m = 2.0
        bx, by = x + m, y + m
        bw, bh = w - 2 * m, h * 0.60
        bottom = by + bh
        radius = 4.0
        tx = bx + bw * 0.28
        tail_w, tail_h = 5.0, 5.0

        path = QPainterPath()
        path.moveTo(bx + radius, by)
        path.lineTo(bx + bw - radius, by)
        path.quadTo(bx + bw, by, bx + bw, by + radius)
        path.lineTo(bx + bw, bottom - radius)
        path.quadTo(bx + bw, bottom, bx + bw - radius, bottom)
        path.lineTo(tx + tail_w, bottom)
        path.lineTo(tx + tail_w * 0.5, bottom + tail_h)
        path.lineTo(tx, bottom)
        path.lineTo(bx + radius, bottom)
        path.quadTo(bx, bottom, bx, bottom - radius)
        path.lineTo(bx, by + radius)
        path.quadTo(bx, by, bx + radius, by)
        path.closeSubpath()
        p.drawPath(path)

    def _draw_account(self, p, r):
        x, y, w, h = r.x(), r.y(), r.width(), r.height()
        head_r = w * 0.17
        head_cx = x + w / 2
        head_cy = y + h * 0.30
        p.drawEllipse(QPointF(head_cx, head_cy), head_r, head_r)

        body_w = w * 0.68
        body_h = h * 0.82
        bx = x + (w - body_w) / 2
        by = head_cy + head_r
        p.drawArc(QRectF(bx, by, body_w, body_h), 0, 180 * 16)

    def _draw_settings(self, p, r):
        cx, cy = r.center().x(), r.center().y()
        R = min(r.width(), r.height()) / 2
        body_r = R * 0.58
        hole_r = R * 0.24
        teeth = 8
        tooth_len = R * 0.26

        p.drawEllipse(QPointF(cx, cy), body_r, body_r)
        p.drawEllipse(QPointF(cx, cy), hole_r, hole_r)

        p.save()
        pen = p.pen()
        pen.setWidthF(2.2)
        p.setPen(pen)
        for i in range(teeth):
            ang = 2 * math.pi * i / teeth - math.pi / 2
            x1 = cx + math.cos(ang) * body_r
            y1 = cy + math.sin(ang) * body_r
            x2 = cx + math.cos(ang) * (body_r + tooth_len)
            y2 = cy + math.sin(ang) * (body_r + tooth_len)
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        p.restore()

    def _draw_exit(self, p, r):
        x, y, w, h = r.x(), r.y(), r.width(), r.height()

        door_left = x + 2.5
        door_top = y + 2.5
        door_bottom = y + h - 2.5
        door_right = x + w * 0.42

        p.drawLine(QPointF(door_left, door_top),
                   QPointF(door_left, door_bottom))
        p.drawLine(QPointF(door_left, door_top),
                   QPointF(door_right, door_top))
        p.drawLine(QPointF(door_right, door_top),
                   QPointF(door_right, door_top + h * 0.30))

        arrow_y = y + h * 0.62
        arrow_start = x + w * 0.34
        arrow_end = x + w - 2.5
        p.drawLine(QPointF(arrow_start, arrow_y),
                   QPointF(arrow_end, arrow_y))

        head = w * 0.20
        p.drawLine(QPointF(arrow_end, arrow_y),
                   QPointF(arrow_end - head, arrow_y - head * 0.75))
        p.drawLine(QPointF(arrow_end, arrow_y),
                   QPointF(arrow_end - head, arrow_y + head * 0.75))


# ==================== 丝滑 Tab 栏 ====================
class TabBar(QWidget):
    tabChanged = Signal(int)

    def __init__(self, tabs, font_family, parent=None):
        super().__init__(parent)
        self._tabs = tabs
        self._font_family = font_family

        self._current = 0
        self._hover_index = -1
        self._progresses = [0.0] * len(tabs)
        self._progresses[0] = 1.0

        self._base_short_w, self._base_full_w, self._base_gap = \
            self._calc_base_sizes()

        self._short_w = self._base_short_w
        self._full_w = self._base_full_w
        self._gap = self._base_gap

        self._anims_by_index = {}
        self.setFixedHeight(52)
        self.setMouseTracking(True)

    def _calc_base_sizes(self):
        f_short = QFont(self._font_family)
        f_short.setPixelSize(14)
        f_short.setWeight(QFont.Bold)
        f_short.setLetterSpacing(QFont.AbsoluteSpacing, 1)
        fm_short = QFontMetrics(f_short)

        f_full = QFont(self._font_family)
        f_full.setPixelSize(15)
        f_full.setWeight(QFont.Bold)
        fm_full = QFontMetrics(f_full)

        f_disabled = QFont(self._font_family)
        f_disabled.setPixelSize(18)
        f_disabled.setWeight(QFont.Bold)
        fm_disabled = QFontMetrics(f_disabled)

        max_short = 0
        max_full = 0
        for tab in self._tabs:
            if tab["disabled"]:
                max_short = max(
                    max_short,
                    fm_disabled.horizontalAdvance(tab["short"]),
                )
            else:
                max_short = max(
                    max_short,
                    fm_short.horizontalAdvance(tab["short"]),
                )
                max_full = max(
                    max_full,
                    fm_full.horizontalAdvance(tab["full"]),
                )

        short_w = max(max_short + 32, 56)
        full_w = max(max_full + 44, short_w + 36)
        return short_w, full_w, 8

    def _recalc_sizes(self):
        n = len(self._tabs)
        worst = (
            self._base_full_w
            + (n - 1) * self._base_short_w
            + (n - 1) * self._base_gap
        )
        avail = self.width()
        if avail <= 0 or worst <= avail:
            self._short_w = self._base_short_w
            self._full_w = self._base_full_w
            self._gap = self._base_gap
            return
        scale = avail / worst
        self._full_w = max(
            int(self._base_full_w * 0.8),
            int(self._base_full_w * scale),
        )
        self._short_w = max(
            int(self._base_short_w * 0.8),
            int(self._base_short_w * scale),
        )
        self._gap = max(6, int(self._base_gap * scale))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._recalc_sizes()
        self.update()

    def _layout_rects(self):
        rects = []
        x = 0
        for i, tab in enumerate(self._tabs):
            if tab["disabled"]:
                w = self._short_w
            else:
                p = self._progresses[i]
                w = self._short_w + (self._full_w - self._short_w) * p
            rects.append(QRect(int(x), 0, int(w), self.height()))
            x += int(w) + self._gap
        return rects

    def _index_at(self, pos):
        for i, rect in enumerate(self._layout_rects()):
            if rect.contains(pos):
                return i
        return -1

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)

        rects = self._layout_rects()

        for i, rect in enumerate(rects):
            tab = self._tabs[i]
            prog = self._progresses[i]
            disabled = tab["disabled"]
            hovered = (i == self._hover_index) and not disabled
            selected = (i == self._current) and not disabled

            if disabled:
                bg = QColor(0, 0, 0, 8)
            elif selected:
                bg = QColor(26, 29, 36)
            elif hovered:
                bg = QColor(0, 0, 0, 20)
            else:
                bg = QColor(0, 0, 0, 8)

            path = QPainterPath()
            path.addRoundedRect(QRectF(rect), 12, 12)
            p.fillPath(path, bg)

            if disabled:
                f = QFont(self._font_family)
                f.setPixelSize(18)
                f.setWeight(QFont.Bold)
                p.setFont(f)
                p.setPen(QColor(140, 140, 148))
                p.drawText(rect, Qt.AlignCenter, tab["short"])
                continue

            short_alpha = int(255 * (1 - prog))
            full_alpha = int(255 * prog)

            if selected:
                short_color = QColor(255, 255, 255)
                full_color = QColor(255, 255, 255)
            else:
                short_color = QColor(70, 74, 82)
                full_color = QColor(70, 74, 82)

            if short_alpha > 4:
                f_short = QFont(self._font_family)
                f_short.setPixelSize(14)
                f_short.setWeight(QFont.Bold)
                f_short.setLetterSpacing(QFont.AbsoluteSpacing, 1)
                p.setFont(f_short)
                c = QColor(short_color)
                c.setAlpha(short_alpha)
                p.setPen(c)
                p.drawText(rect, Qt.AlignCenter, tab["short"])

            if full_alpha > 4:
                f_full = QFont(self._font_family)
                f_full.setPixelSize(15)
                f_full.setWeight(QFont.Bold)
                p.setFont(f_full)
                c = QColor(full_color)
                c.setAlpha(full_alpha)
                p.setPen(c)
                p.drawText(rect, Qt.AlignCenter, tab["full"])

        p.end()

    def mouseMoveEvent(self, event):
        idx = self._index_at(event.position().toPoint())
        if idx != self._hover_index:
            self._hover_index = idx
            self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if self._hover_index != -1:
            self._hover_index = -1
            self.update()
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        idx = self._index_at(event.position().toPoint())
        if 0 <= idx < len(self._tabs):
            if not self._tabs[idx]["disabled"] and idx != self._current:
                self.set_current(idx)
        super().mouseReleaseEvent(event)

    def set_current(self, idx):
        if idx == self._current or self._tabs[idx]["disabled"]:
            return
        old = self._current
        self._current = idx
        self._animate(old, 0.0)
        self._animate(idx, 1.0)
        self.tabChanged.emit(idx)

    def _animate(self, index, target):
        anim = self._anims_by_index.get(index)
        if anim is None:
            anim = QVariantAnimation(self)
            anim.setDuration(320)
            anim.setEasingCurve(QEasingCurve.OutCubic)

            def make_slot(i):
                def slot(v):
                    self._progresses[i] = float(v)
                    self.update()
                return slot

            anim.valueChanged.connect(make_slot(index))
            self._anims_by_index[index] = anim

        anim.stop()
        anim.setStartValue(self._progresses[index])
        anim.setEndValue(float(target))
        anim.start()


# ==================== 可动画面板 ====================
class SidePanel(QWidget):
    clicked = Signal()

    def __init__(self, words, colors, font_family,
                 hover_words=None, final_words=None,
                 clickable=True, parent=None):
        super().__init__(parent)
        self.c1, self.c2, self.c3 = (QColor(c) for c in colors)
        self._words = list(words)
        self._hover_words = list(hover_words) if hover_words else None
        self._final_words = list(final_words) if final_words else None
        self._font_family = font_family
        self._clickable = clickable

        self._hover = 0.0
        self._fill = 0.0
        self._text_progress = 0.0
        self._left_align = 0.0
        self._swap_progress = 0.0
        self._frozen_px = None

        self.setCursor(Qt.PointingHandCursor if clickable else Qt.ArrowCursor)
        self.setFocusPolicy(Qt.StrongFocus)

        self._anim = QPropertyAnimation(self, b"hover", self)
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def _get_hover(self): return self._hover
    def _set_hover(self, v): self._hover = float(v); self.update()
    hover = Property(float, _get_hover, _set_hover)

    def _get_fill(self): return self._fill
    def _set_fill(self, v): self._fill = float(v); self.update()
    fill = Property(float, _get_fill, _set_fill)

    def _get_text_progress(self): return self._text_progress
    def _set_text_progress(self, v): self._text_progress = float(v); self.update()
    textProgress = Property(float, _get_text_progress, _set_text_progress)

    def _get_left_align(self): return self._left_align
    def _set_left_align(self, v): self._left_align = float(v); self.update()
    leftAlign = Property(float, _get_left_align, _set_left_align)

    def _get_swap(self): return self._swap_progress
    def _set_swap(self, v): self._swap_progress = float(v); self.update()
    swapProgress = Property(float, _get_swap, _set_swap)

    def freeze_font_size(self):
        self._frozen_px = self._calc_font_px(
            self.width(), self.height(), len(self._words)
        )

    def unfreeze_font_size(self):
        self._frozen_px = None
        self.update()

    def _calc_font_px(self, w, h, n):
        if self._frozen_px is not None:
            return self._frozen_px
        if n <= 0:
            return 20
        px_by_w = int(min(52, max(16, w * 0.09)))
        avail_h = h - 64
        if avail_h > 0:
            px_by_h = int(avail_h / n * 0.9)
            return max(12, min(px_by_w, px_by_h))
        return px_by_w

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.setClipRect(self.rect())

        w, h = self.width(), self.height()

        grad = QRadialGradient(QPointF(w * 0.32, h * 0.24), max(w, h) * 0.95)
        grad.setColorAt(0.00, self.c1)
        grad.setColorAt(0.46, self.c2)
        grad.setColorAt(1.00, self.c3)
        p.fillRect(self.rect(), grad)

        if self._hover > 0.001:
            p.fillRect(self.rect(),
                       QColor(255, 255, 255, int(30 * self._hover)))

        if self._fill > 0.001:
            white_top = int(round(h * 0.15))
            final_wh = h - white_top
            wh = final_wh * self._fill
            p.fillRect(QRectF(0, h - wh, w, wh), QColor(255, 255, 255))

        self._draw_text(p, w, h)
        p.setClipping(False)
        p.end()

    def _draw_text(self, p, w, h):
        if not self._words:
            return

        display_words = self._words
        if (self._hover_words is not None
                and self.underMouse()
                and self._swap_progress < 0.01):
            display_words = self._hover_words

        n = len(display_words)
        px = self._calc_font_px(w, h, n)
        f = QFont(self._font_family)
        f.setWeight(QFont.Bold)
        f.setPixelSize(px)
        p.setFont(f)
        fm = p.fontMetrics()
        line_h = fm.lineSpacing()
        total_h = line_h * n
        normal_top = h / 2 - total_h / 2

        white_top = int(round(h * 0.15))

        dark = max(0.0, (self._fill - 0.5) * 2)
        v = int(255 * (1 - dark * 0.88))
        base = QColor(v, v, v)

        t = self._text_progress
        la = self._left_align

        if self._final_words is None:
            kits_idx = 2 if n > 2 else n - 1
            kits_line_top = normal_top + kits_idx * line_h
            target_baseline = white_top - fm.descent() - 12
            target_baseline = max(target_baseline, fm.ascent() + 4)
            y_offset = (target_baseline - (kits_line_top + fm.ascent())) * t

            for i, word in enumerate(display_words):
                a = 255 if i == kits_idx else int(255 * (1 - t))
                if a <= 0:
                    continue
                tw = fm.horizontalAdvance(word)
                normal_x = (w - tw) / 2
                if i == kits_idx:
                    x = normal_x + (32 - normal_x) * la
                else:
                    x = normal_x
                y = normal_top + i * line_h + y_offset + fm.ascent()
                c = QColor(255, 255, 255) if i == kits_idx else QColor(base)
                c.setAlpha(a)
                p.setPen(c)
                p.drawText(QPointF(x, y), word)
        else:
            orig_alpha = 1.0 - self._swap_progress
            if orig_alpha > 0.01:
                a = int(255 * orig_alpha)
                for i, word in enumerate(display_words):
                    tw = fm.horizontalAdvance(word)
                    x = (w - tw) / 2
                    y = normal_top + i * line_h + fm.ascent()
                    c = QColor(base)
                    c.setAlpha(a)
                    p.setPen(c)
                    p.drawText(QPointF(x, y), word)

            if self._swap_progress > 0.01:
                fw = self._final_words
                n2 = len(fw)
                max_px_h = int((h - 80) / n2 * 0.85) if n2 else 20
                max_px_w = int(w * 0.5)
                px2 = max(10, min(28, max_px_h, max_px_w))

                f2 = QFont(self._font_family)
                f2.setWeight(QFont.Bold)
                f2.setPixelSize(px2)
                p.setFont(f2)
                fm2 = p.fontMetrics()
                lh2 = fm2.lineSpacing()
                total_h2 = lh2 * n2
                top2 = h / 2 - total_h2 / 2
                a2 = int(255 * self._swap_progress)

                for i, word in enumerate(fw):
                    tw2 = fm2.horizontalAdvance(word)
                    x2 = (w - tw2) / 2
                    y2 = top2 + i * lh2 + fm2.ascent()
                    c2 = QColor(base)
                    c2.setAlpha(a2)
                    p.setPen(c2)
                    p.drawText(QPointF(x2, y2), word)

    def enterEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self._hover)
        self._anim.setEndValue(1.0)
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self._hover)
        self._anim.setEndValue(0.0)
        self._anim.start()
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._clickable and event.button() == Qt.LeftButton:
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit()
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if not self._clickable:
            super().keyPressEvent(event)
            return
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):
            self.clicked.emit()
        else:
            super().keyPressEvent(event)


# ==================== Character Manager ====================

class ActionIconButton(QPushButton):
    """左侧边栏功能按钮：加号 / 笔 / 垃圾桶，自绘图标"""

    def __init__(self, icon_type, tooltip, parent=None):
        super().__init__(parent)
        self._icon_type = icon_type
        self.setFixedSize(40, 40)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(tooltip)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 16);
            }
            QPushButton:pressed {
                background: rgba(0, 0, 0, 32);
            }
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor("#1a1d24"))
        pen.setWidthF(1.8)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)

        size = 18.0
        cx, cy = self.width() / 2, self.height() / 2
        r = QRectF(cx - size / 2, cy - size / 2, size, size)

        if self._icon_type == "add":
            self._draw_add(p, r)
        elif self._icon_type == "edit":
            self._draw_edit(p, r)
        elif self._icon_type == "delete":
            self._draw_delete(p, r)
        p.end()

    def _draw_add(self, p, r):
        cx, cy = r.center().x(), r.center().y()
        half = r.width() / 2
        p.drawLine(QPointF(cx - half, cy), QPointF(cx + half, cy))
        p.drawLine(QPointF(cx, cy - half), QPointF(cx, cy + half))

    def _draw_edit(self, p, r):
        x, y, w, h = r.x(), r.y(), r.width(), r.height()
        p.drawLine(QPointF(x + w * 0.15, y + h * 0.80),
                   QPointF(x + w * 0.72, y + h * 0.23))
        p.drawLine(QPointF(x + w * 0.15, y + h * 0.80),
                   QPointF(x + w * 0.05, y + h * 0.95))
        p.drawLine(QPointF(x + w * 0.05, y + h * 0.95),
                   QPointF(x + w * 0.22, y + h * 0.87))
        p.drawLine(QPointF(x + w * 0.72, y + h * 0.23),
                   QPointF(x + w * 0.85, y + h * 0.10))
        p.drawLine(QPointF(x + w * 0.72, y + h * 0.23),
                   QPointF(x + w * 0.75, y + h * 0.38))
        p.drawLine(QPointF(x + w * 0.85, y + h * 0.10),
                   QPointF(x + w * 0.88, y + h * 0.25))
        p.drawLine(QPointF(x + w * 0.05, y + h * 1.02),
                   QPointF(x + w * 0.85, y + h * 1.02))

    def _draw_delete(self, p, r):
        x, y, w, h = r.x(), r.y(), r.width(), r.height()
        p.drawLine(QPointF(x + w * 0.32, y + h * 0.12),
                   QPointF(x + w * 0.68, y + h * 0.12))
        p.drawLine(QPointF(x + w * 0.10, y + h * 0.22),
                   QPointF(x + w * 0.90, y + h * 0.22))
        p.drawLine(QPointF(x + w * 0.22, y + h * 0.22),
                   QPointF(x + w * 0.28, y + h * 0.92))
        p.drawLine(QPointF(x + w * 0.78, y + h * 0.22),
                   QPointF(x + w * 0.72, y + h * 0.92))
        p.drawLine(QPointF(x + w * 0.28, y + h * 0.92),
                   QPointF(x + w * 0.72, y + h * 0.92))
        p.drawLine(QPointF(x + w * 0.42, y + h * 0.35),
                   QPointF(x + w * 0.44, y + h * 0.80))
        p.drawLine(QPointF(x + w * 0.58, y + h * 0.35),
                   QPointF(x + w * 0.56, y + h * 0.80))


class CharacterListWidget(QWidget):
    """自绘角色列表，每行一张卡片，选中/悬停高亮"""

    itemClicked = Signal(int)

    def __init__(self, font_family, parent=None):
        super().__init__(parent)
        self._font_family = font_family
        self._characters = []
        self._current = -1
        self._hover = -1
        self._item_h = 64
        self._gap = 8
        self.setMouseTracking(True)
        self.setStyleSheet("background: transparent;")

    def set_characters(self, characters):
        self._characters = characters
        if self._current >= len(characters):
            self._current = len(characters) - 1
        self._update_min_size()
        self.update()

    def _content_height(self):
        n = len(self._characters)
        return n * self._item_h + max(0, n - 1) * self._gap

    def sizeHint(self):
        return QSize(200, max(self._content_height(), 100))

    def _update_min_size(self):
        h = max(self._content_height(), 100)
        self.setMinimumHeight(h)
        self.updateGeometry()

    def current_index(self):
        return self._current

    def set_current(self, idx):
        if -1 <= idx < len(self._characters):
            self._current = idx
            self.update()

    def _layout_rects(self):
        rects = []
        y = 0
        for _ in self._characters:
            rects.append(QRect(0, y, self.width(), self._item_h))
            y += self._item_h + self._gap
        return rects

    def _index_at(self, pos):
        for i, rect in enumerate(self._layout_rects()):
            if rect.contains(pos):
                return i
        return -1

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)

        for i, rect in enumerate(self._layout_rects()):
            char = self._characters[i]
            selected = (i == self._current)
            hovered = (i == self._hover)
            tags = char.get("tags", []) or []

            if selected:
                bg = QColor("#1a1d24")
                name_color = QColor(255, 255, 255)
                camp_color = QColor(170, 175, 185)
            elif hovered:
                bg = QColor(0, 0, 0, 16)
                name_color = QColor("#1a1d24")
                camp_color = QColor(100, 100, 110)
            else:
                bg = QColor(0, 0, 0, 6)
                name_color = QColor("#1a1d24")
                camp_color = QColor(100, 100, 110)

            path = QPainterPath()
            path.addRoundedRect(QRectF(rect), 10, 10)
            p.fillPath(path, bg)

            f = QFont(self._font_family)
            f.setWeight(QFont.Bold)
            f.setPixelSize(15)
            fm_name = QFontMetrics(f)
            name_rect = rect.adjusted(16, 8, -16, -rect.height() // 2 + 4)
            elided = fm_name.elidedText(
                char["name"], Qt.ElideRight, max(0, name_rect.width())
            )
            p.setFont(f)
            p.setPen(name_color)
            p.drawText(name_rect, Qt.AlignLeft | Qt.AlignVCenter, elided)

            f2 = QFont(self._font_family)
            f2.setPixelSize(12)
            fm_camp = QFontMetrics(f2)
            camp_rect = rect.adjusted(16, rect.height() // 2, -16, -8)

            dot_size = 6
            dot_gap = 3
            max_dots = 6
            show_tags = tags[:max_dots]
            dots_w = 0
            if show_tags:
                dots_w = (
                    len(show_tags) * dot_size
                    + (len(show_tags) - 1) * dot_gap
                )

            camp_avail_w = max(
                0, camp_rect.width() - (dots_w + 12 if dots_w else 0)
            )
            camp_text = fm_camp.elidedText(
                char["camp"], Qt.ElideRight, camp_avail_w
            )
            p.setFont(f2)
            p.setPen(camp_color)
            p.drawText(camp_rect, Qt.AlignLeft | Qt.AlignVCenter, camp_text)

            if show_tags:
                x = rect.right() - 16 - dots_w
                y = camp_rect.center().y() - dot_size // 2
                p.setPen(Qt.NoPen)
                for tag_id in show_tags:
                    color = QColor(TAG_COLORS.get(tag_id, "#999999"))
                    p.setBrush(color)
                    p.setPen(QPen(QColor(255, 255, 255, 120), 1))
                    p.drawEllipse(x, y, dot_size, dot_size)
                    x += dot_size + dot_gap

        p.end()

    def mouseMoveEvent(self, event):
        idx = self._index_at(event.position().toPoint())
        if idx != self._hover:
            self._hover = idx
            self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hover = -1
        self.update()
        super().leaveEvent(event)

    def wheelEvent(self, event):
        parent = self.parentWidget()
        while parent is not None and not isinstance(parent, QScrollArea):
            parent = parent.parentWidget()

        if parent is not None:
            bar = parent.verticalScrollBar()
            if bar is not None and bar.maximum() > 0:
                delta = event.angleDelta().y()
                bar.setValue(bar.value() - delta // 2)
                event.accept()
                return

        super().wheelEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            idx = self._index_at(event.position().toPoint())
            if 0 <= idx < len(self._characters):
                if idx != self._current:
                    self._current = idx
                    self.update()
                self.itemClicked.emit(idx)
        super().mouseReleaseEvent(event)


class CharacterDetailPanel(QWidget):
    """右侧角色详情（描述区可滚动，支持标签管理）"""

    tags_changed = Signal(list)

    def __init__(self, font_family, parent=None):
        super().__init__(parent)
        self._font_family = font_family
        self._current_char = None
        self._tags = []
        self.setStyleSheet("background: transparent;")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(32, 24, 32, 24)
        lay.setSpacing(8)

        self._title = QLabel()
        self._title.setWordWrap(True)
        self._title.setMinimumWidth(0)
        self._title.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Preferred
        )
        self._title.setStyleSheet(
            "color: #1a1d24; font-size: 28px; font-weight: bold;"
            " background: transparent;"
        )

        self._camp = QLabel()
        self._camp.setMinimumWidth(0)
        self._camp.setWordWrap(True)
        self._camp.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Preferred
        )
        self._camp.setStyleSheet(
            "color: #909098; font-size: 13px; background: transparent;"
        )

        tags_row = QHBoxLayout()
        tags_row.setSpacing(6)

        self._tags_area = QWidget()
        self._tags_area.setStyleSheet("background: transparent;")
        self._tags_area.setMinimumWidth(0)
        self._tags_area.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Preferred
        )
        self._tags_layout = FlowLayout(
            self._tags_area, margin=0, hspacing=6, vspacing=6
        )

        self._add_tag_btn = QPushButton("+")
        self._add_tag_btn.setFixedSize(24, 24)
        self._add_tag_btn.setCursor(Qt.PointingHandCursor)
        self._add_tag_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 0, 0, 8);
                border: 1px dashed rgba(0, 0, 0, 40);
                border-radius: 12px;
                color: #909098;
                font-size: 16px;
                font-weight: bold;
                padding-bottom: 2px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 16);
                border-color: rgba(0, 0, 0, 70);
            }
        """)
        self._add_tag_btn.clicked.connect(self._show_tag_menu)

        tags_row.addWidget(self._tags_area, 1)
        tags_row.addWidget(self._add_tag_btn)

        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(0, 0, 0, 20);")

        self._desc = QTextBrowser()
        self._desc.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._desc.setLineWrapMode(QTextEdit.WidgetWidth)
        self._desc.setMinimumWidth(0)
        self._desc.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Expanding
        )
        self._desc.setOpenExternalLinks(False)
        self._desc.setFrameShape(QFrame.NoFrame)
        self._desc.setStyleSheet(f"""
            QTextBrowser {{
                background: transparent;
                border: none;
                color: #3a3d44;
                font-family: "{font_family}";
                font-size: 15px;
            }}
            QTextBrowser QScrollBar:vertical {{
                background: transparent;
                width: 8px;
                margin: 4px 2px 4px 0px;
                border-radius: 4px;
            }}
            QTextBrowser QScrollBar::handle:vertical {{
                background: rgba(0, 0, 0, 45);
                border-radius: 4px;
                min-height: 24px;
            }}
            QTextBrowser QScrollBar::handle:vertical:hover {{
                background: rgba(0, 0, 0, 85);
            }}
            QTextBrowser QScrollBar::add-line:vertical,
            QTextBrowser QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            QTextBrowser QScrollBar::add-page:vertical,
            QTextBrowser QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
            QTextBrowser QScrollBar:horizontal {{
                height: 0px;
                background: transparent;
            }}
        """)

        lay.addWidget(self._title)
        lay.addWidget(self._camp)
        lay.addLayout(tags_row)
        lay.addSpacing(8)
        lay.addWidget(divider)
        lay.addSpacing(8)
        lay.addWidget(self._desc, 1)

    def set_character(self, char):
        self._current_char = char
        if char is None:
            self._tags = []
            self._title.setText(tr("no_character_title"))
            self._camp.setText("")
            self._desc.setPlainText(tr("no_character_desc"))
        else:
            self._tags = list(char.get("tags", []))
            self._title.setText(char["name"])
            self._camp.setText(f"{tr('camp_label')}  ·  {char['camp']}")
            self._desc.setPlainText(char.get("desc", ""))
        self._rebuild_tags()

    def _rebuild_tags(self):
        while self._tags_layout.count():
            item = self._tags_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        for tag_id in self._tags:
            self._tags_layout.addWidget(self._make_tag_chip(tag_id))

        self._tags_area.updateGeometry()

    def _make_tag_chip(self, tag_id):
        color = QColor(TAG_COLORS.get(tag_id, "#999999"))
        label = QLabel(tag_name(tag_id))
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        label.setStyleSheet(f"""
            QLabel {{
                background: rgba({color.red()}, {color.green()}, {color.blue()}, 40);
                color: {color.name()};
                border-radius: 10px;
                padding: 2px 10px;
                font-size: 12px;
                font-weight: bold;
            }}
        """)
        return label

    def _show_tag_menu(self):
        if self._current_char is None:
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #ffffff;
                border: 1px solid rgba(0, 0, 0, 30);
                border-radius: 8px;
                padding: 6px;
            }
            QMenu::item {
                padding: 6px 24px 6px 12px;
                border-radius: 4px;
                color: #1a1d24;
            }
            QMenu::item:selected {
                background: rgba(0, 0, 0, 15);
            }
            QMenu::indicator {
                width: 14px;
                height: 14px;
            }
        """)

        for tag in TAG_DEFS:
            tid = tag["id"]
            action = menu.addAction(tag_name(tid))
            action.setCheckable(True)
            action.setChecked(tid in self._tags)
            action.triggered.connect(
                lambda checked, t=tid: self._toggle_tag(t, checked)
            )

        menu.exec(self._add_tag_btn.mapToGlobal(
            QPoint(0, self._add_tag_btn.height())
        ))

    def _toggle_tag(self, tag_id, checked):
        if self._current_char is None:
            return
        if checked:
            if tag_id not in self._tags:
                self._tags.append(tag_id)
        else:
            if tag_id in self._tags:
                self._tags.remove(tag_id)
        self._current_char["tags"] = list(self._tags)
        self._rebuild_tags()
        self.tags_changed.emit(self._tags)


class CharacterManagerPage(QWidget):
    """CHA Tab：左右栏宽度恒为 2:3，内容在各自栏内换行/滚动"""

    DIVIDER_W = 1

    def __init__(self, font_family, parent=None, characters=None):
        super().__init__(parent)
        self._font_family = font_family
        self.setStyleSheet("background: transparent;")
        self.setMinimumWidth(0)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)

        if characters is not None:
            self._characters = characters
        else:
            self._characters = [
                {"name": "狼人", "camp": "狼人阵营",
                 "desc": "每晚与同伴共同袭击一名玩家。狼人阵营的核心角色，"
                         "需要在白天伪装成好人。",
                 "tags": ["attack", "night", "open_eye"]},
                {"name": "村民", "camp": "好人阵营",
                 "desc": "没有特殊能力的普通村民。依靠推理、发言和投票"
                         "帮助好人阵营找出狼人。",
                 "tags": ["close_eye", "day"]},
                {"name": "预言家", "camp": "好人阵营",
                 "desc": "每晚可以查验一名玩家的阵营。是好人阵营最重要的"
                         "信息来源之一。",
                 "tags": ["info", "night", "open_eye"]},
                {"name": "女巫", "camp": "好人阵营",
                 "desc": "拥有一瓶解药和一瓶毒药。解药可以救活夜晚被袭击的"
                         "玩家，毒药可以毒杀一名玩家。",
                 "tags": ["heal", "attack", "night", "open_eye"]},
                {"name": "猎人", "camp": "好人阵营",
                 "desc": "死亡时可以开枪带走一名玩家。即使被狼人袭击或被"
                         "投票出局也能反击。",
                 "tags": ["attack", "day"]},
                {"name": "守卫", "camp": "好人阵营",
                 "desc": "每晚可以守护一名玩家，使其当晚不会被狼人袭击。"
                         "不能连续两晚守护同一名玩家。",
                 "tags": ["protect", "night", "open_eye"]},
                {"name": "白痴", "camp": "好人阵营",
                 "desc": "被投票出局时可以翻牌，翻牌后不会被投死，但失去投票权。",
                 "tags": ["day"]},
                {"name": "骑士", "camp": "好人阵营",
                 "desc": "白天可以决斗一名玩家，若对方是狼人则对方出局，"
                         "否则骑士自己出局。",
                 "tags": ["attack", "day"]},
            ]
        self._next_id = 1

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._left_wrap = QWidget()
        self._left_wrap.setStyleSheet("background: transparent;")
        self._left_wrap.setMinimumWidth(0)
        self._left_wrap.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Preferred
        )
        left_layout = QHBoxLayout(self._left_wrap)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        left_bar = QWidget()
        left_bar.setFixedWidth(56)
        left_bar.setStyleSheet("background: transparent;")
        bar_lay = QVBoxLayout(left_bar)
        bar_lay.setContentsMargins(8, 12, 8, 12)
        bar_lay.setSpacing(6)

        self._btn_add = ActionIconButton("add", tr("action_add"))
        self._btn_edit = ActionIconButton("edit", tr("action_edit"))
        self._btn_delete = ActionIconButton("delete", tr("action_delete"))
        self._btn_add.clicked.connect(self._on_add)
        self._btn_edit.clicked.connect(self._on_edit)
        self._btn_delete.clicked.connect(self._on_delete)

        bar_lay.addWidget(self._btn_add)
        bar_lay.addWidget(self._btn_edit)
        bar_lay.addWidget(self._btn_delete)
        bar_lay.addStretch(1)
        left_layout.addWidget(left_bar)

        list_wrap = QWidget()
        list_wrap.setStyleSheet("background: transparent;")
        list_wrap.setMinimumWidth(0)
        list_lay = QVBoxLayout(list_wrap)
        list_lay.setContentsMargins(4, 12, 8, 12)
        list_lay.setSpacing(0)

        self._list = CharacterListWidget(font_family)
        self._list.set_characters(self._characters)
        self._list.itemClicked.connect(self._on_select)
        self._list.setMinimumWidth(0)
        self._list.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Preferred
        )

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._scroll.setFrameShape(QScrollArea.NoFrame)
        self._scroll.setWidget(self._list)
        self._scroll.setStyleSheet(SCROLL_STYLE)
        self._scroll.setMinimumWidth(0)
        list_lay.addWidget(self._scroll, 1)
        left_layout.addWidget(list_wrap, 1)

        self._divider = QWidget()
        self._divider.setFixedWidth(self.DIVIDER_W)
        self._divider.setStyleSheet("background: rgba(0, 0, 0, 30);")

        self._detail = CharacterDetailPanel(font_family)
        self._detail.tags_changed.connect(self._on_tags_changed)
        self._detail.setMinimumWidth(0)
        self._detail.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Preferred
        )

        root.addWidget(self._left_wrap, 2)
        root.addWidget(self._divider, 0)
        root.addWidget(self._detail, 3)

        if self._characters:
            self._list.set_current(0)
            self._detail.set_character(self._characters[0])
        else:
            self._detail.set_character(None)

    def _on_select(self, idx):
        if 0 <= idx < len(self._characters):
            self._detail.set_character(self._characters[idx])

    def _on_add(self):
        dialog = CharacterEditorDialog(
            self, self._font_family, character=None, is_new=True
        )
        if dialog.exec() != QDialog.Accepted:
            return

        new_char = dialog.get_character()
        if new_char is None:
            return

        self._characters.append(new_char)
        self._list.set_characters(self._characters)
        new_idx = len(self._characters) - 1
        self._list.set_current(new_idx)
        self._detail.set_character(new_char)
        QTimer.singleShot(
            0,
            lambda: self._scroll.verticalScrollBar().setValue(
                self._scroll.verticalScrollBar().maximum()
            ),
        )

    def _on_edit(self):
        idx = self._list.current_index()
        if not (0 <= idx < len(self._characters)):
            return

        dialog = CharacterEditorDialog(
            self, self._font_family,
            character=self._characters[idx], is_new=False,
        )
        if dialog.exec() != QDialog.Accepted:
            return

        updated = dialog.get_character()
        if updated is None:
            return

        self._characters[idx] = updated
        self._list.set_characters(self._characters)
        self._list.set_current(idx)
        self._detail.set_character(updated)

    def _on_delete(self):
        idx = self._list.current_index()
        if not (0 <= idx < len(self._characters)):
            return

        char = self._characters[idx]
        ok = ConfirmDialog.ask(
            self,
            tr("delete_title"),
            tr("delete_message", name=char["name"]),
            confirm_text=tr("delete_confirm"),
            danger=True,
        )
        if not ok:
            return

        self._characters.pop(idx)
        self._list.set_characters(self._characters)
        if self._characters:
            new_idx = min(idx, len(self._characters) - 1)
            self._list.set_current(new_idx)
            self._detail.set_character(self._characters[new_idx])
        else:
            self._list.set_current(-1)
            self._detail.set_character(None)

    def _on_tags_changed(self, tags):
        self._list.update()

    def get_characters(self):
        return copy.deepcopy(self._characters)


# ==================== Kits 页面 ====================
class KitsPage(QWidget):
    back_requested = Signal()

    def __init__(self, font_family: str, parent=None, initial_characters=None):
        super().__init__(parent)
        self._font_family = font_family
        self.setStyleSheet("background: transparent;")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._top_spacer = QWidget(self)
        self._top_spacer.setStyleSheet("background: transparent;")
        root.addWidget(self._top_spacer)

        content_wrap = QWidget(self)
        content_wrap.setStyleSheet("background: transparent;")
        wrap_lay = QVBoxLayout(content_wrap)
        wrap_lay.setContentsMargins(20, 14, 20, 20)
        wrap_lay.setSpacing(8)

        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        self._back_btn = QPushButton("←", content_wrap)
        self._back_btn.setFixedSize(44, 44)
        self._back_btn.setCursor(Qt.PointingHandCursor)
        self._back_btn.setStyleSheet("""
            QPushButton {
                color: #1a1d24;
                background: rgba(0, 0, 0, 10);
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 22);
            }
            QPushButton:pressed {
                background: rgba(0, 0, 0, 32);
            }
        """)
        self._back_btn.clicked.connect(self.back_requested.emit)
        top_row.addWidget(self._back_btn)

        tabs = [
            {"short": tr("tab_character_short"),
             "full": tr("tab_character_full"), "disabled": False},
            {"short": tr("tab_config_short"),
             "full": tr("tab_config_full"), "disabled": False},
            {"short": tr("tab_logger_short"),
             "full": tr("tab_logger_full"), "disabled": False},
            {"short": tr("tab_runner_short"),
             "full": tr("tab_runner_full"), "disabled": False},
            {"short": tr("tab_more_short"), "full": "", "disabled": True},
        ]
        self.tabbar = TabBar(tabs, font_family, content_wrap)
        top_row.addWidget(self.tabbar, 1)

        wrap_lay.addLayout(top_row)

        divider = QWidget(content_wrap)
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(0, 0, 0, 30);")
        wrap_lay.addWidget(divider)

        spacer = QWidget(content_wrap)
        spacer.setFixedHeight(10)
        wrap_lay.addWidget(spacer)

        self.content = QStackedWidget(content_wrap)
        self.content.setStyleSheet("background: transparent;")
        wrap_lay.addWidget(self.content, 1)

        self.char_manager = CharacterManagerPage(
            font_family, self.content, characters=initial_characters
        )
        self.content.addWidget(self.char_manager)

        for key in ["tab_config_full", "tab_logger_full", "tab_runner_full"]:
            self.content.addWidget(self._placeholder(tr(key)))

        self.tabbar.tabChanged.connect(self.content.setCurrentIndex)

        root.addWidget(content_wrap, 1)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        h = self.height()
        white_top = int(round(h * 0.15))
        p.fillRect(QRect(0, white_top, self.width(), h - white_top),
                   QColor(255, 255, 255))
        p.end()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        h = self.height()
        self._top_spacer.setFixedHeight(int(round(h * 0.15)))

    def _placeholder(self, title: str) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignCenter)
        lay.setSpacing(8)

        t = QLabel(title, w)
        t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet("color: #1a1d24; font-size: 22px; font-weight: bold;"
                        " background: transparent;")

        s = QLabel(tr("coming_soon"), w)
        s.setAlignment(Qt.AlignCenter)
        s.setStyleSheet("color: #909098; font-size: 14px;"
                        " background: transparent;")

        lay.addWidget(t)
        lay.addWidget(s)
        return w


# ==================== 主舞台 ====================
class Stage(QWidget):
    def __init__(self, left: SidePanel, right: SidePanel,
                 font_family: str, parent=None):
        super().__init__(parent)
        self._left = left
        self._right = right
        self._font_family = font_family
        left.setParent(self)
        right.setParent(self)

        self._amp = QLabel("&", self)
        self._amp.setAlignment(Qt.AlignCenter)
        self._amp.setStyleSheet("background: transparent; color: #f7e8c9;")
        f = QFont(font_family)
        f.setPixelSize(26)
        f.setWeight(QFont.Bold)
        self._amp.setFont(f)
        self._amp.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self._amp_effect = QGraphicsOpacityEffect(self._amp)
        self._amp_effect.setOpacity(1.0)
        self._amp.setGraphicsEffect(self._amp_effect)

        self._animating = False
        self._expanded = False
        self._seq = None
        self._kits_page = None
        self._next_characters = None
        self._topbar = None
        self._footer = None
        self._footer_anim = None

        left.clicked.connect(self._on_left_clicked)

    def set_chrome(self, topbar, footer):
        self._topbar = topbar
        self._footer = footer

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._animating:
            return
        if self._expanded:
            self._layout_expanded()
        else:
            self._layout_normal()

    def _layout_normal(self):
        w, h = self.width(), self.height()
        top = BUTTON_MARGIN - TOPBAR_HEIGHT
        bottom = BUTTON_MARGIN - FOOTER_HEIGHT
        avail_h = h - top - bottom
        side_w = (w - BUTTON_MARGIN * 2 - AMP_SIZE - GAP_AROUND_AMP * 2) / 2

        self._left.setGeometry(
            BUTTON_MARGIN, int(top), int(side_w), int(avail_h)
        )
        self._amp.setGeometry(
            int(BUTTON_MARGIN + side_w + GAP_AROUND_AMP),
            int(top + (avail_h - AMP_SIZE) / 2),
            AMP_SIZE, AMP_SIZE,
        )
        self._right.setGeometry(
            int(BUTTON_MARGIN + side_w + GAP_AROUND_AMP * 2 + AMP_SIZE),
            int(top), int(side_w), int(avail_h),
        )

    def _layout_expanded(self):
        w, h = self.width(), self.height()
        top = BUTTON_MARGIN - TOPBAR_HEIGHT
        bottom = BUTTON_MARGIN - FOOTER_HEIGHT
        avail_h = h - top - bottom

        final_right_w = 80
        right_seam = 20
        gap = 20

        end_right_x = w - right_seam - final_right_w
        end_left_w = end_right_x - gap - BUTTON_MARGIN

        self._left.setGeometry(
            BUTTON_MARGIN, int(top), int(end_left_w), int(avail_h)
        )
        self._right.setGeometry(
            int(end_right_x), int(top), final_right_w, int(avail_h)
        )
        if self._kits_page is not None:
            self._kits_page.setGeometry(self._left.geometry())

    def _on_left_clicked(self):
        if self._animating:
            return
        if self._expanded:
            self._on_kits_back()
        else:
            self.play_expand()

    def play_expand(self):
        if self._footer is not None:
            self._footer.set_content_visible(False)
        self._animating = True
        self._left.freeze_font_size()
        self._right.freeze_font_size()

        w, h = self.width(), self.height()
        top = BUTTON_MARGIN - TOPBAR_HEIGHT
        bottom = BUTTON_MARGIN - FOOTER_HEIGHT
        avail_h = h - top - bottom

        final_right_w = 80
        right_seam = 20
        gap = 20

        start_left = self._left.geometry()
        start_right = self._right.geometry()

        end_right_x = w - right_seam - final_right_w
        end_left_w = end_right_x - gap - BUTTON_MARGIN
        end_left = QRect(BUTTON_MARGIN, int(top),
                         int(end_left_w), int(avail_h))
        end_right = QRect(int(end_right_x), int(top),
                          final_right_w, int(avail_h))

        p1 = QParallelAnimationGroup(self)

        a_fill = QPropertyAnimation(self._left, b"fill")
        a_fill.setStartValue(0.0)
        a_fill.setEndValue(1.0)
        a_fill.setDuration(1100)
        a_fill.setEasingCurve(QEasingCurve.InOutCubic)
        p1.addAnimation(a_fill)

        a_text = QPropertyAnimation(self._left, b"textProgress")
        a_text.setStartValue(0.0)
        a_text.setEndValue(1.0)
        a_text.setDuration(1100)
        a_text.setEasingCurve(QEasingCurve.InOutCubic)
        p1.addAnimation(a_text)

        a_align = QPropertyAnimation(self._left, b"leftAlign")
        a_align.setStartValue(0.0)
        a_align.setEndValue(1.0)
        a_align.setDuration(1100)
        a_align.setEasingCurve(QEasingCurve.InOutCubic)
        p1.addAnimation(a_align)

        p2 = QParallelAnimationGroup(self)

        a_geom_l = QPropertyAnimation(self._left, b"geometry")
        a_geom_l.setStartValue(start_left)
        a_geom_l.setEndValue(end_left)
        a_geom_l.setDuration(800)
        a_geom_l.setEasingCurve(QEasingCurve.InOutCubic)
        p2.addAnimation(a_geom_l)

        a_geom_r = QPropertyAnimation(self._right, b"geometry")
        a_geom_r.setStartValue(start_right)
        a_geom_r.setEndValue(end_right)
        a_geom_r.setDuration(800)
        a_geom_r.setEasingCurve(QEasingCurve.InOutCubic)
        p2.addAnimation(a_geom_r)

        a_swap = QPropertyAnimation(self._right, b"swapProgress")
        a_swap.setStartValue(0.0)
        a_swap.setEndValue(1.0)
        a_swap.setDuration(800)
        a_swap.setEasingCurve(QEasingCurve.InOutCubic)
        p2.addAnimation(a_swap)

        a_amp = QPropertyAnimation(self._amp_effect, b"opacity")
        a_amp.setStartValue(1.0)
        a_amp.setEndValue(0.0)
        a_amp.setDuration(500)
        p2.addAnimation(a_amp)

        self._seq = QSequentialAnimationGroup(self)
        self._seq.addAnimation(p1)
        self._seq.addAnimation(p2)
        self._seq.finished.connect(self._on_anim_done)
        self._seq.start()

    def _on_anim_done(self):
        self._animating = False
        self._expanded = True

        if self._kits_page is None:
            self._kits_page = KitsPage(
                self._font_family, self,
                initial_characters=self._next_characters,
            )
            self._kits_page.back_requested.connect(self._on_kits_back)

        self._kits_page.setGeometry(self._left.geometry())
        self._kits_page.show()
        self._kits_page.raise_()

    def _on_kits_back(self):
        if self._animating:
            return
        if self._kits_page is not None:
            self._kits_page.hide()
        self.play_collapse()

    def play_collapse(self):
        if self._footer is not None:
            self._footer.set_content_visible(True)
        self._animating = True
        self._left.freeze_font_size()
        self._right.freeze_font_size()

        w, h = self.width(), self.height()
        top = BUTTON_MARGIN - TOPBAR_HEIGHT
        bottom = BUTTON_MARGIN - FOOTER_HEIGHT
        avail_h = h - top - bottom
        side_w = (w - BUTTON_MARGIN * 2 - AMP_SIZE - GAP_AROUND_AMP * 2) / 2

        normal_left = QRect(BUTTON_MARGIN, int(top),
                            int(side_w), int(avail_h))
        normal_right_x = BUTTON_MARGIN + side_w + GAP_AROUND_AMP * 2 + AMP_SIZE
        normal_right = QRect(int(normal_right_x), int(top),
                             int(side_w), int(avail_h))

        p1 = QParallelAnimationGroup(self)

        a_geom_l = QPropertyAnimation(self._left, b"geometry")
        a_geom_l.setStartValue(self._left.geometry())
        a_geom_l.setEndValue(normal_left)
        a_geom_l.setDuration(800)
        a_geom_l.setEasingCurve(QEasingCurve.InOutCubic)
        p1.addAnimation(a_geom_l)

        a_geom_r = QPropertyAnimation(self._right, b"geometry")
        a_geom_r.setStartValue(self._right.geometry())
        a_geom_r.setEndValue(normal_right)
        a_geom_r.setDuration(800)
        a_geom_r.setEasingCurve(QEasingCurve.InOutCubic)
        p1.addAnimation(a_geom_r)

        a_swap = QPropertyAnimation(self._right, b"swapProgress")
        a_swap.setStartValue(1.0)
        a_swap.setEndValue(0.0)
        a_swap.setDuration(800)
        a_swap.setEasingCurve(QEasingCurve.InOutCubic)
        p1.addAnimation(a_swap)

        a_amp = QPropertyAnimation(self._amp_effect, b"opacity")
        a_amp.setStartValue(0.0)
        a_amp.setEndValue(1.0)
        a_amp.setDuration(500)
        p1.addAnimation(a_amp)

        p2 = QParallelAnimationGroup(self)

        a_fill = QPropertyAnimation(self._left, b"fill")
        a_fill.setStartValue(1.0)
        a_fill.setEndValue(0.0)
        a_fill.setDuration(1100)
        a_fill.setEasingCurve(QEasingCurve.InOutCubic)
        p2.addAnimation(a_fill)

        a_text = QPropertyAnimation(self._left, b"textProgress")
        a_text.setStartValue(1.0)
        a_text.setEndValue(0.0)
        a_text.setDuration(1100)
        a_text.setEasingCurve(QEasingCurve.InOutCubic)
        p2.addAnimation(a_text)

        a_align = QPropertyAnimation(self._left, b"leftAlign")
        a_align.setStartValue(1.0)
        a_align.setEndValue(0.0)
        a_align.setDuration(1100)
        a_align.setEasingCurve(QEasingCurve.InOutCubic)
        p2.addAnimation(a_align)

        self._seq = QSequentialAnimationGroup(self)
        self._seq.addAnimation(p1)
        self._seq.addAnimation(p2)
        self._seq.finished.connect(self._on_collapse_done)
        self._seq.start()

    def _on_collapse_done(self):
        self._animating = False
        self._expanded = False
        self._left.unfreeze_font_size()
        self._right.unfreeze_font_size()
        self._layout_normal()

    def reset(self):
        if self._seq is not None:
            self._seq.stop()
            self._seq = None
        self._left.setProperty("fill", 0.0)
        self._left.setProperty("textProgress", 0.0)
        self._left.setProperty("leftAlign", 0.0)
        self._right.setProperty("swapProgress", 0.0)
        self._amp_effect.setOpacity(1.0)
        if self._footer is not None:
            self._footer.set_content_visible(True)
        self._left.unfreeze_font_size()
        self._right.unfreeze_font_size()
        self._animating = False
        self._expanded = False
        self._layout_normal()

    def reset_kits_page(self):
        if self._kits_page is not None:
            self._kits_page.deleteLater()
            self._kits_page = None


# ==================== 顶栏 ====================
class TopBar(QWidget):
    def __init__(self, font_family: str, parent=None):
        super().__init__(parent)
        self.setFixedHeight(TOPBAR_HEIGHT)
        self._drag_offset = None

        grid = QGridLayout(self)
        grid.setContentsMargins(32, 0, 32, 0)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 0)
        grid.setColumnStretch(2, 1)

        left_box = QWidget(self)
        left_box.setStyleSheet("background: transparent;")
        left_lay = QHBoxLayout(left_box)
        left_lay.setContentsMargins(0, 0, 0, 0)
        left_lay.setSpacing(10)
        self.btn_about = IconButton("about", "关于")
        self.btn_account = IconButton("account", "账户")
        left_lay.addWidget(self.btn_about)
        left_lay.addWidget(self.btn_account)

        self.logo = QLabel("WPKO2", self)
        self.logo.setAlignment(Qt.AlignCenter)
        f = QFont(font_family)
        f.setPixelSize(30)
        f.setWeight(QFont.Bold)
        f.setLetterSpacing(QFont.AbsoluteSpacing, 6)
        self.logo.setFont(f)
        self.logo.setStyleSheet("color: #e6ecf4; background: transparent;")

        right_box = QWidget(self)
        right_box.setStyleSheet("background: transparent;")
        right_lay = QHBoxLayout(right_box)
        right_lay.setContentsMargins(0, 0, 0, 0)
        right_lay.setSpacing(10)
        self.btn_settings = IconButton("settings", "设置")
        self.btn_exit = IconButton("exit", "退出", danger=True)
        right_lay.addWidget(self.btn_settings)
        right_lay.addWidget(self.btn_exit)

        grid.addWidget(left_box, 0, 0, Qt.AlignLeft | Qt.AlignVCenter)
        grid.addWidget(self.logo, 0, 1, Qt.AlignCenter)
        grid.addWidget(right_box, 0, 2, Qt.AlignRight | Qt.AlignVCenter)

        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)

    def _get_opacity(self):
        return self._opacity_effect.opacity()

    def _set_opacity(self, v):
        self._opacity_effect.setOpacity(float(v))
        self.setAttribute(Qt.WA_TransparentForMouseEvents, float(v) < 0.05)

    opacity = Property(float, _get_opacity, _set_opacity)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_offset = (
                event.globalPosition().toPoint() - self.window().pos()
            )
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_offset is not None and (event.buttons() & Qt.LeftButton):
            self.window().move(
                event.globalPosition().toPoint() - self._drag_offset
            )
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_offset = None
        event.accept()


# ==================== 底栏 ====================
class Footer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(FOOTER_HEIGHT)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self._pulse = PulseLabel("Click to Choose", self)
        lay.addWidget(self._pulse)

        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)

    def _get_opacity(self):
        return self._opacity_effect.opacity()

    def _set_opacity(self, v):
        self._opacity_effect.setOpacity(float(v))
        self.setAttribute(Qt.WA_TransparentForMouseEvents, float(v) < 0.05)

    opacity = Property(float, _get_opacity, _set_opacity)

    def set_content_visible(self, visible):
        self.setVisible(bool(visible))


class PulseLabel(QLabel):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setStyleSheet("background: transparent;")

        f = self.font()
        f.setPixelSize(13)
        f.setLetterSpacing(QFont.AbsoluteSpacing, 3)
        self.setFont(f)

        self._alpha = 0.45

        self._anim = QPropertyAnimation(self, b"textAlpha", self)
        self._anim.setDuration(2600)
        self._anim.setKeyValueAt(0.0, 0.45)
        self._anim.setKeyValueAt(0.5, 1.00)
        self._anim.setKeyValueAt(1.0, 0.45)
        self._anim.setEasingCurve(QEasingCurve.InOutSine)
        self._anim.setLoopCount(-1)
        self._anim.start()

    def _get_text_alpha(self):
        return self._alpha

    def _set_text_alpha(self, v):
        self._alpha = float(v)
        self.update()

    textAlpha = Property(float, _get_text_alpha, _set_text_alpha)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.setOpacity(self._alpha)
        p.setPen(QColor("#c3ccd8"))
        p.setFont(self.font())
        p.drawText(self.rect(), Qt.AlignCenter, self.text())
        p.end()


# ==================== 设置悬浮窗 ====================
class SettingsPopup(QWidget):
    """点击设置按钮弹出的悬浮窗，目前仅支持语言切换"""

    languageChanged = Signal(str)

    def __init__(self, current_lang="zh", parent=None):
        super().__init__(parent, Qt.Popup)
        self._current = current_lang

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(280)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self._container = QFrame(self)
        self._container.setObjectName("popupContainer")
        self._container.setStyleSheet("""
            QFrame#popupContainer {
                background: #1e2430;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 12px;
            }
        """)
        outer.addWidget(self._container)

        lay = QVBoxLayout(self._container)
        lay.setContentsMargins(20, 16, 20, 18)
        lay.setSpacing(12)

        self._title = QLabel()
        self._title.setMinimumWidth(0)
        self._title.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Preferred
        )
        self._title.setStyleSheet(
            "color: #e6ecf4; font-size: 15px; font-weight: bold;"
            " background: transparent;"
        )

        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(255, 255, 255, 25);")

        self._lang_label = QLabel()
        self._lang_label.setStyleSheet(
            "color: #909098; font-size: 12px; background: transparent;"
        )

        lang_row = QHBoxLayout()
        lang_row.setSpacing(8)

        self._btn_zh = self._make_lang_btn("中文")
        self._btn_en = self._make_lang_btn("English")
        self._btn_zh.clicked.connect(lambda: self._set_lang("zh"))
        self._btn_en.clicked.connect(lambda: self._set_lang("en"))
        lang_row.addWidget(self._btn_zh)
        lang_row.addWidget(self._btn_en)

        lay.addWidget(self._title)
        lay.addWidget(divider)
        lay.addWidget(self._lang_label)
        lay.addLayout(lang_row)

        self._sync()
        self._retranslate()

    def _make_lang_btn(self, text):
        b = QPushButton(text)
        b.setCheckable(True)
        b.setFixedHeight(36)
        b.setCursor(Qt.PointingHandCursor)
        b.setMinimumWidth(96)
        b.setStyleSheet("""
            QPushButton {
                color: #cfd6e0;
                background: rgba(255, 255, 255, 15);
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 30);
            }
            QPushButton:checked {
                color: #ffffff;
                background: rgba(255, 255, 255, 50);
                border: 1px solid rgba(255, 255, 255, 80);
            }
        """)
        return b

    def _set_lang(self, code):
        if self._current == code:
            return
        self._current = code
        self._sync()
        self._retranslate()
        self.languageChanged.emit(code)
        self.close()

    def _sync(self):
        self._btn_zh.setChecked(self._current == "zh")
        self._btn_en.setChecked(self._current == "en")

    def _retranslate(self):
        self._title.setText(tr("settings_title"))
        self._lang_label.setText(tr("settings_language"))


# ==================== 叠层弹窗基类 ====================
class _ModalOverlay(QDialog):
    """所有叠层弹窗的公共基类：遮罩 + 居中圆角卡片"""

    CARD_WIDTH = 540

    def __init__(self, parent=None, card_width=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        if parent is not None:
            top = parent.window()
            self.setGeometry(top.geometry())
        if card_width is not None:
            self.CARD_WIDTH = card_width
        self._build_overlay()

    def _build_overlay(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        wrap = QWidget()
        wrap.setStyleSheet("background: transparent;")
        wrap_lay = QVBoxLayout(wrap)
        wrap_lay.setContentsMargins(24, 24, 24, 24)
        wrap_lay.addStretch(1)

        self._card = QFrame()
        self._card.setObjectName("overlayCard")
        self._card.setFixedWidth(self.CARD_WIDTH)
        self._card.setStyleSheet("""
            QFrame#overlayCard {
                background: #ffffff;
                border-radius: 16px;
            }
        """)
        wrap_lay.addWidget(self._card, 0, Qt.AlignCenter)
        wrap_lay.addStretch(1)
        outer.addWidget(wrap)

        shadow = QGraphicsDropShadowEffect(self._card)
        shadow.setBlurRadius(48)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(0, 0, 0, 90))
        self._card.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), QColor(0, 0, 0, 165))
        p.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos_in_card = self._card.mapFrom(self, event.position().toPoint())
            if not self._card.rect().contains(pos_in_card):
                self.reject()
                return
        super().mousePressEvent(event)


# ==================== 角色编辑浮窗 ====================
class CharacterEditorDialog(_ModalOverlay):
    """居中卡片式角色创建 / 编辑浮窗，支持名称、阵营、描述、标签"""

    def __init__(self, parent, font_family, character=None, is_new=True):
        self._font_family = font_family
        self._is_new = is_new
        self._character = dict(character) if character else {}
        self._selected_tags = set(self._character.get("tags", []))
        self._result = None
        super().__init__(parent, card_width=540)
        self._build_card_content()

    def _build_card_content(self):
        lay = QVBoxLayout(self._card)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(14)

        title_text = tr("editor_title_new") if self._is_new else tr("editor_title_edit")
        title = QLabel(title_text)
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #1a1d24;"
            " background: transparent;"
        )
        lay.addWidget(title)

        lay.addWidget(self._make_label(tr("editor_name_label")))
        self._name_edit = QLineEdit()
        self._name_edit.setText(self._character.get("name", ""))
        self._name_edit.setPlaceholderText(tr("editor_name_placeholder"))
        self._style_input(self._name_edit)
        lay.addWidget(self._name_edit)

        lay.addWidget(self._make_label(tr("editor_camp_label")))
        self._camp_edit = QLineEdit()
        self._camp_edit.setText(self._character.get("camp", ""))
        self._camp_edit.setPlaceholderText(tr("editor_camp_placeholder"))
        self._style_input(self._camp_edit)
        lay.addWidget(self._camp_edit)

        lay.addWidget(self._make_label(tr("editor_desc_label")))
        self._desc_edit = QTextEdit()
        self._desc_edit.setPlainText(self._character.get("desc", ""))
        self._desc_edit.setPlaceholderText(tr("editor_desc_placeholder"))
        self._desc_edit.setFixedHeight(110)
        self._desc_edit.setStyleSheet(f"""
            QTextEdit {{
                background: #f5f6f8;
                border: 1px solid rgba(0, 0, 0, 15);
                border-radius: 8px;
                padding: 8px 10px;
                font-family: "{self._font_family}";
                font-size: 14px;
                color: #1a1d24;
            }}
            QTextEdit:focus {{
                border-color: #5b8def;
                background: #ffffff;
            }}
        """)
        lay.addWidget(self._desc_edit)

        lay.addWidget(self._make_label(tr("editor_tags_label")))
        tags_grid = QGridLayout()
        tags_grid.setSpacing(8)
        self._tag_buttons = {}
        for i, tag in enumerate(TAG_DEFS):
            tid = tag["id"]
            btn = self._make_tag_button(tid)
            self._tag_buttons[tid] = btn
            tags_grid.addWidget(btn, i // 4, i % 4)
        lay.addLayout(tags_grid)

        lay.addSpacing(6)
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        btn_row.addStretch(1)

        cancel_btn = QPushButton(tr("editor_cancel"))
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setFixedHeight(38)
        cancel_btn.setMinimumWidth(88)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 0, 0, 6);
                border: none;
                border-radius: 8px;
                color: #1a1d24;
                font-size: 14px;
                padding: 0 18px;
            }
            QPushButton:hover { background: rgba(0, 0, 0, 12); }
            QPushButton:pressed { background: rgba(0, 0, 0, 20); }
        """)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton(tr("editor_save"))
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setFixedHeight(38)
        save_btn.setMinimumWidth(88)
        save_btn.setStyleSheet("""
            QPushButton {
                background: #1a1d24;
                border: none;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover { background: #2a2d34; }
            QPushButton:pressed { background: #0a0d14; }
        """)
        save_btn.clicked.connect(self._on_save)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(save_btn)
        lay.addLayout(btn_row)

    def _make_label(self, text):
        l = QLabel(text)
        l.setStyleSheet(
            "font-size: 13px; color: #6a6d74; font-weight: 600;"
            " background: transparent;"
        )
        return l

    def _style_input(self, w):
        w.setFixedHeight(38)
        w.setStyleSheet(f"""
            QLineEdit {{
                background: #f5f6f8;
                border: 1px solid rgba(0, 0, 0, 15);
                border-radius: 8px;
                padding: 0 12px;
                font-family: "{self._font_family}";
                font-size: 14px;
                color: #1a1d24;
            }}
            QLineEdit:focus {{
                border-color: #5b8def;
                background: #ffffff;
            }}
        """)

    def _make_tag_button(self, tag_id):
        color = QColor(TAG_COLORS.get(tag_id, "#999999"))
        r, g, b = color.red(), color.green(), color.blue()

        btn = QPushButton(tag_name(tag_id))
        btn.setCheckable(True)
        btn.setChecked(tag_id in self._selected_tags)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(30)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: #ffffff;
                border: 1px solid {color.name()};
                border-radius: 15px;
                color: {color.name()};
                font-size: 12px;
                font-weight: bold;
                padding: 0 12px;
            }}
            QPushButton:hover {{
                background: rgba({r}, {g}, {b}, 24);
            }}
            QPushButton:checked {{
                background: {color.name()};
                color: #ffffff;
            }}
        """)
        btn.toggled.connect(
            lambda checked, t=tag_id: self._on_tag_toggled(t, checked)
        )
        return btn

    def _on_tag_toggled(self, tag_id, checked):
        if checked:
            self._selected_tags.add(tag_id)
        else:
            self._selected_tags.discard(tag_id)

    def _on_save(self):
        name = self._name_edit.text().strip()
        if not name:
            self._name_edit.setFocus()
            return

        self._result = {
            "name": name,
            "camp": self._camp_edit.text().strip() or tr("new_character_camp"),
            "desc": self._desc_edit.toPlainText().strip()
                    or tr("new_character_desc"),
            "tags": [t["id"] for t in TAG_DEFS
                     if t["id"] in self._selected_tags],
        }
        self.accept()

    def get_character(self):
        return self._result

    def showEvent(self, event):
        super().showEvent(event)
        self._name_edit.setFocus()


# ==================== 确认浮窗 ====================
class ConfirmDialog(_ModalOverlay):
    """叠层确认窗口：标题 / 消息 / 取消 / 确认（可设为危险色）"""

    def __init__(self, parent, title, message,
                 confirm_text=None, cancel_text=None, danger=False):
        self._title_text = title
        self._message_text = message
        self._confirm_text = confirm_text or tr("editor_save")
        self._cancel_text = cancel_text or tr("editor_cancel")
        self._danger = danger
        super().__init__(parent, card_width=420)
        self._build_card_content()

    def _build_card_content(self):
        lay = QVBoxLayout(self._card)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(14)

        title = QLabel(self._title_text)
        title.setWordWrap(True)
        title.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #1a1d24;"
            " background: transparent;"
        )
        lay.addWidget(title)

        message = QLabel(self._message_text)
        message.setWordWrap(True)
        message.setStyleSheet(
            "font-size: 14px; color: #5a5d64; background: transparent;"
        )
        lay.addWidget(message)

        lay.addSpacing(6)
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        btn_row.addStretch(1)

        cancel_btn = QPushButton(self._cancel_text)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setFixedHeight(38)
        cancel_btn.setMinimumWidth(88)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 0, 0, 6);
                border: none;
                border-radius: 8px;
                color: #1a1d24;
                font-size: 14px;
                padding: 0 18px;
            }
            QPushButton:hover { background: rgba(0, 0, 0, 12); }
            QPushButton:pressed { background: rgba(0, 0, 0, 20); }
        """)
        cancel_btn.clicked.connect(self.reject)

        confirm_btn = QPushButton(self._confirm_text)
        confirm_btn.setCursor(Qt.PointingHandCursor)
        confirm_btn.setFixedHeight(38)
        confirm_btn.setMinimumWidth(88)
        if self._danger:
            confirm_btn.setStyleSheet("""
                QPushButton {
                    background: #d13b3f;
                    border: none;
                    border-radius: 8px;
                    color: #ffffff;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 0 20px;
                }
                QPushButton:hover { background: #b32b30; }
                QPushButton:pressed { background: #8f1f24; }
            """)
        else:
            confirm_btn.setStyleSheet("""
                QPushButton {
                    background: #1a1d24;
                    border: none;
                    border-radius: 8px;
                    color: #ffffff;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 0 20px;
                }
                QPushButton:hover { background: #2a2d34; }
                QPushButton:pressed { background: #0a0d14; }
            """)
        confirm_btn.clicked.connect(self.accept)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(confirm_btn)
        lay.addLayout(btn_row)

    @staticmethod
    def ask(parent, title, message,
            confirm_text=None, cancel_text=None, danger=False):
        dlg = ConfirmDialog(
            parent, title, message,
            confirm_text=confirm_text,
            cancel_text=cancel_text,
            danger=danger,
        )
        return dlg.exec() == QDialog.Accepted

# ==================== 关于浮窗 ====================
class AboutDialog(_ModalOverlay):
    """关于窗口：改类属性即可更新内容"""

    APP_NAME = "WPKO2"
    APP_SUBTITLE = "Werewolves Personal Kits Only & Wolf People Kill Online"
    APP_VERSION = "b0.1"
    APP_AUTHOR = "True_white_"
    APP_REPO = "https://github.com/TROWTruewhite/WPKO2"
    APP_LICENSE = "MIT License"

    def __init__(self, parent, font_family):
        self._font_family = font_family
        super().__init__(parent, card_width=520)
        self._build_card_content()

    def _build_card_content(self):
        lay = QVBoxLayout(self._card)
        lay.setContentsMargins(32, 28, 32, 24)
        lay.setSpacing(16)

        # ---------- 标题 ----------
        title = QLabel(self.APP_NAME)
        f = QFont(self._font_family)
        f.setPixelSize(24)
        f.setWeight(QFont.Bold)
        f.setLetterSpacing(QFont.AbsoluteSpacing, 4)
        title.setFont(f)
        title.setStyleSheet("color: #1a1d24; background: transparent;")
        lay.addWidget(title)

        subtitle = QLabel(self.APP_SUBTITLE)
        subtitle.setStyleSheet(
            "color: #909098; font-size: 13px; background: transparent;"
        )
        lay.addWidget(subtitle)

        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(0, 0, 0, 20);")
        lay.addWidget(divider)

        # ---------- 正文 ----------
        body = QLabel()
        body.setWordWrap(True)
        body.setTextFormat(Qt.RichText)
        body.setTextInteractionFlags(Qt.TextBrowserInteraction)
        body.setOpenExternalLinks(True)
        body.setStyleSheet(
            "color: #3a3d44; font-size: 14px; line-height: 20px;"
            " background: transparent;"
        )
        body.setText(f"""
            <p>狼人杀工具与联机平台。</p>
            <p>
                版本：{self.APP_VERSION}<br>
                作者：{self.APP_AUTHOR}<br>
                仓库：<a href="https://{self.APP_REPO}">{self.APP_REPO}</a><br>
                协议：{self.APP_LICENSE}
            </p>
        """)
        lay.addWidget(body)

        # ---------- 底部按钮 ----------
        btn_row = QHBoxLayout()
        btn_row.addStretch(1)

        close_btn = QPushButton(tr("editor_cancel"))
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setFixedHeight(38)
        close_btn.setMinimumWidth(88)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #1a1d24;
                border: none;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover { background: #2a2d34; }
            QPushButton:pressed { background: #0a0d14; }
        """)
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        lay.addLayout(btn_row)

# ==================== 占位功能页 ====================
class PlaceholderPage(QWidget):
    back_requested = Signal()

    def __init__(self, title: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(40, 32, 40, 32)
        lay.setSpacing(16)

        top = QHBoxLayout()
        back = QPushButton("← 返回主界面", self)
        back.setCursor(Qt.PointingHandCursor)
        back.setStyleSheet(TOP_BTN_QSS)
        back.setFixedHeight(36)
        back.setMinimumWidth(130)
        back.clicked.connect(self.back_requested.emit)
        top.addWidget(back)
        top.addStretch(1)
        lay.addLayout(top)

        t = QLabel(title, self)
        t.setWordWrap(True)
        t.setStyleSheet("color:#f2f4f8; font-size:26px; font-weight:700;"
                        " background: transparent;")
        s = QLabel(subtitle or "功能开发中……", self)
        s.setStyleSheet("color:#8b97a8; font-size:14px; background: transparent;")

        lay.addSpacing(20)
        lay.addWidget(t)
        lay.addWidget(s)
        lay.addStretch(1)


# ==================== 主窗口 ====================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WPKO2")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.resize(1100, 680)
        self.setMinimumSize(900, 560)

        self._font_family = pick_font(FONT_CANDIDATES, "sans-serif")
        self.topbar = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.background = WindowBackground()
        outer.addWidget(self.background)

        inner = QVBoxLayout(self.background)
        inner.setContentsMargins(0, 0, 0, 0)
        inner.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: transparent;")
        inner.addWidget(self.stack)

        self.main_page = self._build_main_page()
        self.stack.addWidget(self.main_page)
        self._pages: dict[str, QWidget] = {}

    def _on_settings_clicked(self):
        if self.topbar is None:
            return
        popup = SettingsPopup(_current_lang, self)
        popup.languageChanged.connect(self._on_language_changed)

        btn = self.topbar.btn_settings
        btn_global = btn.mapToGlobal(QPoint(0, 0))
        popup_w = 280
        x = btn_global.x() + btn.width() - popup_w
        y = btn_global.y() + btn.height() + 6
        popup.move(x, y)
        popup.show()

    def _on_language_changed(self, code):
        if code == _current_lang:
            return

        if not ConfirmDialog.ask(
            self,
            tr("restart_title"),
            tr("restart_text"),
            confirm_text=tr("restart_confirm"),
        ):
            return

        cfg = load_config()
        cfg["language"] = code
        save_config(cfg)

        self._restart_app()

    def _restart_app(self):
        if getattr(sys, "frozen", False):
            QProcess.startDetached(sys.executable, sys.argv[1:])
        else:
            QProcess.startDetached(sys.executable, sys.argv)
        QApplication.quit()

    def _build_main_page(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background: transparent;")

        root = QVBoxLayout(page)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        topbar = TopBar(self._font_family, page)
        self.topbar = topbar
        root.addWidget(topbar)

        left = SidePanel(
            ["Werewolves", "Personal", "Kits", "Only"],
            ("#d13b3f", "#a81f28", "#6f0f16"),
            self._font_family,
        )
        right = SidePanel(
            ["Wolf", "People", "Kill", "Online"],
            ("#8fa4b8", "#64798e", "#3d4c5c"),
            self._font_family,
            hover_words=["正在开发"],
            final_words=["Kill", "正", "在", "开", "发"],
            clickable=False,
        )

        self.stage = Stage(left, right, self._font_family, page)
        root.addWidget(self.stage, 1)

        footer = Footer(page)
        root.addWidget(footer, 0)
        self.stage.set_chrome(topbar, footer)   # ← 加这一行

        topbar.btn_about.clicked.connect(self._on_about_clicked)
        topbar.btn_account.clicked.connect(
            lambda: self.open_page("account", "账户", "登录 / 注册 / 个人资料")
        )
        topbar.btn_settings.clicked.connect(self._on_settings_clicked)
        topbar.btn_exit.clicked.connect(self._quit)

        return page

    def open_page(self, key: str, title: str, subtitle: str = ""):
        page = self._pages.get(key)
        if page is None:
            page = PlaceholderPage(title, subtitle, self.stack)
            page.back_requested.connect(
                lambda: self.stack.setCurrentWidget(self.main_page)
            )
            self.stack.addWidget(page)
            self._pages[key] = page
        self.stack.setCurrentWidget(page)

    def _quit(self):
        if not ConfirmDialog.ask(
            self,
            tr("exit_title"),
            tr("exit_message"),
            confirm_text=tr("exit_confirm"),
            danger=True,
        ):
            return
        QApplication.quit()

    def _on_about_clicked(self):
        AboutDialog(self, self._font_family).exec()


# ==================== 入口 ====================
def main():
    app = QApplication(sys.argv)

    cfg = load_config()
    set_language(cfg.get("language", "zh"))

    ui_font = pick_font(FONT_CANDIDATES, "sans-serif")
    f = QFont(ui_font)
    f.setPixelSize(14)
    app.setFont(f)

    win = MainWindow()
    win.show()

    screen = app.primaryScreen().availableGeometry()
    win.move(screen.center().x() - win.width() // 2,
             screen.center().y() - win.height() // 2)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()