from PIL import Image
import argparse
import os
BUCKET_SIZE = 128


def loopThroughPixels(file, output_dir):
    im = Image.open(file)
    width, height = im.size
    print(width, height)
    for idx_x, x in enumerate(range(0, width, BUCKET_SIZE)):
        start_x = x
        end_x = x + BUCKET_SIZE
        for idx_y, y in enumerate(range(0, height, BUCKET_SIZE)):
            start_y = y
            end_y = y + BUCKET_SIZE
            print((start_x, start_y, end_x, end_y))
            im.crop((start_x, start_y, end_x, end_y)).save(
                "{0}/{1}_{2}_{3}.png".format(output_dir, file.replace(".png", ""), idx_x, idx_y))
    print_slack_images(file, width, height)


def make_output_dir(filename):
    dir_name = filename.replace(".png", "") + "-output"
    try:
        # Create target Directory
        os.mkdir(dir_name)
        print("Directory ", dir_name, " Created ")
    except FileExistsError:
        print("Directory ", dir_name, " already exists")
    return dir_name


def print_slack_images(file, width, height):
    for idx_y, _ in enumerate(range(0, height, BUCKET_SIZE)):
        for idx_x, _ in enumerate(range(0, width, BUCKET_SIZE)):
            print(":{0}_{1}_{2}:".format(file.replace(".png", ""), idx_x, idx_y), end='')
        print("")


def main(args):
    output_dir = make_output_dir(args.file)
    loopThroughPixels(args.file, output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="The file to break into 128x128 images")
    args = parser.parse_args()
    main(args)
