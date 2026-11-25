function run(chart, block=null) {
 const rows=chart.rowMap, R=rows.length, D=chart.ownerIDs.length, live=chart.live.slice(), p=chart.pairHex.map(x=>BigInt("0x"+x)), bits=rows.map((_,i)=>1n<<BigInt(i)), domains=Array.from({length:D},()=>[]);
 rows.forEach((r,i)=>domains[r[0]].push(i)); const stats={acScans:0,acRows:0,relationRows:0,projectionTests:0,reachTests:0,fillTests:0};
 const active=()=>domains.map(d=>d.filter(i=>live[i])); const mask=d=>d.reduce((s,i)=>s|bits[i],0n);
 function ac(ds) {let change=true;while(change){change=false;stats.acScans++;let masks=ds.map(d=>mask(d.filter(i=>live[i])));for(let a=0;a<ds.length;a++){for(const i of ds[a])if(live[i]){stats.acRows++;if(masks.some((m,b)=>b!==a&&!(p[i]&m))){live[i]=false;change=true;}}}if(ds.some(d=>!d.some(i=>live[i])))return false;}return true;}
 if(!ac(domains))return {status:"UNSAT-AC",stats};
 const ds=active(); const lengths=ds.map(d=>rows[d[0]][1].length);
 // Return exact unary/binary clauses on a relation, or decline. Enumeration of the
 // 2-CNF hull is output-capped at explicit table length+1, with unit propagation.
 function relation(words, w) {
   stats.relationRows+=words.length;
   if(!words.length)return {clauses:[[]]};
   const cs=[];
   for(let i=0;i<w;i++){for(let a=0;a<2;a++)if(!words.some(s=>+s[i]===a))cs.push([2*i+(1-a)]);for(let j=i+1;j<w;j++)for(let a=0;a<2;a++)for(let b=0;b<2;b++)if(!words.some(s=>+s[i]===a&&+s[j]===b))cs.push([2*i+1-a,2*j+1-b]);}
   // Polynomial exact recognition via implication reachability, then prefix queries.
   const g=graph(w,cs);if(!g.ok)return null;
   const allowed=new Set(words);let found=0,bad=false;
   function walk(units,s){if(bad)return;stats.projectionTests++;if(!feasible(g,units))return;if(s.length===w){found++;if(!allowed.has(s))bad=true;return;}for(let b=0;b<2;b++)walk([...units,2*s.length+b],s+b);}
   walk([],"");return bad||found!==allowed.size?null:{clauses:cs};
 }
 function graph(w,cs) {const n=2*w,reach=Array.from({length:n},(_,i)=>1n<<BigInt(i));for(const c of cs){if(!c.length)return {ok:false,reach};let [a,b=a]=c;reach[a^1]|=1n<<BigInt(b);reach[b^1]|=1n<<BigInt(a);}for(let k=0;k<n;k++)for(let i=0;i<n;i++){stats.reachTests++;if(reach[i]&(1n<<BigInt(k)))reach[i]|=reach[k];}const ok=Array.from({length:w},(_,i)=>i*2).every(i=>!((reach[i]&(1n<<BigInt(i+1)))&&(reach[i+1]&(1n<<BigInt(i)))));return {ok,reach};}
 function feasible(g,u){if(!g.ok)return false;let a=0n;for(const l of u)a|=g.reach[l];for(let j=0;j<g.reach.length;j+=2)if(((a>>BigInt(j))&3n)===3n)return false;return true;}
 const own=ds.map((d,i)=>relation(d.map(r=>rows[r][1]),lengths[i]));
 const initialEligible=own.map((x,i)=>x?i:-1).filter(x=>x>=0);
 let B=block?block.slice():initialEligible.slice();
 // Compute exact pin conditions for every exterior row relative to each internal owner.
 function pin(a,r){const d=ds[a],ok=d.filter(i=>(p[r]&bits[i])!==0n);if(!ok.length)return {none:true};let pins=[];for(let j=0;j<lengths[a];j++)if(ok.every(i=>rows[i][1][j]===rows[ok[0]][1][j]))pins.push(2*j+(+rows[ok[0]][1][j]));return d.every(i=>ok.includes(i)===pins.every(l=>+rows[i][1][l>>1]===(l&1)))?{pins}:null;}
 let pairs=new Map(),pins=new Map(),removed=[];
 while(B.length){let fail=null;let bs=new Set(B);
  for(let ai=0;ai<B.length&&!fail;ai++){let a=B[ai];if(!own[a]){fail=[a,"domain"];break;}
    for(let bi=ai+1;bi<B.length&&!fail;bi++){let b=B[bi],key=a+","+b;if(!pairs.has(key)){let words=[];for(const i of ds[a])for(const j of ds[b])if(p[i]&bits[j])words.push(rows[i][1]+rows[j][1]);pairs.set(key,relation(words,lengths[a]+lengths[b]));}if(!pairs.get(key))fail=[b,"internal pair"];}
    for(let b=0;b<D&&!fail;b++)if(!bs.has(b))for(const r of ds[b]){let key=a+","+r;if(!pins.has(key))pins.set(key,pin(a,r));if(!pins.get(key)){fail=[a,"external nonpin"];break;}}
  }if(!fail)break;removed.push(fail);B=B.filter(a=>a!==fail[0]);if(block)return {status:"DECLINE",initialEligible,removed,stats};
 }
 if(!B.length)return {status:"DECLINE",initialEligible,removed,stats};
 let off={},w=0,cs=[];for(const a of B){off[a]=w;w+=lengths[a];cs.push(...own[a].clauses.map(c=>c.map(l=>l+2*off[a])));}
 for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){let a=B[i],b=B[j];for(const c of pairs.get(a+","+b).clauses)cs.push(c.map(l=>l<2*lengths[a]?l+2*off[a]:l-2*lengths[a]+2*off[b]));}
 const g=graph(w,cs);if(!g.ok)return {status:"UNSAT-BLOCK",initialEligible,B,stats};
 const E=ds.map((d,i)=>B.includes(i)?[]:d).flat(), unit=new Map(), deletedRows=[],deletedPairs=[];
 for(const r of E){let u=[],bad=false;for(const a of B){const z=pins.get(a+","+r);if(z.none){bad=true;break;}u.push(...z.pins.map(l=>l+2*off[a]));}if(bad||!feasible(g,u)){live[r]=false;deletedRows.push(r);}else unit.set(r,u);}
 for(let i=0;i<E.length;i++){let a=E[i];if(!live[a])continue;for(let j=i+1;j<E.length;j++){let b=E[j];if(!live[b]||!(p[a]&bits[b]))continue;stats.fillTests++;if(!feasible(g,[...unit.get(a),...unit.get(b)])){p[a]&=~bits[b];p[b]&=~bits[a];deletedPairs.push([a,b]);}}}
 const outside=domains.filter((d,i)=>!B.includes(i));let ok=ac(outside);
 return {status:ok?(outside.length?"REDUCED":"SAT-BLOCK"):"UNSAT-FILL",initialEligible,B,removed,w,clauses:cs,offsets:off,deletedRows,deletedPairs,stats,postLive:E.filter(r=>live[r]),postPair:E.filter(r=>live[r]).map(r=>[r,(p[r]&mask(E.filter(j=>live[j]))).toString(16)]),units:E.filter(r=>live[r]).map(r=>[r,unit.get(r)]),guard:chart.guard};
}

