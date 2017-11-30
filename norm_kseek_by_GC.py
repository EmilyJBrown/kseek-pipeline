## takes a file with a list of GC correction output files and an unnormalized kseek file, and writes a new file normalizing
## each kmer count with the appropriate coverage based on GC content and library.

import sys

filesfh=sys.argv[1]
kseekfh=sys.argv[2]
newfh=sys.argv[3]

filesfile=open(filesfh, 'r')
kseekfile=open(kseekfh, 'r')
newfile=open(newfh, 'w')

meandict={}
gcdict={}
mykeys=[(0,0),(0.003333,.05),(.05,.1),(.1,.15),(.15,.2),(.2,.25),(.25,.3),(.3,.35),(.35,.4),(.4,.45),(.45,.5),(.5,.55),(.55,.6),(.6,1)]

for line in filesfile:
	if line=='': break
	line=line.strip()
	myid=line.split('_')[0]
	if myid not in gcdict: gcdict[myid]={}
	for i in mykeys:
		if i not in gcdict[myid]: gcdict[myid][i]=[0,0]
	mypos=0
	myreads=0
	myfile=open(line, 'r')
	for myline in myfile:
		if myline=='': break
		myline=myline.strip()
		if myline.startswith("GC"): continue
		split=myline.split()
		gcwin=float(split[0])
		numpos=int(split[1])
		reads=int(split[2])
		cov=float(split[3])
		mypos+=numpos
		myreads+=reads
		if numpos>100:
			for win in gcdict[myid]:
				if gcwin>win[0] and gcwin<=win[1]:
					gcdict[myid][win][0]+=reads
					gcdict[myid][win][1]+=numpos
			mypos+=numpos
			myreads+=reads
		if numpos<100: continue
	mymean=float(myreads)/float(mypos)
	for gcwin in gcdict[myid]:
		if gcdict[myid][gcwin]==[0,0]:
			gcdict[myid][gcwin]=[myreads,mypos]
	if myid not in meandict: meandict[myid]=mymean
	print str("Done getting the data from library ")+str(myid)

indexdict={}

for line in kseekfile:
	if line=='': break
	line=line.strip()
	split=line.split()
	if line.startswith("total"): continue
	if line.startswith("A/T"): continue
	if line.startswith("C/G"): continue
	if line.startswith("lines"):
		newfile.write(str(line)+'\n')
		for i in range(1,len(split)):
			if i not in indexdict: indexdict[i]=split[i]
	else:
		mykmer=split[0]
		kmer=mykmer.split('/')[0]
		if len(kmer)<2: continue
		newfile.write(str(mykmer))
		mygc=0
		for i in kmer:
			if i=="C" or i=="G": mygc+=1
		gccont=float(mygc)/float(len(kmer))
		for j in range(1, len(split)):
			myid=indexdict[j]
			for gcwin in mykeys:
				if gccont>=gcwin[0] and gccont<=gcwin[1]:
					mynorm=float(gcdict[myid][gcwin][0])/float(gcdict[myid][gcwin][1])
					normcount=float(split[j])/float(mynorm)
			newfile.write('\t'+str(normcount))
		newfile.write('\n')



