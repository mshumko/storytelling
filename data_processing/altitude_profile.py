import pathlib
import matplotlib.pyplot as plt
import numpy as np

import gpxpy

meters_to_feet = 3.28084
plt.rcParams.update({'font.size': 18})


gpx_path = pathlib.Path('./202008_gallatin_crest/gpx_merged_text_2.gpx')

with open(gpx_path, 'r') as gpx_file_handle:
    gpx = gpxpy.parse(gpx_file_handle)

    for track in gpx.tracks:
        for segment in track.segments:
            dist_km = np.zeros(len(segment.points)-1)
            cum_dist_km = np.zeros(len(segment.points)-1)
            elevation = np.zeros(len(segment.points)-1)
            time = np.zeros(len(segment.points)-1, dtype=object)

            for i, (point, next_point) in enumerate(zip(segment.points, segment.points[1:])):
                elevation[i] = point.elevation
                time[i] = point.time
                dist_km[i] = gpxpy.geo.distance(point.latitude, point.longitude, point.elevation,
                                    next_point.latitude, next_point.longitude, next_point.elevation)/1000

cum_dist_km = np.cumsum(dist_km)

fig, ax = plt.subplots(figsize=(8,5))
bx = ax.twinx()

# ax.plot(cum_dist_km, elevation)
ax.fill_between(cum_dist_km, elevation, elevation.min(), color='grey')

# Find the elevation bounds and convert to feet
mn, mx = ax.get_ylim()
bx.set_ylim(mn*meters_to_feet, mx*meters_to_feet)
bx.set_ylabel('Elevation [feet]')

ax.set_xlim(cum_dist_km[0], cum_dist_km[-1])
ax.set_ylim(elevation.min(), None)
ax.set_xlabel('Distance [km]')
ax.set_ylabel('Elevation [m]')

plt.tight_layout()
plt.show()