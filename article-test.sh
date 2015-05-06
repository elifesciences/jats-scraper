#!/bin/bash

pip="pip"
python="python"
if [ -f /usr/bin/python2 ]; then
    # dirty to check to see if this is Arch
    python="python2"
    pip="pip2"
fi


install_virtualenv() {
    virtualenv venv --python=/usr/bin/$python && \
    source venv/bin/activate && \
    $pip install -r requirements.txt
}

install_update_articles() {
    if [ -d elife-articles ]; then
        #echo "pulling any changes"
        cd elife-articles && git pull && cd ..
    else
        #echo "cloning elife-articles repo"
        git clone https://github.com/elifesciences/elife-articles
    fi
}

control_c() {
    echo "interrupt caught, exiting ..."
    exit $?
}

main() {
    passes=0
    for file in elife-articles/*.xml; do
        echo "processing $file ..."
        eval "$python feeds.py ./$file" > /dev/null
        ret=$?
        if [ $ret != 0 ]; then
            echo "failed to process article $file. exiting with code $ret after $passes successful article scrapes."
            exit $ret
        else
            passes=$(( $passes + 1 ))
        fi
    done
    echo "all done. successfully scraped $passes articles"
}

trap control_c SIGINT

install_virtualenv
install_update_articles
main
