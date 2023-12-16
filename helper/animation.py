import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


def main():
    circle = Circle(300, 300, 50)
    images = []
    for frame in range(360):
        img = update(frame, circle)
        images.append(img)
    images[0].save('circle.gif', save_all=True, append_images=images[1:], optimize=False, duration=20, loop=0)


def update(frame, circle):
    img = Image.new('RGB', (800, 600), (0, 0, 0))
    circle.x = 300 + 200 * np.cos(np.radians(frame))
    circle.y = 300 + 200 * np.sin(np.radians(frame))
    draw = ImageDraw.Draw(img)
    draw.ellipse((circle.x - circle.radius, circle.y - circle.radius, circle.x + circle.radius, circle.y + circle.radius), fill=(255, 255, 255))
    return img


if __name__ == '__main__':
    main()
