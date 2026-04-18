"""
Tạo Oculo.icns — icon macOS từ thiết kế favicon động (đôi mắt trên nền gradient xanh-tím)
"""
import math, os, struct, subprocess, tempfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    print("Cài PIL: pip install Pillow")
    raise


def draw_oculo_icon(size: int) -> Image.Image:
    S = size
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ── Nền gradient xanh → tím (giả lập bằng nhiều dải) ──
    c1 = (124, 159, 255)   # #7c9fff
    mid = (92, 108, 240)   # #5c6cf0
    c2 = (167, 139, 250)   # #a78bfa
    pad = int(S * 0.03)
    for i in range(S):
        t = i / (S - 1)
        if t < 0.42:
            tt = t / 0.42
            r = int(c1[0] + (mid[0] - c1[0]) * tt)
            g = int(c1[1] + (mid[1] - c1[1]) * tt)
            b = int(c1[2] + (mid[2] - c1[2]) * tt)
        else:
            tt = (t - 0.42) / 0.58
            r = int(mid[0] + (c2[0] - mid[0]) * tt)
            g = int(mid[1] + (c2[1] - mid[1]) * tt)
            b = int(mid[2] + (c2[2] - mid[2]) * tt)
        draw.line([(i, 0), (i, S - 1)], fill=(r, g, b, 255))

    # ── Mask hình tròn ──
    mask = Image.new("L", (S, S), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse([pad, pad, S - pad - 1, S - pad - 1], fill=255)
    img.putalpha(mask)

    # ── Viền mỏng trắng mờ ──
    border_img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(border_img)
    bw = max(1, int(S * 0.018))
    bdraw.ellipse([pad, pad, S - pad - 1, S - pad - 1],
                  outline=(255, 255, 255, 36), width=bw)
    img = Image.alpha_composite(img, border_img)

    # ── Tham số mắt ──
    W = S
    sc = W / 34.0
    eye_y = 17 * sc
    left_cx  = 10 * sc
    right_cx = 22 * sc
    r_scl   = 5.0 * sc
    r_iris  = 3.0 * sc
    r_pupil = 1.375 * sc

    def draw_eye(layer: Image.Image, cx: float, cy: float):
        d = ImageDraw.Draw(layer)

        # Sclera (trắng với gradient nhẹ)
        x0, y0 = cx - r_scl, cy - r_scl
        x1, y1 = cx + r_scl, cy + r_scl
        d.ellipse([x0, y0, x1, y1], fill=(240, 243, 251, 255))

        # Highlight sclera trên-trái
        hl_r = r_scl * 0.55
        d.ellipse([cx - r_scl * 0.18 - hl_r, cy - r_scl * 0.22 - hl_r,
                   cx - r_scl * 0.18 + hl_r, cy - r_scl * 0.22 + hl_r],
                  fill=(255, 255, 255, 200))

        # Iris (xanh)
        ix, iy = cx, cy  # nhìn thẳng
        d.ellipse([ix - r_iris, iy - r_iris, ix + r_iris, iy + r_iris],
                  fill=(107, 127, 255, 255))
        # Iris inner
        ir2 = r_iris * 0.6
        d.ellipse([ix - ir2, iy - ir2, ix + ir2, iy + ir2],
                  fill=(46, 56, 120, 255))

        # Pupil
        d.ellipse([ix - r_pupil, iy - r_pupil, ix + r_pupil, iy + r_pupil],
                  fill=(12, 14, 24, 255))

        # Catchlight
        cl_r = r_pupil * 0.38
        cl_x = ix + r_pupil * 0.28
        cl_y = iy - r_pupil * 0.32
        d.ellipse([cl_x - cl_r, cl_y - cl_r, cl_x + cl_r, cl_y + cl_r],
                  fill=(255, 255, 255, 210))

    eye_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw_eye(eye_layer, left_cx, eye_y)
    draw_eye(eye_layer, right_cx, eye_y)

    # Soft shadow dưới mắt
    shadow = eye_layer.filter(ImageFilter.GaussianBlur(radius=max(1, int(S * 0.025))))
    shadow_dark = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    for px in range(S):
        for py in range(S):
            a = shadow.getpixel((px, py))[3]
            if a > 0:
                shadow_dark.putpixel((px, py), (0, 0, 0, int(a * 0.35)))

    img = Image.alpha_composite(img, shadow_dark)
    img = Image.alpha_composite(img, eye_layer)

    # ── Gloss overlay (highlight trên-trái) ──
    gloss = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(gloss)
    gr = int(S * 0.38)
    gdraw.ellipse([int(S * 0.08), int(S * 0.06),
                   int(S * 0.08) + gr, int(S * 0.06) + gr],
                  fill=(255, 255, 255, 28))
    gloss = gloss.filter(ImageFilter.GaussianBlur(radius=max(1, int(S * 0.07))))
    img = Image.alpha_composite(img, gloss)

    return img


def make_icns(out_path: str):
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    icns_map = {
        16:   (b'icp4', b'ic11'),
        32:   (b'icp5', b'ic12'),
        64:   (b'icp6', None),
        128:  (b'ic07', b'ic13'),
        256:  (b'ic08', b'ic14'),
        512:  (b'ic09', None),
        1024: (b'ic10', None),
    }

    with tempfile.TemporaryDirectory() as tmp:
        iconset = os.path.join(tmp, "Oculo.iconset")
        os.makedirs(iconset)

        for sz in sizes:
            img = draw_oculo_icon(sz)
            img.save(os.path.join(iconset, f"icon_{sz}x{sz}.png"))
            if sz <= 512:
                img2 = draw_oculo_icon(sz * 2)
                img2.save(os.path.join(iconset, f"icon_{sz}x{sz}@2x.png"))

        # Dùng iconutil của macOS để tạo .icns chuẩn
        result = subprocess.run(
            ["iconutil", "-c", "icns", iconset, "-o", out_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"iconutil error: {result.stderr}")
            # Fallback: tạo thủ công
            _make_icns_manual(iconset, out_path)
        else:
            print(f"Icon tạo thành công: {out_path}")


def _make_icns_manual(iconset_dir: str, out_path: str):
    """Fallback nếu iconutil không có."""
    entries = []
    type_map = {
        "icon_16x16.png":    b"icp4",
        "icon_32x32.png":    b"icp5",
        "icon_128x128.png":  b"ic07",
        "icon_256x256.png":  b"ic08",
        "icon_512x512.png":  b"ic09",
        "icon_32x32@2x.png": b"ic11",
        "icon_64x64@2x.png": b"ic12",
        "icon_256x256@2x.png": b"ic13",
        "icon_512x512@2x.png": b"ic14",
        "icon_1024x1024.png":  b"ic10",
    }
    for fname, tag in type_map.items():
        fpath = os.path.join(iconset_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "rb") as f:
                data = f.read()
            entries.append((tag, data))

    total = 8  # header
    for tag, data in entries:
        total += 8 + len(data)

    with open(out_path, "wb") as f:
        f.write(b"icns")
        f.write(struct.pack(">I", total))
        for tag, data in entries:
            f.write(tag)
            f.write(struct.pack(">I", 8 + len(data)))
            f.write(data)
    print(f"Icon tạo thành công (manual): {out_path}")


if __name__ == "__main__":
    out = str(Path(__file__).parent / "Oculo.icns")
    make_icns(out)
    print(f"Saved: {out}")
