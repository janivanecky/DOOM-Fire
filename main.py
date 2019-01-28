import cv2
import numpy as np
import time

# Parameters.
WIDTH, HEIGHT = 100, 75
FPS = 24.0
DECAY = 0.06

# Set up image.
img = np.zeros((HEIGHT, WIDTH, 3))
img[-1, :, :] = 1.0

start = time.time()
while True:
    # To keep steady FPS we're going to sleep till next frame should be shown.
    end = time.time()
    dt = end - start
    time_to_next_frame = max(0, 1.0 / FPS - dt)
    time.sleep(time_to_next_frame)
    start = time.time()

    # Handle keyboard input.
    k = cv2.waitKey(1) & 0xEFFFFF
    if k == 27: # Esc
        break
    elif k == 32: # Space
        img[-1, :, :] = 1.0 - img[-1, :, :]  # Toggle bottom row on/off.

    # Update fire.
    for y in range(HEIGHT - 1):
        for x in range(WIDTH):
            src_y = min(y + np.random.randint(1, 3), HEIGHT - 1)
            src_x = min(max(x - np.random.randint(-1, 2), 0), WIDTH - 1)
            img[y, x, :] = img[src_y, src_x, :] - np.random.rand(3) * DECAY
    img = np.maximum(0, img)  # Remove negative values.

    # Show frame.
    img_show = cv2.resize(img, (WIDTH * 8, HEIGHT * 8), interpolation=cv2.INTER_NEAREST)
    cv2.imshow("Fire!", img_show)