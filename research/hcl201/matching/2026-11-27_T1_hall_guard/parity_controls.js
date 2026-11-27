// node parity_controls.js (uses same matchingCNF as replay.js; standalone)
function sha(s){
 const K=Uint32Array.from(Array.from({length:64},(_,i)=>{let n=2,c=-1;for(;;n++){let p=true;for(let d=2;d*d<=n;d++)if(n%d===0){p=false;break}if(p&&++c===i)return Math.floor((Math.cbrt(n)%1)*4294967296)}}));
 let H=Uint32Array.from([0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]);
 const b=new Uint8Array(Math.ceil((s.length+9)/64)*64); for(let i=0;i<s.length;i++){if(s.charCodeAt(i)>127)throw Error("non ASCII");b[i]=s.charCodeAt(i)}b[s.length]=128;let dv=new DataView(b.buffer);dv.setUint32(b.length-4,s.length*8);dv.setUint32(b.length-8,Math.floor(s.length*8/4294967296));
 const rr=(x,n)=>(x>>>n)|(x<<(32-n));const w=new Uint32Array(64);
 for(let j=0;j<b.length;j+=64){for(let i=0;i<16;i++)w[i]=dv.getUint32(j+4*i);for(let i=16;i<64;i++){let x=w[i-15],y=w[i-2];w[i]=w[i-16]+(rr(x,7)^rr(x,18)^(x>>>3))+w[i-7]+(rr(y,17)^rr(y,19)^(y>>>10))}
 let [a,c,d,e,f,g,h,l]=H;for(let i=0;i<64;i++){let t1=(l+(rr(f,6)^rr(f,11)^rr(f,25))+((f&g)^(~f&h))+K[i]+w[i])>>>0,t2=((rr(a,2)^rr(a,13)^rr(a,22))+((a&c)^(a&d)^(c&d)))>>>0;l=h;h=g;g=f;f=(e+t1)>>>0;e=d;d=c;c=a;a=(t1+t2)>>>0} [a,c,d,e,f,g,h,l].forEach((x,i)=>H[i]+=x)}
 return Array.from(H,x=>x.toString(16).padStart(8,"0")).join("")
}
function matchingCNF(x){
 const C=x.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));
 const neg=new Set(C.filter(c=>c.length===2&&c.every(x=>x<0)).map(c=>c.map(x=>-x).sort((a,b)=>a-b).join(",")));
 const groups=C.map((c,i)=>({c,i:i+1})).filter(({c})=>c.length>=2&&c.every(v=>v>0)&&c.every((a,i)=>c.slice(i+1).every(b=>neg.has([a,b].sort((a,b)=>a-b).join(",")))));
 const parts=[];let remaining=groups.slice();while(remaining.length){let used=new Set(),part=[],rest=[];for(const g of remaining){if(g.c.some(v=>used.has(v)))rest.push(g);else{part.push(g);g.c.forEach(v=>used.add(v))}}if(used.size!==x.nvars)return {status:"UNKNOWN",reason:"no partition into authenticated exact-one groups",groups:groups.length};parts.push(part);remaining=rest}
 if(parts.length!==3||parts.some(p=>p.length!==parts[0].length))return {status:"UNKNOWN",reason:"no three equal partitions",groups:groups.length};
 let loc=parts.map(p=>{let z={};p.forEach((g,i)=>g.c.forEach(v=>z[v]=i));return z});
 let ev=0,proof=[],calls=0;
 // matching failure has a Hall witness using alternating reachable vertices
 function hall(live,a,b,forced){let k=parts[a].length,banA=forced?loc[a][forced]:-1,banB=forced?loc[b][forced]:-1,adj=Array.from({length:k},()=>[]);
 for(let v of live){ev++;let i=loc[a][v],j=loc[b][v];if(i!==banA&&j!==banB&&!adj[i].includes(j))adj[i].push(j)}
 let mr=Array(k).fill(-1),ml=Array(k).fill(-1);
 function aug(i,seen){for(let j of adj[i]){ev++;if(seen.has(j))continue;seen.add(j);if(mr[j]===-1||aug(mr[j],seen)){mr[j]=i;ml[i]=j;return true}}return false}
 for(let i=0;i<k;i++)if(i!==banA)aug(i,new Set());
 let U=[];for(let i=0;i<k;i++)if(i!==banA&&ml[i]===-1)U.push(i);if(!U.length)return null;
 const L=new Set(U),B=new Set();for(let i of L)for(let j of adj[i]){ev++;B.add(j);if(mr[j]>=0)L.add(mr[j])}
 if(B.size>=L.size)throw Error("bad Hall");return {a,b,forced:forced||0,L:[...L].sort((a,b)=>a-b),B:[...B].sort((a,b)=>a-b)}
 }
 function checkHall(live,h){const {a,b,forced,L,B}=h;let actual=new Set();for(let v of live){if(forced&&(loc[a][v]===loc[a][forced]||loc[b][v]===loc[b][forced]))continue;if(L.includes(loc[a][v]))actual.add(loc[b][v])}if(B.length>=L.length||actual.size!==B.length||B.some(j=>!actual.has(j))||new Set(L).size!==L.length||forced&&L.includes(loc[a][forced]))throw Error("certificate mismatch")}
 function closure(live){let deletes=[];for(;;){let drop=null;for(let [a,b] of [[0,1],[0,2],[1,2]]){calls++;let h=hall(live,a,b,0);if(h){checkHall(live,h);return {live,deletes,fail:h}}for(let v of live){calls++;h=hall(live,a,b,v);if(h){checkHall(live,h);drop={v,h};break}}if(drop)break}if(!drop)return {live,deletes};deletes.push(drop);live=live.filter(v=>v!==drop.v)}}
 let initial=Array.from({length:x.nvars},(_,i)=>i+1),r=closure(initial);proof.push({guard:[],...r});let rootDeleted=r.deletes.length,guardCuts=0;
 while(!r.fail){let rejected=null;for(let v of r.live){let guarded=r.live.filter(w=>w===v||loc.every(l=>l[w]!==l[v]));let t=closure(guarded);if(t.fail){rejected=v;proof.push({guard:[v],...t});guardCuts++;break}}if(rejected===null)break;r=closure(r.live.filter(v=>v!==rejected));proof.push({guard:[],rejected,...r})}
 return {status:r.fail?"UNSAT":"UNKNOWN",groups:parts.map(p=>p.map(g=>g.i)),rootDeleted,guardCuts,remaining:r.live,calls,ev,proof};
}
function generate(k,neighbor){const n=2*k,E=[];for(let a=0;a<n;a++)for(let b=0;b<n;b++)for(let c=0;c<n;c++)if(((a>=k)^(b>=k)^(c>=k))===0)E.push([a,b,c]);if(neighbor)E.push([k,k,k]);E.sort((a,b)=>a[0]-b[0]||a[1]-b[1]||a[2]-b[2]);return {format:"3DM-EXPLICIT-v1",n,triples:E}}
function cnf(G){let C=[];for(let j=0;j<3;j++)for(let a=0;a<G.n;a++){let group=G.triples.map((e,i)=>e[j]===a?i+1:0).filter(Boolean);C.push(group);for(let i=0;i<group.length;i++)for(let h=i+1;h<group.length;h++)C.push([-group[i],-group[h]])}return {nvars:G.triples.length,dimacs:`p cnf ${G.triples.length} ${C.length}\n`+C.map(c=>c.join(" ")+" 0").join("\n")+"\n"}}
function satWitness(k){let remain=Array.from({length:3},()=>[Array.from({length:k},(_,i)=>i),Array.from({length:k-1},(_,i)=>i+k+1)]),W=[[k,k,k]];for(const pattern of [[0,1,1],[1,0,1],[1,1,0]])for(let t=0;t<(k-1)/2;t++)W.push(pattern.map((b,i)=>remain[i][b].pop()));while(remain[0][0].length)W.push(remain.map(r=>r[0].pop()));return W}
for(const b of [false,true]){const G=generate(3,b),s=JSON.stringify(G)+"\n",C=cnf(G);console.log(JSON.stringify({id:sha(s),N:s.length*8,matching:matchingCNF(C),witness:b?satWitness(3):null}))}
