from PIL import Image


def create_gif(images, output_path):

    frames = []

    for img_path in images:

        img = Image.open(img_path)

        img = img.resize((600, 400))

        frames.append(img)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=500,
        loop=0
    )