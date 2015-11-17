#!/bin/bash

install_virtualenv() {
    if [ ! -d venv ]; then
        virtualenv venv --python=`which python2`
    fi
    source venv/bin/activate
    echo "installing deps"
    pip install -qr requirements.txt
}

install_update_articles() {
    if [ -d elife-articles ]; then
        echo "pulling any changes"
        cd elife-articles && git reset --hard && git pull && cd ..
    else
        echo "cloning elife-articles repo"
        git clone https://github.com/elifesciences/elife-articles
    fi
}

install_validator() {
    if [ ! -d elife-eif-schema ]; then
        git clone ssh://git@github.com/elifesciences/elife-eif-schema
    fi
    cd elife-eif-schema    
    git reset --hard
    git fetch
    npm install
    cd ..
}

wipe_old_results() {
    rm -f *.invalid
}

control_c() {
    echo "interrupt caught, exiting ..."
    exit $?
}

main() {
    passes=0
    fails=0
    invalids=0
    for file in elife-articles/*.xml; do
        fname=`basename $file`
        passes=$(( $passes + 1 ))
        
        printf "processing $fname ..."
        python feeds.py ./$file > .tmp.json
        ret=$?
        if [ $ret != 0 ]; then
            printf "FAILED\n"
            mv .tmp.json $fname.error
            fails=$(( $fails + 1 ))
            continue
        else
            printf " generated!"
        fi

        jp.py -f .tmp.json "[0].article[0]" | node elife-eif-schema/validator.js > .err.out
        ret=$?
        if [ $ret != 0 ]; then
            mv .err.out $fname.invalid
            printf " FAILED\n"
            invalids=$(( $invalids + 1 ))
            continue
        else
            printf " validated!"
        fi
        
        printf "\n"
    done
    
    # bundle up any problems
    touch foo.error; cat *.error > all.error; rm foo.error
    touch foo.invalid; cat *.invalid > all.invalid; rm foo.invalid

    results="test-results.`date +'%s'`.tar.gz"
    tar czf $results *.invalid *.error --ignore-failed-read 2> /dev/null
    echo "wrote $results";

    # delete temporary files
    rm -f .tmp.json .err.out *.invalid *.error all-errors all-invalid
    
    echo "all done. ${passes} articles, ${fails} fails, ${invalids} invalid"
    if [ $fails != 0 ] || [ $invalids != 0 ]; then
        # errors or invalid EIF generated, return non-zero response
        exit 1
    fi
    
    # all good!
    exit 0
}

trap control_c SIGINT

install_virtualenv
install_update_articles
install_validator
wipe_old_results
main
