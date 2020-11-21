#!/bin/bash

WORDFILE=/usr/share/dict/words
# seed random from pid

lines=$(cat $WORDFILE  | wc -l)

while True
do
    # using cat means wc outputs only a number, not number followed by filename
    rnum=$((RANDOM*RANDOM%$lines+1))

    MYWORD=$(sed -n "$rnum p" $WORDFILE;)
    curl -k http://cava.thesniderpad.com:5000/api/v1/test_script -d "{\"foo\": \"$MYWORD\"}" -H 'Content-Type: application/json'
    echo " - $MYWORD"
    sleep 1
done
