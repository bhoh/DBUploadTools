#! /bin/sh

LOG=$1

CORRECTIONS="L1FastJet L2Relative L3Absolute L2L3Residual Uncertainty" # 

# Log contains files like:
#    File found: Opened file JetMETCorrections/DBUploadTools/data/Summer15_25nsV6_DATA_L3Absolute_AK4PF.txt 
#    File not found: Did not find JEC file JetMETCorrections/DBUploadTools/data/Summer15_25nsV6_DATA_L4EMF_AK4PF.txt

STATUS=0

for C in $CORRECTIONS; do

    FAILED=`grep "Did not find JEC" "$LOG" | grep ${C}_`

    if [ $? -eq 0 ]; then
        echo "WARNING: text file for $C level not found while creating database. This is not normal, please check carefully."
        while read -r f; do
            echo "    File not found: ${f#Did not find JEC file JetMETCorrections/DBUploadTools/data/}"
        done <<< "$FAILED"
        STATUS=1
    fi
done

exit $STATUS
