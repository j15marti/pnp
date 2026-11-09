/* LSPV-3/515. Strict 3CNF 4-cube matching.
 * Independent XLRUP format-subset verifier and paid-rule controls.
 * NOT the official CakeML checker or full historical R_mix341.
 */
"use strict";
const match=[[0,1,0],[2,3,0],[4,6,1],[5,13,3],[7,15,3],[8,12,2],[9,11,1],[10,14,2]];
const cs=match.map(([a,b,d])=>{if((a^b)!==(1<<d))throw Error("edge");
 return [0,1,2,3].filter(i=>i!==d).map(i=>((a>>i)&1)?-i-1:i+1)});
const src="p cnf 4 8\n"+cs.map(c=>c.join(" ")+" 0\n").join("");
const hints="1 2 3 4 5 6 7 8";
const proof="i x 1 -1 2 3 4 0 "+hints+" 0\n"+"i x 2 1 2 3 4 0 "+hints+" 0\n"+"x 3 0 1 2 0\n"+"i cx 9 0 3 0\n";
function demand(x,msg){if(!x)throw Error(msg)}
function sat(c,x){return c.some(y=>((x>>(Math.abs(y)-1))&1)===(y>0?1:0))}
function row(ls){let set=new Set(ls.map(Math.abs));demand(set.size===ls.length,"xor repeats");
 let mask=0;for(let x of set){demand(x>=1&&x<=4,"xor range");mask^=1<<(x-1)}
 return [mask,1^(ls.filter(x=>x<0).length%2)]}
function verify(source,p,bind=true){
 if(bind)demand(source===src,"original byte mismatch");
 let ss=source.trim().split(/\s+/);demand(ss.slice(0,4).join(" ")==="p cnf 4 8","header");
 let inp=[],cur=[];for(const tok of ss.slice(4)){let x=Number(tok);demand(Number.isInteger(x),"bad literal");
 if(!x){demand(cur.length===3&&new Set(cur.map(Math.abs)).size===3,"proper 3");inp.push(cur);cur=[]}
 else{demand(Math.abs(x)>=1&&Math.abs(x)<=4,"range");cur.push(x)}}
 demand(inp.length===8&&!cur.length,"count");
 let rows=new Map(),ended=false;
 for(const line of p.trim().split("\n")){let t=line.trim().split(/\s+/);
 demand(!ended,"after sink");let part=(start)=>{let j=t.indexOf("0",start);demand(j>=0,"zero delimiter");return[t.slice(start,j).map(Number),j+1]};
 if(t[0]==="i"&&t[1]==="x"){
 let id=Number(t[2]),[ls,j]=part(3),[ids,k]=part(j),r=row(ls);demand(k===t.length&&!rows.has(id)&&id>0,"x syntax");
 demand(ids.length>0&&ids.every(x=>x>=1&&x<=8),"hint");
 for(let a=0;a<16;a++){let parity=0,enc=[];
 for(let i=0;i<4;i++)if(r[0]&(1<<i)){parity^=(a>>i)&1;enc.push((a&(1<<i))?-i-1:i+1)}
 if(parity===r[1])continue;
 demand(ids.some(h=>inp[h-1].every(l=>enc.includes(l))),"covering failed")}
 rows.set(id,r);
 }else if(t[0]==="x"){
 let id=Number(t[1]),[ls,j]=part(2),[parents,k]=part(j),r=row(ls);
 demand(k===t.length&&parents.length===2&&!rows.has(id)&&parents[0]!==parents[1],"xor syntax");
 let a=rows.get(parents[0]),b=rows.get(parents[1]);demand(a&&b,"parent missing");
 demand(r[0]===(a[0]^b[0])&&r[1]===(a[1]^b[1]),"bad xor");rows.set(id,r);
 }else if(t[0]==="i"&&t[1]==="cx"){
 let id=Number(t[2]),[cl,j]=part(3),[par,k]=part(j);
 demand(k===t.length&&id===9&&!cl.length&&par.length===1,"cx syntax");
 demand(JSON.stringify(rows.get(par[0]))==="[0,1]","not contradiction");ended=true;
 }else throw Error("unknown proof record")}
 demand(ended,"no sink");return rows.size}
