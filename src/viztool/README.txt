This was an attempt at making 3d volumetric rendering.
After fidling with many packages like slicer, clearvolume and itk
it seemed that Fiji provided good functionality and a quick script is supplied which opens
slices from a directory and opens the volume renderer for fiji:

../lib/Fiji.app/ImageJ-linux64 -macro show-render.ijm $HOME/QMUL/project/OCTune/src/../out/tooth/tuned-B-Scan/BScan/0.png
