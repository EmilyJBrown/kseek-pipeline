import sys

infh=sys.argv[1]
outfh=sys.argv[2]
cutoff=float(sys.argv[3])

infile=open(infh, 'r')
newfile=open(outfh, 'w')

write=str("no")

for line in infile:
    if line=='': break
    line=line.strip()
    if line.startswith("lines"):
        newfile.write(str(line)+'\n')
    else:
        write=str("yes")
        split=line.split()
        kmer=split[0]
        myvals=split[1:]
        mymax=max(myvals)
        for i in range(1,len(split)):
            if float(split[i])>float(cutoff)*float(mymax) and float(split[i])!=float(mymax): 
                write=str("no")
        if write=="yes":
            newfile.write(str(line)+'\n')
        if write=="no":
            continue

infile.close()
newfile.close()
