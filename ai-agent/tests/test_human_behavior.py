"""Unit tests for human behavior helpers (Bezier curve sanity)."""
import random

from tools.human_behavior import HumanMouse


def test_bezier_curve_endpoints_and_length():
    random.seed(42)
    start = (100.0, 200.0)
    end = (400.0, 300.0)
    pts = HumanMouse.bezier_curve(start, end, num_points=20)
    assert len(pts) == 21
    assert pts[0] == (int(start[0]), int(start[1]))
    assert pts[-1] == (int(end[0]), int(end[1]))


def test_bezier_curve_points_in_reasonable_bbox():
    random.seed(7)
    start = (50.0, 50.0)
    end = (550.0, 450.0)
    pts = HumanMouse.bezier_curve(start, end, num_points=40)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    # Curve stays in a loose bounding region (control points can wander slightly)
    assert min(xs) >= -200
    assert max(xs) <= 900
    assert min(ys) >= -200
    assert max(ys) <= 800


def test_easing_durations_match_segment_count():
    n = 15
    d = HumanMouse.easing_durations(n)
    assert len(d) == n
    assert all(x > 0 for x in d)
