#!/bin/bash
file=$1
fname=`basename $file`
passes=$(( $passes + 1 ))

printf "processing $fname ..."
python feeds.py ./$file > $fname.tmp.json
ret=$?
if [ $ret != 0 ]; then
    printf "FAILED\n"
    mv $fname.tmp.json $fname.error
    exit 1 # fail
fi

printf " generated!"

jp.py -f $fname.tmp.json "[0].article[0]" | node elife-eif-schema/validator.js > $fname.err.out
ret=$?
if [ $ret != 0 ]; then
    mv $fname.err.out $fname.invalid
    printf " FAILED\n"
    exit 2 # fail
fi

printf " validated!\n"
