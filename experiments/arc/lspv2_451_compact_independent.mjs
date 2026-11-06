// LSPV-2/451 independent graph-vs-original-CNF UP controls, Node 18+.
// No FLMV native machine trace and no unrestricted computational lower bound.
const assert=(ok,msg)=>{if(!ok)throw Error(msg||'assertion failed')};
const graphs=[
 ['K4',4,Array.from({length:4},(_,a)=>Array.from({length:4-a-1},(_,j)=>[a,a+j+1])).flat(),1],
 ['cube',8,Array.from({length:8},(_,a)=>Array.from({length:7-a},(_,j)=>a+j+1).filter(b=>{let z=a^b;return z&&!(z&(z-1))}).map(b=>[a,b])).flat(),2],
 ['Petersen',10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i+5,((i+2)%5)+5]),...Array.from({length:5},(_,i)=>[i,i+5])],3]
];
function cnf(H,edges,charge){
 const ends=Array.from({length:H},()=>[]);
 edges.forEach(([a,b],i)=>{ends[a].push(i+1);ends[b].push(i+1)});
 assert(ends.every(x=>x.length===3),'degree');
 const clauses=[];
 for(let v=0;v<H;v++)for(let mask=0;mask<8;mask++){
  const bits=[0,1,2].map(i=>(mask>>i)&1);
  if((bits[0]^bits[1]^bits[2])!==charge[v]){
   clauses.push(ends[v].map((e,i)=>bits[i]?-e:e));
  }
 }
 assert(clauses.length===4*H,'clause count');return clauses;
}
function up(clauses,seed){
 const a=new Map(seed);let forces=0;
 for(;;){let change=false;
  for(const C of clauses){let unknown=[],sat=false;
   for(const lit of C){const z=Math.abs(lit);
    if(!a.has(z))unknown.push(lit);
    else if(a.get(z)===(lit>0)){sat=true;break}
   }
   if(sat)continue;
   if(unknown.length===0)return [false,a,forces];
   if(unknown.length===1){const lit=unknown[0],z=Math.abs(lit),b=lit>0;
    if(a.has(z)){if(a.get(z)!==b)return [false,a,forces]}
    else{a.set(z,b);forces++;change=true;break}
   }
  }
  if(!change)return [true,a,forces];
 }
}
function treeCount(H,edges,S){
 const adj=Array.from({length:H},()=>[]);let seen=new Set(),r=0,cyc=0;
 edges.forEach(([a,b],i)=>{if(S.has(i+1))return;adj[a].push(b);adj[b].push(a)});
 for(let x=0;x<H;x++)if(!seen.has(x)){
  let n=0,degrees=0,stack=[x];seen.add(x);
  while(stack.length){let v=stack.pop();n++;degrees+=adj[v].length;
   for(const w of adj[v])if(!seen.has(w)){seen.add(w);stack.push(w)}
  }
  if(degrees/2===n-1)r++;else cyc++;
 }
 assert(cyc>0,'cyclic component');return r;
}
let checked=0;let rows=[];
for(const [name,H,E,k] of graphs)for(let parity=0;parity<=1;parity++){
 const charge=Array(H).fill(0);charge[0]=parity;const C=cnf(H,E,charge);
 const sets=[Array.from({length:k},(_,i)=>i+1)];
 if(k===3)sets.push(E.map(([a,b],i)=>(a===0||b===0)?i+1:0).filter(Boolean));
 for(const S of sets){const r=treeCount(H,E,new Set(S));let open=0,forced=0;
  for(let mask=0;mask<(1<<k);mask++){
   const start=S.map((e,i)=>[e,!!(mask&(1<<i))]);const [alive,a,t]=up(C,start);
   assert(t<=2*k,'UP forced > 2k');checked++;
   if(alive){open++;forced+=t;
    const untouched=C.filter(c=>c.every(l=>!a.has(Math.abs(l)))).length;
    assert(untouched>=4*Math.max(0,H-6*k),'untouched');checked++;
   }
  }
  assert(open===2**(k-r),'rank count');checked++;
  rows.push({name,parity,k,r,open,forced});
 }
}
console.log(JSON.stringify({checks:checked,rows}));
