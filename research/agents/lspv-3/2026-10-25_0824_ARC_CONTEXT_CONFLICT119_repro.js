function runAudit(){
  "use strict";
  let checks=0;
  function check(x,label){checks++;if(!x)throw Error("FAILED "+label+" check "+checks);}
  function pin(name,value,tag){
    const out=[];
    for(const a of [false,true])for(const b of [false,true])
      out.push([[name,value],[tag+"_a",a],[tag+"_b",b]]);
    return out;
  }
  function free(name,tag){return [[[name,true],[tag+"_u",true],[tag+"_v",true]]];}
  function eq(x,y,tag,reverse=false){
    const clauses=[];
    const pairs=reverse?[[true,true],[false,false]]:[[false,true],[true,false]];
    for(let p=0;p<2;p++)for(let sg of [false,true])
      clauses.push([[x,pairs[p][0]],[y,pairs[p][1]],[tag+(p?"b":"a"),sg]]);
    return clauses;
  }
  const cat=(...cs)=>cs.flatMap(x=>x);
  function atoms(C){return [...new Set(C.flatMap(c=>c.map(l=>l[0])))].sort();}
  function encode(C){
    for(const clause of C)check(clause.length===3&&new Set(clause.map(x=>x[0])).size===3,"proper3");
    const names=atoms(C),n=names.length,m=C.length,h=Math.max(1,Math.ceil(Math.log2(Math.max(n,m)+1)));
    const bw=v=>v.toString(2).padStart(h,"0");
    const loc=new Map(names.map((name,i)=>[name,i+1]));
    let bits="1".repeat(h)+"0"+bw(n)+bw(m);
    for(const clause of C)for(const lit of clause)bits+=(lit[1]?"1":"0")+bw(loc.get(lit[0]));
    check(bits.length===3*h+1+3*m*(h+1),"exact_length");
    return {bits,n,m,h,names};
  }
  function parse(encoded){
    const bits=encoded.bits; let p=0,h=0;
    while(bits[p]==="1"){p++;h++;}
    check(h>0&&bits[p]==="0","unary_h");p++;
    const bin=()=>{const v=parseInt(bits.slice(p,p+h),2);p+=h;return v;};
    const n=bin(),m=bin(),result=[];
    for(let i=0;i<m;i++){
      const c=[];
      for(let j=0;j<3;j++){
        const val=bits[p++]==="1",id=bin();
        check(id>0&&id<=n,"index_range");
        c.push([encoded.names[id-1],val]);
      }
      result.push(c);
    }
    check(p===bits.length&&n===encoded.n&&m===encoded.m,"parse_footer");
    return result;
  }
  function sameCNF(A,B){return JSON.stringify(A)===JSON.stringify(B);}
  function sat(C,fixed={}){
    const recur=(input)=>{
      let a={...input};
      while(true){
        let changed=false, undecided=false, preferred=null;
        for(const clause of C){
          let satisfied=false, unknown=[];
          for(const [v,sgn] of clause){
            if(v in a){if(a[v]===sgn){satisfied=true;break;}}
            else unknown.push([v,sgn]);
          }
          if(satisfied)continue;
          if(unknown.length===0)return false;
          undecided=true;
          if(unknown.length===1){
            const [v,s]=unknown[0];
            if(v in a && a[v]!==s)return false;
            if(!(v in a)){a[v]=s;changed=true;}
          }else if(!preferred)preferred=unknown[0][0];
        }
        if(!changed){
          if(!undecided)return true;
          if(preferred===null)throw Error("DPLL no branch");
          return recur({...a,[preferred]:false})||recur({...a,[preferred]:true});
        }
      }
    };
    return recur(fixed);
  }
  function maskSupport(C,Y){
    let mask=0;
    const n=Y.length;
    for(let x=0;x<(1<<n);x++){
      let fixed={};
      for(let i=0;i<n;i++)fixed[Y[i]]=Boolean((x>>(n-1-i))&1);
      if(sat(C,fixed))mask|=1<<x;
    }
    return mask;
  }
  function conflictGraph(D,Q,n){
    const m=1<<n,adj=Array.from({length:m},()=>Array(m).fill(false));
    for(let d of D)for(let q of Q){
      if((d&q)!==0)continue;
      for(let b=0;b<m;b++)if((d>>b)&1)
        for(let c=0;c<m;c++)if((q>>c)&1){
          check(b!==c,"disjoint_edge");
          adj[b][c]=adj[c][b]=true;
        }
    }
    return adj;
  }
  function graphEdges(G){let E=[];for(let i=0;i<G.length;i++)for(let j=i+1;j<G.length;j++)if(G[i][j])E.push([i,j]);return E;}
  function coloring(G){
    const n=G.length, colors=Array(n).fill(-1);
    let best=n+1,bestColors=[];
    function rec(i,used){
      if(used>=best)return;
      if(i===n){best=used;bestColors=colors.slice();return;}
      for(let c=0;c<=used;c++){
        if(c>=best)break;
        let okay=true;
        for(let j=0;j<i;j++)if(colors[j]===c&&G[i][j]){okay=false;break;}
        if(okay){colors[i]=c;rec(i+1,Math.max(used,c+1));}
      }
      colors[i]=-1;
    }
    rec(0,0);
    return {chi:best,colors:bestColors};
  }
  function coarse(d,q,color){
    for(let i=0;i<color.length;i++)if((d>>i)&1)
      for(let j=0;j<color.length;j++)if((q>>j)&1&&color[i]===color[j])return true;
    return false;
  }
  function allPartitions(n){
    let out=[],a=Array(n).fill(-1);
    function rec(i,used){if(i===n){out.push(a.slice());return;}
      for(let c=0;c<=used;c++){a[i]=c;rec(i+1,Math.max(used,c+1));}
    }
    a[0]=0;rec(1,1);return out;
  }
  const part4=allPartitions(4);
  check(part4.length===15,"Bell4");
  let exhaustiveCases=0,randomCases=0;
  for(let d=0;d<16;d++)for(let q=0;q<16;q++){
    const G=conflictGraph([d],[q],2);
    for(let h of part4){
      const proper=graphEdges(G).every(([b,c])=>h[b]!==h[c]);
      const exact=((d&q)!==0),approx=coarse(d,q,h);
      check(proper===(exact===approx),"onepair_iff");exhaustiveCases++;
    }
  }
  let seed=119;
  const rnd=()=>((seed=Math.imul(seed,1664525)+1013904223|0)>>>0);
  for(let k=0;k<512;k++){
    const D=[rnd()%16,rnd()%16],Q=[rnd()%16,rnd()%16];
    const G=conflictGraph(D,Q,2);
    for(let h of part4){
      const proper=graphEdges(G).every(([b,c])=>h[b]!==h[c]);
      const exact=D.every(d=>Q.every(q=>coarse(d,q,h)===((d&q)!==0)));
      check(proper===exact,"twoby2_iff");
      randomCases++;
    }
  }
  // Real ordinary proper-3CNF root -> child -> grandchild and two admissible contexts.
  const P0=cat([[["y",true],["ra",true],["rb",true]],[["z",true],["rc",true],["rd",true]]]);
  const P1=cat(P0,pin("y",false,"pin1"));
  const P2=cat(P1,pin("z",false,"pin2"));
  const Qpos=cat(pin("y",false,"qposy"),pin("z",false,"qposz"));
  const Qneg=cat(pin("y",true,"qnegy"),pin("z",true,"qnegz"));
  const D=[P0,P1,P2],Q=[Qpos,Qneg],Y=["y","z"];
  const Dm=D.map(x=>maskSupport(x,Y)),Qm=Q.map(x=>maskSupport(x,Y));
  check(JSON.stringify(Dm)===JSON.stringify([15,3,1]),"pin_tree_masks");
  check(JSON.stringify(Qm)===JSON.stringify([1,8]),"context_masks");
  const Gr=conflictGraph(Dm,Qm,2),cr=coloring(Gr);
  const Ga=conflictGraph(Dm,[1,2,4,8],2),ca=coloring(Ga);
  check(cr.chi===2&&ca.chi===3,"strict_context_compression");
  const h_y=[0,0,1,1];
  for(let p=0;p<3;p++)for(let q=0;q<2;q++){
    const X=cat(D[p],Q[q]);const enc=encode(X);
    check(sameCNF(X,parse(enc)),"ordinary_roundtrip");
    const actual=sat(parse(enc)),intersection=(Dm[p]&Qm[q])!==0;
    check(actual===intersection,"real_both_labels");
    check(coarse(Dm[p],Qm[q],h_y)===actual,"restricted_coarse_join");
  }
  const Qbad=cat(pin("y",false,"bad_y"),pin("z",true,"bad_z"));
  const wrong=coarse(Dm[2],maskSupport(Qbad,Y),h_y);
  const trueLabel=sat(cat(D[2],Qbad));
  check(wrong&&!trueLabel,"second_level_false_SAT");
  // SAT-hard implicit conflict graph: both-label prefixes/suffixes, source names y,z,w.
  const core=cat(pin("y",false,"corey"),free("z","corez"),free("w","corew"));
  const next1=cat(core,pin("z",false,"depth1"));
  const next2=cat(next1,pin("w",false,"depth2"));
  const good=cat(pin("y",false,"good_y"),pin("z",false,"good_z"),pin("w",false,"good_w"));
  const satF=[[["fx",true],["fa",true],["fb",true]]];
  const unsatF=cat(pin("fx",true,"fpos"),pin("fx",false,"fneg"));
  const hornF=[[["hx",false],["hy",false],["hz",true]]];
  const affineSatF=eq("ax","ay","aeq");
  const affineUnsatF=cat(eq("ax","ay","aeq2"),eq("ax","ay","aneq2",true));
  const disconnectedF=cat([[["i1",true],["i2",true],["i3",true]],[["j1",true],["j2",true],["j3",true]]]);
  const falseCases=[["sat",satF,true],["unsat",unsatF,false],["horn_sat",hornF,true],
    ["affine_sat",affineSatF,true],["affine_unsat",affineUnsatF,false],
    ["disconnected_sat",disconnectedF,true]];
  let hardControls=[];
  for(const [name,F,expected] of falseCases){
    check(sat(F)===expected,"source_F_"+name);
    const bad=cat(pin("y",true,"bad_y"),free("z","bad_z"),free("w","bad_w"),F);
    const subsets=[core,next1,next2],BB=["y","z","w"];
    const dm=subsets.map(x=>maskSupport(x,BB)),qm=[maskSupport(good,BB),maskSupport(bad,BB)];
    const graph=conflictGraph(dm,qm,3),opt=coloring(graph);
    check(opt.chi===(expected?2:1),"NP_hard_palette_"+name);
    for(let lev=0;lev<3;lev++){
      for(let j=0;j<2;j++){
        const C=cat(subsets[lev],j===0?good:bad),e=encode(C),parsed=parse(e);
        check(sameCNF(C,parsed),"real_roundtrip_"+name);
        const outcome=sat(parsed);
        check(outcome===(j===0),"both_labels_all_levels_"+name);
        check(outcome===Boolean(dm[lev]&qm[j]),"support_glue_"+name);
      }
    }
    hardControls.push({name,F_SAT:expected,chi:opt.chi,edges:graphEdges(graph).length,
      actualJoinLabelsByLevel:["root","child","grandchild"].map(()=>[true,false]),
      encodedBitsByLevel:subsets.map(x=>[encode(cat(x,good)).bits.length,encode(cat(x,bad)).bits.length])});
  }
  // Identical private-name reuse invalidates a declared boundary gluing.
  const collisionP=cat(pin("u",false,"private_left"),free("y","public_left"));
  const collisionQ=cat(pin("u",true,"private_right"),free("y","public_right"));
  const privateMaskP=maskSupport(collisionP,["y"]),privateMaskQ=maskSupport(collisionQ,["y"]);
  check(privateMaskP===3&&privateMaskQ===3&&!(sat(cat(collisionP,collisionQ))),"private_name_collision");
  const repairedQ=collisionQ.map(cl=>cl.map(([n,s])=>[n==="u"?"u_right":n,s]));
  check(sat(cat(collisionP,repairedQ)),"private_name_rename_repair");
  // Paid ordinary bit counts as an explicit example, not a FLMV performance certificate.
  const twoLevelLengths=D.map(x=>encode(x).bits.length);
  const allMaterializations=[];
  let materializedBits=0,parsedBits=0;
  for(let p=0;p<3;p++)for(let q=0;q<2;q++){
    const e=encode(cat(D[p],Q[q]));
    allMaterializations.push({depth:p,suffix:q,bits:e.bits.length,header:3*e.h+1,body:3*e.m*(e.h+1),vars:e.n,clauses:e.m});
    materializedBits+=e.bits.length;
    parse(e);parsedBits+=e.bits.length;
  }
  return {run_id:"ARC-CONTEXT-CONFLICT119",model:"exact ordinary proper-3CNF semantics; finite source program audit, NOT measured FLMV machine",
    check_count:checks,seed_initial:119,method:"exhaustive 1x1 all 16x16 support pairs and all Bell(4) colorings; seeded 512 2x2 families times all Bell(4) partitions; real proper-3CNF SAT/UNSAT roundtrips at two actual levels", 
    mask_exhaustive_checks:exhaustiveCases,mask_random_checks:randomCases,
    restricted:{Dm,Qm,edges:graphEdges(Gr),chi:cr.chi,coloring:cr.colors,universal_suffix_chi:ca.chi,source_identity:Y,
      descendant_input_bits:twoLevelLengths,
      materially_serialized:allMaterializations,eager_written_bits_example:materializedBits,parsed_read_bits_example:parsedBits,
      second_level_bad_context:{bad_support:maskSupport(Qbad,Y),source_correct_label:trueLabel,one_bit_quotient_label:wrong}},
    sat_hard_two_level:hardControls,
    private_name_hostile:{left_support:privateMaskP,right_support:privateMaskQ,shared_private_unsat:true,renamed_disjoint_sat:true},
    deliberately_unmeasured:{FLMV_bit_time:null,peak_simultaneous_workspace:null,temporal_state_flips:null,circuit_hardware:null,
      model_specific_index_read_write_steps:null},
    status:{graph_characterization:"PROVED/EXACT restricted, independent review pending",hardness:"PROVED/EXACT many-one SAT-hard implicit palette optimization, independent review pending",
      finite_instances:"COMPUTATIONAL",all_input_favorable_arc:"OPEN",P_vs_NP:"OPEN"}
  };
}
if(typeof module!=="undefined"&&require.main===module){process.stdout.write(JSON.stringify(runAudit(),null,2)+"\n");}
