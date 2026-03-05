from PIL import Image


CANVAS = (1800, 1200)


def compose_layout(images, output):

    canvas = Image.new("RGB", CANVAS, "white")

    grid_h = int(CANVAS[1] * 0.75)

    cell_w = CANVAS[0] // 3
    cell_h = grid_h // 2

    idx = 0

    for y in range(2):

        for x in range(3):

            if idx >= len(images):
                break

            img = Image.open(images[idx])

            img = img.resize((cell_w, cell_h))

            canvas.paste(img, (x * cell_w, y * cell_h))

            idx += 1

    canvas.save(output)