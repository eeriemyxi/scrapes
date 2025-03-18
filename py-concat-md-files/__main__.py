import pathlib
import sys


def walk_for_md(output_file, depth, walk_dir):
    dirs = []
    for file in walk_dir.iterdir():
        if file.suffix == ".md":
            output_file.write(file.read_text())
        elif file.is_dir() and depth != 0:
            dirs.append(file)
    for dir in dirs:
        walk_for_md(output_file, depth - 1, dir)


def main():
    args = sys.argv[1:]
    cwd = pathlib.Path.cwd()

    if args and args[0] in ("-h", "--help"):
        print(
            f"Usage: {sys.argv[0]} [directory={cwd}] [depth=1] [output-file=<stdout>]"
        )
        exit(1)

    directory = pathlib.Path(args.pop(0)) if args else cwd
    assert directory.is_dir()

    depth = int(args.pop(0)) if args else 1
    output_file = open(pathlib.Path(args.pop(0)), "w") if args else sys.stdout

    walk_for_md(output_file, depth, directory)

    output_file.close()


if __name__ == "__main__":
    main()
