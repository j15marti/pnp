function sha(s){
 const K=[],H=[]; for(let p=2;K.length<64;p++){let prime=true;for(let i=2;i*i<=p;i++)if(p%i===0){prime=false;break}if(prime){if(H.length<8)H.push((Math.sqrt(p)%1*4294967296)|0);K.push((Math.cbrt(p)%1*4294967296)|0)}}
 const l=s.length, len=((l+9+63)>>6)<<6, b=new Uint8Array(len);for(let i=0;i<l;i++){if(s.charCodeAt(i)>127)throw Error("ASCII only");b[i]=s.charCodeAt(i)}b[l]=128;let z=l*8;for(let i=0;i<6;i++){b[len-1-i]=z%256;z=Math.floor(z/256)}
 const w=new Int32Array(64),rot=(x,n)=>(x>>>n)|(x<<(32-n));for(let q=0;q<len;q+=64){for(let i=0;i<16;i++)w[i]=(b[q+4*i]<<24)|(b[q+4*i+1]<<16)|(b[q+4*i+2]<<8)|b[q+4*i+3];for(let i=16;i<64;i++){let a=w[i-15],c=w[i-2];w[i]=(w[i-16]+(rot(a,7)^rot(a,18)^(a>>>3))+w[i-7]+(rot(c,17)^rot(c,19)^(c>>>10)))|0}let [a,c,d,e,f,g,h,j]=H;for(let i=0;i<64;i++){let t=(j+(rot(f,6)^rot(f,11)^rot(f,25))+((f&g)^(~f&h))+K[i]+w[i])|0,u=((rot(a,2)^rot(a,13)^rot(a,22))+((a&c)^(a&d)^(c&d)))|0;j=h;h=g;g=f;f=(e+t)|0;e=d;d=c;c=a;a=(t+u)|0}for(const [i,x] of [a,c,d,e,f,g,h,j].entries())H[i]=(H[i]+x)|0}return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("");
}

function compile(instance){
 const lines=instance.dimacs.trimEnd().split("\n");lines.shift();let next=instance.nvars;const F=[],parents=[];const add=(a,id)=>{F.push(a);parents.push(id)};
 lines.forEach((line,i)=>{const a=line.split(/\s+/).map(Number);a.pop();const id=i+1;if(!a.length){let v=++next;add([v,v,v],id);add([-v,-v,-v],id)}else if(a.length<=3){while(a.length<3)a.push(a[a.length-1]);add(a,id)}else{let prev=++next;add([a[0],a[1],prev],id);for(let j=2;j<a.length-2;j++){let t=++next;add([-prev,a[j],t],id);prev=t}add([-prev,a[a.length-2],a[a.length-1]],id)}});
 const types=[],used=[],edges=[],groups=new Map(),reps={},owners=[];
 const V=(t,owner)=>{types.push(t);used.push(0);owners.push(owner);return types.length-1},P=v=>4*v+used[v]++,E=(a,b,s=0)=>edges.push([a,b,s]);
 const wire=(a,b,s)=>{const v=Array.from({length:5},()=>V("E",["wire",a,b]));for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)E(P(v[i]),P(v[j]));E(a,P(v[0]),s);E(b,P(v[1]),0)};
 const occ=(id,s,p)=>{if(!groups.has(id))groups.set(id,[]);groups.get(id).push([p,s])};
 F.forEach(([a,b,c],i)=>{const L=x=>["x"+Math.abs(x),Number(x<0)],z="z"+i,T=[[L(a),L(b),[z,0]],[[z,1],L(c),["f",0]]];for(let j=0;j<2;j++)for(let k=0;k<2;k++){let v=V("B",["clause",parents[i],i,j,k]);for(const [id,s] of T[j])occ(id,s,P(v));occ("w"+i+"_"+j,0,P(v))}});
 for(const [id,O] of groups){reps[id]=O[0];if(O.length===2){wire(O[0][0],O[1][0],O[0][1]^O[1][1]);continue}const a=Array.from({length:(O.length-2)/2},()=>V("E",["carrier",id]));for(let i=1;i<a.length;i++)wire(P(a[i-1]),P(a[i]),0);let k=0;for(const v of a)while(used[v]<4){const [p,s]=O[k++];wire(P(v),p,s)}if(k!==O.length)throw Error("fanout")}
 return {network:{format:"STRICT-EB4-v1",types,edges},source_map:{original_n:instance.nvars,ternary_clauses:F,original_clause_ids:parents,representative_ports:reps,vertex_provenance:owners}};
}

