#!/bin/tcsh

# Check Number of Args
if ( $#argv != 1 )  then
   echo "Usage: $0 exam"
   exit 100
endif

set EXAM=$1
set GESTATEXP=/home/alta/BLTSpeaking/ged-pm574/artificial-error/ge-stat-experiment1.sh
set CLCBASE=/home/alta/CLC/LNRC/exams
set SRC=$CLCBASE/$EXAM
# set NAMES=/home/alta/BLTSpeaking/ged-pm574/artificial-error/temp.txt

# $GESTATEXP $EXAM
# ls -l $SRC/*.corr | sed "s/.*\///" | sed -r "s/\.[^.]*$//" >> $NAMES
foreach f (`ls -l $SRC/*.corr | sed "s/.*\///" | sed -r "s/\.[^.]*//"`)
    $GESTATEXP $EXAM $f
end
