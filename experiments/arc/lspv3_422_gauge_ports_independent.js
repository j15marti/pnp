// LSPV-3/422: independent finite gauge-covariance audit for Rmix341-CANON2.
// Run: node lspv3_422_gauge_ports_independent.js
// Does not change the historical R_mix341 calculus.
"use strict";
function ordered(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x)}
function equal(a,b){return JSON.stringify(a)===JSON.stringify(b)}
function check(p,m){if(!p)throw Error(m)}
function facet(a,b,z,t,j){const x=j>>1,y=j&1;return ordered([x?-a:a,y?-b:b,t[x+2*y]?z:-z])}
function ftransform(t,da,db,dz){return Array.from({length:4},(_,j)=>t[((j&1)^da)+2*((j>>1)^db)]^dz)}
function sign(l,d){return d[Math.abs(l)]?-l:l}
function flipClause(c,d){return ordered(c.map(x=>sign(x,d)))}
function indexFlip(j,da,db){return 2*((j>>1)^da)+((j&1)^db)}
function oriented(A,B,p){let v=[];for(const s of [1,-1])if(A.includes(s*p)&&B.includes(-s*p))v.push(ordered([...A.filter(x=>x!==s*p),...B.filter(x=>x!==-s*p)]));return v}
function evalGate(t,a,b){return t[a+2*b]}
function gateTable(n){return Array.from({length:4},(_,j)=>(n>>j)&1)}
function tests(){
 let count=0,ports=0,orientedChecks=0,assignments=0,gfChecks=0;
 const masks=[[0,0,0,1],[0,1,1,0],[0,1,1,1],[1,1,1,0]];
 for(let f=0;f<16;f++)for(let g=0;g<16;g++)for(let h of masks){
   let a=gateTable(f),b=gateTable(g),c=h;
   for(let bits=0;bits<8;bits++){
     let d={1:0,2:0,3:bits&1,4:(bits>>1)&1,5:(bits>>2)&1};
     const A=ftransform(a,0,0,d[3]),B=ftransform(b,d[3],d[3],d[4]),C=ftransform(c,d[3],d[4],d[5]);
     const defs=[{inputs:[1,1],var:3,old:a,now:A},{inputs:[3,3],var:4,old:b,now:B},{inputs:[3,4],var:5,old:c,now:C}];
     for(let v=0;v<4;v++){
       let x=v&1,z=evalGate(a,x,x),w=evalGate(b,z,z),u=evalGate(c,z,w);
       let zp=evalGate(A,x,x),wp=evalGate(B,zp,zp),up=evalGate(C,zp,wp);
       check(zp===(z^d[3])&&wp===(w^d[4])&&up===(u^d[5]),"gate value covariance");
       assignments++;
     }
     for(const gate of defs){
       let [i,j]=gate.inputs,z=gate.var;
       for(let k=0;k<4;k++){
         const after=indexFlip(k,d[i],d[j]);
         check(equal(flipClause(facet(i,j,z,gate.old,k),d),facet(i,j,z,gate.now,after)),"facet selector "+k);
         ports++;
         const src=facet(i,j,z,gate.old,k), src2=facet(i,j,z,gate.now,after);
         for(const unit of [[i],[-i]]){
           const orig=oriented(src,unit,i),mapped=oriented(src2,flipClause(unit,d),i);
           check(equal(orig.map(q=>JSON.stringify(flipClause(q,d))).sort(),mapped.map(JSON.stringify).sort()),"oriented RES");
           orientedChecks++;
         }
       }
     }
     const E1={mask:[1,3,4],rhs:1},E2={mask:[2,4,5],rhs:0};
     const cov=e=>({mask:e.mask,rhs:e.rhs^e.mask.reduce((v,x)=>v^d[x],0)});
     const xor=(x,y)=>({mask:ordered([...new Set([...x.mask,...y.mask])].filter(v=>x.mask.includes(v)!==y.mask.includes(v))).map(Math.abs),rhs:x.rhs^y.rhs});
     const x=xor(E1,E2),y=xor(cov(E1),cov(E2)),z=cov(x);
     check(equal(y,z),"GF(2) covariance");gfChecks++;
     count++;
   }
 }
 check(count===8192,"case count");
 return {status:"PASS",status_scope:"CANON2 proposed completion (not historical native bytes)",cases:count,gate_semantic_assignments:assignments,paid_DEF_facet_port_checks:ports,oriented_RES_checks:orientedChecks,GF2_checks:gfChecks,paid_gates_preserved:true,B3:"OPEN",P_versus_NP:"OPEN"};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(tests(),null,2));
