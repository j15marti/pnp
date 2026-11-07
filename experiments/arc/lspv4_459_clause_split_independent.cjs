// LSPV-4/459 independent clause-split expander control (Node >=18 or V8).
// Finite verification, NOT asymptotic proof or a proof of P!=NP.
function assert(x,m){if(!x)throw Error(m||"assertion");}
function edgesOf(name){
 if(name==="K4"){let e=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)e.push([i,j]);return [4,e];}
 if(name==="cube"){let e=[];for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)if(pop(i^j)===1)e.push([i,j]);return [8,e];}
 if(name==="Petersen"){let e=[];for(let i=0;i<5;i++){e.push([i,(i+1)%5].sort((a,b)=>a-b));e.push([i,i+5]);e.push([i+5,5+(i+2)%5].sort((a,b)=>a-b));}return [10,e];}
 throw Error("unknown graph");
}
function pop(x){let n=0;while(x){n+=x&1;x>>=1;}return n;}
function path(a,b){let anc=new Set(),t=a;while(t){anc.add(t);t>>=1;}t=b;while(!anc.has(t))t>>=1;let z=t,x=a,p=[],q=[];while(x!==z){p.push(x);x>>=1;}p.push(z);x=b;while(x!==z){q.push(x);x>>=1;}return p.concat(q.reverse());}
function comps(c,h){let adj=x=>[x>>1,2*x,2*x+1].filter(y=>y>=1&&y<=h&&y!==x);
 let seen=new Set([c]),out=[];for(let z of adj(c)){if(seen.has(z))continue;let v=[z],s=new Set();seen.add(z);while(v.length){let x=v.pop();s.add(x);for(let y of adj(x))if(!seen.has(y)){seen.add(y);v.push(y);}}out.push(s);}return out;
}
function compute(name,seed){
 let [H,ee]=edgesOf(name),edges=ee.map(([a,b])=>[Math.min(a,b),Math.max(a,b)]);
 assert(edges.length===3*H/2,"not cubic");
 let clauses=[];
 for(let v=0;v<H;v++){let inc=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);assert(inc.length===3);
   for(let a=0;a<8;a++){if(pop(a)%2===Number(v===0))continue;clauses.push({vertex:v,lits:inc.map((id,i)=>(a&(1<<i))?-id:id)});}}
 assert(clauses.length===4*H);
 let h=31,order=clauses.map((_,i)=>i),state=seed|0;
 function rand(){state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0;}
 for(let i=order.length-1;i>0;i--){let j=rand()%(i+1);[order[i],order[j]]=[order[j],order[i]];}
 let owner=Array(clauses.length);order.forEach((j,i)=>owner[j]=i%h+1);
 let blockLoads=Array(h+1).fill(0);owner.forEach(v=>blockLoads[v]++);
 let maxB=Math.max(...blockLoads);assert(maxB<=H/4,"max clauses/block promise");
 let home=Array.from({length:H},(_,v)=>owner[clauses.findIndex(c=>c.vertex===v)]);
 let bags=Array.from({length:h+1},()=>new Set());
 clauses.forEach((cl,j)=>cl.lits.forEach(l=>bags[owner[j]].add(Math.abs(l))));
 for(let e=1;e<=edges.length;e++){let sites=new Set();clauses.forEach((cl,j)=>{if(cl.lits.some(x=>Math.abs(x)===e))sites.add(owner[j]);});
 let anchor=[...sites][0];for(let v of sites)for(let z of path(anchor,v))bags[z].add(e);}
 let adh=new Map();for(let v=2;v<=h;v++)adh.set(v,new Set([...bags[v]].filter(x=>bags[v>>1].has(x))));
 let w=Math.max(...[...adh.values()].map(x=>x.size)),c=-1,cc=null,sizes=null;
 for(let cand=1;cand<=h;cand++){let tmp=comps(cand,h),sz=tmp.map(B=>home.filter(v=>B.has(v)).length);if(Math.max(0,...sz)<=H/2){c=cand;cc=tmp;sizes=sz;break;}}
 assert(c>0,"centroid missing");
 let pair=cc.map((B,i)=>[B,sizes[i]]).sort((a,b)=>b[1]-a[1]),selected=[],num=0;
 for(let [B,n] of pair){if(num>=H/4)break;selected.push(B);num+=n;}
 assert(num>=H/4&&num<=H/2,"balance selection");
 let U=new Set(home.flatMap((v,i)=>selected.some(B=>B.has(v))?[i]:[]));
 let cut=new Set(edges.flatMap((e,i)=>(U.has(e[0])!==U.has(e[1]))?[i+1]:[]));
 let boundary=new Set(),cross=[];
 for(let v=2;v<=h;v++)if((v>>1)===c&&selected.some(B=>B.has(v))||(v===c&&selected.some(B=>B.has(v>>1)))){cross.push(v);for(let e of adh.get(v))boundary.add(e);}
 assert([...cut].every(e=>boundary.has(e)),"crossing variable not in interface");
 let eps=Infinity;for(let mask=1;mask<2**H;mask++){let k=pop(mask);if(k>H/2)continue;
 let bd=edges.filter(([a,b])=>Boolean(mask&(1<<a))!==Boolean(mask&(1<<b))).length;eps=Math.min(eps,bd/k);}
 assert(cut.size+1e-9>=eps*U.size&&cut.size<=3*w,"expansion/width bound");
 return {graph:name,H,clauses:4*H,tree_nodes:h,max_clauses_in_block:maxB,centroid:c,side:U.size,graph_edge_expansion:eps,cut:cut.size,interface_union:boundary.size,max_interface:w,lower_bound:eps*H/12};
}
function runAll(){let rows=[];for(let name of ["K4","cube","Petersen"])for(let i=0;i<8;i++)rows.push(compute(name,459+7919*i));return {status:"COMPUTATIONAL",runs:rows.length,failures:0,rows};}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(runAll(),null,2));