function importDeltas(c,ms,bh){let x=JSON.parse(JSON.stringify(c));for(const d of [ms,bh]){if(!d)continue;for(const [i,h] of d.delta??[]){let p=BigInt("0x"+x.pairHex[i]),m=BigInt("0x"+h);x.pairHex[i]=(p&~m).toString(16);}for(const i of d.removedRows??[])x.live[i]=false;}return x;}

function makeChart(domains, allowed){let rowMap=domains.flatMap((d,i)=>d.map(s=>[i,s])), n=rowMap.length;return {ownerIDs:domains.map((_,i)=>i),rowMap,live:Array(n).fill(true),guard:[],pairHex:rowMap.map(([a,x],i)=>rowMap.reduce((m,[b,y],j)=>a!==b&&allowed(a,x,b,y)?m|(1n<<BigInt(j)):m,0n).toString(16))};}

function controls(){let out=[]; // K_n equality owners: block first half of edges; all rows distinct; actual shared bits explicit.
for(const n of [4,6,10,16]){let e=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)e.push([i,j]);let c=makeChart(e.map(()=>["00","01","10","11"]),(a,x,b,y)=>e[a].every((v,i)=>!e[b].includes(v)||x[i]===y[e[b].indexOf(v)]));let B=e.map((_,i)=>i).slice(0,Math.floor(e.length/2));let z=run(c,B);out.push({n,block:B.length,status:z.status,rows:z.deletedRows?.length,pairs:z.deletedPairs?.length,stats:z.stats});}
 // Chain of equalities with exterior endpoints; opposite pins become pair nogood.
for(const odd of [false,true]){let c=makeChart(Array.from({length:5},()=>["0","1"]),(a,x,b,y)=>{let i=Math.min(a,b),j=Math.max(a,b);return j-i!==1||((x===y)!==(odd&&i===2));});
 let z=run(c,[1,2,3]);out.push({chain:odd,status:z.status,deletedPairs:z.deletedPairs,stats:z.stats});}
 // Odd parity triangle internal, arc consistent yet UNSAT.
let c=makeChart(Array.from({length:3},()=>["0","1"]),(a,x,b,y)=>x!==y);let z=run(c,[0,1,2]);out.push({oddTriangle:z.status,stats:z.stats});return out;}


