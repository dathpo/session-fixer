import argparse
import os
import re
from signal import SIGINT, signal


class SessionFixer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.file_dir = os.path.dirname(os.path.realpath(filepath))
        self.filename = os.path.split(filepath)[1][:-4]
        self.text = None

    def parse_text(self):
        with open(self.filepath, mode="r", encoding="utf-8-sig") as reader:
            self.text = reader.readlines()
        reader.close()

    def write_file(self):
        new_filename = self.filename + "_fixed.txt"
        with open(os.path.join(self.file_dir, new_filename), mode="w", encoding="utf-8-sig") as writer:
            for line in self.text:
                res = re.search('.*(?=&uri=)', line)
                if res:
                    line = self.fix_link(res, line)
                writer.write(line)
        writer.close()

    @staticmethod
    def fix_link(match, text):
        return text.replace(match[0], "")[5:]


def args_parser():
    signal(SIGINT, sigint_handler)
    arg_parser = argparse.ArgumentParser(description="Session Export Fixer")
    arg_parser.add_argument("filepath", help="Session .txt file")
    arguments = arg_parser.parse_args()
    return arguments


def sigint_handler(sig, frame):
    """
    ISR to handle the Ctrl-C combination and stop the program in a clean way
    """
    exit(2)


if __name__ == "__main__":
    args = args_parser()
    fixer = SessionFixer(args.filepath)
    fixer.parse_text()
    fixer.write_file()
