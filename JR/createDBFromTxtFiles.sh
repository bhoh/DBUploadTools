#! /bin/sh

ERA=$1
ERA2=$2
DIR=$PWD/../../JRDatabase/textFiles/$ERA

if [ $# -lt 1 ]; then
    echo "Usage: ./createDBFromTxtFiles.sh ERA"
    exit 1
fi

if [ ! -d "$DIR" ]; then
    echo "Error: $DIR does not exist"
    exit 1
fi

if [ -d "../data" ]; then
    #XXX
    rm -r ../data
    #echo "Error: 'data' folder already exist. Please remove it before launching this script"
    #exit 1
fi

# Copy folder
cp -r "$DIR" ../data

# Delete symlinks
../removeSymlinks.sh ../data
: '
if [ -z "$ERA2" ]; then
    LOG=${ERA}.log
else
    LOG=${ERA2}.log
fi
'
# Create database
#cmsRun createDBFromTxtFiles.py era=$ERA path=JetMETCorrections/DBUploadTools/data/ &> "$LOG"
cmsRun createDBFromTxtFiles.py era=$ERA era2=$ERA2 path=JetMETCorrections/DBUploadTools/data/

: '
./parseLog.sh "$LOG"
if [ $? -eq 0 ]; then
    if [ -z "$ERA2" ]; then
        echo "Database successfully created as ${ERA}.db"
    else
        echo "Database successfully created as ${ERA2}.db"
    fi
fi
'
