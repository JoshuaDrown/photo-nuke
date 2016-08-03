import argparse
import logging
import pyexiv2
import os

# Get a local logger for writing log messages instead of using extraineous 'print' lines
logger = logging.getLogger(__name__)


VIDEO_EXTENSIONS = '.mp4', '.mov', '.mts', '.avi', '.thm' ,'.mpg', '.m4v'
PHOTO_EXTENSIONS = '.jpg', '.nef', '.tif', '.png', '.bmp', '.raw', 'crw', 'dng'
EXTENSIONS = [VIDEO_EXTENSIONS + PHOTO_EXTENSIONS]


def get_extension(filename):
    extension = os.path.splitext(filename.lower())[1]
    return extension

def get_date(d):
    exifdata = pyexiv2.metadata.ImageMetadata(d)
    exifdata.read()
    if 'Exif.Photo.DateTimeOriginal' in exifdata.exif_keys:
        dateTag = exifdata['Exif.Photo.DateTimeOriginal']
    elif 'Exif.Image.DateTime' in exifdata.exif_keys:
        dateTag = exifdata['Exif.Image.DateTime']
    else:
        logger.warning('A suitable date/time stamp could not be found for {}.'.format(filename))
        return 'None'
#thanks to smart people at stackoverflow.com for this next little gem.
    date = dict((k.strip(), v.strip())
            for k,v in (item.split(':')
            for item in dateTag.value.strftime(
                'year:%Y, month:%m, day:%d, hour:%H, min:%M, sec:%S').split(',')))
    return date


# Added this to start to deal with videos. Pyexiv2 does not support video.
def video_move(indir,outdir,filename):
    os.renames(filename,os.path.join(outdir,'videos',filename))
    logger.info('IM A VIDEO')


# read EXIF data for date of photo creation then rename the file with
# it's date/timeand move it to it's proper year/month directory
def meta_move(indir,outdir):
    try:
        os.chdir(indir)
        for f in os.listdir(os.curdir):
            extension = get_extension(f)
            if extension in PHOTO_EXTENSIONS:
                datetime = get_date(f)
                if 'None' in datetime:
                    newpath = os.path.join(outdir, 'nodate', f)
                else:
                    newname = '{}{}{}_{}{}{}'.format(
                            datetime['year'],
                            datetime['month'],
                            datetime['day'],
                            datetime['hour'],
                            datetime['min'],
                            datetime['sec']) + extension
                    newpath = os.path.join(
                            outdir,
                            datetime['year'],
                            datetime['month'],
                            newname)
                if os.path.isfile(newpath):
                    os.remove(f)
                    logger.warn('{} has already been placed in the library.'.format(f))
                else:
                    logger.info('Moving {} to {}'.format(f, newpath))
                    os.renames(f, newpath)
            elif extension in VIDEO_EXTENSIONS:
                video_move(indir,outdir,f)
    except IOError as ioerr:
        logger.warn('File error: ' + str(ioerr))
        pass


def main():
    # Set up global logging at the WARNING level, but the local logger to the DEBUG level
    logging.basicConfig(level=logging.WARNING)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(
            description="Utility for moving pictures into directories based on EXIF data.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
            "-s",
            "--source_path",
            default=os.getcwd(),
            help="Path to input directory")
    parser.add_argument(
            "-t",
            "--target_path",
            default='/mnt/MediaStorage/SubaquaticPhotos',
            help="Path to output directory")
    args = parser.parse_args()

    logger.info('Placing processed files in: {}'.format(args.target_path))

    for dirpath, dirnames, filenames in os.walk(args.source_path, topdown=False):
        logger.info('PROCESSING {}'.format(dirpath))
        meta_move(dirpath, args.target_path)


if __name__ == "__main__":
    main()