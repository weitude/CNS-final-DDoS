import argparse
import os
from os import path

def format_string(input_string):
    components = input_string.split()

    # Extract the desired values
    No = components[0]
    Time = components[1]
    Source = components[2]
    Destination = components[4]
    Protocol = components[5]
    Length = components[6]
    Info = ' '.join(components[7:])
    if Protocol != 'UDP':
        return ""

    output_string = f'"{No}","{Time}","{Source}","{Destination}","{Protocol}","{Length}","{Info}"\n'
    return output_string


def generate_csv(input_file):
    output_file = input_file.replace('pcapng', 'csv')

    # Generate CSV content using tshark command
    command = f'tshark -r {input_file} -Y "udp" > {output_file}'
    os.system(command)

    # Insert column headers at the beginning of the file
    with open(output_file, 'r+') as f:
        Lines = f.readlines()
        f.seek(0, 0)
        f.write('"No.","Time","Source","Destination","Protocol","Length","Info"\n')
        for line in Lines:
            f.write(format_string(line))

    print(f"CSV file '{output_file}' created.")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate CSV file from pcapng file.")
    parser.add_argument("-f", "--file", dest="input_file", required=True, help="Input pcapng file")
    args = parser.parse_args()

    if not path.isfile(args.input_file):
        print(f"Error: {args.input_file} is not a pcapng file")
        raise SystemExit
    extension = args.input_file.split(".")[-1]
    if extension != "pcapng":
        print(f"Error: {args.input_file} is not a pcapng file")
        raise SystemExit

    generate_csv(args.input_file)
