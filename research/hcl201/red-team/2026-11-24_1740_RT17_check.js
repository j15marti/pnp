"use strict";
function run(){
 const stats={seed:174017,small:0,sat:0,unsat:0,cartesian:0,noncartesian:0,probes:0,lifts:0,assertions:0,counts:0,matrixEntries:0,gaussian:0,maxLocalLabels:0,scaling:[]};
 const assert=(x)=>{stats.assertions++;if(!x)throw Error("assertion "+stats.assertions)};
 let seed=stats.seed;const rand=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n};
 const bit=i=>1n<<BigInt(i);
 const parity=x=>{let b=0;while(x){x&=x-1n;b^=1}return b};
 const pow=n=>1n<<BigInt(n);
 function gauss(rows){stats.gaussian++;const p=new Map();for(let [a,b] of rows){while(a){let i=a.toString(2).length-1;if(!p.has(i)){p.set(i,[a,b]);break}const q=p.get(i);a^=q[0];b^=q[1]}if(!a&&b)return null}return p}
 function reduce(p,a,b=0){while(a){let i=a.toString(2).length-1;if(!p.has(i))return [a,b];let q=p.get(i);a^=q[0];b^=q[1]}return [a,b]}
 function pure(rows,mask){const p=new Map(),out=[];for(let [a,b] of rows){let v=a&~mask;while(v){let i=v.toString(2).length-1;if(!p.has(i)){p.set(i,[a,b]);break}let q=p.get(i);a^=q[0];b^=q[1];v=a&~mask}if(!v&&a)out.push([a,b]);}return out}
 function charsum(rows,q,r){const p=gauss(rows);if(!p)return 0n;const [a,b]=reduce(p,q);return a?0n:(b?-1n:1n)*pow(r-p.size)}
 function compile(node,masks){let labels=[],D=0;for(const term of node.terms){let p=gauss(term.rows);if(!p)continue;let rows=[...p.values()];let ps=node.edges.map(e=>pure(rows,masks[e]));let pool=ps.flat(),basis=gauss(pool),cross=[];for(let row of rows){if(reduce(basis,row[0])[0]){cross.push(row);pool.push(row);basis=gauss(pool)}}let k=cross.length;D=Math.max(D,k);for(let s=0;s<2**k;s++){let a=0n,b=0;for(let j=0;j<k;j++)if((s>>j)&1){a^=cross[j][0];b^=cross[j][1]}labels.push({k,c:BigInt(term.c)*(b?-1n:1n),ps,chars:node.edges.map(e=>a&masks[e])})}}
 for(let l of labels)l.c*=pow(D-l.k);stats.maxLocalLabels=Math.max(stats.maxLocalLabels,labels.length);return {labels,D}}
 function setup(width,nodes){let start=0,masks=width.map(r=>{let m=(pow(r)-1n)<<BigInt(start);start+=r;return m});let compiled=nodes.map(n=>compile(n,masks));return {width,nodes,masks,compiled,d:start}}
 function count(S,probe=0n,pins=[]){stats.counts++;let {width,nodes,masks,compiled}=S;let guards=masks.map(m=>pins.filter(([a])=>(a&m)===a));let M=null,D=0;for(let i=nodes.length-1;i>=0;i--){let {labels,D:k}=compiled[i];D+=k;let next=labels.map(l=>l.c);if(M){let e=i,ii=nodes[i].edges.indexOf(e),jj=nodes[i+1].edges.indexOf(e);for(let t=0;t<labels.length;t++){let sum=0n;let l=labels[t];for(let s=0;s<M.length;s++){let r=compiled[i+1].labels[s];stats.matrixEntries++;sum+=M[s]*charsum([...l.ps[ii],...r.ps[jj],...guards[e]],l.chars[ii]^r.chars[jj]^(probe&masks[e]),width[e])}next[t]*=sum}}M=next}let z=M.reduce((a,b)=>a+b,0n);assert(z%pow(D)===0n);return z/pow(D)}
 function val(S,x){return S.nodes.every(n=>n.terms.reduce((a,t)=>a+(t.rows.every(([m,b])=>parity(m&x)===b)?t.c:0),0)===1)}
 function brute(S){let a=[];for(let x=0n;x<pow(S.d);x++)if(val(S,x))a.push(x);return a}
 function verify(S){let a=brute(S),z=count(S);assert(z===BigInt(a.length));stats.small++;if(z)stats.sat++;else stats.unsat++;let non=S.compiled.some(n=>n.D>0);stats[non?"noncartesian":"cartesian"]++;
 // Exact root affine closure: small audit all nonzero forms; restart after each independent deduction.
 if(!z)return;
 let hull=[];let changed=true;while(changed){changed=false;for(let q=1n;q<pow(S.d);q++){if(!reduce(gauss(hull),q)[0])continue;let w=count(S,q);stats.probes++;let ref=a.reduce((v,x)=>v+(parity(q&x)?-1n:1n),0n);assert(w===ref);if(w===z||w===-z){hull.push([q,w===z?0:1]);changed=true;break}}}
 // positive-count self reduction, edge-local pins only. Coordinate closure at each guard.
 let pins=[],word=0n;for(let i=0;i<S.d;i++){let q=bit(i);let known=reduce(gauss(hull),q);let z0=count(S,0n,[...pins,[q,0]]),z1=count(S,0n,[...pins,[q,1]]);assert(z0+z1===count(S,0n,pins));let b=z0?0:1;if(!known[0])assert(b===known[1]);pins.push([q,b]);if(b)word|=q}
 assert(val(S,word));stats.lifts++;
 }
 function mk(width,kind,flip=0){let n=width.length,offset=0,first=width.map(r=>{let a=bit(offset);offset+=r;return a});let nodes=[{edges:[0],terms:[{c:1,rows:[[first[0],0]]}]}];for(let i=1;i<n;i++)nodes.push({edges:[i-1,i],terms:[{c:1,rows:[[first[i-1]^first[i],0]]}]});nodes.push({edges:[n-1],terms:[{c:1,rows:[[first[n-1],flip]]}]});return setup(width,nodes)}
 for(let k=0;k<48;k++){let width=[1+rand(3),1+rand(3)];let n=2;let masks=[pow(width[0])-1n,(pow(width[1])-1n)<<BigInt(width[0])];let nodes=[];for(let i=0;i<=n;i++){let edges=i===0?[0]:i===n?[n-1]:[i-1,i];let mask=edges.reduce((a,e)=>a|masks[e],0n);let rows=Array.from({length:1+rand(3)},()=>[BigInt(rand(2**(width[0]+width[1])))&mask,rand(2)]);let c=rand(2);nodes.push({edges,terms:c?[{c:1,rows:[]},{c:-1,rows}]:[{c:1,rows}]})}verify(setup(width,nodes))}
 // explicit Cartesian and opposite-label controls
 for(let n=2;n<=4;n++)for(let b=0;b<2;b++)verify(mk(Array(n).fill(2),0,b));
 for(let r of [8,32,128])for(let n of [4,16])for(let b=0;b<2;b++){let S=mk(Array(n).fill(r),0,b),z=count(S);assert(z===(b?0n:pow(n*(r-1))));let p=count(S,bit(0)^bit(r*(n-1)));assert(p===z);stats.scaling.push({edges:n,rank:r,flip:b,count:z.toString(),localCross:1,totalCross:n-1,ambient:S.d})}
 // exact BA11 Cartesian specialization on small explicit separable terms.
 let S=setup([2,2],[{edges:[0],terms:[{c:1,rows:[[1n,0]]}]},{edges:[0,1],terms:[{c:1,rows:[]},{c:-1,rows:[[2n,0],[4n,1]]}]},{edges:[1],terms:[{c:1,rows:[[8n,1]]}]}]);verify(S);assert(S.compiled.every(x=>x.D===0));
 return stats;
}
console.log(JSON.stringify(run(),null,2));
