function run(){
"use strict";
// LSPV-1/504 independent finite semantic test, NOT historical R_mix341 checker.
function val(op,a,b){return (op>>(2*a+b))&1;}
function aff(op){let v=[val(op,0,0),val(op,0,1),val(op,1,0),val(op,1,1)];return (v[0]^v[1]^v[2]^v[3]) ? null:[v[0],v[2]^v[0],v[1]^v[0]];}
function asrt(x,msg){if(!x)throw Error(msg);checks++;}
function evalCircuit(n,gates,bits){let z=Array.from({length:n},(_,j)=>(bits>>j)&1);for(let g of gates)z.push(val(g[0],z[g[1]],z[g[2]]));return z;}
function formValue(f,bits){let m=f[0],v=f[1];while(m){let t=m&(-m),i=31-Math.clz32(t);v^=(bits>>i)&1;m^=t;}return v;}
function tree(n,gates){let leaves=[{G:[],F:Array.from({length:n},(_,j)=>[1<<j,0])}];for(let j=0;j<gates.length;j++){let [op,x,y]=gates[j],next=[];asrt(x<n+j&&y<n+j&&x>=0&&y>=0,"bad gate input");for(let leaf of leaves){let a=leaf.F[x],b=leaf.F[y],z=aff(op);
if(z){next.push({G:leaf.G,F:leaf.F.concat([[(z[1]?a[0]:0)^(z[2]?b[0]:0),z[0]^(z[1]?a[1]:0)^(z[2]?b[1]:0)]])});continue;}
for(let k=0;k<2;k++){let d0=val(op,k,0),d1=val(op,k,1),v=d0^d1;next.push({G:leaf.G.concat([[a,k]]),F:leaf.F.concat([[v?b[0]:0,d0^(v?b[1]:0)]])});}}
leaves=next;}return leaves;}
let checks=0,paths=0,leaves=0,nonlin=0,big=0,malformed=0,missingBranch=0,wrongTarget=0;
const families=[];
for(let op=0;op<16;op++)families.push({n:3,g:[[op,0,1],[6,3,2],[6,4,0]]});
for(let n=3;n<=7;n++){let gs=[];for(let j=0;j<n-1;j++)gs.push([6,n+j-1>=n?n+j-1:0,(j+1)%n]);gs.push([8,n+n-2,n-1]);gs.push([6,n+n-1,0]);families.push({n,g:gs});}
for(let fam of families){let {n,g}=fam,T=tree(n,g),nu=g.filter(x=>aff(x[0])===null).length;asrt(T.length===2**nu,"leaf count");nonlin+=nu;leaves+=T.length;if(n>=6)big++;
for(let bits=0;bits<(1<<n);bits++){let orig=evalCircuit(n,g,bits),ok=0;
for(let l of T){if(!l.G.every(([a,k])=>formValue(a,bits)===k))continue;ok++;
for(let i=0;i<orig.length;i++)asrt(formValue(l.F[i],bits)===orig[i],"gate affine normalization");
let a=[0,n,g.length+n-1].filter(x=>x<orig.length),b=[1,n].filter(x=>x<orig.length);
let f=[0,0],u=0;
for(let i of a){f[0]^=l.F[i][0];f[1]^=l.F[i][1];u^=orig[i];}
for(let i of b){f[0]^=l.F[i][0];f[1]^=l.F[i][1];u^=orig[i];}
asrt(formValue(f,bits)===u,"global XOR commutes");}
asrt(ok===1,"unique affine-guard leaf");paths++;
}}
let bad=false;try{tree(2,[[8,0,3]]);}catch(e){bad=true;}asrt(bad,"malformed gate accepted");malformed++;
let t=tree(2,[[8,0,1]]),wrong=false;for(let x=0;x<4;x++)if(t.slice(0,1).filter(l=>l.G.every(([a,k])=>formValue(a,x)===k)).length!==1)wrong=true;asrt(wrong,"missing AND branch accepted");missingBranch++;
let yy=evalCircuit(2,[[8,0,1]],3),l=t.find(l=>l.G.every(([a,k])=>formValue(a,3)===k));asrt((formValue(l.F[2],3)^1)!==yy[2],"flipped row RHS accepted");wrongTarget++;
return {run:"LSPV-1/504",kind:"COMPUTATIONAL independent JS affine-guard semantic controls",source:"experiments/arc/lspv1_504_affine_guard_controls.cjs",families:families.length,gate_tables_tested:16,checks,leaf_records:leaves,input_paths:paths,nonlinear_gate_instances:nonlin,large_affine_cone_controls:big,malformed_rejected:malformed,omitted_AND_branch_rejected:missingBranch,wrong_row_RHS_rejected:wrongTarget,authoritative_historical_checker:false,full_syntactic_proof_checker:false,p_vs_np:"OPEN"};
}
console.log(JSON.stringify(run(),null,2));