function native(g){
 const n=g.types.length*4,p=Array.from({length:n},(_,i)=>i),s=new Uint8Array(n),size=new Int32Array(n).fill(1),seen=new Set(),ports=new Set();
 function f(a){if(p[a]===a)return [a,0];let [r,b]=f(p[a]);s[a]^=b;p[a]=r;return [r,s[a]]}
 function u(a,b,t){let [x,k]=f(a),[y,l]=f(b);if(x===y){if((k^l)!==t)throw Error("signed contradiction");return}if(size[x]<size[y])[x,y]=[y,x];p[y]=x;s[y]=k^l^t;size[x]+=size[y]}
 for(const [a,b,t] of g.edges){let x=a>>2,y=b>>2,k=Math.min(x,y)+":"+Math.max(x,y);if(x===y||seen.has(k)||ports.has(a)||ports.has(b)||a<0||b<0||a>=n||b>=n||![0,1].includes(t))throw Error("graph");seen.add(k);ports.add(a);ports.add(b);u(a,b,t)}
 if(ports.size!==n)throw Error("ports");
 for(let v=0;v<g.types.length;v++)if(g.types[v]==="E")for(let j=1;j<4;j++)u(4*v,4*v+j,0);else if(g.types[v]!=="B")throw Error("type");
 const ids=new Map(),rows=[],map=[];for(let i=0;i<n;i++){const [r,t]=f(i);if(!ids.has(r))ids.set(r,ids.size);map.push([ids.get(r),t])}
 for(let v=0;v<g.types.length;v++)if(g.types[v]==="B"){let x=map.slice(4*v,4*v+4).map(([i,t])=>(1n<<BigInt(i+1))^BigInt(t));rows.push({v,x})}
 return {r:ids.size,rows,map};
}

