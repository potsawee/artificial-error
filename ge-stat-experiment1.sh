#!/bin/tcsh

# Check Number of Args
if ( $#argv != 3 )  then
   echo "Usage: $0 exam file tgtdir"
   exit 100
endif

set EXAM=$1
set FILE=$2
set TGTDIR=$3

set ORIG=/home/alta/CLC/LNRC/exams/$EXAM/$FILE
# set TGT=/home/alta/BLTSpeaking/ged-pm574/artificial-error/work/$EXAM/$FILE
set TGT=$TGTDIR/$EXAM/$FILE
set STM2CTM=/home/alta/BLTSpeaking/ged-pm574/artificial-error/scripts/stm2ctm.awk
set MAKESTM=/home/alta/BLTSpeaking/ged-pm574/artificial-error/scripts/makestm.py
set SCORING=/home/alta/BLTSpeaking/ged-kmk/cued/local/run/step-scoring
set PRA2GEDX=/home/alta/BLTSpeaking/ged-pm574/artificial-error/scripts/pra2gedx.py

if (! -d $TGT) mkdir -p $TGT

echo "-----------------------------------------------------"
echo "file: $ORIG"
echo "-----------------------------------------------------"

python3 $MAKESTM $ORIG.corr $TGT/file.corr.stm
echo "convert to stm done"
python3 $MAKESTM $ORIG.spell $TGT/file.spell.stm
echo "convert to stm done"
awk -f $STM2CTM $TGT/file.spell.stm > $TGT/file.spell.ctm
echo "convert to ctm done"

$SCORING $TGT/file.corr.stm $TGT/file.spell.ctm $TGT/align >> $TGT/align.log.txt
echo "alignment done"

python3 $PRA2GEDX $TGT/align/file.spell.ctm.pra $TGT/$FILE.gedx
echo "convert pra to gedx done"
