"use strict";
// LSPV-2/497 independently replayable V8 source grammar test.
// Not the historical R_mix341 checker and not an FLMV machine.
function mk(name){
 let H,L,R,edges,M;
 if(name==="K33"){H=6;L=[0,1,2];R=[3,4,5];edges=L.flatMap(u=>R.map(v=>[u,v]));M=L.map(u=>[u,u+3]);}
 else if(name==="Q3"){H=8;L=[0,3,5,6];R=[1,2,4,7];edges=[];for(let u=0;u<8;u++)for(let v=u+1;v<8;v++)if([1,2,4].includes(u^v))edges.push([u,v]);M=L.map(u=>[Math.min(u,u^1),Math.max(u,u^1)]);}
 else {H=14;L=[0,1,2,3,4,5,6];R=L.map(u=>u+7);edges=L.flatMap(u=>[0,1,3].map(s=>[u,7+(u+s)%7])).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);M=L.map(u=>[u,u+7]);}
 let f=edges.filter(e=>!M.some(p=>p[0]===e[0]&&p[1]===e[1]));
 return {H,L,R,M,f,order:L.concat(R),name};
}
function clauses(ids,q){let out=[];for(let b=0;b<8;b++){let a=[(b>>2)&1,(b>>1)&1,b&1];if((a[0]^a[1]^a[2])!==q)out.push(ids.map((v,j)=>a[j]?-v:v));}return out;}
function varset(g,v,a,b){
 let ids=[];for(let j=0;j<g.M.length;j++)if(g.M[j].includes(v)){let word=g.L.includes(v)?a:b;ids.push(2*j+1+((word>>j)&1));}
 for(let j=0;j<g.f.length;j++)if(g.f[j].includes(v))ids.push(g.H+j+1);
 return ids.sort((x,y)=>x-y);
}
function gen(g,a,b){
 let H=g.H,w=Math.ceil(Math.log2(2*H+1));
 let cs=g.order.flatMap(v=>clauses(varset(g,v,a,b),v===0?1:0));
 let s="11100011"+"1".repeat(H)+"0"+"1".repeat(2*H)+"0";
 for(let c of cs)for(let lit of c)s+=(lit<0?"1":"0")+Math.abs(lit).toString(2).padStart(w,"0");
 return {s:s+"10",cs};
}
function valid(s,g){
 let H=g.H,w=Math.ceil(Math.log2(2*H+1));
 if(typeof s!=="string"||!/^[01]+$/.test(s)||s.length!==3*H+12+12*H*(w+1))return "OUTSIDE";
 let head="11100011"+"1".repeat(H)+"0"+"1".repeat(2*H)+"0";
 if(s.slice(0,head.length)!==head||s.slice(-2)!=="10")return "OUTSIDE";
 for(let p=0;p<H;p++){
  let v=g.order[p],start=head.length+p*12*(w+1),data=[];
  for(let i=0;i<12;i++){let k=start+i*(w+1),id=parseInt(s.slice(k+1,k+w+1),2);data.push(s[k]==="1"?-id:id);}
  let j=g.M.findIndex(pair=>pair.includes(v));if(j<0)return "OUTSIDE";
  let id=Math.abs(data[0]);if(id!==2*j+1&&id!==2*j+2)return "OUTSIDE";
  let local=[id];for(let t=0;t<g.f.length;t++)if(g.f[t].includes(v))local.push(H+t+1);
  if(local.length!==3)return "OUTSIDE";
  let want=clauses(local.sort((x,y)=>x-y),v===0?1:0).flat();
  if(!data.every((z,i)=>z===want[i]))return "OUTSIDE";
 }
 const first=v=>{let p=g.order.indexOf(v),at=head.length+p*12*(w+1)+1;return parseInt(s.slice(at,at+w),2);};
 return g.M.some(([u,v])=>first(u)!==first(v))?"MEMBER_SAT":"MEMBER_UNSAT";
}
function mutate(s,k){return s.slice(0,k)+(s[k]==="1"?"0":"1")+s.slice(k+1);}
function run(){
 let cases=0,checks=0,rejected=0,sat=0,unsat=0,graphs=[];
 const check=(a,msg)=>{checks++;if(!a)throw Error(msg+" #"+checks);};
 for(let nm of ["K33","Q3","HEAWOOD"]){
  let g=mk(nm),m=g.H/2,pairs=[];
  if(m<=4){for(let a=0;a<1<<m;a++)for(let b=0;b<1<<m;b++)pairs.push([a,b]);}
  else{for(let a=0;a<1<<m;a++)pairs.push([a,a]);for(let a=0;a<64;a++)pairs.push([a,a^1]);}
  for(let [a,b] of pairs){
   let {s,cs}=gen(g,a,b);check(valid(s,g)===(a===b?"MEMBER_UNSAT":"MEMBER_SAT"),"decision "+nm+" "+a+" "+b);
   check(cs.length===4*g.H&&new Set(cs.map(c=>c.join(","))).size===4*g.H,"original clauses");
   check(cs.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3&&c.every(x=>Math.abs(x)>=1&&Math.abs(x)<=2*g.H)),"proper source");
   cases++;sat+=a!==b;unsat+=a===b;
  }
  const s=gen(g,0,0).s,head=8+(g.H+1)+(2*g.H+1),width=Math.ceil(Math.log2(2*g.H+1)),unit=12*(width+1);
  const bad=[mutate(s,0),s.slice(0,-2)+"00",s+"1",s.slice(0,-1),"x"+s.slice(1),mutate(s,head),mutate(s,head+1),s.slice(0,head+unit)+s.slice(head,head+unit)+s.slice(head+2*unit),mutate(s,8),mutate(s,8+g.H+1),mutate(s,head+8*(width+1))];
  for(let y of bad){check(valid(y,g)==="OUTSIDE","corrupt "+nm);rejected++;}
  graphs.push({graph:nm,H:g.H,N:s.length,pairs:pairs.length});
 }
 return {artifact:"LSPV2_497_INDEPENDENT_V8",cases,sat,unsat,rejected,checks,graphs,native_FLMV:false,historical_Rmix341:false};
}
