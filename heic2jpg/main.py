import os
import subprocess
import glob
import logging


def convert_heic_to_jpg(dir):
    """Convert HEIC files to JPG"""
    try:
        for root, dirs, files in os.walk(dir):
            for name in dirs:
                fullpath = os.path.join(root, name)
                ftype = ".HEIC"
                files = glob.glob(fullpath + f'/*{ftype}')
                # list only directories that have HEIC files
                if len([name for name in os.listdir(fullpath)
                        if name.endswith(ftype)]) > 0:
                    logging.info(
                        f'Found HEIC files in: {fullpath} , converting to JPG')
                    # use glob to find HEIC files in fullpath and log them
                    for f in files:
                        logging.info(f'Found {f}')

                    subprocess.run(
                        ['mogrify', '-format', 'jpg', fullpath + f'/*{ftype}'])
                else:
                    logging.info(f'No HEIC files in: {fullpath}')
    except Exception as e:
        logging.error(e)


def delete_heic_files(dir):
    """Remove HEIC files after conversion
    """
    try:
        for root, dirs, files in os.walk(dir):
            for name in dirs:
                fullpath = os.path.join(root, name)
                ftype = ".HEIC"
                files = glob.glob(fullpath + f'/*{ftype}')
                # Delete HEIC files after conversion and if jpg files exist
                if len([name for name in os.listdir(fullpath)
                        if name.endswith('.jpg')]) > 0 and \
                        len([name for name in os.listdir(fullpath)
                             if name.endswith(ftype)]) > 0:
                    logging.info(
                        f'Deleting HEIC files in: {fullpath}')
                    for f in files:
                        logging.info(f'Deleting {f}')
                        os.remove(f)
    except Exception as e:
        logging.error(e)


def main():
    logging.basicConfig(level=logging.INFO, filename='heic2jpg.log',
                        filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        directory = './'
        # Check if mogrify is installed
        if not os.path.isfile('/usr/bin/mogrify'):
            logging.error('mogrify not installed, exiting')
            logging.error('Install it: sudo apt install imagemagick')
            exit(1)
        # Convert HEIC files to JPG
        convert_heic_to_jpg(directory)
        # Delete HEIC files after conversion and if jpg files exist
        delete_heic_files(directory)

    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    main()
