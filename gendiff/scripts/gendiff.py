import argparse
from gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("first_file", type=str)
    parser.add_argument("second_file", type=str)
    parser.add_argument("-f", "--format", type=str, help="set format of output",
                        choices=["stylish", "plain", "json"],
                        default="stylish")

    args = parser.parse_args()
    first_file = args.first_file
    second_file = args.second_file
    format = args.format

    diff_string = generate_diff(first_file, second_file, format)
    print(diff_string)


if __name__ == '__main__':
    main()
