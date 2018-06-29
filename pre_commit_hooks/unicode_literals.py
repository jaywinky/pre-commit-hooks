from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse


def has_coding(line):
    if not line.strip():
        return False
    return (
        line.lstrip()[0:1] == b'#' and (
            b'unicode' in line or
            b'encoding' in line or
            b'coding:' in line or
            b'coding=' in line
        )
    )


def fix_unicode_literals(f):
    found = False
    coding = None
    for counter, line in enumerate(f.readlines()):
        if not coding and has_coding(line):
            coding = counter

        if line.startswith(b'def') or line.startswith(b'class'):
            break

        if line.startswith(b'from __future__ import unicode_literals'):
            found = True
            break

    if found:
        return 0

    f.seek(0)
    lines = []

    if isinstance(coding, int):
        for line in range(coding + 1):
            lines.append(f.readline())
    lines.append(b'from __future__ import unicode_literals\n\n')
    rest = f.read()

    # Otherwise, write out the new file
    f.seek(0)
    f.truncate()

    for line in lines:
        f.write(line)

    f.write(rest)

    return 1


def main(argv=None):
    parser = argparse.ArgumentParser('Fix missing unicode literals import')
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    fmt = 'Added unicode literals import to {filename}'

    for filename in args.filenames:
        with open(filename, 'r+b') as f:
            file_ret = fix_unicode_literals(f)
            retv |= file_ret
            if file_ret:
                print(fmt.format(
                    filename=filename,
                ))

    return retv


if __name__ == "__main__":
    exit(main())
