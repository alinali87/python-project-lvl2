import argparse
from gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("first_file", type=str)
    parser.add_argument("second_file", type=str)
    parser.add_argument("-f", "--format", type=str,
                        help="set format of output")

    args = parser.parse_args()
    first_file = args.first_file
    second_file = args.second_file

    diff_string = generate_diff(first_file, second_file)
    print(diff_string)


if __name__ == '__main__':
    main()
