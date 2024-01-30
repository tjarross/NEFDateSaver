import exifread
import os
import sys
from datetime import datetime
import re


def main():
    if len(sys.argv) > 2:
        print("Enter only one directory.")
    files = [f for f in os.listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1], f))]
    for file in sorted(files):
        with open(os.path.join(sys.argv[1], file), 'rb') as f:
            tags = exifread.process_file(f)
        dt = datetime.strptime(str(tags["Image DateTimeOriginal"]), "%Y:%m:%d %H:%M:%S")
        new_filename = os.path.join(sys.argv[1], f"{datetime.strftime(dt, '%Y%m%d_%Hh%Mm%Ss')}_{file}")
        if re.match(".*?/\d{4}[01]\d[0-3]\d_[0-2]\dh[0-5]\dm[0-5]\ds_DSC_\d{4}.NEF", new_filename) is not None:
            print(new_filename)
            os.rename(os.path.join(sys.argv[1], file), new_filename)
        else:
            raise Exception(f"File not well formatted: {new_filename}")


if __name__ == "__main__":
    main()