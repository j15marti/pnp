function audit(){
const rng=n=>Array.from({length:n},(_,i)=>i);
let checks=0, trials=0, transitions=0, nativeRows=0;const cap=2000000;
function ck(ok,msg){checks++;if(!ok)throw Error(msg);if(checks+trials+transitions>cap)throw Error("cap")}
const bit=(w,i)=>(w>>i)&1;
const ag=[...rng(3).map(r=>rng(3).map(c=>3*r+c)),...rng(3).map(c=>rng(3).map(r=>3*r+c)),...rng(3).map(k=>rng(3).map(r=>3*r+(r+k)%3)),...rng(3).map(k=>rng(3).map(r=>3*r+(k-r+3)%3))];
const bx=(a,b)=>a^b,alpha=[0,2,3,1];
function make(kind,L){
let blocks=[],eq=[],rhs=[],first=new Map();
for(let j=0;j<L;j++){
 if(kind==="AG9"){for(let row of ag){let i=blocks.length;blocks.push({terms:[0,7],vars:row.map(v=>9*j+v)});
 for(let k=0;k<3;k++){let v=9*j+row[k],p=3*i+k;if(first.has(v)){eq.push([first.get(v),p]);rhs.push(0)}else first.set(v,p)}}}
 else blocks.push({terms:[1,2,4,7],vars:rng(3).map(k=>3*j+k)});
}
if(kind==="parity"){eq.push(rng(3*L));rhs.push(1)}
return {kind,L,blocks,eq,rhs};
}
function native(a){
let rows=[],colors=[],pins=[],controls=[],nv=0;
for(let [j,B] of a.blocks.entries())for(let t of B.terms){
 let vs=rng(4).map(()=>nv++),cs=rng(3).map(()=>nv++);
 pins.push([vs[0],1],[vs[3],1]);
 for(let i=0;i<3;i++){rows.push([vs[i],vs[i+1],cs[i]]);colors.push(i%2);controls.push({id:cs[i],occ:3*j+i,flip:bit(t,i)^1^(i%2)})}
}
let used=Array.from({length:nv},()=>new Set());
rows.forEach((r,i)=>r.forEach(v=>{ck(!used[v].has(colors[i]),"partial partition");used[v].add(colors[i])}));
let complete=[],part=[];
for(let copy=0;copy<12;copy++)rows.forEach((r,i)=>{complete.push(r.map(v=>copy*nv+v));part.push(colors[i])});
for(let v=0;v<nv;v++)for(let p=0;p<4;p++)if(!used[v].has(p))for(let j=0;j<4;j++){complete.push([j*nv+v,(4+bx(j,p))*nv+v,(8+bx(j,alpha[p]))*nv+v]);part.push(p)}
let seen=new Set(),cnt=Array.from({length:4},()=>new Set());
for(let [i,row] of complete.entries()){nativeRows++;ck(new Set(row).size===3,"distinct");for(let v of row){ck(!cnt[part[i]].has(v),"partition uniqueness");cnt[part[i]].add(v)}for(let p=0;p<3;p++)for(let q=p+1;q<3;q++){let k=[row[p],row[q]].sort((x,y)=>x-y).join(",");ck(!seen.has(k),"linearity");seen.add(k)}}
ck(cnt.every(s=>s.size===12*nv),"perfect partitions");
let rep=new Map(),guard=[];
for(let c of controls){if(rep.has(c.occ)){let x=rep.get(c.occ);guard.push({vars:[x.id,c.id],rhs:x.flip^c.flip})}else rep.set(c.occ,c)}
for(let [i,e] of a.eq.entries()){let r=a.rhs[i];let vs=e.map(k=>{let x=rep.get(k);r^=x.flip;return x.id});guard.push({vars:vs,rhs:r})}
for(let [id,rhs] of pins)guard.push({vars:[id],rhs});
return {nv:12*nv,clauses:complete.length,guard,encodedBytes:JSON.stringify({n:12*nv,clauses:complete,partitions:part,guard}).length,partialRows:rows,colors,pins,controls};
}
function tables(a){let out=[];for(let B of a.blocks){let words=[];for(let w=0;w<8;w++){let all=true;
 for(let t of B.terms){let ext=false;for(let u=0;u<4;u++){trials++;let y=[1,bit(u,0),bit(u,1),0],x=y.map((b,i)=>b^(i%2));let ok=true;for(let i=0;i<3;i++){let c=bit(w,i)^bit(t,i)^1^(i%2);if(x[i]===x[i+1]&&x[i]===c)ok=false}ext||=ok}
 ck(ext===(w!==t),"direct path vs term");all&&=ext}
 ck(all===!B.terms.includes(w),"joint table");if(all)words.push(w)}
 out.push(words)}return out}
function add(b,x){while(x){let p=x.toString(2).length-1;if(b.has(p))x^=b.get(p);else {b.set(p,x);return}}}
function has(b,x){while(x){let p=x.toString(2).length-1;if(!b.has(p))return false;x^=b.get(p)}return true}
function syndrome(a,table){
 let m=a.blocks.length, cols=Array(3*m).fill(0n),h=0n;
 a.eq.forEach((r,i)=>{let b=1n<<BigInt(i);if(a.rhs[i])h|=b;for(let j of r)cols[j]^=b});
 let suffix=Array(m+1);suffix[m]=new Map();
 for(let j=m-1;j>=0;j--){suffix[j]=new Map(suffix[j+1]);for(let k=0;k<3;k++)add(suffix[j],cols[3*j+k])}
 let pref=new Map(),maxWidth=0,widths=[],states=new Set([0n]),peak=1,visited=1,firstEmpty=null;
 ck(has(suffix[0],h),"guard consistent");
 for(let j=0;j<m;j++){for(let k=0;k<3;k++)add(pref,cols[3*j+k]);let l=pref.size+suffix[j+1].size-suffix[0].size;ck(l>=0,"lambda");maxWidth=Math.max(maxWidth,l);widths.push(l);
 let next=new Set();for(let s of states)for(let w of table[j]){transitions++;let x=s;for(let k=0;k<3;k++)if(bit(w,k))x^=cols[3*j+k];if(has(suffix[j+1],x^h))next.add(x)}
 ck(BigInt(next.size)<=1n<<BigInt(l),"rank cap");states=next;peak=Math.max(peak,states.size);visited+=states.size;if(!states.size&&firstEmpty===null)firstEmpty=j+1
 }
 return {maxWidth,widths,peak,visited,firstEmpty,sat:states.has(h)}
}
const result=[];
for(const [kind,Ls] of [["AG9",[1,2,4,8]],["parity",[1,2,4,8,16,32,64,128]]])for(let L of Ls){
 let a=make(kind,L),p=native(a),tbl=tables(a),s=syndrome(a,tbl);ck(!s.sat,"UNSAT DP");
 // independent global obstruction: each AG9 copy has 36 covered pairs, minimum16 equal vs12; parity all local words even and global odd.
 if(kind==="AG9"){let pairs=new Set();for(let r of ag)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)pairs.add([r[i],r[j]].sort((x,y)=>x-y).join(","));ck(pairs.size===36,"AG9 pair coverage");for(let w=0;w<512;w++){trials++;ck(ag.some(r=>r.every(v=>bit(w,v)===bit(w,r[0]))),"AG9 exhaustive")}}
 else ck(tbl.every(t=>t.every(w=>(bit(w,0)^bit(w,1)^bit(w,2))===0)),"even parity contradiction");
 result.push({kind,L,blocks:a.blocks.length,nativeVariables:p.nv,nativeClauses:p.clauses,encodedBytes:p.encodedBytes,guards:p.guard.length,maxWidth:s.maxWidth,peak:s.peak,visited:s.visited,firstEmpty:s.firstEmpty,sat:s.sat,sourceRecipe:a})
}
// minimal SAT neighboring control: delete odd syndrome requirement (only correctness falsifier).
let a=make("parity",4);a.rhs[0]=0;ck(syndrome(a,tables(a)).sat,"even syndrome control");
return {result,checks,trials,transitions,nativeRows,cap,execution:"interleaved finite reference; counters partial, no all-channel closure"};
}
console.log(JSON.stringify(audit(),null,2));
