'use strict';
// TMR-1/094. Exhaustive finite certificate for unary automorphisms and
// translation-equivariant binary candidates, plus independent positive tests.
// The proof that EVERY polymorphism is translation equivariant and a shifted
// projection is in the separate manuscript; exhaustive tests are computational.
const MOD=5; const S=new Set([1,3]);
const mod=(x)=>((x%MOD)+MOD)%MOD;
const beat=(a,b)=>S.has(mod(b-a));
let assertions=0;
function check(ok,msg){assertions++;if(!ok)throw Error('FAILED '+msg);}
function permutations(a){if(!a.length)return [[]];const out=[];for(let i=0;i<a.length;i++)for(const rest of permutations(a.slice(0,i).concat(a.slice(i+1))))out.push([a[i],...rest]);return out;}
const perms=permutations([0,1,2,3,4]);
let autos=[];
for(const p of perms){let good=true;for(let a=0;a<5;a++)for(let b=0;b<5;b++){
  if(beat(a,b)!==beat(p[a],p[b]))good=false;
} if(good)autos.push(p);}
check(autos.length===5,'automorphism count');
for(const p of autos)check(p.every((v,i)=>v===mod(i+p[0])),'each automorphism a rotation');
// Every f(a,b)=a+h(b-a) is simultaneously translation equivariant. Exhaust
// all 5^5 offset tables h and compare with the predicted ten polymorphisms.
const accepted=[];
for(let id=0;id<3125;id++){
  const h=[];let t=id;for(let i=0;i<5;i++){h.push(t%5);t=Math.floor(t/5);}
  const f=(a,b)=>mod(a+h[mod(b-a)]);
  let good=true;
  for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(const da of [1,3])for(const db of [1,3]){
    if(!beat(f(a,b),f(mod(a+da),mod(b+db))))good=false;
  }
  if(good){accepted.push(h);const isP0=h.every(z=>z===h[0]);const isP1=h.every((z,d)=>z===mod(h[0]+d));check(isP0||isP1,'no unexpected binary polymorphism');}
}
check(accepted.length===10,'precisely ten binary polymorphisms');
for(let c=0;c<5;c++){
  check(accepted.some(h=>h.every(z=>z===c)),'first projection offset '+c);
  check(accepted.some(h=>h.every((z,d)=>z===mod(c+d))),'second projection offset '+c);
}
// Verify candidate polymorphisms directly in arities 1..5 by checking every
// input tuple and every simultaneous permitted beat increment. No assumption
// about noncandidate operations is made by this positive control.
const arityChecks={};
for(let k=1;k<=5;k++){
  let tuples=5**k, moves=2**k, checks=0;
  for(let i=0;i<k;i++)for(let c=0;c<5;c++){
    for(let code=0;code<tuples;code++){
      const x=[];let a=code;for(let j=0;j<k;j++){x.push(a%5);a=Math.floor(a/5);}
      for(let mask=0;mask<moves;mask++){
        const y=x.map((v,j)=>mod(v+((mask>>j)&1?3:1)));
        check(beat(mod(x[i]+c),mod(y[i]+c)),`projection ${k},${i},${c},${code},${mask}`);
        checks++;
      }
    }
  }
  arityChecks[k]=checks;
}
// For k=3, none of the 15 candidate operations obeys idempotent WNU:
// f(y,x,x)=f(x,y,x)=f(x,x,y) for all x,y, because any projection fails.
let wnu3=0;
for(let i=0;i<3;i++)for(let c=0;c<5;c++){
  const f=(x)=>mod(x[i]+c);
  let idempotent=true,weak=true;
  for(let x=0;x<5;x++)for(let y=0;y<5;y++){
    if(f([x,x,x])!==x)idempotent=false;
    const v=[[y,x,x],[x,y,x],[x,x,y]].map(z=>f(z));
    if(!v.every(z=>z===v[0]))weak=false;
  }
  if(idempotent&&weak)wnu3++;
}
check(wnu3===0,'no ternary WNU among classified candidates');
const result={case:'TMR-1/094',template:'Z5; delta in {1,3}',automorphisms:autos.length,
 binary_equivariant_tables:3125,binary_polymorphisms:accepted.length,
 expected_all_k_arity:k=>5*k,candidate_direct_checks:arityChecks,ternary_wnu_candidates:wnu3,assertions,failures:0,
 caveat:'Computational finite verification. All-arity characterization requires independent symbolic proof.'};
delete result.expected_all_k_arity;
console.log(JSON.stringify(result,null,2));
