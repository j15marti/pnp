"use strict";
function parseStrictProper3Dimacs(input){
  const lines=input.trimEnd().split(/\r?\n/);
  if(!/^p cnf [1-9][0-9]* [1-9][0-9]*$/.test(lines[0]))throw Error("header");
  const [, ,nstr,mstr]=lines[0].split(" ");
  const n=Number(nstr),m=Number(mstr);
  if(!Number.isSafeInteger(n)||!Number.isSafeInteger(m)||lines.length!==m+1)throw Error("count");
  const F=[];
  for(let i=1;i<lines.length;i++){
    if(!/^-?[0-9]+ -?[0-9]+ -?[0-9]+ 0$/.test(lines[i]))throw Error("clause syntax");
    const vals=lines[i].split(" ").map(Number);
    const ids=vals.slice(0,3).map(Math.abs);
    if(ids.some(id=>id===0||id>n)||new Set(ids).size!==3)throw Error("proper");
    F.push(vals.slice(0,3));
  }
  return {n,m,F};
}
function runFixtureTests(raw){
  let pass=0; const ok=(x,msg)=>{pass++;if(!x)throw Error(msg)};
  for(const item of raw.cases){
    for(const F of Object.values(item.data)){
      const src="p cnf "+item.n+" "+F.length+"\n"+F.map(c=>c.join(" ")+" 0").join("\n")+"\n";
      const parsed=parseStrictProper3Dimacs(src);
      ok(parsed.m===F.length&&parsed.n===item.n,"roundtrip");
      const bad=[
        src.replace(" "+F.length+"\n"," "+(F.length+1)+"\n"),
        src.replace("p cnf "+item.n,"p cnf "+(item.n-1)),
        src.replace(/^([\s\S]*?) 0\n/, "$1 1\n"),
        src.replace(/^p cnf [^\n]+\n[^\n]+/, "p cnf "+item.n+" "+F.length+"\n1 1 3 0"),
        src+"nonsense\n",
        src.replace(/^p cnf/, "p cfn")
      ];
      for(let i=0;i<bad.length;i++){
        let rejected=false;try{parseStrictProper3Dimacs(bad[i])}catch(e){rejected=true}
        ok(rejected,"malformed escaped: "+i);
      }
    }
  }
  return {checks:pass,invalid_rejections:raw.cases.length*3*6};
}
const fs=require("fs");const raw=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
console.log(JSON.stringify(runFixtureTests(raw)));