#Extract exif data from photos to database

#What data are we looking for?
#	Date, Time, Tags, Location, All of it?

#these are as necessary as coconut halves
import os
import glob




#Extract all of the EXIF information...with extreme predjudice.
#Returns EXIF data in Key/Value paired dictionary.
#Uses PIL... not compatible with .NEF, or any other RAW format for that matter.
from PIL import Image
from PIL.ExifTags import Tags
def get_exif(path):
	exif = {}
	i = Image.open(f)
	info = i._getexif()
	for tag, value in info.items():
			decoded = TAGS.get(tag, tag)
			exif[decoded] = value
	return exif
#Associate a file with it's EXIF data (crude database)
def build_dict(path):
	dictionary = {}
	for f in glob.glob(os.path.join(path, '*'))
		info = get_exif(f)
		dictionary[f] = info


#OR... we can do it this way:		
#Uses GExiv2... WAAAAAAY more powerfull.
import gi
gi.require_version('GExiv2', '0.10')
from gi.repository.GExiv2 import Metadata as m

def get_exiv2(path):
	exif = {}
	for tag in m.get_tags(m(path)):
		exif[tag] = m.get(m(path), tag)
#Associate a file with it's EXIF data (crude database)
def build_dict2(path):
	dictionary = {}
	for f in glob.glob(os.path.join(path, '*'))
		info = get_exiv2(f)
		dictionary[f] = info

