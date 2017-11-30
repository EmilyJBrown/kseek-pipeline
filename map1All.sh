#!/bin/bash
#$ -S /bin/bash
#$ -q long_term.q
#$ -j y
#$ -N run_bowtie2
#$ -cwd
#$ -l h_vmem=25G
#$ -pe bscb 4
#$ -binding linear:2
#date
d1=$(date +%s)
echo $HOSTNAME
echo $1
echo $2
mkdir -p /workdir/$USER/$JOB_ID
cd /workdir/$USER/$JOB_ID
/programs/bin/labutils/mount_server cbsufsrv5 /data1
cp /fs/cbsufsrv5/data1/mouse_MA/30x/$1_1.fq.gz .
cp /fs/cbsufsrv5/data1/mouse_MA/30x/$1_2.fq.gz .
cp -r /fs/cbsufsrv5/data1/ejb289/mouse_MA/INDEXES/ .

bowtie2 -p 8 --no-unal --no-1mm-upfront -x INDEXES/$2 -1 $1_1.fq.gz -2 $1_2.fq.gz | samtools view -bS - | samtools sort -o $1.map_to_$2.sorted.bam -O bam -

mv *.sorted.bam $HOME/mouse_MA_30x/.
cd ..
rm -r ./$JOB_ID
#date
d2=$(date +%s)
sec=$(( ( $d2 - $d1 ) ))
hour=$(echo - | awk '{ print '$sec'/3600}')
echo Runtime: $hour hours \($sec\s\)
