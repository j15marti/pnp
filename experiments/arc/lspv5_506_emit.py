# LSPV-5/506: emit stdin for lspv5_506_frontier.c. Usage: python3 lspv5_506_emit.py <packet> <cap> <wmax> <0=slot|1=byte> | ./frontier
import sys; sys.path.insert(0,__import__('os').path.dirname(__file__))
from lspv5_506_recompute_frontier import dag
p,s=dag(sys.argv[1]); cap,wmax,obj=sys.argv[2:5]
print(len(p),cap,wmax,obj)
for ps,z in zip(p,s): print(z,len(ps),*ps)
