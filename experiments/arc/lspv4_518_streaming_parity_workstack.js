/* LSPV-4/518: independent signed original strict-3CNF and sequential-stack DFS audit.
   Restricted semantic upper control, NOT native FLMV or R_mix341 execution. */
const LSPV4_518_RESULT = (function () {
"use strict";
let checks=0, rejected=0, children=0;
function requireIt(x,msg){checks++;if(!x)throw Error(msg)}
function graphs(r) {
  if(r===0){let a=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)a.push([i,j]);return [4,a];}
  const a=[], n=2*r;
  for(let i=0;i<r;i++){
    a.push([i,(i+1)%r],[r+i,r+(i+1)%r],[i,r+i]);
  }
  return [n,a.map(p=>p.slice().sort((u,v)=>u-v)).sort((x,y)=>x[0]-y[0]||x[1]-y[1])];
}
const baseForbidden=["001","010","100","111"];
function encode(n,edges,b) {
 const m=edges.length, w=Math.ceil(Math.log2(m+1));
 let packet="10110110"+"1".repeat(m)+"0",signAt=[];
 for(let v=0;v<n;v++){
   const ids=edges.flatMap(([x,y],j)=>x===v||y===v?[j+1]:[]);
   requireIt(ids.length===3,"cubic");
   for(const trip of baseForbidden){
     for(let z=0;z<3;z++){
       packet+=ids[z].toString(2).padStart(w,"0");
       if(z===0)signAt.push([v,packet.length]);
       packet+=String((Number(trip[z])^(z===0?b[v]:0)));
     }
   }
 }
 return {packet:packet+"01",signAt};
}
function decode(packet){
 if(!/^([01]+)$/.test(packet)||!packet.startsWith("10110110"))return null;
 let pos=8,m=0;
 while(packet[pos]==="1"){m++;pos++;}
 if(packet[pos]!=="0"||m<6||m%3)return null;
 pos++;
 let n=2*m/3,w=Math.ceil(Math.log2(m+1));
 if(packet.length!==8+m+1+12*n*(w+1)+2||!packet.endsWith("01"))return null;
 const charges=[],owners=Array.from({length:m+1},()=>[]);
 for(let v=0;v<n;v++){
   let ids, sigs=[];
   for(let a=0;a<4;a++){
     let local=[],sign="";
     for(let j=0;j<3;j++){
       const eid=parseInt(packet.slice(pos,pos+w),2);pos+=w;
       const val=packet[pos++];if(!eid||eid>m)return null;
       local.push(eid);sign+=val;
     }
     if(new Set(local).size!==3)return null;
     if(ids&&local.join(",")!==ids.join(","))return null;
     ids=local;sigs.push(sign);
   }
   const s0=baseForbidden, s1=baseForbidden.map(x=>String(Number(x[0])^1)+x.slice(1));
   const bb=JSON.stringify(sigs)===JSON.stringify(s0)?0:JSON.stringify(sigs)===JSON.stringify(s1)?1:-1;
   if(bb<0)return null;
   charges.push(bb);
   for(const eid of ids)owners[eid].push(v);
 }
 if(pos!==packet.length-2)return null;
 let adj=Array.from({length:n},()=>[]);
 for(let e=1;e<=m;e++){
   if(owners[e].length!==2||owners[e][0]===owners[e][1])return null;
   const [u,v]=owners[e];adj[u].push(v);adj[v].push(u);
 }
 if(adj.some(x=>x.length!==3||new Set(x).size!==3))return null;
 let reached=new Set([0]),pending=[0];
 for(let i=0;i<pending.length;i++)for(const j of adj[pending[i]])if(!reached.has(j)){reached.add(j);pending.push(j);}
 if(reached.size!==n)return null;
 return {charges,m,n};
}
function traverse(r,bp){
 let states=Array(r+1).fill(0),dep=0,par=bp,down=0,up=0,labels=[];
 for(;;){
   if(dep===r){
     labels.push(1-par);
     dep--;up++;
     if(states[dep]===2)par^=1;
   } else if(states[dep]===0){
     states[dep]=1;dep++;states[dep]=0;down++;
   } else if(states[dep]===1){
     states[dep]=2;par^=1;dep++;states[dep]=0;down++;
   } else {
     if(dep===0)break;
     dep--;up++;if(states[dep]===2)par^=1;
   }
 }
 requireIt(labels.length===2**r,"leaves");
 requireIt(down===2*(2**r-1)&&up===down,"edges");
 requireIt(par===bp,"parity restoration");
 return {labels,down,up,peak:r+1};
}
const cases=[];
for(const [name,r] of [["K4",0],["prism3",3],["prism4",4],["prism5",5]]){
 const [n,edges]=graphs(r),k=n-1, base=encode(n,edges,Array(n).fill(0));
 requireIt(decode(base.packet)!==null,"base");
 for(let bits=1;bits<=Math.min(k,8);bits++){
   const plan=traverse(bits,0);
   for(let d=0;d<2**bits;d++){
     const b=Array(n).fill(0);
     for(let i=0;i<bits;i++)b[i]=(d>>(bits-i-1))&1;
     const c=encode(n,edges,b),got=decode(c.packet);
     requireIt(got&&got.charges.join("")===b.join(""),"parse source");
     let diffs=0;
     for(let i=0;i<c.packet.length;i++)if(c.packet[i]!==base.packet[i])diffs++;
     requireIt(diffs===4*b.reduce((a,z)=>a+z,0),"4-bit charge blocks");
     requireIt(plan.labels[d]===1-(b.reduce((a,z)=>a^z,0)),"parity label");
     children++;
   }
 }
 const bad=[base.packet.slice(0,-1),base.packet+"0","0"+base.packet.slice(1),base.packet.slice(0,8)+"0"+base.packet.slice(9),base.packet.slice(0,-2)+"11"];
 for(const s of bad){requireIt(decode(s)===null,"corrupt rejection");rejected++;}
 const p=traverse(k,0);
 cases.push({name,n,m:edges.length,length:base.packet.length,q:2**k,down:p.down,up:p.up,peak:p.peak,sat:p.labels.reduce((a,z)=>a+z,0)});
}
return {status:"PASS",title:"LSPV-4/518 Independent V8 sibling-port test",cases,checks,children,rejected,model:"Original source bit serialization + symbolic adjacent WORK-stack; no native FLMV or historic R_mix341"};
})()

if (typeof console !== 'undefined' && console.log) console.log(JSON.stringify(LSPV4_518_RESULT,null,2));