function lift(chart,z,ext){
 if(!["REDUCED","SAT-BLOCK"].includes(z.status))throw Error("not a projected chart");
 const n=2*z.w,reach=Array.from({length:n},(_,i)=>1n<<BigInt(i));
 for(const [a,b=a] of z.clauses){reach[a^1]|=1n<<BigInt(b);reach[b^1]|=1n<<BigInt(a);}
 for(let k=0;k<n;k++)for(let i=0;i<n;i++)if(reach[i]&(1n<<BigInt(k)))reach[i]|=reach[k];
 const u=new Map(z.units);let a=0n;
 const consistent=m=>{for(let j=0;j<n;j+=2)if(((m>>BigInt(j))&3n)===3n)return false;return true;};
 for(const r of ext){if(!u.has(r))throw Error("inactive exterior");for(const l of u.get(r))a|=reach[l];}
 if(!consistent(a))throw Error("inconsistent exterior");
 for(let j=0;j<n;j+=2){if(a&(3n<<BigInt(j)))continue;let v=a|reach[j];if(!consistent(v))v=a|reach[j+1];if(!consistent(v))throw Error("no extension");a=v;}
 const ans=ext.slice();
 for(const b of z.B){let d=chart.rowMap.findIndex(([i,s],r)=>i===b&&chart.live[r]&&[...s].every((v,j)=>a&(1n<<BigInt(2*(z.offsets[b]+j)+Number(v)))));if(d<0)throw Error("missing lift row");ans.push(d);}
 if(ans.length!==chart.ownerIDs.length||new Set(ans.map(r=>chart.rowMap[r][0])).size!==ans.length)throw Error("invalid lift length");
 for(const r of ans)for(const s of ans)if(r!==s&&!(BigInt("0x"+chart.pairHex[r])&(1n<<BigInt(s))))throw Error("bad original pair");
 return ans;
}
function exhaustiveControls(makeChart,run){
 let seed=0x47543235;const rand=()=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed/4294967296;};
 let counts={controls:0,sat:0,unsat:0,declines:0,projectionWords:0,lifts:0,assertions:0};let details=[];
 for(let t=0;t<100;t++){let domains=[["0","1"],["0","1"],["0","1"],["00","01","10"],["00","01","10"]];let allowed=new Map();
 for(let i=0;i<5;i++)for(let j=i+1;j<5;j++){let m=new Set();for(const x of domains[i])for(const y of domains[j])if(rand()<.76)m.add(x+"/"+y);allowed.set(i+","+j,m);}
 const c=makeChart(domains,(i,x,j,y)=>i<j?allowed.get(i+","+j).has(x+"/"+y):allowed.get(j+","+i).has(y+"/"+x));
 const z=run(c,[0,1,2]);let D=domains.map((d,i)=>c.rowMap.map((r,k)=>r[0]===i?k:-1).filter(k=>k>=0));let ok=(r,s)=>!!(BigInt("0x"+c.pairHex[r])&(1n<<BigInt(s)));
 let expected=new Set(),actual=new Set(),sat=false;for(const a of D[0])for(const b of D[1])for(const d of D[2])for(const e of D[3])for(const f of D[4]){let v=[a,b,d,e,f];if(v.every((r,i)=>v.slice(i+1).every(s=>ok(r,s)))){expected.add(e+","+f);sat=true;}}
 counts.controls++;counts[sat?"sat":"unsat"]++;
 if(z.status==="DECLINE"){counts.declines++;continue;}
 if(z.status==="REDUCED"){let q=new Map(z.postPair);for(const e of D[3])for(const f of D[4])if(q.has(e)&&q.has(f)&&(BigInt("0x"+q.get(e))&(1n<<BigInt(f)))){actual.add(e+","+f);lift(c,z,[e,f]);counts.lifts++;}}
 if(actual.size!==expected.size||[...expected].some(x=>!actual.has(x)))throw Error("projection mismatch "+t+" "+z.status);
 counts.projectionWords+=expected.size;counts.assertions++;details.push({t,expected:expected.size,status:z.status});
 }
 return {seed:"0x47543235",counts,details};
}
function codeObstruction(){
 const rows=Array.from({length:8},(_,i)=>i),nae=[1,2,3,4,5,6];let domains=0,bijections=0,passes=0;
 const majority=(a,b,c)=>(a&b)|(a&c)|(b&c);
 const pin=(D,S)=>{let both=7,any=0;for(const x of S){both&=x;any|=x;}return D.filter(x=>(x&both)===both&&((x&(~any&7))===0)).length===S.length;};
 function perm(a,p=[]){if(!a.length){bijections++;if([0,1,2].every(j=>[0,1].every(b=>pin(D,p.filter((_,i)=>((nae[i]>>j)&1)===b)))))passes++;return;}for(let i=0;i<a.length;i++)perm(a.filter((_,j)=>i!==j),[...p,a[i]]);}
 let D=[];for(let i=0;i<8;i++)for(let j=i+1;j<8;j++){D=rows.filter(k=>k!==i&&k!==j);if(D.every(a=>D.every(b=>D.every(c=>D.includes(majority(a,b,c)))))){domains++;perm(D);}}
 return {domains,bijections,passes};
}
module.exports={run,importDeltas,makeChart,controls,lift,exhaustiveControls,codeObstruction};
