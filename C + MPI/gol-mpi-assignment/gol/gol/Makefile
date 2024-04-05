cd c/Users/orzma/OneDrive/文件/gol-mpi-assignment/gol/gol

scp -r c/Users/orzma/OneDrive/文件/gol-mpi-assignment jch235@ssh.data.vu.nl:/home/jch235

VUipe@0974144700

ssh jch235@ssh.data.vu.nl

scp -r jch235@ssh.data.vu.nl:/home/jch235/gol-mpi-assignment ppp23049@fs0.das5.cs.vu.nl:/home/ppp23049

tDm11gPf

ssh ppp23049@fs0.das5.cs.vu.nl

module load prun

module load openmpi/gcc

mpicc -Wall -O3 -o gol-par gol-par.c -lm

prun -v -1 -np 4 -script $PRUN_ETC/prun-openmpi ./gol-par 40 40 10 1 1

---

mpicc gol-par.c -o gol-par

mpiexec -n 4 ./gol-par 20 20 10 0 0

-----

scp -r ppp23049@fs0.das5.cs.vu.nl:/home/ppp23049/ppp-assignment-2024-gol-julia jch235@ssh.data.vu.nl:/home/jch235

scp -r jch235@ssh.data.vu.nl:/home/jch235/ppp-assignment-2024-gol-julia /mnt/c/Users/orzma/Downloads

----

scp -r c/Users/orzma/OneDrive/文件/ppp-assignment-2024-gol-julia jch235@ssh.data.vu.nl:/home/jch235

VUipe@0974144700

ssh jch235@ssh.data.vu.nl

scp -r jch235@ssh.data.vu.nl:/home/jch235/ppp-assignment-2024-gol-julia ppp23049@fs0.das5.cs.vu.nl:/home/ppp23049

tDm11gPf

ssh ppp23049@fs0.das5.cs.vu.nl

module load julia/1.7.3

julia --project=. benchmark.jl 24000 24000 4 5 2