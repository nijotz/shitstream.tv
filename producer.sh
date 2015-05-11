#!/bin/bash

url_file="shitstream-urls"
downloads="shitstream-downloads"
source_url="http://infoforcefeed.shithouse.tv/interrogate/youtube"

cat /dev/null > $url_file

num_pages=$(curl -s $source_url | grep page= | sed -r 's/.*page=([0-9]*).*/\1/' | sort | tail -n 1)

for page in $(seq 0 "$num_pages"); do
    echo "Getting page $page of $num_pages"
    page_url="${source_url}?page=${page}"
    curl -s "$page_url" | grep youtube.com/watch | sed -r 's%.*(v=[-0-9a-zA-Z\_]*).*%https://www.youtube.com/watch?\1%' >> $url_file
done

youtube-dl --id -a $url_file --download-archive $downloads
