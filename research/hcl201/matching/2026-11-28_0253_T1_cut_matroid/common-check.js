
function pairClosure(F,cap=1000000){
 let f=F.map(x=>({...x})),visits=0,changed=true,rounds=0,removed=0,proof=[];
 while(changed){changed=false;rounds++;let d=new Map();
 for(let i=0;i<f.length;i++){let x=f[i];if(x.m===0n)return {status:"UNSAT",visits,rounds,removed,proof};for(let a=0;a<x.s.length;a++)for(let b=a;b<x.s.length;b++){let s=a===b?[x.s[a]]:[x.s[a],x.s[b]],key=s.join(","),m=0;for(let w=0;w<2**x.s.length;w++){if(++visits>cap)return {status:"UNKNOWN-CAP",visits,rounds,removed,proof};if(bit(x.m,w))m|=1<<(((w>>a)&1)+(a===b?0:2*((w>>b)&1)))}let r=d.get(key);if(!r)r={s,m,owners:[i]};else{r.m&=m;r.owners.push(i)}d.set(key,r)}}
 for(let i=0;i<f.length;i++){let x=f[i],old=x.m;for(let a=0;a<x.s.length;a++)for(let b=a;b<x.s.length;b++){let key=(a===b?[x.s[a]]:[x.s[a],x.s[b]]).join(","),r=d.get(key);for(let w=0;w<2**x.s.length;w++){if(++visits>cap)return {status:"UNKNOWN-CAP",visits,rounds,removed,proof};if(bit(x.m,w)&&!(r.m&(1<<(((w>>a)&1)+(a===b?0:2*((w>>b)&1)))))){x.m&=~(1n<<BigInt(w));removed++}}}if(x.m!==old){changed=true;proof.push([rounds,i,old.toString(16),x.m.toString(16)])}if(!x.m)return {status:"UNSAT",visits,rounds,removed,proof}}
 }return {status:"SURVIVES",visits,rounds,removed,proof,factors:serial(f)}
}
function common(compile,corpus,reg){let r=experiment(compile,corpus,reg);for(let a of r)for(let k of ["native","cnf"]){let f=a[k].artifact.residual.map(([s,h,o])=>({s,m:BigInt("0x"+h),o}));a[k].pairs=pairClosure(f);a[k].pairGuarded=a[k].artifact.guards.map(g=>{let z=pack([...f,...g.guard.map(([v,b])=>({s:[v],m:1n<<BigInt(b),o:[]}))]);return {guard:g.guard,result:pairClosure(z,100000)}})}return r}
