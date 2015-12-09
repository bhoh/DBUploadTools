#! /bin/sh

ERA=$1
DIR=$PWD/../../JECDatabase/textFiles/$ERA

if [ $# -ne 1 ]; then
    echo "Usage: ./createDBFromTxtFiles.sh ERA"
    exit 1
fi

if [ ! -d "$DIR" ]; then
    echo "Error: $DIR does not exist"
    exit 1
fi

if [ -d "../data" ]; then
    echo "Error: 'data' folder already exist. Please remove it before launching this script"
    exit 1
fi

# Copy folder
cp -r "$DIR" ../data

# Delete symlinks
../removeSymlinks.sh ../data

# Create database
LOG=`mktemp`
cmsRun createDBFromTxtFiles.py era=$ERA path=JetMETCorrections/DBUploadTools/data/ &> "$LOG"

./parseLog.sh "$LOG"

if [ $? -eq 0 ]; then
    echo "Database successfully created as ${ERA}.db"
fi
