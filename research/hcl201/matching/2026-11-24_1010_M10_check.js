"use strict";
function runM10(){
 const pop=x=>{let n=0;while(x){x&=x-1n;n++}return n};
 const bit=i=>1n<<BigInt(i);
 const hi=x=>x.toString(2).length-1;
 const assert=(c,msg)=>{if(!c)throw Error(msg)};
 let seed=2011010;
 const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const stats={seed:2011010,randomNetworks:0,referenceAssignments:0,decisions:0,SAT:0,UNSAT:0,UNKNOWN:0,lifts:0,hulls:0,uniformChecks:0,uniformAccepted:0,uniformDeclined:0,uniformUnknown:0,badPatternsExamined:0,closureTightened:0,closureFixed:0,scales:[]};
 function space(cols,target){
   const piv=new Map(),ker=[];
   for(let i=0;i<cols.length;i++){
     let v=cols[i],m=bit(i);
     while(v&&piv.has(hi(v))){const [w,z]=piv.get(hi(v));v^=w;m^=z}
     if(v)piv.set(hi(v),[v,m]);else ker.push(m);
   }
   let a=0n,v=target;
   while(v&&piv.has(hi(v))){const [w,z]=piv.get(hi(v));v^=w;a^=z}
   return {a,ker,ok:!v,rank:piv.size};
 }
 function basis(vs){const p=new Map();for(let v of vs){while(v&&p.has(hi(v)))v^=p.get(hi(v));if(v)p.set(hi(v),v)}return [...p.values()]}
 function inspan(v,bs){return space(bs,v).ok}
 function word(a,ker,i){let j=0;while(i){if(i&1n)a^=ker[j];i>>=1n;j++}return a}
 function normalize(arcs,hlo,hhi){
   const raw=arcs.map(a=>({s:a.s,g:BigInt(a.g),l:BigInt(a.s===1?a.l:-a.u),u:BigInt(a.s===1?a.u:-a.l)}));
   const L=raw.reduce((v,a)=>v+a.l,0n),U=raw.reduce((v,a)=>v+a.u,0n);
   if(hlo<L||hhi>U||hlo>hhi)return null;
   const max=(a,b)=>a>b?a:b,min=(a,b)=>a<b?a:b;
   let base=0n,offset=0n;const map=new Map();
   const fixed=raw.map((a,i)=>{
     let l=max(a.l,hlo-(U-a.u)),u=min(a.u,hhi-(L-a.l));
     if(l!==a.l||u!==a.u)stats.closureTightened++;
     if(l===u)stats.closureFixed++;
     base+=l;if(l&1n)offset^=a.g;
     const w=u-l;
     if(w){if(!map.has(a.g))map.set(a.g,{g:a.g,w:0n,ids:[]});const c=map.get(a.g);c.w+=w;c.ids.push(i)}
     return {...a,l,u,w};
   });
   const cs=[...map.values()],W=cs.reduce((v,c)=>v+c.w,0n);
   return {arcs:fixed,cs,W,base,offset};
 }
 function syndrome(cs,p){let t=0n;for(let i=0;i<cs.length;i++)if(p&bit(i))t^=cs[i].g;return t}
 function badSet(D,H,cap=3){
   const k=D.cs.length,W=D.W;
   if(H<0n||H>W)return {outside:true};
   const dl=BigInt(k)-H,du=BigInt(k)-(W-H),d=Number(dl>du?dl:du);
   if(d>cap)return {unknown:true,d};
   let parity=0n;for(let i=0;i<k;i++)if(D.cs[i].w&1n)parity|=bit(i);
   const full=bit(k)-1n, bad=new Set();
   function add(center,lim){
     if(lim<=0)return;
     function rec(start,left,mask){
       const p=center^mask;stats.badPatternsExamined++;
       if((pop(p)&1)===Number(H&1n))bad.add(p);
       if(left===0)return;
       for(let j=start;j<k;j++)rec(j+1,left-1,mask|bit(j));
     }
     rec(0,lim-1,0n);
   }
   add(full,Number(dl));add(full^parity,Number(du));
   return {bad,d:Math.max(0,d)};
 }
 function lift(D,H,p){
   const totals=D.cs.map((c,i)=>p&bit(i)?1n:0n);
   let spare=H-totals.reduce((a,b)=>a+b,0n);
   assert(spare>=0n&&!(spare&1n),"invalid lower bound");
   for(let i=0;i<totals.length;i++){let room=D.cs[i].w-totals[i];room-=room&1n;const a=room<spare?room:spare;totals[i]+=a;spare-=a}
   assert(spare===0n,"invalid upper bound");
   const signed=D.arcs.map(a=>a.l);
   for(let i=0;i<totals.length;i++){let r=totals[i];for(const j of D.cs[i].ids){const a=D.arcs[j].w<r?D.arcs[j].w:r;signed[j]+=a;r-=a}assert(!r,"class lift")}
   return signed.map((v,i)=>v*BigInt(D.arcs[i].s));
 }
 function verify(arcs,x,h,t){
   let net=0n,tag=0n;for(let i=0;i<x.length;i++){assert(x[i]>=BigInt(arcs[i].l)&&x[i]<=BigInt(arcs[i].u),"original bounds");net+=BigInt(arcs[i].s)*x[i];if(x[i]&1n)tag^=BigInt(arcs[i].g)}
   assert(net===h&&tag===t,"original witness");
 }
 function decide(D,h,t,cap=3,probe=null){
   if(!D)return {status:"UNSAT"};
   const H=h-D.base,target=t^D.offset,cols=D.cs.map((c,i)=>((c.g<<1n)|1n)|(probe&&((probe.row&bit(i))!==0n)?bit(probe.shift):0n));
   const tar=(target<<1n)|(H&1n)|(probe&&probe.value?bit(probe.shift):0n);
   if(H<0n||H>D.W)return {status:"UNSAT"};
   const A=space(cols,tar);
   if(!A.ok)return {status:"UNSAT"};
   const B=badSet(D,H,cap);if(B.unknown)return {status:"UNKNOWN"};
   const bad=[...B.bad].filter(p=>{let v=0n;for(let i=0;i<cols.length;i++)if(p&bit(i))v^=cols[i];return v===tar});
   const n=bit(A.ker.length),bn=BigInt(bad.length);
   if(n===bn)return {status:"UNSAT",count:n,bad:bn};
   const blocked=new Set(bad);let p;
   for(let i=0n;i<=bn;i++){const w=word(A.a,A.ker,i);if(!blocked.has(w)){p=w;break}}
   assert(p!==undefined,"witness search");
   let hull;
   if(n>2n*bn)hull=A.ker;
   else {const dif=[];for(let i=0n;i<n;i++){const w=word(A.a,A.ker,i);if(!blocked.has(w))dif.push(w^p)}hull=basis(dif)}
   return {status:"SAT",p,hull,x:lift(D,H,p),count:n,bad:bn};
 }
 function saturation(D,lo,up,cap=3){
   if(!D)return "UNSAT";
   const L=lo-D.base,U=up-D.base,k=BigInt(D.cs.length),W=D.W;
   if(L<0n||U>W)return "UNSAT";
   if(k-L>BigInt(cap)||k-(W-U)>BigInt(cap))return "UNKNOWN";
   const cols=D.cs.map(c=>(c.g<<1n)|1n),A=space(cols,0n),size=bit(A.ker.length);
   const boundary=new Set();
   for(let h=L;h<=U&&h<k;h++)boundary.add(h);
   for(let h=U;h>=L&&h>W-k;h--)boundary.add(h);
   for(const H of boundary){
     const B=badSet(D,H,cap);assert(B.bad,"boundary cap");
     const counts=new Map();
     for(const p of B.bad){const t=syndrome(D.cs,p);const count=(counts.get(t)||0n)+1n;counts.set(t,count);if(count===size)return "DECLINED"}
   }
   return "SATURATED";
 }
 function ref(arcs){
   const out=[];function rec(i,x,h,t){
     if(i===arcs.length){out.push({x:[...x],h,t});return}
     const a=arcs[i];for(let v=a.l;v<=a.u;v++){x.push(BigInt(v));rec(i+1,x,h+BigInt(a.s*v),t^((v&1)?BigInt(a.g):0n));x.pop()}
   }rec(0,[],0n,0n);stats.referenceAssignments+=out.length;return out;
 }
 function classWord(D,x){let p=0n;for(let i=0;i<D.cs.length;i++){let v=0n;for(const j of D.cs[i].ids)v+=BigInt(D.arcs[j].s)*x[j]-D.arcs[j].l;if(v&1n)p|=bit(i)}return p}
 for(let z=0;z<180;z++){
   const arcs=Array.from({length:2+rand(6)},()=>{const l=rand(2);return {l,u:l+rand(4),s:rand(2)?1:-1,g:rand(8)}});
   const refx=ref(arcs),lo=refx.reduce((a,r)=>r.h<a?r.h:a,refx[0].h),up=refx.reduce((a,r)=>r.h>a?r.h:a,refx[0].h);
   const h=lo+BigInt(rand(Number(up-lo+1n))),D=normalize(arcs,h,h);
   for(let tt=0;tt<8;tt++){
     const t=BigInt(tt),re=refx.filter(r=>r.h===h&&r.t===t),a=decide(D,h,t);
     stats.decisions++;stats[a.status]++;
     if(a.status==="UNKNOWN")continue;
     assert((a.status==="SAT")===!!re.length,"decision mismatch");
     if(a.status==="SAT"){
       verify(arcs,a.x,h,t);stats.lifts++;
       const ps=[...new Set(re.map(r=>classWord(D,r.x)))],bs=basis(ps.map(p=>p^ps[0]));
       assert(a.hull.length===bs.length&&ps.every(p=>inspan(p^a.p,a.hull)),"hull mismatch");stats.hulls++;
       const row=BigInt(rand(1<<D.cs.length));
       for(let value=0;value<2;value++){
         const q=decide(D,h,t,3,{row,value,shift:5});
         const re2=ps.some(p=>((pop(p&row)&1)===value));
         stats.decisions++;stats[q.status]++;
         assert(q.status!=="UNKNOWN"&&(q.status==="SAT")===re2,"probe mismatch");
         if(q.status==="SAT"){verify(arcs,q.x,h,t);assert((pop(q.p&row)&1)===value,"probe witness");stats.lifts++}
       }
     }
   }
   const l=lo+BigInt(rand(Number(up-lo+1n))),r=l+BigInt(rand(Number(up-l+1n))),Q=normalize(arcs,l,r);
   const sat=saturation(Q,l,r);
   stats.uniformChecks++;
   if(sat==="UNKNOWN")stats.uniformUnknown++;
   else{
     let truth=true;
     for(let h=l;h<=r;h++){
       const actual=new Set(refx.filter(x=>x.h===h).map(x=>x.t));
       for(let t=0n;t<8n;t++){
         const expected=space(Q.cs.map(c=>(c.g<<1n)|1n),((t^Q.offset)<<1n)|((h-Q.base)&1n)).ok;
         if(expected!==actual.has(t))truth=false;
       }
     }
     assert((sat==="SATURATED")===truth,"uniform mismatch");
     if(truth)stats.uniformAccepted++;else stats.uniformDeclined++;
   }
   stats.randomNetworks++;
 }
 for(const k of [8,16,32,64,128,256]){
   for(const dep of [false,true]){
     const gs=Array.from({length:k},(_,i)=>dep?(i<4?BigInt(i):bit(i-2)):bit(i));
     const arcs=gs.flatMap(g=>[{l:0,u:1,s:1,g},{l:0,u:1,s:1,g}]);
     const h=BigInt(k-2),D=normalize(arcs,h,h),all=gs.reduce((a,b)=>a^b,0n),neighbor=all^gs[k-1]^gs[k-2];
     const a=decide(D,h,all),b=decide(D,h,neighbor),sat=saturation(D,h,h);
     assert(a.status===(dep?"SAT":"UNSAT")&&b.status==="SAT","scale decision");
     assert(sat===(dep?"SATURATED":"DECLINED"),"scale saturation");
     if(a.status==="SAT")verify(arcs,a.x,h,all);verify(arcs,b.x,h,neighbor);
     stats.scales.push({k,arcs:arcs.length,dependent:dep,fullTarget:a.status,neighbor:b.status,uniform:sat,forbiddenPatterns:badSet(D,h-D.base).bad.size,augmentedNullity:space(D.cs.map(c=>(c.g<<1n)|1n),0n).ker.length});
   }
 }
 // Huge binary widths: exact arithmetic; no expansion into unit arcs.
 const huge=2n**100n,arcs=[{l:0n,u:huge,s:1,g:1n},{l:0n,u:huge,s:1,g:2n}],h=huge,D=normalize(arcs,h,h);
 const a=decide(D,h,3n);assert(a.status==="SAT","huge capacity");verify(arcs,a.x,h,3n);stats.hugeCapacityBits=101;
 return stats;
}
console.log(JSON.stringify(runM10(),null,2));
