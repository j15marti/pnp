// Runs the pinned compile() (commit 21b9d53, copied verbatim as compile_pinned_21b9d53.js)
// on a JSON list of {id,nvars,dimacs} read from stdin; writes {id,network,source_map} list to stdout.
const fs=require("node:fs");
const src=fs.readFileSync(__dirname+"/compile_pinned_21b9d53.js","utf8");
const body=src.slice(0,src.indexOf("function auditLocal"));
const compile=new Function("require",body+"\nreturn compile;")(require);
const inp=JSON.parse(fs.readFileSync(0,"utf8"));
const out=inp.map(x=>{const G=compile(x);return {id:x.id,network:G.network,source_map:G.source_map}});
process.stdout.write(JSON.stringify(out));
