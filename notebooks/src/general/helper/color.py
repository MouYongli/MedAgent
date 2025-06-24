import colorsys

def generate_color_variants(base_color_hex, n):
    """
    Generate `n` variants of a base color by adjusting brightness.
    """
    base_color_hex = base_color_hex.lstrip("#")
    r, g, b = [int(base_color_hex[i:i+2], 16)/255.0 for i in (0, 2, 4)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    color_variants = []
    steps = n + 1  # avoid full white or black
    for i in range(1, steps):
        li = 0.35 + (i / steps) * 0.4  # keep brightness in a good range
        ri, gi, bi = colorsys.hls_to_rgb(h, li, s)
        color_variants.append(f"rgb({int(ri * 255)}, {int(gi * 255)}, {int(bi * 255)})")
    return color_variants
