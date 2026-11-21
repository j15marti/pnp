"""New low-output-bit tests of split-family quotient perturbations."""
from pathlib import Path
import json,hashlib
from fractions import Fraction

def main():
    path=Path(__file__).resolve().parents[1]/'results/raw/t5_accounting_orientation1_20261121.json'
    data=path.read_bytes(); source=json.loads(data); rows=[]; tested=0
    for case in source['cases']:
        y=case['target_count']; E=case['E']; n=case['n']; N=case['N']
        assert y%(10*(1<<E))==0
        for k in range(1,13):
            tally=[0]*k
            for z in range(1<<k):
                fake=y+10*z
                assert 0<=fake<=5**n and fake%10==0
                for r in range(1,k+1):
                    # OR of raw count bits1..r (bit0 is the LSB).
                    accepts=((fake>>1)&((1<<r)-1))!=0
                    assert ((y>>1)&((1<<r)-1))==0
                    tally[r-1]+=accepts
                tested+=1
            for r,t in enumerate(tally,1):
                adv=Fraction(t,1<<k)
                assert adv==1-Fraction(1,1<<r)
                rows.append(dict(case=case['name'],N=N,E=E,k=k,conditional_entropy_bits=k,OR_gates=r-1,raw_bit_positions=list(range(1,r+1)),advantage=str(adv)))
    print(json.dumps(dict(status='PASS',seed=None,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),source_sha256=hashlib.sha256(data).hexdigest(),fake_values_enumerated=tested,rows=rows,k37=dict(N=6059,E=37,entropy_bits=37,OR_gates=36,advantage=str(1-Fraction(1,1<<37)),method='symbolic formula, not exhaustive enumeration'),scope='Residue tests only; prior source counts reused by explicit file pin; no solver runtime lower bound'),indent=2,sort_keys=True))
if __name__=='__main__':main()
