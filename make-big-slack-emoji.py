from PIL import Image
import argparse
BUCKET_SIZE = 128


def loopThroughPixels(file):
    im = Image.open(file)
    width, height = im.size
    print(width, height)
    whole_image = []
    for idx_x, x in enumerate(range(0, width, BUCKET_SIZE)):
        start_x = x
        end_x = x + BUCKET_SIZE - 1 if x + BUCKET_SIZE - 1 < width else width
        to_add = []
        for idx_y, y in enumerate(range(0, height, BUCKET_SIZE)):
            start_y = y
            end_y = y + BUCKET_SIZE - 1 if y + BUCKET_SIZE - 1 < height else height
            im.crop((start_x, start_y, end_x, end_y)).save(
                "{0}_{1}_{2}.png".format(file.replace(".png", ""), idx_x, idx_y))
            to_add.append("{0}_{1}_{2}".format(file.replace(".png", ""), idx_x, idx_y))
        whole_image.append(to_add)
    print_slack_images(file, width, height)


def print_slack_images(file, width, height):
    for idx_y, _ in enumerate(range(0, height, BUCKET_SIZE)):
        for idx_x, _ in enumerate(range(0, width, BUCKET_SIZE)):
            print(":{0}_{1}_{2}:".format(file.replace(".png", ""), idx_x, idx_y), end='')
        print("")


def main(args):
    loopThroughPixels(args.file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="The file to break into 128x128 images")
    args = parser.parse_args()
    main(args)
