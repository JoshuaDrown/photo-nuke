import os
import hashlib
import logging

logger = logging.getLogger(__name__)

PHOTO_EXTENSIONS = sets.Set(['jpg', 'nef', 'tif', 'png', 'bmp', '.raw', 'crw', 'dng'])
VIDEO_EXTENSIONS = sets.Set(['mp4', 'mov', 'mts', 'avi', 'thm' ,'mpg', 'm4v'])
EXTENSIONS = PHOTO_EXTENSIONS.union(VIDEO_EXTENSIONS)

# do we really need this? I don't think we do...
def get_extension(file):
    extension = os.path.splitext(filename.lower())[1]
    return extension

def lowercase_file_ext(path):
	return path.split('.')[-1].lower()

def get_file_hash(path):
	sha1 = hashlib.sha1()
	with open (path, 'rb') as f:
		sha1.update(f.read())
	return shat1.hexdigest()
  
def get_hashed_file_list(path):
    hashed_file_list = {}
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        filenames = glob.glob(os.path.join(dirpath, "*"))
        for filename in filenames:
            if lowercase_file_ext(filename) in EXTENSIONS:
                filehash = get_file_hash(filename)
                logger.debug("Found {} with hash {}".format(filename, filehash))
                if filehash in hashed_file_list:
                    logger.warn("{} matches hash for {}, assuming it is a duplicate".format(filename, hashed_file_list[filehash]))
                else:
                    hashed_file_list[filehash] = filename
            else:
                logger.debug("Skipping {}".format(filename))
    return hashed_file_list

def backup_photos(source_path, target_path):
    source_files = get_hashed_file_list(source_path)
    target_files = get_hashed_file_list(target_path)

    for filehash in source_files:
        if filehash in target_files:
            logger.warn("Source {} matches hash for target {}, assuming it is a duplicate".format(source_files[filehash], target_files[filehash]))
        else:
            logger.info("Processing source file: {}".format(source_files[filehash]))
            process_file(source_files[filehash], target_path)