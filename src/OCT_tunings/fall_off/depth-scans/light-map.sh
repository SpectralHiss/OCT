# CAUTION this was run from within data folder
set -e
ARG=""
for f in Depth*; do
	ARG+=" ${f}/B-Scans/OCTImage0001.png"
done
convert $ARG -evaluate-sequence max light-map.png
