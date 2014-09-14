import json
import glob
from PIL import Image
from PIL.ExifTags import TAGS
from pprint import pprint
 
def get_exif_data(fname):
    """Get embedded EXIF data from image file."""
    ret = {}
    try:
        img = Image.open(fname)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        print 'IOERROR ' + fname
    return ret

def gps_dict_to_double(data):
    latC = data.get(1, None)
    latT = data.get(2, None)
    longC = data.get(3, None)
    longT = data.get(4, None)
    lat = latT[0][0]/float(latT[0][1])
    lat += latT[1][0]/float(latT[1][1])/60
    lat += latT[2][0]/float(latT[2][1])/3600
    long = longT[0][0]/float(longT[0][1])
    long += longT[1][0]/float(longT[1][1])/60
    long += longT[2][0]/float(longT[2][1])/3600       
    if latC == 'S':
        lat *= -1
    if longC == 'W':
        long *= -1
    ret = (lat, long)
    return ret

def get_lat_long_from_image(imageName):
    metadata = get_exif_data(imageName)
    gpsData = metadata.get('GPSInfo', None)
    if gpsData != None:
        return gps_dict_to_double(gpsData)
    else:
        return None

piglets = {}
i = 0

for filename in glob.glob('*.jpg'):
    i += 1
    piglets[i] = get_lat_long_from_image(filename)

f = open('database.json','w')
json = json.dump(piglets, f)

f.close()
