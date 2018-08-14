#!/bin/tcsh
# Check Number of Args
if ( $#argv != 3 )  then
   echo "Usage: $0 exam workdir tgt"
   exit 100
endif

set EXAM=$1
set WORKDIR=$2
set TGT=$3

set GESTATEXP=/home/alta/BLTSpeaking/ged-pm574/artificial-error/scripts/ge-stat-experiment1.sh
set CLCBASE=/home/alta/CLC/LNRC/exams
set SRC=$CLCBASE/$EXAM
# set TGT=/home/alta/BLTSpeaking/ged-pm574/artificial-error/gedx-tsv
# set WORKDIR=/home/alta/BLTSpeaking/ged-pm574/artificial-error/work

foreach f (`ls -l $SRC/*.corr | sed "s/.*\///" | sed -r "s/\.[^.]*//"`)
  cat $WORKDIR/$EXAM/$f/$f.gedx >> $TGT/$EXAM.gedx.tsv
  echo "\n" >> $TGT/$EXAM.gedx.tsv
end
