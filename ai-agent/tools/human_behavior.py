"""
Human-behavior simulation for sync Playwright (time-based delays, no asyncio.sleep in tools).
Tất cả delay đi qua HumanTiming — không gọi time.sleep trực tiếp từ browser.py cho pacing.
"""
from __future__ import annotations

import os
import random
import sys
import time
from typing import List, Tuple

_FAST_MODE: bool = os.getenv("BROWSER_FAST_MODE", "").lower() in ("1", "true", "yes")


class HumanTiming:
    """Mọi pacing/delay nên đi qua class này."""

    @staticmethod
    def _sleep_ms(ms: float) -> None:
        time.sleep(max(0.0, ms) / 1000.0)

    @staticmethod
    def think(min_ms: float = 200, max_ms: float = 800) -> None:
        if _FAST_MODE:
            HumanTiming._sleep_ms(min(50.0, min_ms * 0.1))
            return
        mid = (min_ms + max_ms) / 2
        sigma = (max_ms - min_ms) / 6
        delay = random.gauss(mid, sigma)
        delay = max(min_ms, min(max_ms, delay))
        HumanTiming._sleep_ms(delay)

    @staticmethod
    def read(text_length: int) -> None:
        base_ms = (text_length / 1300) * 60 * 1000
        actual = base_ms * random.uniform(0.7, 1.3)
        actual = max(500, min(5000, actual))
        HumanTiming._sleep_ms(actual)

    @staticmethod
    def between_actions() -> None:
        if _FAST_MODE:
            time.sleep(random.uniform(0.05, 0.15))
            return
        time.sleep(random.uniform(0.3, 1.2))

    @staticmethod
    def after_navigate() -> None:
        if _FAST_MODE:
            time.sleep(random.uniform(0.15, 0.35))
            return
        time.sleep(random.uniform(0.6, 1.2))

    @staticmethod
    def after_click() -> None:
        if _FAST_MODE:
            time.sleep(random.uniform(0.05, 0.12))
            return
        time.sleep(random.uniform(0.2, 0.5))

    @staticmethod
    def typing_delay(char: str) -> float:
        if char in " \n\t":
            base = random.uniform(80, 180)
        elif char in ".,;:!?":
            base = random.uniform(100, 200)
        elif char.isupper():
            base = random.uniform(60, 140)
        else:
            base = random.uniform(40, 120)
        if random.random() < 0.03:
            base += random.uniform(300, 800)
        return base / 1000.0


class HumanMouse:
    """Di chuyển chuột theo đường cong Bezier (sync page.mouse)."""

    _current_pos: Tuple[int, int] = (720, 450)

    @staticmethod
    def bezier_curve(
        start: Tuple[float, float],
        end: Tuple[float, float],
        num_points: int = 10,
    ) -> List[Tuple[int, int]]:
        x0, y0 = start
        x3, y3 = end
        offset_x = (x3 - x0) * random.uniform(0.2, 0.8)
        offset_y = (y3 - y0) * random.uniform(0.2, 0.8)
        x1 = x0 + offset_x + random.uniform(-50, 50)
        y1 = y0 + random.uniform(-30, 30)
        x2 = x0 + offset_x + random.uniform(-50, 50)
        y2 = y3 + random.uniform(-30, 30)
        points: List[Tuple[int, int]] = []
        for i in range(num_points + 1):
            t = i / num_points
            x = (
                (1 - t) ** 3 * x0
                + 3 * (1 - t) ** 2 * t * x1
                + 3 * (1 - t) * t**2 * x2
                + t**3 * x3
            )
            y = (
                (1 - t) ** 3 * y0
                + 3 * (1 - t) ** 2 * t * y1
                + 3 * (1 - t) * t**2 * y2
                + t**3 * y3
            )
            points.append((int(x), int(y)))
        return points

    @staticmethod
    def easing_durations(num_segments: int) -> List[float]:
        durations: List[float] = []
        n = max(1, num_segments)
        for i in range(num_segments):
            t = i / n
            if t < 0.2:
                speed = 0.3 + t * 3.5
            elif t > 0.8:
                speed = 0.3 + (1 - t) * 3.5
            else:
                speed = 1.0 + random.uniform(-0.2, 0.2)
            durations.append(max(0.005, 0.02 / speed))
        return durations

    @classmethod
    def move_to(cls, page, target_x: int, target_y: int) -> None:
        current = getattr(cls, "_current_pos", (720, 450))
        target_x += random.randint(-3, 3)
        target_y += random.randint(-3, 3)
        points = cls.bezier_curve(current, (float(target_x), float(target_y)))
        if len(points) < 2:
            cls._current_pos = (target_x, target_y)
            return
        durations = cls.easing_durations(len(points) - 1)
        for i in range(len(points) - 1):
            x, y = points[i + 1]
            page.mouse.move(x, y)
            time.sleep(durations[i])
        cls._current_pos = (target_x, target_y)

    @classmethod
    def click(cls, page, x: int, y: int, button: str = "left") -> None:
        if _FAST_MODE:
            cls.move_to(page, x, y)
            page.mouse.down(button=button)
            time.sleep(random.uniform(0.03, 0.07))
            page.mouse.up(button=button)
            return
        # Overshoot: land slightly past target, micro-correct back (human motor pattern)
        overshoot_x = x + int(random.gauss(0, 5))
        overshoot_y = y + int(random.gauss(0, 5))
        cls.move_to(page, overshoot_x, overshoot_y)
        if abs(overshoot_x - x) > 2 or abs(overshoot_y - y) > 2:
            time.sleep(random.uniform(0.04, 0.09))
            cls.move_to(page, x, y)
        time.sleep(random.uniform(0.05, 0.15))
        page.mouse.down(button=button)
        time.sleep(random.uniform(0.08, 0.25))
        page.mouse.up(button=button)

    @staticmethod
    def idle_movement(page, duration_sec: float = 2.0) -> None:
        if _FAST_MODE:
            return
        end = time.monotonic() + duration_sec
        x = random.randint(400, 1000)
        y = random.randint(200, 600)
        # Slow drift direction — simulates reading/idle cursor behavior
        drift_vx = random.uniform(-1.5, 1.5)
        drift_vy = random.uniform(-0.8, 0.8)
        while time.monotonic() < end:
            x = int(x + drift_vx + random.uniform(-4, 4))
            y = int(y + drift_vy + random.uniform(-3, 3))
            if x < 150 or x > 1300:
                drift_vx = -drift_vx
            if y < 120 or y > 780:
                drift_vy = -drift_vy
            x = max(150, min(1300, x))
            y = max(120, min(780, y))
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.08, 0.2))


