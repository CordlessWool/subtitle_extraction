#!/bin/bash
#
# Script that extracts subtitles from a mkv file.
#
# Requires mkvmerge, mkvextract

hash mkvmerge 2>/dev/null || { echo >&2 "Error: Command mkvmerge not found"; exit 1; }
hash mkvextract 2>/dev/null || { echo >&2 "Error: Command mkvextract not found"; exit 1; }


file_name=$1
sub_name=$2
dest=$3

IFS='
'

tracks=$(LANG=en_US.utf8 LANGUAGE=en_US.utf8 mkvmerge --identify-verbose "$file_name" | tail --lines=+2)

for track in $tracks; do
	track_id=""
	[[ "$track" =~ Track\ ID\ ([0-9]+) ]] &&
		track_id=${BASH_REMATCH[1]}
	[[ "$track" =~ language:([a-z]+) ]] &&
		language=${BASH_REMATCH[1]}
	[[ "$track" =~ track_name:([^ ]+) ]] &&
		track_name=${BASH_REMATCH[1]}
	[[ "$track" =~ Track\ ID\ [0-9]+:\ ([a-z]*) ]] &&
		track_type=${BASH_REMATCH[1]}

	ext=""
	if [[ "$track" =~ S_TEXT/UTF8 ]]; then
		ext="srt"
	elif [[ "$track" =~ S_TEXT/ASS ]]; then
		ext="ssa"
	elif [[ "$track" =~ S_TEXT/USF ]]; then
		ext="usf"
	elif [[ "$track" =~ S_VOBSUB ]]; then
		ext="sub"
	elif [[ "$track" =~ S_HDMV/PGS ]]; then
		ext="sup"
	fi

	if [[ "$track_id" == "" ]]; then
		continue
	fi

	if [[ "$track_type" != "subtitles" ]]; then
		continue
	fi

	name="$track_id"
	if [[ "$language" != "" ]]; then
		name="$name.$language"
	fi

	if [[ "$track_name" != "" ]]; then
		track_name=${track_name/\//_}   # replace '/' with '_'
		track_name=${track_name/\\s/\ }  # replace '\s' with ' '
		track_name=${track_name/\\2/\"}  # replace '\2' with '"'
		track_name=${track_name/\\c/:}   # replace '\c' with ':'
		track_name=${track_name/\\h/#}   # replace '\h' with '#'
	fi

	if [[ ${dest: -1} == "/" ]]; then
        dest=${dest::-1}
	fi

	mkvextract tracks "$file_name" "$track_id:${dest}/${sub_name%.*}.$name.$ext"
done
