# Subtilte Extration

This script try to match file names from a source folder and a destination folder. 
Subfolders are included. The subtitles will extract from mkv files in source folder to
the destination folder with name of matched file in destination folder + language name. 
(e.x. name.lang.sub).

Docker could be run with:
docker run --rm -d \\\
-u <user-id> \\\
-v <source>:/data/src \\\
-v <destination>:/data/dest \\\
cordlesswool/subtitle_extraction:latest


To run python script install first mkvtoolnix via apt: 

pip3 install regex

python3 ./extract_sub.py \<source> \<destination>
