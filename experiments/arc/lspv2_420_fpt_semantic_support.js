/* LSPV-2/420. Deterministic FPT checker for essential support of paid 2-input gate DAGs.
   Pure JS ES2020. No SAT oracle, dependencies or native exported-wire assumptions. */
function bit(f,a,b){return (f>>(a+2*b))&1}
function nl(f){return (f^(f>>1)^(f>>2)^(f>>3))&1}
function affine(f,A,B){let c=f&1,p=bit(f,1,0)^c,q=bit(f,0,1)^c;return {m:(p?A.m:0n)^(q?B.m:0n),c:c^(p?A.c:0)^(q?B.c:0)}}
function solvable(eqs){let piv=new Map();for(let e of eqs){let m=e.m,c=e.c;while(m){let b=m&-m,old=piv.get(b);if(!old){piv.set(b,{m,c});break}m^=old.m;c^=old.c}if(!m&&c)return false}return true}
function checkSyntax(C){let {n,gates,output}=C;if(!Number.isSafeInteger(n)||n<1||!Array.isArray(gates)||!Number.isSafeInteger(output)||output<0||output>=n+gates.length)throw Error("shape");for(let i=0;i<gates.length;i++){let g=gates[i];if(!Number.isSafeInteger(g.a)||!Number.isSafeInteger(g.b)||g.a<0||g.b<0||g.a>=n+i||g.b>=n+i||!Number.isInteger(g.f)||g.f<0||g.f>15)throw Error("illegal paid DEF")}}
function fpt(C){
  checkSyntax(C);let {n,gates,output}=C, nonlinear=gates.filter(g=>nl(g.f)).length;let active=new Set(),seen=new Set(),stack=[output];
  while(stack.length){let u=stack.pop();if(seen.has(u))continue;seen.add(u);if(u<n)active.add(u);else{let g=gates[u-n];stack.push(g.a,g.b)}}
  let support=[], attempts=0;
  for(let j of [...active].sort((a,b)=>a-b)){let found=false;
    for(let guess=0;guess<16**nonlinear;guess++){attempts++;let left=[],right=[],eqs=[],k=0;
      for(let i=0;i<n;i++){left.push({m:1n<<BigInt(i),c:0});right.push({m:1n<<BigInt(i),c:i===j?1:0})}
      for(let g of gates){let A=left[g.a],B=left[g.b],C=right[g.a],D=right[g.b];
        if(nl(g.f)){let nib=Math.floor(guess/(16**k))%16;k++;let a=nib&1,b=(nib>>1)&1,c=(nib>>2)&1,d=(nib>>3)&1;
          eqs.push({m:A.m,c:A.c^a},{m:B.m,c:B.c^b},{m:C.m,c:C.c^c},{m:D.m,c:D.c^d});
          left.push({m:0n,c:bit(g.f,a,b)});right.push({m:0n,c:bit(g.f,c,d)});
        }else{left.push(affine(g.f,A,B));right.push(affine(g.f,C,D))}
      }
      let x=left[output],y=right[output];eqs.push({m:x.m^y.m,c:1^x.c^y.c});
      if(solvable(eqs)){found=true;break}
    }
    if(found)support.push(j)
  }
  return {support,nonlinear,active:active.size,attempts};
}
function evalC(C,x){let v=[];for(let i=0;i<C.n;i++)v.push((x>>i)&1);for(let g of C.gates)v.push(bit(g.f,v[g.a],v[g.b]));return v[C.output]}
function brute(C){let S=[];for(let j=0;j<C.n;j++){for(let x=0;x<(1<<C.n);x++){if(evalC(C,x)!==evalC(C,x^(1<<j))){S.push(j);break}}}return S}
function audit(){
  let seed=4201337,checks=0,hist={},cases=0,maxAttempts=0;
  function rng(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
  function eq(x,y){checks++;if(JSON.stringify(x)!==JSON.stringify(y))throw Error("FPT/BRUTE MISMATCH "+JSON.stringify({x,y}))}
  function test(C){let r=fpt(C);eq(r.support,brute(C));hist[r.nonlinear]=(hist[r.nonlinear]||0)+1;cases++;maxAttempts=Math.max(maxAttempts,r.attempts);return r}
  for(let n=1;n<=5;n++)for(let a=0;a<n;a++)for(let b=0;b<n;b++)for(let f=0;f<16;f++)test({n,gates:[{a,b,f}],output:n});
  const oneGate=cases;
  for(let n=2;n<=5;n++)for(let count=0;count<100;count++){
     let gates=[],k=0,size=1+rng()%7;
     for(let i=0;i<size;i++){
       let a=rng()%(n+i),b=rng()%(n+i),f=rng()%16;
       if(nl(f)&&k>=3)f^=8;
       if(nl(f))k++;gates.push({a,b,f})
     }
     test({n,gates,output:n+gates.length-1})
  }
  const guard=(contradiction)=>{
     let n=6,gates=[{a:0,b:1,f:8}],z=6;
     if(contradiction){gates.push({a:6,b:6,f:6});z=7}
     for(let i=2;i<6;i++){gates.push({a:z,b:i,f:8});z=n+gates.length-1}
     return {n,gates,output:z}
  };
  const pos=test(guard(false)),neg=test(guard(true));
  eq(pos.support,[0,1,2,3,4,5]);eq(neg.support,[]);
  let bad=0;
  for(let C of [{n:1,gates:[{a:1,b:0,f:8}],output:1},{n:1,gates:[{a:0,b:0,f:16}],output:1},{n:1,gates:[],output:2}]){try{fpt(C)}catch(e){bad++}}
  eq(bad,3);
  return {version:"LSPV2-420-FPT-ESS-SUPPORT",kind:"deterministic/exhaustive small truth tables",seed:4201337,oneGate,cases,checks,hist,maxAttempts,invalid_rejected:bad,guardSAT:pos.support,guardUNSAT:neg.support,provenance:"syntactically legal paid total two-input DEF DAGs; no LOCAL or equation export",status:"finite computation supports independent theorem; B3 and P-vs-NP OPEN"};
}

/* Run in Node.js: console.log(JSON.stringify(audit(),null,2)); */
if (typeof module !== 'undefined' && typeof require !== 'undefined' && require.main === module) console.log(JSON.stringify(audit(),null,2));
