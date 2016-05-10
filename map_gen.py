import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import Image
import ImageDraw
import datetime
import StringIO
import argparse
import datetime
import sys

path = "/Users/pablo/Downloads/"
out_im_size = (450, 300)
coordict = {"EGLL": (51.4700, -0.4543), "EIDW": (53.4264, -6.2499), "EGPH": (55.9508, -3.3615),
            "EHAM": (52.3105, 4.7683), "EBBR": (50.9010, 4.4856), "LFPG": (49.0097, 2.5479),
            "LFBO": (43.6294, 1.3677), "LEMD": (40.4839, -3.5680), "LEBL": (41.2974, 2.0833),
            "LPPT": (38.7756, -9.1354), "LIRF": (41.7999, 12.2462), "LIMC": (45.6301, 8.7255),
            "LSZH": (47.4582, 8.5555), "EDDM": (48.3537, 11.7750), "EDFH": (49.9458, 7.2642),
            "EDDT": (52.5588, 13.2884), "EKCH": (55.6180, 12.6508), "ENGM": (60.1976, 11.1004),
            "ESSA": (59.6498, 17.9238), "EFHK": (60.3210, 24.9529), "LOWW": (48.1158, 16.5666)}

def lon2pix(lon, wsize):
    return int(round((180. + lon) * (wsize/360.)))

def lat2pix(lat, hsize):
    return int(round((90 - lat) * (hsize/180.)))

def getxy(lon, lat, wsize, hsize):
    return lon2pix(lon, wsize), lat2pix(lat, hsize)

def dt2idx(dt, interval=6, year=2006):
    strt_dt = datetime.datetime(year, 1, 1, 0, 0, 0)
    idxs = divmod(((dt-strt_dt).days*24) + (dt-strt_dt).seconds//3600, 6)
    if idxs[1] != 0:
        raise Exception('Whops!')
    return idxs[0]

def get_weather_map(param, dt):
	
    arr = np.load(path + "{}_{}_low_uint8.npy".format(param, dt.year))
    np_im = plt.imshow(arr[:, :, dt2idx(dt, year=dt.year)], interpolation='none').make_image()
    h, w, d = np_im.as_rgba_str()
    rgba_array = np.fromstring(d, dtype=np.uint8).reshape(h, w, 4)

    im = Image.fromarray(rgba_array[::-1, :, :-1])
    im = im.resize(out_im_size, Image.NONE)
    output = StringIO.StringIO()
    im.save(output, format="PNG")
    #output.seek(0)
    #return output
    return output.getvalue()

def get_rain_map(dt):

    df = pd.read_csv(path + "airports_rain.csv", na_values="nil", parse_dates="timestamp")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    im = Image.open(path + "Earth-Color4096.jpg")
    w, h = im.size
    r = 8
    for key, coords in coordict.iteritems():
        x, y = getxy(coords[1], coords[0], w, h)
        draw = ImageDraw.Draw(im)
        if not pd.isnull(df.iloc[dt2idx(dt)][key]):
            if df.iloc[dt2idx(dt)][key]:
                draw.ellipse((x-r, y-r, x+r, y+r), fill=(0,255,0,0))
            else:
                draw.ellipse((x-r, y-r, x+r, y+r), fill=(255,0,0,0))
							        

    im = im.crop((lon2pix(-50, w), lat2pix(75, h), lon2pix(40, w), lat2pix(15, h)))
    im = im.resize(out_im_size, Image.ANTIALIAS)
    output = StringIO.StringIO()
    im.save(output, format="PNG")
    #output.seek(0)
    #return output
    return output.getvalue()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Deep Weather visualiser")
    parser.add_argument(dest="timestamp", type=str, help="Request")
    parser.add_argument(dest="maptype", type=str, help="Map type")
    parser.add_argument(dest="param", type=str, help="Param value")

    args = parser.parse_args()

    dt = datetime.datetime.strptime(args.timestamp, "%Y-%m-%dT%H:%M:%S")

    if args.maptype == "rain":
	    sys.stdout.write(get_rain_map(dt))
    elif args.maptype == "weather":
	    sys.stdout.write(get_weather_map(args.param, dt))
