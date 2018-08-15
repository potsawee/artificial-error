#!/bin/tcsh

# To combine to the file into one => Run this manually once all transitions are extracted by run-step1
set MYPATH=/home/alta/BLTSpeaking/ged-pm574/artificial-error/scripts/fisher/work15082018
foreach f (`ls -1 $MYPATH/*.txt`)
    cat $f >> $MYPATH/fisher-all.txt
end
echo "combine done"
