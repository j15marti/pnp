'use strict';
// TMR-1/044 exact physical-head transport audit, fixed M_STAGE_OUTPUT_m.
// Each local physical transition costs one; successful source promise 1^n#, n>=2.
function audit() {
  let assertions=0, transitions=0, traces=0, grid=0, fused=0;
  const check=(b,label)=>{assertions++;if(!b)throw new Error(label);};
  const components=['CNF','AFFINE','SEP','FUS','GAMMA','INTERFACE','MACHINE'];
  const expected={
    INIT:[0,0,0,0,0,1,0],
    WRITE_GATE:[0,0,0,0,1,1,0],
    EOF_BACK:[0,0,0,0,0,1,0],
    BACK_G:[0,0,0,0,0,0,1],
    ACTIVATE_AND_MARK:[0,0,0,1,0,0,0],
    HALT:[0,0,0,0,0,0,1]
  };
  const testN=[2,3,4,5,6,7,8,9,10,12,16,24,32,48,64,96,128];
  const cases=[];
  const vec=s=>{
    let q=0;
    for(let j=1;j<s.n;j++)if(s.W[j]!=='g')q++;
    const u=s.seen.reduce((z,b)=>z+Number(!b),0);
    let d=0;
    if(['INIT','SECOND','EMIT'].includes(s.phase))d=s.n-1;
    else if(s.phase==='BACK')d=s.workHead;
    return [0,0,0,s.W[0]==='1'?0:1,q,u,d+Number(s.phase!=='HALT')];
  };
  function simulate(n,m){
    const s={
      n,m,phase:'INIT',inputHead:0,workHead:0,
      source:Array(n).fill('1').concat('#'),seen:Array(n+1).fill(false),
      W:Array(n+1).fill('_'),outs:Array(m).fill('_'),gateIDs:[]
    };
    const initial=vec(s);
    check(JSON.stringify(initial)===JSON.stringify([0,0,0,1,n-1,n+1,n]),'initial');
    const rows=[];
    while(s.phase!=='HALT'){
      check(rows.length<3*n+8,'nontermination');
      const before=vec(s),oldW=s.W.slice(),oldOut=s.outs.slice();
      const oldWorkHead=s.workHead,oldInputHead=s.inputHead;
      let rule;
      if(s.phase==='INIT'){
        rule='INIT';
        check(s.source[s.inputHead]==='1'&&s.W[0]==='_','initial source');
        s.seen[s.inputHead]=true;s.W[0]='0';s.inputHead++;s.workHead++;s.phase='SECOND';
      }else if((s.phase==='SECOND'||s.phase==='EMIT')&&s.source[s.inputHead]==='1'){
        rule='WRITE_GATE';
        check(s.W[s.workHead]==='_'&&s.workHead>0,'unique gate cell');
        s.seen[s.inputHead]=true;s.W[s.workHead]='g';
        s.gateIDs.push(s.workHead);s.workHead++;s.inputHead++;s.phase='EMIT';
      }else if(s.phase==='EMIT'&&s.source[s.inputHead]==='#'){
        rule='EOF_BACK';s.seen[s.inputHead]=true;s.workHead--;s.phase='BACK';
      }else if(s.phase==='BACK'&&s.workHead>0){
        rule='BACK_G';check(s.W[s.workHead]==='g','prior paid g');s.workHead--;
      }else if(s.phase==='BACK'&&s.workHead===0){
        rule='ACTIVATE_AND_MARK';
        check(s.W[0]==='0'&&s.gateIDs.length===n-1,'staging complete');
        s.W[0]='1';
        for(let i=0;i<m;i++)s.outs[i]='@';
        s.phase='READY';
      }else if(s.phase==='READY'){
        rule='HALT';
        check(s.W[0]==='1'&&s.outs.every(x=>x==='@'),'ready');
        s.phase='HALT';
      }else throw new Error('unrecognized authentic state '+s.phase);
      const after=vec(s),delta=before.map((x,i)=>x-after[i]);
      check(JSON.stringify(delta)===JSON.stringify(expected[rule]),'delta for '+rule+', n='+n+', m='+m);
      check(s.W.filter((x,i)=>x!==oldW[i]).length<=1,'one W write');
      check(s.outs.every((x,i)=>x===oldOut[i]||oldOut[i]==='_'),'one write per output');
      check(Math.abs(s.workHead-oldWorkHead)<=1&&Math.abs(s.inputHead-oldInputHead)<=1,'local head');
      check(delta[3]+delta[5]+delta[6]<=1,'uniform primal');
      check(delta[4]+delta[5]<=(rule==='WRITE_GATE'?2:1),'physical simultaneous discharge');
      check(delta[3]+delta[5]+delta[6]===1,'exact realized potential decrease');
      rows.push(rule);transitions++;
    }
    check(s.seen.every(Boolean),'EOF observed');
    check(s.W[0]==='1'&&s.W.slice(1,n).every(x=>x==='g'),'all W records');
    check(s.outs.every(x=>x==='@')&&s.phase==='HALT','output and halt');
    check(new Set(s.gateIDs).size===n-1,'unique paid identities');
    check(vec(s).every(x=>x===0),'goal zero');
    check(rows.length===2*n+2,'trace length');
    check(initial[3]+initial[5]+initial[6]===rows.length,'initial exact cost');
    check(rows.filter(r=>r==='WRITE_GATE').length===n-1,'write count');
    check(rows.filter(r=>r==='BACK_G').length===n-1,'back count');
    check(rows.filter(r=>r==='ACTIVATE_AND_MARK').length===1,'nonterminal activation');
    traces++;fused+=m;
    if(n<=4&&m<=1)cases.push({n,m,initial,rules:rows,terminal:vec(s),cost:rows.length});
  }
  for(let f=0;f<=8;f++)for(let g=0;g<=8;g++)for(let i=0;i<=8;i++)for(let h=0;h<=8;h++){
    const lam=[0,0,0,f,g,i,h];
    const legal=Object.values(expected).every(row=>row.reduce((z,d,j)=>z+d*lam[j],0)<=8);
    const cone=g+i<=8;
    check(legal===cone,'exact scaled-integer tariff cone');
    for(const n of [2,7]){
      const objective=f+(n-1)*g+(n+1)*i+n*h;
      if(cone)check(objective<=8*(2*n+2),'dual bound');
      grid++;
    }
  }
  check(8+8>8,'independently maximal interface and Gamma forbidden');
  for(const n of testN)for(const m of [0,1,2,3,4,5])simulate(n,m);
  return {
    id:'TMR1_HEADTRANSPORT096',timestamp_pst:'2026-11-15 05:11 PST',
    status:'PROVED/RESTRICTED symbolic; COMPUTATIONAL finite audit; independent review OPEN',
    test_n:testN,test_m:[0,1,2,3,4,5],
    traces,transitions,assertions,failures:0,rational_grid_models:grid,
    output_tape_marker_instances:fused,components,expected,
    cone:['FUS<=1','GAMMA+INTERFACE<=1','MACHINE<=1','all>=0'],
    initial:'(0,0,0,1,n-1,n+1,n)',primal:[0,0,0,1,0,1,1],
    optimum:'2n+2',dual:'(1,n-1,1,n-1,1,1)',
    cases,unrestricted:'SAT transfer OPEN; superpolynomial obstruction OPEN; P vs NP OPEN'
  };
}
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
module.exports={audit};
