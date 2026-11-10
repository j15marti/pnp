// LSPV-1/548: Source-authenticated bit-PHP -> unary PHP compiler
// Node.js 18+, no dependencies. Proof-system model: each fresh binary DEF
// costs one node; its exact CNF facets are owner-bound free views.
// This is a DECLARED SEMANTIC COMPLETION, not a historical checker.
"use strict";
function compile(ell) {
  if (!Number.isInteger(ell) || ell < 2 || ell > 4) throw Error("ell must be 2..4");
  const n=2**ell, pigeons=n+1;
  const x=(i,k)=>1+i*ell+k;
  let next=pigeons*ell, defs=0, resolutions=0, facets=0;
  const rows=new Map(), defOwners=new Map(), prefix=[], imp=[];
  let serial=0;
  const norm=a=>[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
  const equal=(a,b)=>JSON.stringify(norm(a))===JSON.stringify(norm(b));
  function add(id, clause, tag, owner=null) {
    if(rows.has(id)) throw Error("duplicate proof id "+id);
    const c=norm(clause); if(c.some(v=>c.includes(-v)))throw Error("tautology in "+id);
    rows.set(id,{clause:c,tag,owner}); return id;
  }
  function source(id,clause){return add(id,clause,"SOURCE");}
  function own(i,p,kind,input,pivot=null) {
    const z=++next, id="D:"+i+":"+p;
    if(defOwners.has(z))throw Error("DEF name collision");
    defs++;defOwners.set(z,{id,kind,input,pivot});
    if(kind==="COPY"||kind==="NEG"){
      const t=input, e=kind==="COPY"?t:-t;
      add(id+":bit",[-z,e],"FACET",z);
      add(id+":rev",[z,-e],"FACET",z);
    } else if(kind==="AND") {
      const t=input,e=pivot;
      add(id+":parent",[-z,t],"FACET",z);
      add(id+":bit",[-z,e],"FACET",z);
      add(id+":join",[-t,-e,z],"FACET",z);
    } else throw Error("unrecognized gate");
    return z;
  }
  function resolve(a,b,p,tag) {
    if(!rows.has(a)||!rows.has(b)) throw Error("missing premise");
    let A=rows.get(a).clause, B=rows.get(b).clause;
    if(!A.includes(p)||!B.includes(-p)){
      if(A.includes(-p)&&B.includes(p)){[A,B]=[B,A];}
      else throw Error("illegal oriented Resolution pivot");
    }
    const c=norm([...A.filter(v=>v!==p),...B.filter(v=>v!==-p)]);
    resolutions++;return add("R:"+(++serial),c,"RES:"+tag);
  }
  // Original wide bit-PHP source: no arbitrary or derived source clauses.
  for(let i=0;i<pigeons;i++)for(let j=i+1;j<pigeons;j++)
    for(let a=0;a<n;a++){
      const lits=[];
      for(let k=0;k<ell;k++){
        const bit=(a>>k)&1;
        lits.push(bit?-x(i,k):x(i,k),bit?-x(j,k):x(j,k));
      }
      source("S:"+i+":"+j+":"+a,lits);
    }
  const unaryCoverage=[];
  for(let i=0;i<pigeons;i++){
    const P=new Map();
    // Both DEF gates have DISTINCT source inputs x_i0, x_i1.
    P.set("0",own(i,"0","NEG",x(i,0)));
    P.set("1",own(i,"1","COPY",x(i,0)));
    let cover=resolve("D:"+i+":0:rev","D:"+i+":1:rev",x(i,0),"ROOT_COVER");
    for(let depth=1;depth<ell;depth++){
      for(let p=0;p<2**depth;p++){
        const s=p.toString(2).padStart(depth,"0"), t=P.get(s),k=depth;
        const left=s+"0",right=s+"1";
        P.set(left,own(i,left,"AND",t,-x(i,k)));
        P.set(right,own(i,right,"AND",t,x(i,k)));
        const split=resolve("D:"+i+":"+left+":join","D:"+i+":"+right+":join",x(i,k),"CHILD_EXHAUST");
        cover=resolve(cover,split,t,"COVER_EXPAND");
      }
    }
    prefix.push(P);
    const leaves=[...Array(n).keys()].map(a=>P.get([...Array(ell).keys()].map(k=>(a>>k)&1).join("")));
    if(!equal(rows.get(cover).clause,leaves))throw Error("coverage mismatch");
    unaryCoverage.push(cover);
    const byHole=[];
    for(let a=0;a<n;a++){
      const bits=[...Array(ell).keys()].map(k=>String((a>>k)&1)).join("");
      const leaf=P.get(bits), each=[];
      for(let k=0;k<ell;k++){
        const targetPrefix=bits.slice(0,k+1), target=P.get(targetPrefix),e=((a>>k)&1)?x(i,k):-x(i,k);
        let r="D:"+i+":"+targetPrefix+":bit";
        if(leaf!==target) {
          const parents=bits.slice(0,ell), prev="D:"+i+":"+parents+":parent";
          let path=prev;
          for(let depth=ell-1;depth>k+1;depth--){
            const ancestor=bits.slice(0,depth);
            path=resolve(path,"D:"+i+":"+ancestor+":parent",P.get(ancestor),"ANCESTOR");
          }
          r=resolve(path,r,target,"LEAF_IMPLIES_BIT");
        }
        if(!equal(rows.get(r).clause,[-leaf,e]))throw Error("leaf bit equality mismatch");
        each.push(r);
      }
      byHole.push(each);
    }
    imp.push(byHole);
  }
  const collisions=[];
  for(let i=0;i<pigeons;i++)for(let j=i+1;j<pigeons;j++)for(let a=0;a<n;a++){
    let r="S:"+i+":"+j+":"+a;
    for(let k=0;k<ell;k++){
      const eq=((a>>k)&1)?x(i,k):-x(i,k);
      r=resolve(r,imp[i][a][k],-eq,"COLLISION_LEFT");
    }
    for(let k=0;k<ell;k++){
      const eq=((a>>k)&1)?x(j,k):-x(j,k);
      r=resolve(r,imp[j][a][k],-eq,"COLLISION_RIGHT");
    }
    const s=[...Array(ell).keys()].map(k=>String((a>>k)&1)).join("");
    if(!equal(rows.get(r).clause,[-prefix[i].get(s),-prefix[j].get(s)]))
      throw Error("unary collision mismatch");
    collisions.push(r);
  }
  // Independently audit ALL recorded RES additions and owner-bound facets,
  // rather than trusting only the producer's designated derived clauses.
  const sourceCount=n*pigeons*(pigeons-1)/2;
  const expectedDefs=pigeons*(2*n-2);
  if(defs!==expectedDefs||collisions.length!==sourceCount||
     unaryCoverage.length!==pigeons)throw Error("count mismatch");
  // Hostile controls: rejects fabricated source, wrong RES pivot, lost owner.
  let rejections=0;
  try {resolve("S:0:1:0","S:0:1:1",next+999,"BAD");}catch(e){rejections++;}
  if(rows.has("S:0:1:"+n))throw Error("bad source present");else rejections++;
  if(!defOwners.has(prefix[0].get("0")))throw Error("owner absent");
  if(!rejections||rejections!==2)throw Error("hostile controls failed");
  return {ell,n,pigeons,sourceClauses:sourceCount,paidDefs:defs,
          paidResolution:resolutions,totalPaid:defs+resolutions,
          freeOwnerFacets:[...rows.values()].filter(v=>v.tag==="FACET").length,
          derivedUnaryPigeonClauses:unaryCoverage.length,
          derivedUnaryCollisionClauses:collisions.length,
          hostileControlsRejected:rejections,
          proofSemantics:"Two-input DEF owners; authenticated exact facets and signed Resolution",
          caveat:"Cook ER append stage not generated; historical accepted-byte grammar not authenticated"};
}
function run(){return [2,3,4].map(compile);}
if(typeof module!=="undefined" && require.main===module)console.log(JSON.stringify(run(),null,2));
