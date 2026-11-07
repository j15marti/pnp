// LSPV-4/459 signed strict 3-CNF odd/even and corrupt-source regression.
// This is a separate finite model; NOT the historical R_mix341 checker.
function assert(b,s){if(!b)throw Error(s);}
function graph(n){if(n===4){let e=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)e.push([a,b]);return e;}
if(n===8){let e=[];for(let a=0;a<8;a++)for(let b=a+1;b<8;b++)if(((a^b).toString(2).match(/1/g)||[]).length===1)e.push([a,b]);return e;}
if(n===10){let e=[];for(let i=0;i<5;i++)e.push([i,(i+1)%5],[i,i+5],[i+5,5+(i+2)%5]);return e;}
throw Error("unsupported");}
function build(n,odd){let E=graph(n),rows=[];
for(let v=0;v<n;v++){let ids=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean),chi=(odd&&v===0)?1:0;
assert(ids.length===3);
for(let a=0;a<8;a++){let p=((a&1)+((a>>1)&1)+((a>>2)&1))%2;if(p===chi)continue;
rows.push([v,ids.map((id,i)=>(a&(1<<i))?-id:id)]);}}
return {n,E,odd,rows};}
function authentic(F){let {n,E,odd,rows}=F,orig=build(n,odd),key=row=>row[0]+":"+row[1].join(",");
return JSON.stringify(rows.map(key).sort())===JSON.stringify(orig.rows.map(key).sort());}
function sat(F){let m=F.E.length;
for(let mask=0;mask<2**m;mask++){let good=F.rows.every(([,cl])=>cl.some(z=>Boolean(mask&(1<<(Math.abs(z)-1)))===(z>0)));
if(good)return true;}return false;}
function check(){let trials=[],neg=0;for(let n of [4,8,10])for(let odd of [false,true]){
let F=build(n,odd);assert(F.rows.length===4*n,"size");assert(authentic(F),"auth");let truth=sat(F);
assert(truth===!odd,"odd/even parity semantics");trials.push({n,variables:F.E.length,original_strict_clauses:F.rows.length,odd_charge:odd,SAT:truth});
let mutation=mod=>{let copy={...F,rows:F.rows.map(([v,c])=>[v,c.slice()])};mod(copy.rows);assert(!authentic(copy),"corrupt accepted");neg++;};
mutation(rows=>rows.pop());mutation(rows=>rows.push(rows[0]));mutation(rows=>rows[0][1][0]*=-1);
mutation(rows=>rows[0][1].pop());mutation(rows=>rows[0][1][0]=999999);
}
return {cases:trials.length,SAT:trials.filter(x=>x.SAT).length,UNSAT:trials.filter(x=>!x.SAT).length,corruptions_rejected:neg,trials};}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(check(),null,2));