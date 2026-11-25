function run(){
 const stats={assertions:0,scans:0,owners:0,rows:0,branches:0,leaves:0,contradictions:0,referenceWords:0};
 function ok(x){stats.assertions++;if(!x)throw Error("assertion "+stats.assertions)}
 function compile(n,cnf){
  let nv=n+1;const C=[],gates=[];const r=1;const fresh=()=>++nv;
  const add=(a,b,c)=>{ok(new Set([Math.abs(a),Math.abs(b),Math.abs(c)]).size===3);C.push([a,b,c])};
  function copy(a){const z=fresh();add(a,-z,r);add(-a,z,r);gates.push(["copy",z,a]);return z}
  function and(a,b){if(Math.abs(a)===Math.abs(b))b=copy(b);const z=fresh();add(a,b,-z);add(-z,a,r);add(-z,b,r);gates.push(["and",z,a,b]);return z}
  const or=(a,b)=>-and(-a,-b);
  const lit=a=>Math.sign(a)*(Math.abs(a)+1);
  const t=cnf.map(c=>c.map(lit).reduce(or)).reduce(and);
  const u=fresh(),b=or(-t,u);
  add(u,b,r);
  const D=C.map(c=>c.slice());D[D.length-1][0]=-u;
  return {nv,C,D,u,t,gates};
 }
 const bit=i=>1n<<BigInt(i-1);
 function reduce(B,m,b){for(const [p,row,rhs] of B){if(m&p){m^=row;b^=rhs}}return [m,b]}
 function insert(B,m,b){[m,b]=reduce(B,m,b);if(!m)return b?-1:0;B.push([m&-m,m,b]);stats.rows++;return 1}
 const parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 function closure(B,C){
  restart:while(true){stats.scans++;
   for(const c of C){stats.owners++;const vars=c.map(a=>bit(Math.abs(a)));
    const local=Array.from({length:8},(_,k)=>vars.reduce((m,v,i)=>m^((k>>i&1)?v:0n),0n));
    const known=[];for(let k=1;k<8;k++){const [m,b]=reduce(B,local[k],0);if(!m)known.push([k,b])}
    const words=[];for(let w=0;w<8;w++){
     const a=c.map((l,i)=>(w>>i&1)^(l<0?1:0));if(a[0]===a[1]&&a[1]===a[2])continue;
     if(known.every(([k,b])=>parity(BigInt(k&w))===b))words.push(w)
    }
    if(!words.length){stats.contradictions++;return false}
    for(let k=1;k<8;k++){
     const b=parity(BigInt(k&words[0]));if(words.every(w=>parity(BigInt(k&w))===b)){
      const s=insert(B,local[k],b);if(s<0){stats.contradictions++;return false}if(s>0)continue restart;
     }
    }
   }
   return true;
  }
 }
 const evalLit=(x,l)=>Number(Boolean(x&bit(Math.abs(l))))^(l<0?1:0);
 function valid(x,C){return C.every(c=>{const a=c.map(l=>evalLit(x,l));return !(a[0]===a[1]&&a[1]===a[2])})}
 function count(n,C,guards=[]){
  let witness=null;
  function visit(B){if(!closure(B,C))return 0;
   let x=0n,k=0;for(let i=1;i<=n;i++){const [m,b]=reduce(B,bit(i),0);if(m){k=i;break}if(b)x|=bit(i)}
   if(!k){stats.leaves++;ok(valid(x,C));for(const [v,b] of guards)ok(evalLit(x,v)===b);if(witness===null)witness=x;return 1}
   stats.branches++;let total=0;for(const b of [0,1]){const A=B.slice();ok(insert(A,bit(k),b)===1);total+=visit(A)}return total
  }
  const B=[];insert(B,bit(1),0);if(!closure(B,C))return {z:0,w:null};
  for(const [v,b] of guards){if(insert(B,bit(v),b)<0)return {z:0,w:null};if(!closure(B,C))return {z:0,w:null}}
  const z=visit(B);if(witness!==null){const flipped=((1n<<BigInt(n))-1n)^witness;ok(valid(flipped,C))}
  return {z,w:witness===null?null:witness.toString(16)}
 }
 function ref(n,F){let z=0;for(let x=0;x<2**n;x++){stats.referenceWords++;if(F.every(c=>c.some(l=>((x>>(Math.abs(l)-1)&1)^(l<0?1:0))===1)))z++}return z}
 const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(c=>[c,c.map(x=>-x)]);
 let cases=[["unit",1,[[1]]],["contradictory",1,[[1],[-1]]],["tautology",1,[[1,-1]]],["duplicate",2,[[1,1,2],[-2]]],["Fano",7,fano],["Fano-delete",7,fano.slice(1)]];
 let seed=87201;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};
 for(let i=0;i<10;i++){const n=3+(i%2),m=2+i%5;const F=Array.from({length:m},()=>Array.from({length:3},()=>{const v=1+rnd()%n;return rnd()>>>31?v:-v}));cases.push(["random-"+i,n,F])}
 const out=[];
 for(const [name,n,F] of cases){
  const z=ref(n,F),{nv,C,D,u,t}=compile(n,F);
  const a=count(nv,C),b=count(nv,D),ag=count(nv,C,[[u,0]]),bg=count(nv,D,[[u,0]]);
  ok(a.z===2**(n+1)-z);ok(b.z===2**(n+1));ok(bg.z-ag.z===z);ok(a.w!==null&&b.w!==null);
  out.push({name,n,F,compiledVariables:nv,owners:C.length,sourceCount:z,rootCount:2*a.z,flipCount:2*b.z,guardedRootRelative:ag.z,guardedFlipRelative:bg.z,rootWitnessR0:a.w,flipWitnessR0:b.w});
 }
 for(const a of [0,1])for(const b of [0,1]){
  let zlist=[];for(const z of [0,1]){const nae=(x,y,w)=>!(x===y&&y===w);if(nae(a,b,1-z)&&nae(1-z,a,0)&&nae(1-z,b,0))zlist.push(z)}ok(zlist.length===1&&zlist[0]===(a&b))
 }
 return {seed:87201,stats,cases:out};
}
console.log(JSON.stringify(run(),null,2));
