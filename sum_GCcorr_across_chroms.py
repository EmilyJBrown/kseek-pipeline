## take a file with a list of directories you want to sum from, and a file with a list of the samples it should find there
## writes a single file for each sample to a new directory

import sys
import os

dirfh=sys.argv[1]
readsfh=sys.argv[2]

dirfile=open(dirfh, 'r')
readsfile=open(readsfh, 'r')

try:
	os.mkdir('./GC_cor_summed_across_chroms/')
except OSError:
	print "Output directory already exists.  Writing to it."

gcdict={}
reads=[]

for line in readsfile:
	if line=='': break
	line=line.strip()
	split=line.split('.')
	myid=split[0]
	if myid not in gcdict: gcdict[myid]={}
	reads.append(line)

for mydir in dirfile:
	if mydir=='': break
	mydir=mydir.strip()
	for myread in reads:
		myfh=str(mydir)+str(myread)
		myfile=open(myfh, 'r')
		myid=myread.split('.')[0]
		if myid not in gcdict:
			gcdict[myid]={}
		for line in myfile:
			if line=='': break
			line=line.strip()
			split=line.split()
			if line.startswith("GC"): continue
			gcbin=split[0]
			numpos=int(split[1])
			overlaps=int(split[2])
			if gcbin in gcdict[myid]: 
				gcdict[myid][gcbin][0]+=numpos
				gcdict[myid][gcbin][1]+=overlaps
			if gcbin not in gcdict[myid]: gcdict[myid][gcbin]=[numpos, overlaps]
	print str("Counted all files for directory")+str(mydir)

for myid in gcdict:
	mynewfh=str('./GC_cor_summed_across_chroms/')+str(myid)+str(".sum_GC_corr.txt")
	newfile=open(mynewfh, 'w')
	newfile.write(str("GC")+'\t'+str("Num.Pos.")+'\t'+str("OverlappingReads")+'\t'+str("Avg.Covg.")+'\n')
	mybins=gcdict[myid].keys()
	for gcbin in sorted(mybins):
		numpos=gcdict[myid][gcbin][0]
		numreads=gcdict[myid][gcbin][1]
		newfile.write(str(gcbin)+'\t'+str(numpos)+'\t'+str(numreads)+'\t'+str(float(numreads)/float(numpos))+'\n')
	newfile.close()
dirfile.close()
readsfile.close()



