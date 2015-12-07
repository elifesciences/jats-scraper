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

    find elife-articles/ -iname "*.xml" -print0 | xargs -0 --max-procs=4 -n 1 "./subarticletest.sh"

    #for file in elife-articles/*.xml; do
    #    ./subarticletest.sh $file
    #    ret=$?
    #    if [ $ret == 1 ]; then fails=$(( $fails + 1 )); fi
    #    if [ $ret == 2 ]; then invalids=$(( $invalids + 1 )); fi
    #done
    
    # bundle up any problems
    touch foo.error; cat *.error > all.error; rm foo.error
    touch foo.invalid; cat *.invalid > all.invalid; rm foo.invalid

    results="test-results.`date +'%s'`.tar.gz"
    tar czf $results *.invalid *.error --ignore-failed-read 2> /dev/null
    echo "wrote $results";

    # delete temporary files
    rm -f *.tmp.json *.err.out *.invalid *.error all-errors all-invalid
    
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
