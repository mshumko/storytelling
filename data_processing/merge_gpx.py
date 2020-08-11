# Merge the gpx files in the directory given by -dir arg. 
# Creates a gpx file with the name "child_directory_merged.py"
# in the same directory.

import argparse
import pathlib

import gpxpy

parser = argparse.ArgumentParser(description='Gpx track merger script.')
parser.add_argument('dir', type=str,
                    help=('The directory to look for all gpx files, sort '
                        'them by time and save the merged file to that directory.'))

args = parser.parse_args()
path = pathlib.Path(args.dir)
# Check that the path exists
if not path.exists():
    raise FileNotFoundError(f'{path} does not exist.')

gpx_paths = sorted(list(path.glob('*.gpx')))
save_name = f'{path.parts[-1]}_merged.xml'

save_gpx = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()
save_gpx.tracks.append(gpx_track)
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

for gpx_path in gpx_paths:
    with open(gpx_path, 'r') as gpx_file_handle:
        gpx = gpxpy.parse(gpx_file_handle)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    gpx_segment.points.append(point)
            #     for point in segment.points:
            #         print(point.latitude, point.longitude, point.elevation)
#             save_gpx.tracks.append(track)



with open(path / save_name, 'w') as f:
        f.write(save_gpx.to_xml())