def get_size(l, w, h):
    area = 2 * (l * w + l * h + w * h)
    volume = l * w * h
    return [area, volume]
