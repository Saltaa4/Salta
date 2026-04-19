def move_ball(x, y, keys, step, width, height, radius):
    if keys[0] and x - step >= radius:  # LEFT
        x -= step
    if keys[1] and x + step <= width - radius:  # RIGHT
        x += step
    if keys[2] and y - step >= radius:  # UP
        y -= step
    if keys[3] and y + step <= height - radius:  # DOWN
        y += step

    return x, y