function solve(chart,mode,cap=10000000){
 let work=0;const pay=(x=1)=>{work+=x;if(work>cap)throw Error("cap")},basis=new Map(),history=[],stats=[];
 const pivot=x=>x.toString(2).length-1;
 function red(x){for(const [i,b] of [...basis.entries()].sort((a,b)=>b[0]-a[0])){pay();if((x>>BigInt(i))&1n)x^=b}return x}
 function add(x){x=red(x);if(x===1n)return -1;if(!x)return 0;basis.set(pivot(x),x);return 1}
 try{
 for(const {x} of chart.rows){if(add(x.reduce((a,b)=>a^b,0n))<0)return {status:"NO",work,stats,history};}
 const initialRank=basis.size;
 for(let epoch=0;epoch<=chart.r;epoch++){
  const forms=[],index=new Map(),clauses=[],triOwners=[],constant=0;
  const id=x=>{let a=x&~1n;if(!a)return [0,Number(x&1n)];if(!index.has(a)){index.set(a,forms.length+1);forms.push(a)}return [index.get(a),Number(x&1n)]};
  for(const {v,x} of chart.rows){let a=red(x[0]^x[1]),b=red(x[0]^x[2]),c=a^b;const A=id(a),B=id(b),C=id(c);triOwners.push([v,A,B,C]);clauses.push([A,B]);if(mode!=="single"){clauses.push([A,C],[B,C]);/* a OR b is equivalent to a OR c and b OR c jointly, BUT not individually: all three are individually equivalent on parity c=a xor b? a=b=1 => c=0, both true; a=0,b=1=> c=1; a=1,b=0=>c=1. yes. */}}
  const q=forms.length+1,L=2*q,bits=Array.from({length:L},(_,i)=>1n<<BigInt(i)),R=bits.slice(),direct=new Set();
  // literal index 2*i+value: observation i equals value. A signed form a is true when observation = 1 xor offset.
  const lit=([i,t])=>2*i+(1^t);
  let newArcs=0;function arc(a,b){pay();if(!(R[a]&bits[b])){R[a]|=bits[b];newArcs++;}direct.add(a*L+b)}
  function clause(a,b){arc(a^1,b);arc(b^1,a)}
  arc(1,0);for(const [a,b] of clauses)clause(lit(a),lit(b));
  const triples=[];if(mode==="hybrid")for(let i=0;i<forms.length;i++)for(let j=i+1;j<forms.length;j++){pay();const k=index.get(forms[i]^forms[j]);if(k>j+1)triples.push([i+1,j+1,k]);}
  let passes=0,derived=0;
  function closure(){for(let k=0;k<L;k++)for(let i=0;i<L;i++){pay();if(R[i]&bits[k])R[i]|=R[k]}}
  function has(a,b){return Boolean(R[a]&bits[b])}
  while(true){
    closure();passes++;
    for(let i=0;i<q;i++)if(has(2*i,2*i+1)&&has(2*i+1,2*i)){stats.push({epoch,rank:basis.size,forms:forms.length,triples:triples.length,passes,derived,direct:direct.size});return {status:"NO",initialRank,rank:basis.size,work,stats,history,contradiction:i}}
    if(mode!=="hybrid")break;
    let before=newArcs;
    for(const [i,j,k] of triples)for(let a=0;a<2;a++)for(let b=0;b<2;b++){
      pay();let c=a^b,A=2*i+a,B=2*j+b,C=2*k+c;
      // A joint row is impossible if any two of its literals conflict via implication or one is forced false.
      if(has(A,B^1)||has(B,A^1)||has(A,C^1)||has(C,A^1)||has(B,C^1)||has(C,B^1)||has(A,A^1)||has(B,B^1)||has(C,C^1)){
       let old=newArcs;clause(A^1,B^1);clause(A^1,C^1);clause(B^1,C^1);if(newArcs>old)derived++;
      }
    }
    if(newArcs===before)break;
  }
  let eq=[],seen=new Set();
  for(let i=1;i<q;i++){for(let a=0;a<2;a++)if(has(2*i+a,2*i+(a^1)))eq.push(forms[i-1]^BigInt(a^1));for(let j=1;j<i;j++){pay();for(let b=0;b<2;b++)if(has(2*i,2*j+b)&&has(2*j+b,2*i))eq.push(forms[i-1]^forms[j-1]^BigInt(b));}}
  let newRank=0;for(const e of eq){const k=add(e);if(k<0)return {status:"NO",initialRank,rank:basis.size,work,stats,history};if(k){newRank++;history.push(e.toString(16));}}
  stats.push({epoch,rank:basis.size,forms:forms.length,triples:triples.length,passes,derived,direct:direct.size,equations:eq.length,newRank});
  if(!newRank){
   // Assign free coordinates zero, solve triangular basis in ascending order.
   let w=1n;for(const [i,b] of [...basis.entries()].sort((a,b)=>a[0]-b[0])){let z=b&w,par=0;while(z){pay();z&=z-1n;par^=1}if(par)w|=1n<<BigInt(i)}
   const value=b=>{let z=b&w,par=0;while(z){pay();z&=z-1n;par^=1}return par};
   if(chart.rows.every(({x})=>x.reduce((a,b)=>a+value(b),0)===2))return {status:"YES",initialRank,rank:basis.size,work,stats,history,witness:w.toString(16)};
   return {status:"UNKNOWN",initialRank,rank:basis.size,work,stats,history};
  }
 }
 }catch(e){if(e.message==="cap")return {status:"UNKNOWN_CAP",rank:basis.size,work,stats,history};throw e}
}
module.exports={sha,compile,native,solve};
