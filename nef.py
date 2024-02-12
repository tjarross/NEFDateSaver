import exifread
import os
import sys
from datetime import datetime
import re
import exiftool


def main():
    if len(sys.argv) > 2:
        print("Enter one directory to process.")
    files = [f for f in os.listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1], f))]
    for file in sorted(files):
        dt = None

        if re.match(r"\d{4}(0\d|1[012])([012]\d|3[01])_([01]\d|2[0123])h[0-5]\dm[0-5]\ds_DSC_\d{4}.(NEF|JPG|MOV)", file) is not None:
            print(f"File already formatted '{file}'")
            continue

        if file.endswith(".NEF") or file.endswith(".JPG"):
            with open(os.path.join(sys.argv[1], file), 'rb') as f:
                tags = exifread.process_file(f, stop_tag="EXIF DateTimeOriginal")
            dt = datetime.strptime(str(tags["EXIF DateTimeOriginal"]), "%Y:%m:%d %H:%M:%S")
        elif file.endswith(".MOV"):
            with exiftool.ExifToolHelper() as et:
                metadata = et.get_metadata(os.path.join(sys.argv[1], file))
                dt = datetime.strptime(str(metadata[0]["MakerNotes:CreateDate"]), "%Y:%m:%d %H:%M:%S")
        else:
            print(f"File type not supported: '{file}'")
            continue

        new_filename = f"{datetime.strftime(dt, '%Y%m%d_%Hh%Mm%Ss')}_{file}"
        if re.match(r"\d{4}(0\d|1[012])([012]\d|3[01])_([01]\d|2[0123])h[0-5]\dm[0-5]\ds_DSC_\d{4}.(NEF|JPG|MOV)", new_filename) is not None:
            print(new_filename)
            os.rename(os.path.join(sys.argv[1], file), os.path.join(sys.argv[1], new_filename))
        else:
            raise Exception(f"File not well formatted: {new_filename}")


if __name__ == "__main__":
    main()