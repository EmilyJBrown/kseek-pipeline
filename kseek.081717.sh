#!/bin/bash
#$ -S /bin/bash
#$ -q long_term.q
#$ -j y
#$ -N run_kseek
#$ -cwd
#$ -l h_vmem=10G
#$ -pe bscb 1
#$ -binding linear:2
#date
d1=$(date +%s)
echo $HOSTNAME
echo $1
mkdir -p /workdir/$USER/$JOB_ID
cd /workdir/$USER/$JOB_ID
/programs/bin/labutils/mount_server cbsufsrv5 /data1
cp /fs/cbsufsrv5/data1/mouse_MA/30x/$1.fq.gz .
cp $HOME/scripts/k_seek.r4.pl .
cp $HOME/scripts/split_fastq_25mill.py .

python split_fastq_25mill.py $1.fq.gz splitreads.txt
#!/bin/bash
for myread in `cat splitreads.txt`; do
  perl k_seek.r4.pl $myread $myread.kseekOUT.100cutoff
done

mv *kseekOUT* $HOME/mouse_MA_30x/.
cd ..
rm -r ./$JOB_ID
#date
d2=$(date +%s)
sec=$(( ( $d2 - $d1 ) ))
hour=$(echo - | awk '{ print '$sec'/3600}')
echo Runtime: $hour hours \($sec\s\)
