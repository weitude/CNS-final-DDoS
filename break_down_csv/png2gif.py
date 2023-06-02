import os
import argparse
from PIL import Image


def convert_to_gif(directory, output_path):
    image_files = sorted([f for f in os.listdir(directory) if f.endswith('.png')], key=lambda x: int(x.split('_')[1].split('.')[0]))
    print(image_files)
    images = []

    for file_name in image_files:
        file_path = os.path.join(directory, file_name)
        image = Image.open(file_path)
        images.append(image)

    images[0].save(output_path, save_all=True, append_images=images[1:], duration=150, loop=0)
    print(f"GIF file '{output_path}' created successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate GIF file from png files.")
    parser.add_argument("-p", "--path", dest="path", required=True, help="Input directory path")
    args = parser.parse_args()

    input_path = args.path.rstrip('/')
    if not os.path.isdir(input_path):
        print("Error: The provided path is not a directory.")
    else:
        directory_name = os.path.basename(input_path)
        output_file = f"{directory_name}.gif"
        output_path = os.path.join(input_path, output_file)
        print("Input path   |", input_path)
        print("Generate GIF |", output_path)
        convert_to_gif(input_path, output_path)
