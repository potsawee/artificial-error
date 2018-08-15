#!/bin/tcsh

# Check Number of Args
if ( $#argv != 3 )  then
   echo "Usage: $0 transcr tgtdir tgtname"
   echo "e.g. $0 /home/alta/CTS/Fisher/transcripts/fsh_qt_eng_tr_031016/bbn/auto-segmented lib/work-step1 fsh_bbn_031016"
   exit 100
endif


set TRANSCR=$1
set TGTDIR=$2
set TGTNAME=$3

set STEP1=/home/alta/BLTSpeaking/ged-pm574/artificial-error/scripts/fisher/step1bbn.py

if ( ! -d $TGTDIR ) then
    mkdir -p $TGTDIR
endif

touch $TGTDIR/$TGTNAME.txt

foreach f (`ls -1 $TRANSCR/*.trans`)
    python3 $STEP1 $f >> $TGTDIR/$TGTNAME.txt
    echo "$f ... done"
end
