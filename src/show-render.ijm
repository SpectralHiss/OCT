
file=getArgument;
if (file=="") exit ("No argument!"); 
run("Image Sequence...", "open=file sort");

run("Volume Viewer");
selectWindow("Volume_Viewer_1","display_mode=4, scale=2.5");