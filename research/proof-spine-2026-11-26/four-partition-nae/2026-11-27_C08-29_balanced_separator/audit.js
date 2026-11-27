function audit(){
const gadget=[[0,4,11],[1,5,7],[2,6,8],[3,9,10],[0,1,6],[8,9,11],[2,7,10],[3,4,5],[1,8,10],[4,6,9],[2,5,11],[0,3,7],[4,7,8],[5,6,10],[1,3,11],[0,2,9]];
const ports=gadget[5],counts={checks:0,localWords:0,phaseWords:0,matchingTerms:0,syndromeWords:0},cap=10000000;function tick(k){counts[k]++;if(Object.values(counts).reduce((a,b)=>a+b,0)>cap)throw Error("cap")}function ck(v,m){tick("checks");if(!v)throw Error(m)}const rng=n=>Array.from({length:n},(_,i)=>i);
function nae(t,b){return t.some(v=>b(v)!==b(t[0]))}
let table=Array(8).fill(0),original=0;for(let w=0;w<4096;w++){tick("localWords");let b=v=>(w>>v)&1;if(gadget.every(t=>nae(t,b)))original++;if(gadget.every((t,i)=>i===5||nae(t,b)))table[ports.reduce((s,v,j)=>s+(b(v)<<j),0)]++}
ck(original===0&&table[0]>0&&table[7]>0&&table.slice(1,7).every(x=>x===0),"critical gadget");
function make(rows){let k=rows.length,used=rng(k).map(()=>0),native=[],part=[],cross=[];for(let j=0;j<k;j++)for(let i=0;i<16;i++)if(i!==5){native.push(gadget[i].map(v=>12*j+v));part.push(Math.floor(i/4))}
for(let row of rows){cross.push(native.length);native.push(row.map(j=>12*j+ports[used[j]++]));part.push(1)}
ck(used.every(x=>x===3),"cubic");let pairs=new Set();for(let t of native){ck(new Set(t).size===3,"distinct");for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let e=[t[i],t[j]].sort((a,b)=>a-b).join(",");ck(!pairs.has(e),"linear");pairs.add(e)}}for(let p=0;p<4;p++){let a=native.flatMap((t,i)=>part[i]===p?t:[]);ck(a.length===12*k&&new Set(a).size===12*k,"partition")}
let a=Array.from({length:12*k},()=>[]);native.forEach((t,i)=>{if(!cross.includes(i))for(let v of t)for(let u of t)a[v].push(u)});let seen=new Set(),cs=[];for(let v=0;v<a.length;v++)if(!seen.has(v)){let q=[v];seen.add(v);for(let i=0;i<q.length;i++)for(let u of a[q[i]])if(!seen.has(u)){seen.add(u);q.push(u)}cs.push(q)}ck(cs.length===k&&cs.every(t=>t.length===12),"actual components");
return {native,part,cross,cs}}
function tree(rows){let k=rows.length,adj=rng(2*k).map(()=>[]),edges=[];for(let i=0;i<k;i++)for(let j=0;j<3;j++){let e=edges.length,u=i,v=k+rows[i][j];edges.push([u,v]);adj[u].push([v,e]);adj[v].push([u,e])}
let par=Array(2*k).fill(-1),pe=Array(2*k).fill(-1),q=[0];par[0]=0;for(let i=0;i<q.length;i++)for(let [v,e] of adj[q[i]])if(par[v]===-1){par[v]=q[i];pe[v]=e;q.push(v)}ck(q.length===2*k,"connected");
let chords=rng(edges.length).filter(e=>!pe.includes(e));ck(chords.length===k+1,"rank");function gauge(mask){let p=Array(2*k).fill(0);for(let v of q.slice(1))p[v]=p[par[v]]^((mask>>pe[v])&1);return chords.reduce((s,e,j)=>s|((((mask>>e)&1)^p[edges[e][0]]^p[edges[e][1]])<<j),0)}
return {edges,chords,gauge}}
function classify(rows){let k=rows.length,{edges,chords,gauge}=tree(rows),terms=[],phaseNO=[],support=new Set();function rec(i,used,perm,mask){if(i===k){tick("matchingTerms");let parity=0;for(let a=0;a<k;a++)for(let b=a+1;b<k;b++)parity^=Number(perm[a]>perm[b]);terms.push([mask,parity]);return}for(let j=0;j<3;j++){let v=rows[i][j];if(!(used>>v&1))rec(i+1,used|1<<v,[...perm,v],mask|1<<(3*i+j))}}rec(0,0,[],0);ck(terms.length>0,"Hall");
function bitpar(x){let p=0;while(x){x&=x-1;p^=1}return p}
for(let s=0;s<(1<<(k+1));s++){tick("syndromeWords");let mask=chords.reduce((a,e,j)=>a|((s>>j&1)<<e),0),ok=false;for(let w=0;w<(1<<k);w+=2){tick("phaseWords");if(rows.every((r,i)=>{let x=r.map((v,j)=>(w>>v&1)^(mask>>(3*i+j)&1));return x[0]!==x[1]||x[0]!==x[2]})){ok=true;break}}let p=terms[0][1]^bitpar(terms[0][0]&mask),same=terms.every(([m,b])=>(b^bitpar(m&mask))===p);ck(ok!==same,"phase vs matching");if(!ok)phaseNO.push(s)}
function gen(i,mask){if(i===k){tick("syndromeWords");support.add(gauge(mask));return}for(let j=0;j<3;j++)gen(i+1,mask|1<<(3*i+j))}gen(0,0);ck(support.size+phaseNO.length===1<<(k+1)&&phaseNO.every(s=>!support.has(s)),"direct support vs phase");ck(phaseNO.length<=1,"unique exception");return {rank:k+1,support:support.size,missing:phaseNO,matchingTerms:terms.length}}
let cases=[];for(let k of [3,5,7,9]){let rows=rng(k).map(i=>[i,i,(i+1)%k]),src=make(rows),a=classify(rows);ck(a.missing.length===1&&a.missing[0]===0,"odd cycle native NO");cases.push({kind:"odd-double-cycle",k,variables:12*k,owners:16*k,classification:a,source:src,rows})}
let fano=[];for(let i=1;i<8;i++)for(let j=i+1;j<8;j++){let k=i^j;if(j<k)fano.push([i-1,j-1,k-1])}let f=make(fano),fc=classify(fano);ck(fc.missing.length===1&&fc.missing[0]===0,"Fano native NO");cases.push({kind:"Fano",k:7,variables:84,owners:112,classification:fc,source:f,rows:fano});
let controls=[];for(let k of [3,4,5,6,7,8]){let rows=rng(k).map(i=>[i,(i+1)%k,(i+2)%k]),a=classify(rows);controls.push({kind:"circulant local falsifier",k,...a})}
return {gadget,ports,table,original,counts,cap,cases,controls}
}
console.log(JSON.stringify(audit(),null,2));
