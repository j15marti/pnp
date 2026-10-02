#!/usr/bin/env python3
"""Source-bound adaptive replay on declared SU05/Hadamard Boolean-grid LDE leaves.

COMPUTATIONAL finite control only. A committed source word w determines legal
orbit-shift slices S_s <= F_2^m. A future challenge s asks for the canonical
RREF basis of S_s. The complete response signature Sigma(w) is the tuple of
canonical slice bases over all legal shifts.

The no-reread retention lower bound on a source family W is exactly
ceil(log2(max signature-fiber requirement)) in the injective case below:
different complete signatures must occupy different committed states if every
future slice can be challenged exactly. We report log2(number of distinct
signatures), plus semantic-fiber versions for simple free side information.

This does NOT lower-bound unrestricted static SAT: the source word is statically
available and every response can be recomputed by interpolation/orbit evaluation.
"""
import itertools, json, math, time
from pathlib import Path

ns={}
exec(Path("experiments/product_span/vms_lde_hadamard_leaf.py").read_text().replace('if __name__=="__main__":main()',''),ns)
lagrange_eval,primitive_root,bits=ns["lagrange_eval"],ns["primitive_root"],ns["bits"]

def canonical_basis(rows):
    B={}
    for value in rows:
        x=value
        for p in sorted(B, reverse=True):
            if (x>>p)&1: x ^= B[p]
        if not x: continue
        p=x.bit_length()-1
        for q in list(B):
            if (B[q]>>p)&1: B[q] ^= x
        B[p]=x
    return tuple(B[p] for p in sorted(B, reverse=True))

def slices_for_word(word,p,m):
    k=math.ceil(math.log2(p)); g=primitive_root(p); N=p-1
    labels=[bits(lagrange_eval(word,pow(g,t,p),p),k) for t in range(N)]
    out=[]
    for s in range(N):
        cols=[sum(labels[(s+i)%N][j]<<i for i in range(m)) for j in range(k)]
        out.append(canonical_basis(cols))
    return tuple(out)

def signature(word,p,m):
    return slices_for_word(word,p,m)

def semantic_bit(word):
    # Deliberately weak free semantic side channel: OR of source bits.
    return int(any(word))

def analyze(p,h,m):
    words=[w for w in itertools.product((0,1), repeat=h) if len(set(w))>1]
    t0=time.perf_counter()
    sigs={}
    sem_sigs={0:set(),1:set()}
    for w in words:
        sig=signature(w,p,m)
        sigs.setdefault(sig,[]).append(w)
        sem_sigs[semantic_bit(w)].add(sig)
    elapsed=time.perf_counter()-t0
    distinct=len(sigs)
    max_collision=max(map(len,sigs.values()))
    bits_needed=math.ceil(math.log2(distinct)) if distinct>1 else 0
    max_sem=max(len(v) for v in sem_sigs.values())
    sem_bits=math.ceil(math.log2(max_sem)) if max_sem>1 else 0

    # Adaptive prefix classes: after challenges 0..t-1, count surviving distinct
    # response prefixes. This measures how quickly legal openings distinguish
    # committed source realizations for this fixed challenge order.
    N=p-1; prefix=[]
    for t in range(1,N+1):
        classes={sig[:t] for sig in sigs}
        prefix.append({"challenges":t,"distinct_prefix_signatures":len(classes),
                       "retention_bits_ceiling_log2":math.ceil(math.log2(len(classes))) if len(classes)>1 else 0})
    examples=[]
    for group in sigs.values():
        if len(group)>1:
            examples.append(["".join(map(str,w)) for w in group[:4]])
            if len(examples)>=5: break
    return {
      "p":p,"h":h,"m":m,"orbit_N":N,"nonconstant_sources":len(words),
      "distinct_complete_signatures":distinct,
      "signature_collision_max":max_collision,
      "no_reread_signature_retention_bits":bits_needed,
      "free_semantic_side_channel":"OR(word)",
      "max_distinct_signatures_in_semantic_fiber":max_sem,
      "no_reread_retention_bits_with_free_semantic_side_info":sem_bits,
      "collision_examples":examples,
      "prefix_profile":prefix,
      "full_reread_recompute_seconds_for_all_sources":elapsed,
      "recompute_algorithm":"canonical interpolation -> full multiplicative orbit -> binary labels -> canonical GF(2) slice basis"
    }

def main():
    cases=[(17,4,4),(29,5,5),(37,6,6),(43,7,7),(53,8,8),(67,9,9)]
    out={"status":"COMPUTATIONAL finite source-bound ACR control",
      "realization":"axis-parallel canonical Boolean-grid LDE leaf + SU05 multiplicative orbit + standard binary label/Hadamard legal slices",
      "challenge":"post-commitment orbit shift s; response is canonical GF(2) basis of committed legal slice S_s",
      "cases":[analyze(*x) for x in cases],
      "guards":[
        "No-reread signature bits are exact finite state-class counts for this declared challenge family, not SAT runtime lower bounds.",
        "Static full reread/recomputation is explicitly available and defeats any generic reacquisition-hardness inference.",
        "Finite parameter controls do not establish asymptotic SU/vMS behavior or exact vMS internal binary sampler uniqueness.",
        "P versus NP remains open."
      ]}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
