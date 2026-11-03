/* LSPV-1 368 independent, no-import source/witness and transfer-envelope referee. Node 18+. */
"use strict";
function verify(d){
  let checks=0;
  function ok(x,n){if(!x)throw Error("independent check failed: "+n);checks++;}
  function parse(src){
    if(typeof src!=="string"||/[^\x20-\x7e\n]/.test(src))return null;
    const L=src.replace(/\n$/,"").split("\n"),H=/^p cnf ([1-9]\d*) (0|[1-9]\d*)$/.exec(L.shift());
    if(!H||Number(H[2])!==L.length)return null;
    let n=Number(H[1]),clauses=[];
    if(!Number.isSafeInteger(n))return null;
    for(const s of L){
      const toks=s.trim().split(/\s+/);if(toks.pop()!=="0")return null;
      if(toks.some(z=>!/^\-?[1-9]\d*$/.test(z)))return null;
      const c=toks.map(Number);
      if(c.some(z=>!Number.isSafeInteger(z)||!z||Math.abs(z)>n))return null;
      clauses.push(c);
    }
    return {n,clauses};
  }
  function truth(c,word){
    for(const row of c){
      let found=false;
      for(const literal of row){
        const bit=Math.floor(word/(2**(Math.abs(literal)-1)))%2;
        if(bit===(literal>0?1:0)){found=true;break;}
      }
      if(!found)return false;
    }
    return true;
  }
  function models(f){let c=0;for(let a=0;a<2**f.n;a++)if(truth(f.clauses,a))c++;return c;}
  function expectedPHP(h){
    let c=[],v=(p,j)=>p*h+j+1;
    for(let p=0;p<h+1;p++){let r=[];for(let j=0;j<h;j++)r.push(v(p,j));c.push(r);}
    for(let p=0;p<h+1;p++)for(let q=p+1;q<h+1;q++)for(let j=0;j<h;j++)c.push([-v(p,j),-v(q,j)]);
    return c;
  }
  ok(d.runId==="HARD-PHP-QUERY-EXPONENT-FIREWALL368","runId");
  for(const t of d.php){
    let f=parse(t.source);
    ok(!!f&&f.n===t.n,"PHP source");ok(t.bitLength===8*t.source.length,"source bits");
    ok(JSON.stringify(f.clauses)===JSON.stringify(expectedPHP(t.h)),"authentic PHP");
    ok(t.m===f.clauses.length,"PHP clause count");
    ok(models(f)===0,"PHP UNSAT");
    ok(t.deletion.length===f.clauses.length,"all deletion count");
    for(let j=0;j<t.deletion.length;j++){
      const c=f.clauses.filter((_,i)=>i!==j);
      ok(truth(c,t.deletion[j]),"deletion SAT witness");
      ok(!truth(f.clauses,t.deletion[j]),"witness falsifies original");
    }
    let target=0;
    for(let j=0;j<f.clauses.length;j++)for(let k=0;k<f.clauses[j].length;k++){
      const [a,b,w]=t.flips[target++]||[];
      ok(a===j&&b===k,"signed index");
      const c=f.clauses.map((cl,i)=>i!==j?cl:cl.map((x,z)=>z===k?-x:x));
      ok(truth(c,w),"sign-flip SAT witness");
      ok(!truth(f.clauses,w),"original not satisfied");
    }
    ok(target===t.flips.length,"all flip controls");
  }
  const graph=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  function checkK4(src,charge){
    let f=parse(src);ok(!!f&&f.n===6&&f.clauses.length===16,"K4 source");
    let rows=[];
    for(let v=0;v<4;v++){
      const ids=graph.flatMap((e,i)=>e.includes(v)?[i+1]:[]);
      for(let bits=0;bits<8;bits++){
        let p=0;for(let j=0;j<3;j++)p^=(bits>>j)&1;
        if(p!==charge[v])rows.push(ids.map((x,j)=>((bits>>j)&1)?-x:x));
      }
    }
    ok(JSON.stringify(f.clauses)===JSON.stringify(rows),"K4 signed parity clauses");
    return models(f);
  }
  ok(checkK4(d.k4.odd,[1,0,0,0])===0,"odd parity UNSAT");
  ok(checkK4(d.k4.even,[0,0,0,0])===8,"even parity SAT 8");
  ok(d.k4.oddModels===0&&d.k4.evenModels===8,"record parity");
  for(const s of d.sentinels){
    ok(s.source==="p cnf 1 "+s.t+"\n"+"1 0\n".repeat(s.t),"canonical true sentinel");
    let f=parse(s.source);ok(f!==null&&models(f)===1,"SAT sentinel valid");
    ok(s.bitLength===8*s.source.length,"sentinel bits");
  }
  for(let i=1;i<d.sentinels.length;i++)
    ok(d.sentinels[i].bitLength-d.sentinels[i-1].bitLength<=40,"length dense");
  for(const s of d.malformed)ok(parse(s)===null,"malformed reject");
  const f=parse(d.unit.source),p=d.unit.proof;
  ok(!!f&&f.clauses.length===2,"unit source");
  ok(f.clauses[p.a].includes(p.pivot)&&f.clauses[p.b].includes(-p.pivot),"genuine pivot");
  ok(JSON.stringify(f.clauses[p.a].filter(x=>x!==p.pivot).concat(f.clauses[p.b].filter(x=>x!==-p.pivot)))===JSON.stringify(p.conclusion),"derived empty");
  for(const e of d.costEnvelopes){
    const t=d.php.find(x=>x.h===e.h);ok(!!t&&t.bitLength===e.Nbits,"cost source ID");
    ok((BigInt(e.Nbits)**3n).toString()===e.chargedPHPUpper,"symbolic cubic");
    ok((BigInt(e.Nbits)**8n).toString()===e.possibleSentinelDelay,"symbolic K delay");
  }
  return {runId:d.runId,status:"PASS",assertions:checks,phpCases:d.php.length,deletionWitnesses:d.php.reduce((a,x)=>a+x.deletion.length,0),signFlipWitnesses:d.php.reduce((a,x)=>a+x.flips.length,0),sentinels:d.sentinels.length};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),p=process.argv[2]||"results/raw/arc/2026-11-03_1055_LSPV1_PHP_QUERY_EXPONENT368.json";
 console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(p,"utf8"))),null,2));
}
if(typeof module!=="undefined")module.exports={verify};