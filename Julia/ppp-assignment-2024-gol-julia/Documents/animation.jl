using Distributed
@everywhere using Pkg
@everywhere Pkg.activate(@__DIR__,io=devnull)
@everywhere include("solution.jl")

using Test

init_fun = glider   
m=2000
n=2000
M=2
N=2
nodes=1
steps=10
worldstep=1
# game_serial(init_fun,m,n,steps,worldstep)
# game_parallel(init_fun,m,n,M,N,nodes,steps,worldstep)

@test game_check(init_fun,m,n,M,N,nodes,steps,worldstep)