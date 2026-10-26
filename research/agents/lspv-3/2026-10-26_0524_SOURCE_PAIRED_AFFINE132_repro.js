'use strict';
// LSPV-3 SOURCE-PAIRED-AFFINE132: finite independent source-ID/pairing audit.
// Standard Node.js only. This does not measure FLMV workspace.
let checks=0;function ok(x,m){checks++;if(!x)throw Error(m||'assertion');}
const trip=[0,1,2,3,4,5,6,7].map(t=>[t&1,(t>>1)&1,(t>>2)&1]);
function k4(){let e=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)e.push([a,b]);return [e,4];}
function torus(r){const v=(i,j,p)=>4*(i*r+j)+p;let E=[];for(let i=0;i<r;i++)for(let j=0;j<r;j++){for(let p=0;p<4;p++)E.push([v(i,j,p),v(i,j,(p+1)%4)]);E.push([v(i,j,1),v(i,(j+1)%r,3)],[v(i,j,2),v((i+1)%r,j,0)]);}return [E,4*r*r];}
function petersen(){let e=[];for(let i=0;i<5;i++)e.push([i,(i+1)%5],[i,i+5],[i+5,((i+2)%5)+5]);return[e,10];}
function build(E,n,odd){let inc=Array.from({length:n},()=>[]),rows=[],cert=[];E.forEach(([a,b],i)=>{ok(a!==b);inc[a].push(i+1);inc[b].push(i+1);});
inc.forEach((names,i)=>{ok(names.length===3);names.sort((a,b)=>a-b);let ids=[],rhs=Number(odd&&i===0);for(let word of trip)if(((word[0]+word[1]+word[2])%2)!==rhs){ids.push(rows.length);rows.push(names.map((x,j)=>word[j]?-x:x));}ok(ids.length===4);cert.push({names,rhs,ids,mate:[]});});
let slots=new Map();cert.forEach((rec,i)=>rec.names.forEach((x,j)=>{if(!slots.has(x))slots.set(x,[]);slots.get(x).push([i,j]);}));for(let ps of slots.values()){ok(ps.length===2);let [[i,j],[k,l]]=ps;cert[i].mate[j]=[k,l];cert[k].mate[l]=[i,j];}return {rows,cert};}
function encode(rows,n){let lines=['p cnf '+n+' '+rows.length+'\n'],pos=lines[0].length,offsets=[];for(let c of rows){offsets.push(pos);let s=c.join(' ')+' 0\n';lines.push(s);pos+=s.length;}return {source:lines.join(''),offsets};}
function attach(c,offsets){return c.map(r=>({names:[...r.names],rhs:r.rhs,ptr:r.ids.map(i=>offsets[i]),mate:r.mate.map(p=>[...p])}));}
function verify(source,proof){try{let ls=source.split('\n'),hdr=ls[0].split(' '),n=+hdr[2];if(hdr[0]!=='p'||hdr[1]!=='cnf'||+hdr[3]!==ls.length-2)return false;
let pos=ls[0].length+1,byoffset=new Map();for(let line of ls.slice(1,-1)){let z=line.split(' ').map(Number),c=z.slice(0,-1);if(z.at(-1)!==0||c.length!==3||new Set(c.map(Math.abs)).size!==3||c.some(v=>Math.abs(v)>n||!v))return false;byoffset.set(pos,c);pos+=line.length+1;}
let rhs=0;for(let i=0;i<proof.length;i++){let r=proof[i];if(r.names.length!==3||new Set(r.names).size!==3||r.ptr.length!==4||new Set(r.ptr).size!==4||r.mate.length!==3)return false;rhs^=r.rhs;let seen=new Set();for(let p of r.ptr){let c=byoffset.get(p);if(!c||r.names.some(x=>!c.some(l=>Math.abs(l)===x)))return false;let word=r.names.map(x=>c.find(l=>Math.abs(l)===x)<0?1:0);if(((word[0]+word[1]+word[2])%2)===r.rhs)return false;seen.add(word.join(''));}if(seen.size!==4)return false;
for(let j=0;j<3;j++){let [k,l]=r.mate[j];if(k<0||k>=proof.length||l<0||l>2||(k===i&&l===j))return false;let o=proof[k];if(!o||!o.mate[l]||o.names[l]!==r.names[j]||o.mate[l][0]!==i||o.mate[l][1]!==j)return false;}}
return rhs===1;}catch(e){return false;}}
function gf2(E,n,b){let eq=Array(n).fill(0n);E.forEach(([u,v],i)=>{let bit=1n<<BigInt(i);eq[u]^=bit;eq[v]^=bit;});let basis=new Map();for(let k=0;k<eq.length;k++){let x=eq[k],z=b[k];while(x){let j=x.toString(2).length-1;if(basis.has(j)){let [a,y]=basis.get(j);x^=a;z^=y;}else{basis.set(j,[x,z]);break;}}if(!x&&z)return false;}return true;}
function brute(rows,n){for(let k=0;k<2**n;k++)if(rows.every(c=>c.some(l=>Boolean((k>>(Math.abs(l)-1))&1)===(l>0))))return true;return false;}
function pin(x,a,b){return [[x,a,b],[x,a,-b],[x,-a,b],[x,-a,-b]];}
let out=[];
for(let [name,[E,n]] of [['K4',k4()],['Petersen',petersen()],...([3,4,5].map(r=>['torus_'+r,torus(r)]))]){
let odd=build(E,n,true),even=build(E,n,false),enc=encode(odd.rows,E.length),ce=attach(odd.cert,enc.offsets),es=encode(even.rows,E.length);ok(verify(enc.source,ce));ok(!verify(es.source,attach(even.cert,es.offsets)));ok(!gf2(E,n,[1,...Array(n-1).fill(0)]));ok(gf2(E,n,Array(n).fill(0)));
for(let i=0;i<n;i++){let smaller=E.map(()=>null);let filteredE=[]; // drop a parity EQUATION, not graph edges
let charged=[1,...Array(n-1).fill(0)];let equations=[];E.forEach(([u,v],j)=>{});let rows=Array(n).fill(0n);E.forEach(([u,v],j)=>{let b=1n<<BigInt(j);rows[u]^=b;rows[v]^=b;});let basis=new Map(),good=true;for(let t=0;t<n;t++)if(t!==i){let x=rows[t],z=charged[t];while(x){let lead=x.toString(2).length-1;if(basis.has(lead)){let [a,b]=basis.get(lead);x^=a;z^=b;}else{basis.set(lead,[x,z]);break;}}if(!x&&z)good=false;}ok(good);}
for(let attack of ['charge','offset','self','missing','rename']){let a=JSON.parse(JSON.stringify(ce));if(attack==='charge')a[0].rhs^=1;if(attack==='offset')a[0].ptr[0]+=1;if(attack==='self')a[0].mate[0]=[0,0];if(attack==='missing')a.pop();if(attack==='rename')a[0].names[0]=E.length+1;ok(!verify(enc.source,a),'tamper '+attack);}
let extra=encode([...odd.rows,[E.length+1,E.length+2,E.length+3]],E.length+3);ok(verify(extra.source,attach(odd.cert,extra.offsets)));
if(name==='K4'){ok(!brute(odd.rows,6));ok(brute(even.rows,6));for(let [C,nv] of [[odd.rows.concat(pin(-1,7,8)),8],[odd.rows.concat(pin(-1,7,8),pin(2,9,10)),10]]){let e=encode(C,nv);ok(verify(e.source,attach(odd.cert,e.offsets)));ok(!brute(C,nv));}}
out.push({name,vertices:n,edges:E.length,source_bytes:enc.source.length,quartets:ce.length,certificate_json_bytes:JSON.stringify(ce).length,odd_verified:true,even_rejected:true,proper_subsets_consistent:true});}
const W='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'.split(';').map(s=>s.split(' ').map(Number));ok(!brute(W,15));for(let i=1;i<=15;i++)ok(W.filter(c=>c.includes(i)).length===2&&W.filter(c=>c.includes(-i)).length===2);
// Exact symbolic degree-three identity is proved in report; finite truth table checks both charges.
for(let rhs=0;rhs<2;rhs++)for(let word of trip){let s=trip.filter(w=>(w.reduce((a,b)=>a+b,0)&1)!==rhs).reduce((a,w)=>a+Number(w.every((x,i)=>x===word[i])),0);ok(s===(word.reduce((a,b)=>a+b,0)^rhs)%2);}
console.log(JSON.stringify({run:'SOURCE-PAIRED-AFFINE132-COMPACT',assertions:checks,graph_controls:out,W1_exact_signed_2P2N_verified:true,all_UNSAT_coverage:'OPEN',ARC_EDGE_90:'OPEN'},null,2));