function resolve(a,b){let out=[];for(let x of a)if(b.includes(-x)){
 let z=[...new Set([...a.filter(y=>y!==x),...b.filter(y=>y!==-x)])];
 if(z.every(y=>!z.includes(-y)))out.push(z)}return out}
function same(a,b){return a.slice().sort((x,y)=>x-y).join(",")===b.slice().sort((x,y)=>x-y).join(",")}
const res=[[9,1,2,[3,4]],[22,4,5,[-1,-3]],[28,6,8,[1,-4]],
 [37,3,22,[-3,4]],[50,7,22,[-1,-4]],[57,9,37,[4]],[62,28,50,[-4]],[65,57,62,[]]];
function rescheck(){let d=new Map(cs.map((c,i)=>[i+1,c]));for(const [id,a,b,c] of res){
 demand(resolve(d.get(a),d.get(b)).some(t=>same(t,c)),"pivot");d.set(id,c)}
 let visited=new Set();function walk(id){if(visited.has(id))return;visited.add(id);
 let p=res.find(x=>x[0]===id);if(p){walk(p[1]);walk(p[2])}}
 walk(65);demand(cs.every((_,i)=>visited.has(i+1)),"missing source");
 return {paid:8,source_count:8,shared_node:22,all_16_premise_edges_paid_distinctly:false}}
function corecheck(){let by={};for(const c of cs){let k=c.map(Math.abs).sort().join(",");
 (by[k]||(by[k]=[])).push(c)}demand(Object.keys(by).length===4,"groups");
 for(const list of Object.values(by)){demand(list.length===2,"group2");let v=list[0].map(Math.abs).sort();
 let truth=list.map(c=>Array.from({length:8},(_,b)=>{let a=0;v.forEach((x,j)=>{if(b&(1<<j))a|=1<<(x-1)});return sat(c,a)}));
 demand(truth.every(a=>a.filter(Boolean).length===7),"source affine");
 demand(truth[0].filter((x,i)=>x&&truth[1][i]).length===6,"pair affine")}
 return {supports:4,sources_per_support:2,distinct_factors:12,affine_seeds:0,refutations:0}}
function shrink(){let d=new Map(cs.map((c,i)=>[i+1,Array.from({length:16},(_,a)=>sat(c,a))]));
 let steps=[[1,2],[4,5],[6,8],[3,7],[9,10],[11,12],[13,14]],supports=[];
 steps.forEach(([a,b],i)=>{let tt=d.get(a).map((x,j)=>x&&d.get(b)[j]),v=[];
 for(let k=0;k<4;k++)if(tt.some((x,j)=>x!==tt[j^(1<<k)]))v.push(k+1);
 demand(v.length<=3,"free shrink invalid");d.set(i+9,tt);supports.push(v)});
 demand(d.get(15).every(x=>!x),"no FALSE");return {paid:7,supports,model:"DISTINCT free support-minimizing AND3, not historical"}}
function run(){demand(src.length===86&&proof.length===94,"bytes");
 for(let a=0;a<16;a++)demand(cs.filter(c=>!sat(c,a)).length===1,"partition");
 for(let j=0;j<8;j++)demand(Array.from({length:16},(_,a)=>a).filter(a=>cs.every((c,k)=>k===j||sat(c,a))).length===2,"deletion");
 demand(verify(src,proof)===3,"XLRUP");
 let n=0;function bad(s,p){try{verify(s,p)}catch(e){n++;return}throw Error("corrupt accepted")}
 bad(src.replace("2 3 4 0","-2 3 4 0"),proof);
 bad(src,proof.replace("7 8 0","7 999 0"));
 bad(src,proof.replace("1 2 3 4 5 6 7 8 0","1 2 3 4 5 6 0"));
 bad(src,proof.replace("x 3 0 1 2 0","x 3 0 1 88 0"));
 bad(src,proof.replace("i cx 9 0 3 0","i cx 9 1 0 3 0"));
 bad(src,proof.replace("i cx 9 0 3 0",""));
 demand(n===6,"negatives");
 return {original_source_bytes:src.length,original_clauses:8,variables:4,matching:match,
  source_clause_false_count_per_assignment:1,sat_assignments_per_deletion:2,
  xlrup_bytes:proof.length,xlrup_records:4,hint_references:16,
  external_depth:3,negative_rejections:n,fixed_support_core:corecheck(),
  ordinary_resolution:rescheck(),distinct_free_shrink_control:shrink()}}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));