"use strict";
function audit() {
  "use strict";
  const stats={sources:0,assignments:0,walsh_checks:0,sharp_unsat:0,allzero:0,
    random:0,controls:0,radius_neighbors:0,nearest_sat:0,blocks:0,errors:0,max_m:0};
  const ok=(v,msg)=>{if(!v){stats.errors++;throw Error(msg)}};
  const E=(v,sig)=>({v,sig});
  const cube=(list,offset=0)=>list.map(s=>E([offset,offset+1,offset+2],s));
  function violated(F,a) {
    let total=0;for(const C of F){let b=true;for(let j=0;j<3;j++)
      if(((a>>C.v[j])&1)!==((C.sig>>j)&1)){b=false;break}
      if(b)total++;
    }return total;
  }
  function SAT(F,n){for(let a=0;a<(1<<n);a++)if(violated(F,a)===0)return true;return false}
  function moments(F){
    let M=new Map();
    for(const C of F)for(let mask=1;mask<8;mask++){
      let p=1,S=[];
      for(let j=0;j<3;j++)if((mask>>j)&1){S.push(C.v[j]);if((C.sig>>j)&1)p=-p;}
      S.sort((a,b)=>a-b);let key=S.join(",");
      M.set(key,(M.get(key)||0)+p);
    }return M;
  }
  function check(F,n,label){
    let M=moments(F),min=1e9,max=-1,sum=0;
    for(let a=0;a<(1<<n);a++){
      let v=violated(F,a),spectral=F.length;
      for(let [key,c] of M){
        if(c===0)continue;
        let x=1;for(let t of key.split(","))if((a>>Number(t))&1)x=-x;
        spectral+=c*x;
      }
      ok(spectral===8*v,"Walsh "+label);
      min=Math.min(min,v);max=Math.max(max,v);sum+=v;
      stats.assignments++;stats.walsh_checks++;
    }
    let zero=[...M.values()].every(x=>x===0);
    ok(8*sum===F.length*(1<<n),"mean "+label);
    ok(min<=Math.floor(F.length/8),"robust bound "+label);
    ok(zero===(min===max),"flat iff zero "+label);
    ok(zero===(8*min===F.length),"sharp iff zero "+label);
    ok((min===0)===SAT(F,n),"distance zero iff SAT "+label);
    stats.sources++;stats.max_m=Math.max(stats.max_m,F.length);
    if(zero)stats.allzero++;
    if(zero&&F.length)stats.sharp_unsat++;
    return {min,max,zero};
  }
  for(let m=0;m<=8;m++){
    function rec(A,start){
      if(A.length===m){check(cube(A),3,"E3 m="+m);return;}
      for(let s=start;s<8;s++){A.push(s);rec(A,s);A.pop()}
    }rec([],0);
  }
  let seed=0x6b8b4567;
  function rnd(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;}
  for(let n=4;n<=6;n++)for(let z=0;z<900;z++){
    let m=1+rnd()%17,F=[];
    for(let i=0;i<m;i++){
      let vs=[];while(vs.length<3){let j=rnd()%n;if(!vs.includes(j))vs.push(j)}
      F.push(E(vs,rnd()%8));
    }
    check(F,n,"random"+n);stats.random++;
  }
  const tests=[
    {n:3,F:cube([0,1,3]),label:"Horn-like"},
    {n:3,F:cube([0,3,5,6]),label:"XOR parity"},
    {n:4,F:[E([0,1,3],0),E([0,1,3],4)],label:"2SAT auxiliary lift"},
    {n:5,F:[E([0,1,2],7),E([1,2,3],1),E([2,3,4],2)],label:"path"},
    {n:6,F:[...cube([0,1,2,3,4,5,6,7]),...cube([0,1,2,3,4,5,6,7],3)],label:"disjoint products"},
    {n:3,F:cube([0,0,1,2,3,4,5,6,7]),label:"duplication"},
    {n:5,F:[E([4,2,0],3),E([3,1,4],5)],label:"renaming"}
  ];
  for(let q of tests){check(q.F,q.n,q.label);stats.controls++}
  let families=[];
  for(let r=1;r<=8;r++){
    let F=cube(Array.from({length:8*r},(_,i)=>Math.floor(i/r)));
    let out=check(F,3,"Ur"+r);
    ok(out.min===r&&out.max===r&&out.zero,"Ur flat");
    for(let s=0;s<8;s++)for(let j=0;j<3;j++){
      let G=F.map(e=>E(e.v,e.sig));
      for(let i=s*r;i<(s+1)*r;i++)G[i].sig^=1<<j;
      ok(SAT(G,3),"sensitive block Ur"+r);stats.blocks++;
    }
    families.push({r,clauses:8*r,editable_sign_bits:24*r,distance:r,
      nearest_sat_count:"8*3^r",block_sensitivity:24,sensitivity:r===1?24:0});
    if(r<=3){
      const bits=24*r;
      function layer(A,start,left){
        if(left===0){
          let G=F.map(e=>E(e.v,e.sig));
          for(let p of A)G[Math.floor(p/3)].sig^=1<<(p%3);
          let isSat=SAT(G,3);
          if(A.length<r)ok(!isSat,"no nearer SAT");
          else if(isSat)stats.nearest_sat++;
          stats.radius_neighbors++;return;
        }
        for(let i=start;i<=bits-left;i++){
          A.push(i);layer(A,i+1,left-1);A.pop();
        }
      }
      for(let d=0;d<=r;d++)layer([],0,d);
    }
  }
  ok(stats.nearest_sat===312,"nearest neighbors");
  ok(stats.sources===15585,"source count");
  return {run:"TMR2-SRG22",status:"COMPUTATIONAL",seed:"0x6b8b4567",
    exhaustive:"three-variable clause multisets, sizes 0..8",stats,families,
    limits:"No TM compiler; no specialized Horn, 2SAT, GF2, or treewidth solver executed"};
}
console.log(JSON.stringify(audit(),null,2));
