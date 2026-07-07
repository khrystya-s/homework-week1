import os
import sys

def list_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(root, file))


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <repository_path>")
        return

    repo_path = sys.argv[1]

    if not os.path.exists(repo_path):
        print("Directory does not exist.")
        return

    list_files(repo_path)


if __name__ == "__main__":
    main()