"use strict";
const audit = function audit() {
  const check=(ok,msg)=>{if(!ok)throw Error(msg)};
  const original=t=>{const z=4*t+1, f=[];for(let i=0;i<t;i++)f.push([z,4*i+1,4*i+2]);for(let j=0;j<t;j++)f.push([-z,4*j+3,4*j+4]);return f};
  const expanded=t=>{const p=[];for(let i=0;i<t;i++)for(let j=0;j<t;j++)p.push([4*i+1,4*i+2,4*j+3,4*j+4]);return p};
  const truth=(lit,mask)=>lit>0?Boolean(mask & (1<<(lit-1))):!Boolean(mask & (1<<(-lit-1)));
  const sat=(cs,mask)=>cs.every(c=>c.some(lit=>truth(lit,mask)));
  const serial=(n,cs)=>"p cnf "+n+" "+cs.length+"\n"+cs.map(c=>c.join(" ")+" 0\n").join("");
  const makeCircuit=t=>{const nodes=[]; const gate=(op,x,y)=>{const v=4*t+nodes.length+1;nodes.push({v,op,x,y});return v};let a=[],b=[];for(let i=0;i<t;i++)a.push(gate("OR",4*i+1,4*i+2));for(let j=0;j<t;j++)b.push(gate("OR",4*j+3,4*j+4));while(a.length>1)a=[gate("AND",a[0],a[1]),...a.slice(2)];while(b.length>1)b=[gate("AND",b[0],b[1]),...b.slice(2)];const root=gate("OR",a[0],b[0]);return {nodes,root}};
  const evalCircuit=(c,mask,t)=>{const v=new Map();for(let i=1;i<=4*t;i++)v.set(i,Boolean(mask&(1<<(i-1))));for(let g of c.nodes)v.set(g.v,g.op==="OR"?(v.get(g.x)||v.get(g.y)):(v.get(g.x)&&v.get(g.y)));return v};
  const tseitin=c=>{const cs=[];for(let {v,op,x,y} of c.nodes){if(op==="OR")cs.push([v,-x],[v,-y],[-v,x,y]);else cs.push([-v,x],[-v,y],[v,-x,-y])}cs.push([c.root]);return cs};
  const satValues=(cs,m)=>cs.every(c=>c.some(l=>l>0?m.get(l):!m.get(-l)));
  const parse=s=>{const ls=s.trimEnd().split("\n"),h=ls[0].trim().split(/\s+/);check(h.length===4&&h[0]==="p"&&h[1]==="cnf","header");const n=+h[2],m=+h[3];check(n>0&&m>=0&&ls.length===m+1,"record count");const cs=ls.slice(1).map(s=>{const v=s.trim().split(/\s+/).map(Number);check(v.length>1&&v.at(-1)===0&&v.slice(0,-1).every(x=>x!==0&&Math.abs(x)<=n),"literal syntax");return v.slice(0,-1)});return {n,cs}};
  const compact=(s,factor=2)=>{const {n,cs}=parse(s);check(n%4===0,"shape");const t=n/4, p=expanded(t);check(t>=1&&cs.length>=t*t&&cs.length-t*t<=factor*t,"context bound");for(let j=0;j<t*t;j++)check(cs[j].length===4&&cs[j].every((x,k)=>x===p[j][k]),"noncanonical prefix");const R=cs.slice(t*t);check(R.every(c=>c.length>=1&&c.length<=3),"context width");return serial(4*t+1,[...original(t),...R])};
  const fam=[];let assignments=0,contexts=0,critical=0;
  for(let t=1;t<=4;t++){
    const f=original(t),p=expanded(t),circ=makeCircuit(t),tc=tseitin(circ);let yes=0;
    check(f.length===2*t&&p.length===t*t&&circ.nodes.length===4*t-1&&tc.length===12*t-2,"sizes");
    check(tc.reduce((a,c)=>a+c.length,0)===28*t-6,"Tseitin literal slots");
    for(let mask=0;mask<2**(4*t);mask++){
      const z=1<<(4*t),e=sat(f,mask)||sat(f,mask|z),q=sat(p,mask),v=evalCircuit(circ,mask,t);
      check(e===q&&e===v.get(circ.root)&&satValues(tc,v)===e,"semantic "+t+"/"+mask);
      assignments++;if(e)yes++;
      if(t===4){const labels=[[],[[-1],[-2]],[[-3],[-4]],[[-1],[-2],[-3],[-4]]];for(let R of labels){const ok=sat(R,mask);check((e&&ok)===(q&&ok),"both-side context");contexts++}}
    }
    for(let i=0;i<t;i++)for(let j=0;j<t;j++){
      let mask=(2**(4*t)-1);const four=[4*i+1,4*i+2,4*j+3,4*j+4];for(let k of four)mask&=~(1<<(k-1));
      check(!sat(p,mask),"critical false");check(p.filter(c=>!sat([c],mask)).length===1,"unique critical clause");
      for(let k of four)check(sat(p,mask|(1<<(k-1))),"upward neighbor");
      critical++;
    }
    fam.push({t,assignments:2**(4*t),yes,original_clauses:2*t,projected_clauses:t*t,gates:4*t-1,gate_input_wires:8*t-2,Tseitin_clauses:tc.length,Tseitin_literal_occurrences:28*t-6,original_bytes:serial(4*t+1,f).length,projected_bytes:serial(4*t,p).length,Tseitin_bytes:serial(circ.root,tc).length});
  }
  check(assignments===69904&&contexts===262144,"reproduction totals");
  const lengths=[];for(let t of [1,2,3,4,8,16,32,64,128])for(let k of [0,t]){
    const R=[];for(let i=0;i<k;i++)R.push([4*i+1,-(4*i+2),4*i+3]);
    const inp=serial(4*t,[...expanded(t),...R]),out=compact(inp),n=inp.length*8,c=out.length*8;
    lengths.push({t,R:k,N_bits:n,Nchild_bits:c,ratio:Math.round(c/n*1e6)/1e6,below_N_to_075:c<=n**.75});
  }
  const malformed=serial(16,expanded(4)).replace("1 2 3 4 0","1 2 3 5 0");let rejected=false;
  try{compact(malformed)}catch(e){rejected=true}check(rejected,"malformed rejected");
  const t2=original(2), R=[[-1],[-2],[-3],[-4]],dropped=[[9,5,6],[-9,7,8],...R];let fromSAT=false;
  for(let m=0;m<512;m++)if(sat([...t2,...R],m))fromSAT=true;
  check(!fromSAT&&sat(dropped,~15 & 511),"unsafe deletion counterexample");
  const embeds=[];
  for(let k of [7,8]){
    const G=[];for(let m=0;m<k;m++)G.push([0,1,2].map(i=>(m&(1<<i))?i+1:-(i+1)));
    const t=2*k,B=[];for(let i=0;i<t;i++)B.push(4*i+3,4*i+4);
    const R=Array.from({length:t},(_,i)=>[4*i+1]);
    for(let c of G)R.push(c.map(l=>l>0?B[l-1]:-B[-l-1]));
    const inp=serial(4*t,[...expanded(t),...R]),out=compact(inp,2);
    let Gsat=false;for(let m=0;m<8;m++)Gsat ||=sat(G,m);
    check(Gsat===(k===7),"embedding expected label");
    embeds.push({G_clauses:k,t,R_clauses:R.length,G_SAT:Gsat,N_bits:8*inp.length,Nchild_bits:8*out.length});
  }
  return {name:"LSPV2 SINGLE-CHILD PROJECTION CLOSURE",date:"2026-10-28",status:{single_child:"PROVED/RESTRICTED",NP_hard_source:"PROVED/RESTRICTED",finite:"COMPUTATIONAL",recursive_closure:"OPEN",P_vs_NP:"OPEN"},assignment_controls:assignments,context_assignment_controls:contexts,critical_pairs:critical,family:fam,physical_growth:lengths,malformed_rejected:rejected,unsafe_deletion_falsified:!fromSAT,embedded_3SAT_controls:embeds,limitations:"This code models fixed-width Boolean relations and actual ASCII DIMACS output bytes; it is not a TM-cycle or peak-workspace certificate."};
};
console.log(JSON.stringify(audit(),null,2));
