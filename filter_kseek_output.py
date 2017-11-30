import sys

kseekinfh=sys.argv[1]
newfh=sys.argv[2]

kseekin=open(kseekinfh, 'r')
newfile=open(newfh, 'w')

for line in kseekin:
    if line=='': break
    line=line.strip()
    split=line.split()
    if split[0].startswith("lines"):
        newfile.write(str(line)+'\n')
        continue
    else:
        kmer=split[0]
        counts=[]
        for count in split[1:]:
            counts.append(int(count))
        maxcount=max(counts)
        if maxcount<100: continue
        if maxcount>=100:
            newfile.write(str(line)+'\n')
kseekin.close()
newfile.close()
