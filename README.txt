All of the python code is in src/
there is no explicit entrypoint main program, all programs are tests which validate the packages.
hence after installing (likely with pip install -r requirements.txt), browsing to test and running pytest will run the code will demonstrate the work.
the data directory contains some sample data, the phantom dataset, Xray, mirror, and oct tooth grab.
RAWOCTProcessor is untouched from the previous version and is kept for reference.