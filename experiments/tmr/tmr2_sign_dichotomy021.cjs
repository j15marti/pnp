// TMR-2/021 reproducible finite sign-pivotal audit. Run: node tmr2_sign_dichotomy021.cjs
// Fixed three-distinct-variable clauses, all work counted by this test harness.
// This is a finite semantic test, NOT a deterministic SAT machine lower bound.
function run() {
  const count={formulas:0,sat:0,unsat:0,sign_flips:0,sat_pivotal:0,unsat_pivotal:0,essential_clauses:0,renamings:0};
  let rng=202611140721>>>0;
  function rand(n){rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng%n;}
  function build(n){
    const clauses=[],lookup=new Map(), masks=[],flips=[];
    const full=(1n<<BigInt(1<<n))-1n;
    function key(c){return c.map(x=>x.join(':')).join(',');}
    function mask(c){let z=0n;for(let a=0;a<(1<<n);a++)if(c.some(([v,s])=>(((a>>v)&1)^s)!==0))z|=1n<<BigInt(a);return z;}
    for(let v=0;v<n;v++)for(let w=v+1;w<n;w++)for(let z=w+1;z<n;z++)for(let b=0;b<8;b++){
      const c=[[v,b&1],[w,(b>>1)&1],[z,(b>>2)&1]];
      lookup.set(key(c),clauses.length);clauses.push(c);masks.push(mask(c));
    }
    for(const c of clauses){let f=[];for(let j=0;j<3;j++){let d=c.map(x=>x.slice());d[j][1]^=1;f.push(lookup.get(key(d)));}flips.push(f);}
    return {n,clauses,masks,flips,full};
  }
  const pools={};for(let n=3;n<=6;n++)pools[n]=build(n);
  function check(n,inds,rename=false){
    const P=pools[n],m=inds.length,{masks,full,flips}=P;
    const pre=[full],suf=new Array(m+1).fill(full);
    for(const idx of inds)pre.push(pre.at(-1)&masks[idx]);
    for(let i=m-1;i>=0;i--)suf[i]=suf[i+1]&masks[inds[i]];
    const sat=pre[m]!==0n;
    count.formulas++;count[sat?'sat':'unsat']++;
    const witnesses=new Set();
    for(let i=0;i<m;i++){
      let H=pre[i]&suf[i+1],critical=0;
      for(let j=0;j<3;j++){
        const switched=masks[flips[inds[i]][j]];
        const actual=((H&switched)!==0n)!==sat;
        const predicted=sat?((H&switched)===0n):(H!==0n);
        if(actual!==predicted)throw Error('classification mismatch '+n+','+i+','+j);
        if(actual){
          critical++;
          if(sat){count.sat_pivotal++;if((H&(full^masks[inds[i]]))!==0n)throw Error('no redundancy');}
          else count.unsat_pivotal++;
        }
        count.sign_flips++;
      }
      if(sat){if(critical>1)throw Error('SAT >1 pivot per clause');}
      else {
        if(critical!==3*Number(H!==0n))throw Error('UNSAT no all-or-none');
        if(critical){
          count.essential_clauses++;
          let a=0;while((H&(1n<<BigInt(a)))===0n)a++;
          if(witnesses.has(a))throw Error('duplicated deletion witness');
          witnesses.add(a);
        }
      }
    }
    if(rename){
      const perm=Array.from({length:n},(_,i)=>i);
      for(let i=n-1;i>0;i--){let j=rand(i+1);[perm[i],perm[j]]=[perm[j],perm[i]];}
      const msk=c=>{let z=0n;for(let a=0;a<(1<<n);a++)if(c.some(([v,s])=>(((a>>v)&1)^s)!==0))z|=1n<<BigInt(a);return z;};
      let v=full;for(const idx of inds)v&=msk(P.clauses[idx].map(([x,s])=>[perm[x],s]));
      if((v!==0n)!==sat)throw Error('renaming');
      count.renamings++;
    }
  }
  let cube=Array.from({length:8},(_,i)=>i);
  // Exactly 43,758 ordered-count canonical E3 multisets with 0..10 clauses.
  function fixedLength(prefix,start,left){if(left===0){check(3,prefix);return;}for(let i=start;i<8;i++)fixedLength([...prefix,i],i,left-1);}
  for(let m=0;m<=10;m++)fixedLength([],0,m);
  const cubeFormulas=count.formulas;
  for(const [n,cases,limit] of [[4,3000,25],[5,1500,30],[6,500,40]]){
    const size=pools[n].masks.length;
    for(let z=0;z<cases;z++){
      const m=rand(limit+1),inds=Array.from({length:m},()=>rand(size));
      check(n,inds,z%17===0);
    }
  }
  // Hostile: full cube UNSAT, duplicate cube UNSAT, unique missing signature SAT,
  // two independent UNSAT components (no 2-SAT auxiliary control in this JS file).
  check(3,cube,true);check(3,cube.flatMap(i=>[i,i]),true);
  check(3,[1,2,3,4,5,6,7,1,1,1,1],true);
  const P6=pools[6], key=c=>c.map(x=>x.join(':')).join(',');
  const map6=new Map(P6.clauses.map((c,i)=>[key(c),i]));
  const product=[];
  for(let b=0;b<8;b++)for(const base of [0,3]){
    let c=[[base,b&1],[base+1,(b>>1)&1],[base+2,(b>>2)&1]];
    product.push(map6.get(key(c)));
  }
  check(6,product,true);
  if(cubeFormulas!==43758)throw Error('E3 count');
  return {theorem:'TMR2-SCB21',status:'COMPUTATIONAL',model:'proper width-three distinct-ID sign flips',
    exhaustive_e3_max_clauses:10,exhaustive_e3_formulas:cubeFormulas,
    random_counts:{n4:3000,n5:1500,n6:500},counts:count,failed_assertions:0};
}
const result=run();
if(typeof process!=='undefined')console.log(JSON.stringify(result,null,2));
result;