class HumanKeyboard:
    """Gõ phím và scroll tự nhiên (sync)."""

    @classmethod
    def type_text(cls, page, selector: str, text: str, clear_first: bool = True) -> None:
        loc = page.locator(selector).first
        if _FAST_MODE:
            loc.click(timeout=10000)
            if clear_first:
                loc.fill("")
            loc.fill(text)
            time.sleep(random.uniform(0.05, 0.12))
            return
        loc.click(timeout=10000)
        time.sleep(random.uniform(0.1, 0.3))
        if clear_first:
            try:
                page.keyboard.press("ControlOrMeta+A")
            except Exception:
                mod = "Meta+A" if sys.platform == "darwin" else "Control+A"
                try:
                    page.keyboard.press(mod)
                except Exception:
                    pass
            time.sleep(random.uniform(0.05, 0.15))
            page.keyboard.press("Backspace")
        # Burst-pause pattern: type 3-7 words in a burst, then pause to "think"
        word_count = 0
        burst_limit = random.randint(3, 7)
        for char in text:
            if random.random() < 0.02 and char.isalpha():
                wrong = random.choice("qwertyuiopasdfghjklzxcvbnm")
                page.keyboard.press(wrong)
                time.sleep(random.uniform(0.1, 0.3))
                page.keyboard.press("Backspace")
                time.sleep(random.uniform(0.05, 0.15))
            page.keyboard.type(char, delay=0)
            time.sleep(HumanTiming.typing_delay(char))
            if char == " ":
                word_count += 1
                if word_count >= burst_limit:
                    time.sleep(random.uniform(0.18, 0.55))
                    word_count = 0
                    burst_limit = random.randint(3, 7)
        time.sleep(random.uniform(0.2, 0.5))

    @staticmethod
    def scroll_naturally(
        page,
        direction: str = "down",
        distance: int | None = None,
        steps: int | None = None,
    ) -> None:
        if distance is None:
            distance = random.randint(200, 600)
        if steps is None:
            steps = random.randint(4, 10)
        sign = -1 if direction == "up" else 1
        for i in range(steps):
            # Ease-out momentum: heavier chunks at start, lighter at end (deceleration feel)
            factor = (steps - i) / steps
            chunk = int((distance / steps) * factor * 1.8) + random.randint(-15, 15)
            chunk = max(8, chunk)
            page.mouse.wheel(0, sign * chunk)
            # Gap grows toward end: start fast, coast to stop
            delay = random.uniform(0.04, 0.09) + (i / steps) * 0.13
            time.sleep(delay)
