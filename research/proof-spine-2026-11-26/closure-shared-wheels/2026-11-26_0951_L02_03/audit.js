function audit(){
 let checks=0,seed=261126;const ok=(p)=>{checks++;if(!p)throw Error("assertion "+checks)};const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const bits=w=>[w>>3&1,w>>2&1,w>>1&1,w&1], pc=w=>{let s=0;while(w){s+=w&1;w>>>=1}return s};
 const masks=Array.from({length:4},(_,h)=>{let m=0;for(let n=0;n<2;n++)for(let w=0;w<2;w++)m|=1<<(8*n+4*w+2*(n|((h>>w)&1))+w);return m});
 const words=Array.from({length:16},(_,i)=>bits(i));let tableComplements=0;
 for(let m=0;m<65536;m++)if(pc(m)===4)for(let i=0;i<16;i++){ok((pc(m&~(1<<i))>=4)===!(m>>i&1));tableComplements++}
 const mate=[];for(let i=0;i<16;i++){let sig=masks.map(m=>m>>i&1);mate[i]=sig.every(v=>v===0)?-2:sig.every(v=>v===1)?-1:masks.map((_,j)=>j).length; if(mate[i]===4)mate[i]=Array.from({length:16},(_,j)=>j).find(j=>masks.every(m=>((m>>j&1)+(m>>i&1))===1));ok(mate[i]!==undefined);for(const m of masks)ok((mate[i]===-2?1:mate[i]===-1?0:m>>mate[i]&1)===1-(m>>i&1))}
 function grid(n,cs){const k=Math.max(2,n,cs.length);let h=new Uint8Array(k*k);for(let j=0;j<k;j++)if(j>=cs.length)h[j]=3;else for(let lit of cs[j])h[(Math.abs(lit)-1)*k+j]|=lit>0?2:1;return {k,h,t:Array.from(h,x=>masks[x])}}
 function cnf(n,cs){let count=0;for(let a=0;a<2**n;a++)if(cs.every(c=>c.some(l=>Boolean(a>>(Math.abs(l)-1)&1)===(l>0))))count++;return count}
 function frontier(g){let st=new Map([[0,1n]]);for(let i=0;i<g.k;i++){let nx=new Map();for(const [v,c] of st)for(let w=0;w<2;w++){let s=0;for(let j=0;j<g.k;j++){let n=v>>j&1;let possible=[0,1].filter(b=>g.t[i*g.k+j]>>(8*n+4*w+2*b+w)&1);ok(possible.length===1);s|=possible[0]<<j}nx.set(s,(nx.get(s)||0n)+c)}st=nx}return st.get((1<<g.k)-1)||0n}
 let small=0,sat=0,unsat=0;
 for(let z=0;z<240;z++){let n=1+rnd(4),m=rnd(7),cs=Array.from({length:m},()=>Array.from({length:rnd(5)},()=>{let l=1+rnd(n);return rnd(2)?l:-l}));let g=grid(n,cs),c=cnf(n,cs);ok(frontier(g)===BigInt(c)*(1n<<BigInt(g.k-n)));small++;c?sat++:unsat++}
 function ids(k,i,j){let base=k*(k+1);return [base+i*k+j,i*(k+1)+j+1,base+(i+1)*k+j,i*(k+1)+j]}
 function closure(g){let k=g.k,d=new Uint8Array(2*k*(k+1)).fill(3),base=k*(k+1);for(let j=0;j<k;j++){d[base+j]=1;d[base+k*k+j]=2}let rounds=0,changed=true;while(changed){changed=false;rounds++;for(let i=0;i<k;i++)for(let j=0;j<k;j++){let e=ids(k,i,j),t=g.t[i*k+j],sup=[0,0,0,0];for(let w=0;w<16;w++)if((t>>w&1)&&e.every((a,b)=>d[a]&(1<<words[w][b])))for(let b=0;b<4;b++)sup[b]|=1<<words[w][b];for(let b=0;b<4;b++){let old=d[e[b]];d[e[b]]&=sup[b];if(!d[e[b]])return {d,rounds,empty:true};if(old!==d[e[b]])changed=true}}}return {d,rounds,empty:false}}
 function pair(b,yes){let cs=[];for(let q=0;q<b;q++)for(let s=0;s<8;s++){let p=s===7&&(yes||q>0)?6:s;cs.push(Array.from({length:3},(_,j)=>(3*q+j+1)*(p>>j&1?-1:1)))}return grid(3*b,cs)}
 function assignment(g,w,second=null){let k=g.k,a=new Uint8Array(2*k*(k+1)),base=k*(k+1);for(let i=0;i<k;i++)for(let j=0;j<=k;j++)a[i*(k+1)+j]=w[i];for(let j=0;j<k;j++){let t=0,seen=0;for(let i=0;i<k;i++){let h=g.h[i*k+j];if(second===null)t|=h>>w[i]&1;else if(h){seen++;t=seen===1?h>>w[i]&1:seen===2?second[j]:1}a[base+(i+1)*k+j]=t}}return a}
 function verify(g,a,allowed=null){let k=g.k;for(let i=0;i<k;i++)for(let j=0;j<k;j++){let e=ids(k,i,j),word=e.reduce((v,x)=>2*v+a[x],0);if(!((allowed?allowed[i*k+j]:g.t[i*k+j])>>word&1))return false}return Array.from({length:k},(_,j)=>a[k*(k+1)+j]===0&&a[k*(k+1)+k*k+j]===1).every(Boolean)}
 const cache=new Map();
 function affmask(m,p){let key=p+":"+m;if(cache.has(key))return cache.get(key);let vals=words.filter((_,i)=>m>>i&1),out=65535;for(let z=0;z<p**4;z++){let c=[],v=z;for(let j=0;j<4;j++){c.push(v%p);v=Math.floor(v/p)}let dot=w=>w.reduce((s,x,j)=>s+x*c[j],0)%p,r=dot(vals[0]);if(vals.every(w=>dot(w)===r))for(let j=0;j<16;j++)if(dot(words[j])!==r)out&=~(1<<j)}cache.set(key,out);return out}
 let scales=[],affineWitnesses=0;
 for(let b of [1,2,4,8,16]){let rec={blocks:b,k:8*b};for(let yes of [false,true]){let g=pair(b,yes),r=closure(g);ok(!r.empty);let k=g.k,base=k*(k+1);for(let i=0;i<k;i++)for(let j=0;j<=k;j++)ok(r.d[i*(k+1)+j]===3);for(let j=0;j<k;j++){let active=[];for(let i=0;i<k;i++)if(g.h[i*k+j])active.push(i);ok(active.length===3);for(let i=0;i<=k;i++)ok(r.d[base+i*k+j]===(i<=active[0]?1:i>active[2]?2:3))}
 let a=assignment(g,new Uint8Array(k).fill(1));ok(verify(g,a)===yes);if(b<=2)ok(frontier(g)===(yes?1n<<BigInt(k-3*b):0n));
 if(b<=8)for(let p of [2,3]){let al=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++){let e=ids(k,i,j),m=g.t[i*k+j];for(let word=0;word<16;word++)if(!e.every((x,z)=>r.d[x]&(1<<words[word][z])))m&=~(1<<word);al.push(affmask(m,p))}
 let supp=new Uint8Array(r.d.length);for(let v=-1;v<2*k;v++){let w=new Uint8Array(k),s=new Uint8Array(k);if(v>=0&&v<k)w[v]=1;else if(v>=k)s[v-k]=1;let a=assignment(g,w,s);ok(verify(g,a,al));for(let i=0;i<a.length;i++)supp[i]|=1<<a[i];affineWitnesses++}ok(supp.every((x,i)=>x===r.d[i]))}
 rec[yes?"yes":"no"]={closureRounds:r.rounds,freePhysicalEdges:r.d.filter(v=>v===3).length};}scales.push(rec)}
 let circuitTests=0;for(let z=0;z<100;z++){let g=[];for(let i=0;i<40;i++){let op=rnd(3),a=rnd(64+i),b=rnd(64+i);g.push([op,a,b])}for(let trial=0;trial<40;trial++){let m=Array.from({length:4},()=>masks[rnd(4)]),x=Array.from({length:64},(_,i)=>m[i>>4]>>(i&15)&1),dual=x.map((v,i)=>{let j=mate[i&15];return j===-2?1:j===-1?0:m[i>>4]>>j&1});for(let [op,a,b] of g){let p=x[a],q=x[b],u=dual[a],v=dual[b];x.push(op===0?p&q:op===1?p|q:1-p);dual.push(op===0?u|v:op===1?u&v:p);ok(dual.at(-1)===1-x.at(-1))}circuitTests++}}
 return {seed:261126,checks,tableComplements,masks:masks.map(m=>m.toString(16)),mate,small,sat,unsat,scales,affineWitnesses,circuitTests};
}
console.log(JSON.stringify(audit(), null, 2));
