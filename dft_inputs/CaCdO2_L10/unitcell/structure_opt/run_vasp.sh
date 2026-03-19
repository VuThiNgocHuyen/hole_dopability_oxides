#!/bin/zsh
#$ -S /bin/zsh
#$ -cwd
#$ -V
#$ -j y
#$ -o std.log
#$ -pe all_pe* 36
#$ -q ato_gpu.q

num_kpoints_line=`wc -l KPOINTS | cut -d " " -f1`
if [ $num_kpoints_line -ge 6 ]; then
  vasp_version=6.2.1
else
  vasp_version=6.4.1
fi

relax=""

if [ $QUEUE = "ato_gpu.q" ] || [ $QUEUE = "ato_tmp.q" ]; then
#if [ $QUEUE = "ato_gpu.q" ]; then
  export PATH=/opt_gpu/nvidia/hpc_sdk/Linux_x86_64/23.3/comm_libs/mpi/bin:/opt_gpu/nvidia/hpc_sdk/Linux_x86_64/23.3/compilers/bin:$PATH
  
  export MKL_THREADING_LAYER=INTEL
  export UCX_MEMTYPE_CACHE=n
  export NO_STOP_MESSAGE=1
  export OMP_NUM_THREADS=12
  VASP=/home/kuma/bin/vasp.${vasp_version}_gpu${relax}/bin/vasp_std
  num_process=4
else
  VASP=/home/kuma/bin/vasp.${vasp_version}${relax}/bin/vasp_std
  num_process=36
fi

echo $QUEUE

hostname >| exec_host

echo num processsor: $num_process
echo vasp command: $VASP
python /home/kuma/vasp6_custodian.py mpirun -np $num_process $VASP
touch finished
