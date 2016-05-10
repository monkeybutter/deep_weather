import datetime
from map_gen import map_gen
dt = datetime.datetime(2013, 1, 1, 0, 0, 0)
#print map_gen.get_weather_map("z850", dt)
print map_gen.get_map(dt)
