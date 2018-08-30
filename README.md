
Artificial Grammatical Error
=====================================================

Extract the CLC statistics
--------------------------------------
- **ge-stat-experiment1.sh**: To extract gedx file for any exam file  
Usage: ./ge-stat-experiment1.sh exam file tgtdir  
e.g.	 ./ge-stat-experiment1.sh IELTS 2000_42 tmp  
This script makes use of the following file
	- makestm.py: Make an stm file from a .inc/.spell/.corr file
	- stm2ctm.awk: Convert an stm file to a ctm file
	- pra2gedx.py: Convert from a pra file to a .gedx file

- **run-ge-stat-experiment1.sh**: To execute ge-stat-experiment1.sh for all files in the target exam  
	Run: 
	
		./run-ge-stat-experiment1.sh exam tgtdir 
		 
	e.g. ./run-ge-stat-experiment1.sh IELTS tmp
    
- **combine_gedx.sh**: To combine .gedx.tsv for all files in an exam into one file 
	Run: 
	
		./combine_gedx.sh.sh exam workdir tgt
		 
	e.g. ./combine_gedx.sh.sh IELTS tmp lib/gedx-tsv/work-16082018

*gedx.tsv format* - files from different exams should be concatanated to make a **master.gedx.tsv**
	
	i       	i       		c  
	am      	am      		c  
	certain 	certainty 		i
	you     	you     		c
	will    	will    		c
	provide 	provide 		c
	
*gedx.ins.tsv* - this is the file that the Unigram/Bigram needs in order to corrput a native-speech corpus. It combines insertion errors to the previous words, or the following words if they appear at the beginning of sentences.

	we		we			c
	call		call	to		i
	the		the			c
	centre		centre			c
	
To convert gedx.tsv to gedx.ins.tsv - the input/output are defined in sequencemodel.py, run:

	python3 sequencemodel.py ins
	
Corrupt native-speech corpora
--------------------------------------
### Native-Speech Corpora
- AMI	~ 2M
- Switchboard ~ 3.1M
- Fisher ~ 35.1M

### sequencemodel.py
This Python scrips provides classes for Unigram / Bigram models which are used in ami2gedtsv.py, cts2gedtsv.py, and fisher2gedtsv.py.

### AMI
Run:

	python3 ami2gedtsv.py [unigram/bigram]

Setting:

- path1 = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/ami-train+sil.mlf"
- path2 = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/ami-work/ami7-1"
- gedx_path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-24082018/master.gedx.ins.tsv"

### Switchboard CTS
Run:

	python3 cts2gedtsv.py [unigram/bigram]

Setting:

- path1 = "/home/nst/yq236/tools/kaldi-trunk-git/egs/swbd/s5c/data/train/text"
- path2= "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/cts-work/cts6"
- gedx_path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-24082018/master.gedx.ins.tsv"

### Fisher CTS
Run:

	python3 fisher/fisher2gedtsv.py

Setting:

- path1 = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/fisher/work15082018/fisher-all.txt"
- path2 = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/fisher/fisher6"
- gedx_path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-24082018/master.gedx.ins.tsv"

Process the Fisher Corpus
--------------------------------------

Run to process each directory for LDC/BBN:

	./fisher/run-step1ldc.sh transcr tgtdir tgtname
	./fisher/run-step1bbn.sh transcr tgtdir tgtname

Once all the directories are processed in step 1:

	./fisher/run-step2.sh
	
Other Tools
--------------------------------------
- **split_data.py**: Once ami2gedtsv.py generates .ged.tsv file, this script will prepare train/dev/test sets in the TLC format.  
	
	Run:
	 
		python3 split_data.py orig tgt name
		
	e.g. python3 split_data.py lib/ami-work/ami6.ged.tsv lib/tsv ami6
	
- **data_processing.py**: Processing done to AMI/Switchboard are manually defined in this file e.g. python dictionary for mapping

		



