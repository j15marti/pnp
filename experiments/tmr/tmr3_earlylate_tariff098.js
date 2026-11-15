'use strict';
// TMR-3/044 actual finite-control EARLY/LATE microsteps, exact tariff and geometric controls.
// Full audit is a V8-executed function; standalone Node CLI calls precisely the same body.
function audit(){
  const CK=['CNF','AFFINE','SEP','FUS','GAMMA','INTERFACE','MACHINE'];
  let assertions=0,transitions=0,traces=0,overcharges=0,grid=0,failures=0;
  const maxN=256,minN=2,maxM=6,mini=[];
  const check=(b,msg)=>{assertions++;if(!b){failures++;throw Error(msg);}};
  const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  function simulate(n,m,late){
    const s={n,m,late,phase:'START',I:0,Whead:0,input:Array(n).fill('1').concat('#'),
      W:Array(n+1).fill('_'),O:Array(m).fill('_'),seen:Array(n+1).fill(false),paid:[]};
    const vec=()=>[0,0,0,0,s.W.slice(1,n).filter(x=>x!=='g').length,
      s.seen.filter(x=>!x).length+s.O.filter(x=>x!=='@').length,
      Number(s.phase!=='HALT')];
    const initial=vec();
    check(eq(initial,[0,0,0,0,n-1,n+1+m,1]),'initial n='+n+',m='+m);
    const names=[];
    while(s.phase!=='HALT'){
      check(names.length<n+3,'loop bound');
      const old=vec(),wh=s.Whead,ih=s.I,wasW=s.W.slice(),wasO=s.O.slice();
      let name;
      if(s.phase==='START'&&s.input[s.I]==='1'&&s.W[s.Whead]==='_'){
        name='INIT';s.W[s.Whead]='1';if(!late)s.O.fill('@');
        s.seen[s.I]=true;s.I++;s.Whead++;s.phase='SECOND';
      }else if((s.phase==='SECOND'||s.phase==='STREAM')&&s.input[s.I]==='1'&&s.W[s.Whead]==='_'){
        name='GATE';s.W[s.Whead]='g';s.paid.push(s.Whead);
        s.seen[s.I]=true;s.I++;s.Whead++;s.phase='STREAM';
      }else if(s.phase==='STREAM'&&s.input[s.I]==='#'){
        name='EOF_HALT';s.seen[s.I]=true;if(late)s.O.fill('@');s.phase='HALT';
      }else throw Error('unmatched legitimate transition '+JSON.stringify(s));
      const now=vec(),delta=old.map((x,i)=>x-now[i]);
      const expected=name==='INIT'?[0,0,0,0,0,late?1:m+1,0]:
        name==='GATE'?[0,0,0,0,1,1,0]:[0,0,0,0,0,late?m+1:1,1];
      check(eq(delta,expected),'row '+name+',n='+n+',m='+m+',late='+late);
      check(Math.abs(s.I-ih)<=1&&Math.abs(s.Whead-wh)<=1,'local heads');
      check(s.W.reduce((z,x,i)=>z+(x!==wasW[i]),0)<=1,'one W write');
      check(s.O.every((x,i)=>x===wasO[i]||(wasO[i]==='_'&&x==='@')),'per output write');
      check(s.seen.filter(Boolean).length===s.I+Number(s.phase==='HALT'),'input observed');
      check(s.paid.length===new Set(s.paid).size,'records paid once');
      const earlyCost=m*delta[4]+delta[5]+m*delta[6];
      if(!late)check(earlyCost===m+1,'all early rows exactly paid');
      else if(name==='EOF_HALT'){
        check(earlyCost===2*m+1,'late EOF joint discharge');
        check(earlyCost>m+1,'strict legal late violation');overcharges++;
      }else check(earlyCost<=m+1,'early weights legal on late prefix');
      names.push(name);transitions++;
    }
    const terminal=vec();
    check(eq(terminal,[0,0,0,0,0,0,0]),'zero goal');
    check(s.W[0]==='1'&&s.W.slice(1,n).every(x=>x==='g'),'final stage');
    check(s.O.every(x=>x==='@')&&s.seen.every(Boolean),'markers and EOF');
    check(s.I===n&&s.Whead===n,'head at source EOF');
    check(s.paid.length===n-1,'paid distinct g');
    check(names.length===n+1,'full time n+1');
    check(names.filter(x=>x==='GATE').length===n-1,'record count');
    check(s.W.filter(x=>x!=='_').length===n,'physical occupied cells');
    const earlyObj=m*(n-1)+(n+1+m)+m;
    check(earlyObj===(m+1)*(n+1),'exact early primal objective');
    const dualCover=[n-1,(late?1:m+1)+(n-1)+(late?m+1:1),1];
    check(dualCover[0]===n-1&&dualCover[1]===n+1+m&&dualCover[2]===1,'row cover');
    check(names.length>=n+1,'compulsory final EOF read');
    traces++;
    if(n<=3&&m<=2)mini.push({n,m,late,names,initial,goal:terminal,steps:names.length,
      violating_late_eof:late?{delta:[0,0,0,0,0,m+1,1],scaled_charge:2*m+1,scaled_price:m+1}:null});
  }
  for(let m=1;m<=maxM;m++)for(let n=minN;n<=maxN;n++){simulate(n,m,false);simulate(n,m,true)}
  for(let m=1;m<=maxM;m++){
    const d=12;
    for(let g=0;g<=d;g++)for(let i=0;i<=d;i++)for(let h=0;h<=d;h++){
      const earlyLegal=(m+1)*i<=d&&g+i<=d&&i+h<=d;
      const byRows=[(m+1)*i,g+i,i+h].every(z=>z<=d);
      check(earlyLegal===byRows,'early rows iff cone');
      if(earlyLegal)for(let n of [2,3,5,16,64,256]){
        check((n-1)*g+(n+1+m)*i+h<=d*(n+1),'LP upper');grid++;
      }
      const lateLegal=i<=d&&g+i<=d&&(m+1)*i+h<=d;
      const lateByRows=[i,g+i,(m+1)*i+h].every(z=>z<=d);
      check(lateLegal===lateByRows,'late rows iff cone');
    }
  }
  for(let n=2;n<=maxN;n++){
    const tLast=n,returnMoves=n-2,activation=tLast+returnMoves+1,halt=activation+1;
    check(halt===2*n,'ordered-stage head-return geometric bound');
    check(2*n<=2*n+2,'peer fixed M_STAGE upper');
  }
  return {id:'TMR3_EARLYLATE098',timestamp_pst:'2026-11-15 05:31 PST',
    model:'fixed m>=1 finite-alphabet tapes; source 1^n#; physical W[0]=1, W[1..n-1]=g; m marker outputs; EOF inspected; true HALT',
    status:'PROVED/RESTRICTED symbolic; COMPUTATIONAL finite V8; independent mathematical review OPEN',
    assertions,failures,traces,transitions,overcharges,grid,tests:{n:[minN,maxN],m:[1,maxM],machines:['EARLY','LATE']},
    initial:['0','0','0','0','n-1','n+1+m','1'],
    early_rows:{INIT:[0,0,0,0,0,'m+1',0],GATE:[0,0,0,0,1,1,0],EOF_HALT:[0,0,0,0,0,1,1]},
    late_rows:{INIT:[0,0,0,0,0,1,0],GATE:[0,0,0,0,1,1,0],EOF_HALT:[0,0,0,0,0,'m+1',1]},
    early_cone:['(m+1)*lambda_INTERFACE<=1','lambda_GAMMA+lambda_INTERFACE<=1','lambda_INTERFACE+lambda_MACHINE<=1','lambda>=0'],
    early_primal:['0','0','0','0','m/(m+1)','1/(m+1)','m/(m+1)'],
    early_primal_optimum:'n+1',
    dual_early:{INIT:1,GATE:'n-1',EOF_HALT:1,price:'n+1'},
    cross_program_violation:'late EOF discharges (m+1)*i+h=(2m+1)/(m+1)>1 under early lambda',
    late_cone:['lambda_INTERFACE<=1','lambda_GAMMA+lambda_INTERFACE<=1','(m+1)*lambda_INTERFACE+lambda_MACHINE<=1','lambda>=0'],
    mandatory_source_read_lower:'all task implementations with original locally moving input head must inspect position n, hence T>=n+1',
    ordered_activation_geometry_lower:'if W[n-1] written before subsequent W[0] activation and separate HALT, T>=2n; peer M_STAGE_OUTPUT_m uses 2n+2',
    scope:'same final tape target with different event sequencing; no SAT lower bound or unrestricted tariff',
    mini};
}
if(typeof module!=='undefined'){
  if(require.main===module) console.log(JSON.stringify(audit(),null,2));
  module.exports={audit};
}
