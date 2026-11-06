#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <sys/resource.h>
#include <vector>

using U16 = uint16_t;

struct State {
  std::vector<U16> clauses;
  std::vector<U16> factors;
  std::vector<U16> equations;
  std::vector<U16> conditions;
};

struct InterfaceInfo {
  unsigned min_sources = std::numeric_limits<unsigned>::max();
  uint64_t subset_occurrences = 0;
};

using Catalog = std::map<uint32_t, InterfaceInfo>;
using ClauseCatalog = std::map<uint32_t, InterfaceInfo>;

static int pc(unsigned x) { return __builtin_popcount(x); }

template <class T> static void uniq(std::vector<T>& v) {
  std::sort(v.begin(), v.end());
  v.erase(std::unique(v.begin(), v.end()), v.end());
}

static U16 clause_code(unsigned pos, unsigned neg) {
  return U16(pos | (neg << 8));
}

static unsigned clause_support(U16 c) {
  return (c & 255u) | ((c >> 8) & 255u);
}

static U16 factor_code(unsigned support, unsigned table) {
  return U16(support | (table << 8));
}

static U16 equation_code(unsigned mask, unsigned rhs) {
  return U16(mask | ((rhs & 1u) << 8));
}

static unsigned local_index(unsigned assignment, unsigned support) {
  unsigned idx = 0, out = 0;
  for (unsigned v = 0; v < 8; ++v) if ((support >> v) & 1u) {
    idx |= ((assignment >> v) & 1u) << out;
    ++out;
  }
  return idx;
}

static unsigned expand_table(U16 f, unsigned union_support) {
  const unsigned support = f & 255u;
  const unsigned table = (f >> 8) & 255u;
  const unsigned k = pc(union_support);
  unsigned ans = 0;
  for (unsigned a = 0; a < (1u << k); ++a) {
    unsigned global = 0, bit = 0;
    for (unsigned v = 0; v < 8; ++v) if ((union_support >> v) & 1u) {
      global |= ((a >> bit) & 1u) << v;
      ++bit;
    }
    if ((table >> local_index(global, support)) & 1u) ans |= 1u << a;
  }
  return ans;
}

static U16 clause_as_factor(U16 c) {
  const unsigned pos = c & 255u, neg = (c >> 8) & 255u;
  const unsigned support = pos | neg;
  const unsigned k = pc(support);
  unsigned table = 0;
  for (unsigned a = 0; a < (1u << k); ++a) {
    unsigned global = 0, bit = 0;
    for (unsigned v = 0; v < 8; ++v) if ((support >> v) & 1u) {
      global |= ((a >> bit) & 1u) << v;
      ++bit;
    }
    if ((global & pos) || (((~global) & 255u) & neg)) table |= 1u << a;
  }
  return factor_code(support, table);
}

static U16 equation_as_factor(U16 e) {
  const unsigned mask = e & 255u, rhs = (e >> 8) & 1u;
  const unsigned k = pc(mask);
  unsigned table = 0;
  for (unsigned a = 0; a < (1u << k); ++a)
    if ((pc(a) & 1) == int(rhs)) table |= 1u << a;
  return factor_code(mask, table);
}

static int affine_equation(U16 f) {
  const unsigned support = f & 255u, table = (f >> 8) & 255u;
  for (unsigned mask = 0; mask < 256; ++mask) {
    if (mask & ~support) continue;
    for (unsigned rhs = 0; rhs < 2; ++rhs) {
      const U16 e = equation_code(mask, rhs);
      if (expand_table(equation_as_factor(e), support) == table) return int(e);
    }
  }
  return -1;
}

static int strict_resolve(U16 a, U16 b) {
  unsigned ap = a & 255u, an = (a >> 8) & 255u;
  unsigned bp = b & 255u, bn = (b >> 8) & 255u;
  const unsigned piv = (ap & bn) | (an & bp);
  if (pc(piv) != 1) return -1;
  const unsigned rp = (ap | bp) & ~piv;
  const unsigned rn = (an | bn) & ~piv;
  if (rp & rn) return -1;
  return int(clause_code(rp, rn));
}

static U16 and_factor(U16 a, U16 b) {
  const unsigned support = (a & 255u) | (b & 255u);
  const unsigned table = expand_table(a, support) & expand_table(b, support);
  return factor_code(support, table);
}

static void add_factor(State& s, U16 f) {
  s.factors.push_back(f);
  s.conditions.push_back(f);
  const int e = affine_equation(f);
  if (e >= 0) s.equations.push_back(U16(e));
}

static void finalize(State& s) {
  uniq(s.clauses); uniq(s.factors); uniq(s.equations);
  for (U16 c : s.clauses) if (pc(clause_support(c)) <= 3)
    s.conditions.push_back(clause_as_factor(c));
  for (U16 e : s.equations) if (pc(e & 255u) <= 3)
    s.conditions.push_back(equation_as_factor(e));
  uniq(s.conditions);
}

static std::array<std::array<int,3>,18> side(bool right) {
  if (!right) return {{{1,3,4},{1,-3,-4},{-1,3,-4},{-1,-3,4},
    {2,5,-6},{2,-5,6},{-2,5,6},{-2,-5,-6},
    {3,5,-7},{3,-5,7},{-3,5,7},{-3,-5,-7},
    {4,6,-7},{4,-6,7},{-4,6,7},{-4,-6,-7},
    {1,-2,15},{-1,2,15}}};
  return {{{8,10,-11},{8,-10,11},{-8,10,11},{-8,-10,-11},
    {9,12,-13},{9,-12,13},{-9,12,13},{-9,-12,-13},
    {10,12,-14},{10,-12,14},{-10,12,14},{-10,-12,-14},
    {11,13,-14},{11,-13,14},{-11,13,14},{-11,-13,-14},
    {8,9,-15},{-8,-9,-15}}};
}

static std::vector<int> side_vars(bool right) {
  return right ? std::vector<int>{8,9,10,11,12,13,14,15}
               : std::vector<int>{1,2,3,4,5,6,7,15};
}

static std::vector<U16> encode_side(bool right) {
  const auto src = side(right);
  const auto vars = side_vars(right);
  std::vector<U16> out;
  for (auto c : src) {
    unsigned pos = 0, neg = 0;
    for (int x : c) {
      const unsigned v = std::lower_bound(vars.begin(), vars.end(), std::abs(x)) - vars.begin();
      (x > 0 ? pos : neg) |= 1u << v;
    }
    out.push_back(clause_code(pos, neg));
  }
  return out;
}

static uint32_t global_key(U16 f, bool right) {
  const auto vars = side_vars(right);
  const unsigned local_support = f & 255u;
  unsigned global_support = 0;
  for (unsigned i = 0; i < 8; ++i)
    if ((local_support >> i) & 1u) global_support |= 1u << (vars[i] - 1);
  const unsigned table = (f >> 8) & 255u;
  return uint32_t(global_support | (table << 16));
}

static uint32_t global_clause_key(U16 c, bool right) {
  const auto vars = side_vars(right);
  const unsigned local_pos = c & 255u, local_neg = (c >> 8) & 255u;
  unsigned global_pos = 0, global_neg = 0;
  for (unsigned i = 0; i < 8; ++i) {
    if ((local_pos >> i) & 1u) global_pos |= 1u << (vars[i] - 1);
    if ((local_neg >> i) & 1u) global_neg |= 1u << (vars[i] - 1);
  }
  return uint32_t(global_pos | (global_neg << 16));
}

static void add_catalog(Catalog& cat, ClauseCatalog& clauses,
                        const State& s, unsigned sub, bool right) {
  std::set<uint32_t> seen;
  for (U16 f : s.conditions) seen.insert(global_key(f, right));
  for (uint32_t key : seen) {
    auto& x = cat[key];
    x.min_sources = std::min(x.min_sources, unsigned(pc(sub)));
    ++x.subset_occurrences;
  }
  std::set<uint32_t> seen_clauses;
  for (U16 c : s.clauses) seen_clauses.insert(global_clause_key(c, right));
  for (uint32_t key : seen_clauses) {
    auto& x = clauses[key];
    x.min_sources = std::min(x.min_sources, unsigned(pc(sub)));
    ++x.subset_occurrences;
  }
}

struct Metrics { uint64_t partitions=0, res_pairs=0, and_pairs=0, xor_pairs=0; };

static Catalog run_side(bool right, Metrics& metrics, ClauseCatalog& clause_cat) {
  const auto src = encode_side(right);
  const unsigned n = src.size(), full = (1u << n) - 1;
  std::vector<State> dp(1u << n);
  Catalog cat;
  for (unsigned i = 0; i < n; ++i) {
    dp[1u << i].clauses.push_back(src[i]);
    finalize(dp[1u << i]);
    add_catalog(cat, clause_cat, dp[1u << i], 1u << i, right);
  }
  for (unsigned sz = 2; sz <= n; ++sz) {
    for (unsigned sub = 1; sub <= full; ++sub) {
      if (unsigned(pc(sub)) != sz) continue;
      State cur;
      for (unsigned a = (sub - 1) & sub; a; a = (a - 1) & sub) {
        const unsigned b = sub ^ a;
        if (!b || a > b) continue;
        ++metrics.partitions;
        const State& A = dp[a]; const State& B = dp[b];
        metrics.res_pairs += uint64_t(A.clauses.size()) * B.clauses.size();
        for (U16 x : A.clauses) for (U16 y : B.clauses) {
          const int z = strict_resolve(x, y);
          if (z >= 0) cur.clauses.push_back(U16(z));
        }
        metrics.and_pairs += uint64_t(A.conditions.size()) * B.conditions.size();
        for (U16 x : A.conditions) for (U16 y : B.conditions)
          if (pc((x & 255u) | (y & 255u)) <= 3) add_factor(cur, and_factor(x,y));
        metrics.xor_pairs += uint64_t(A.equations.size()) * B.equations.size();
        for (U16 x : A.equations) for (U16 y : B.equations)
          cur.equations.push_back(equation_code((x ^ y) & 255u,
                                                ((x >> 8) ^ (y >> 8)) & 1u));
      }
      finalize(cur);
      dp[sub] = std::move(cur);
      add_catalog(cat, clause_cat, dp[sub], sub, right);
    }
    std::cerr << (right ? "R" : "L") << " size=" << sz
              << " catalog=" << cat.size() << "\n";
  }
  return cat;
}

static unsigned key_support(uint32_t k) { return k & 0xffffu; }
static unsigned key_table(uint32_t k) { return (k >> 16) & 255u; }

static unsigned global_local_index(unsigned assignment, unsigned support) {
  unsigned idx = 0, out = 0;
  for (unsigned v = 0; v < 15; ++v) if ((support >> v) & 1u) {
    idx |= ((assignment >> v) & 1u) << out;
    ++out;
  }
  return idx;
}

static unsigned expand_global(uint32_t key, unsigned union_support) {
  const unsigned support = key_support(key), table = key_table(key);
  const unsigned k = pc(union_support);
  unsigned ans = 0;
  for (unsigned a = 0; a < (1u << k); ++a) {
    unsigned global = 0, bit = 0;
    for (unsigned v = 0; v < 15; ++v) if ((union_support >> v) & 1u) {
      global |= ((a >> bit) & 1u) << v;
      ++bit;
    }
    if ((table >> global_local_index(global, support)) & 1u) ans |= 1u << a;
  }
  return ans;
}

static int affine_global(unsigned support, unsigned table) {
  for (unsigned mask = support;; mask = (mask - 1) & support) {
    for (unsigned rhs = 0; rhs < 2; ++rhs) {
      unsigned want = 0;
      const unsigned k = pc(support);
      for (unsigned a = 0; a < (1u << k); ++a) {
        unsigned global = 0, bit = 0;
        for (unsigned v = 0; v < 15; ++v) if ((support >> v) & 1u) {
          global |= ((a >> bit) & 1u) << v;
          ++bit;
        }
        if ((pc(global & mask) & 1) == int(rhs)) want |= 1u << a;
      }
      if (want == table) return int(mask | (rhs << 15));
    }
    if (mask == 0) break;
  }
  return -1;
}

static std::string vars_json(unsigned support) {
  std::ostringstream o; o << "["; bool first = true;
  for (unsigned v = 0; v < 15; ++v) if ((support >> v) & 1u) {
    if (!first) o << ",";
    first = false;
    o << (v + 1);
  }
  o << "]"; return o.str();
}

struct Witness {
  uint32_t left, right;
  unsigned support, table, min_sources;
  int equation;
};

int main() {
  const auto start = std::chrono::steady_clock::now();
  Metrics lm, rm;
  ClauseCatalog left_clauses, right_clauses;
  Catalog left = run_side(false, lm, left_clauses);
  Catalog right = run_side(true, rm, right_clauses);

  std::array<uint64_t,4> left_by_support{}, right_by_support{};
  for (auto [k,_] : left) ++left_by_support[pc(key_support(k))];
  for (auto [k,_] : right) ++right_by_support[pc(key_support(k))];

  uint64_t tested = 0, eligible = 0, affine = 0, contradictions = 0, nonaffine = 0;
  unsigned min_eligible = 99, min_affine = 99, min_contradiction = 99;
  std::vector<Witness> examples;
  for (const auto& [lk,li] : left) for (const auto& [rk,ri] : right) {
    ++tested;
    const unsigned support = key_support(lk) | key_support(rk);
    if (pc(support) > 3) continue;
    ++eligible;
    const unsigned sources = li.min_sources + ri.min_sources;
    min_eligible = std::min(min_eligible, sources);
    const unsigned table = expand_global(lk, support) & expand_global(rk, support);
    const int eq = affine_global(support, table);
    if (eq >= 0) {
      ++affine; min_affine = std::min(min_affine, sources);
      if (table == 0) { ++contradictions; min_contradiction = std::min(min_contradiction, sources); }
      if (examples.size() < 24) examples.push_back({lk,rk,support,table,sources,eq});
    } else ++nonaffine;
  }

  uint64_t cross_res_pairs = 0;
  unsigned min_cross_res_sources = 99;
  unsigned min_cross_res_support = 99;
  uint64_t cross_res_support_at_most_three = 0;
  std::array<uint64_t,16> cross_res_by_support{};
  std::set<uint32_t> cross_resolvents;
  for (const auto& [lk,li] : left_clauses)
    for (const auto& [rk,ri] : right_clauses) {
      const unsigned lp = lk & 0xffffu, ln = lk >> 16;
      const unsigned rp = rk & 0xffffu, rn = rk >> 16;
      const unsigned piv = (lp & rn) | (ln & rp);
      if (pc(piv) != 1) continue;
      const unsigned outp = (lp | rp) & ~piv;
      const unsigned outn = (ln | rn) & ~piv;
      if (outp & outn) continue;
      ++cross_res_pairs;
      const unsigned out_support_size = pc(outp | outn);
      min_cross_res_support = std::min(min_cross_res_support, out_support_size);
      if (out_support_size <= 3) ++cross_res_support_at_most_three;
      ++cross_res_by_support[out_support_size];
      min_cross_res_sources = std::min(min_cross_res_sources,
                                        li.min_sources + ri.min_sources);
      cross_resolvents.insert(uint32_t(outp | (outn << 16)));
    }

  rusage ru{}; getrusage(RUSAGE_SELF, &ru);
  const double sec = std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout << "{\n"
    << "  \"run\": \"LSPV-5/REFEREE391 cross-cut side-local interface closure\",\n"
    << "  \"scope\": \"all side-local source-once RES+AND3+XOR outcomes admissible as historical AND3 inputs; no LOCAL or DEF\",\n"
    << "  \"left_unique_conditions\": " << left.size() << ",\n"
    << "  \"right_unique_conditions\": " << right.size() << ",\n"
    << "  \"left_unique_clauses\": " << left_clauses.size() << ",\n"
    << "  \"right_unique_clauses\": " << right_clauses.size() << ",\n"
    << "  \"left_by_support_size\": [" << left_by_support[0] << "," << left_by_support[1] << "," << left_by_support[2] << "," << left_by_support[3] << "],\n"
    << "  \"right_by_support_size\": [" << right_by_support[0] << "," << right_by_support[1] << "," << right_by_support[2] << "," << right_by_support[3] << "],\n"
    << "  \"cross_pair_tests\": " << tested << ",\n"
    << "  \"support_at_most_three_pairs\": " << eligible << ",\n"
    << "  \"affine_conjunction_pairs\": " << affine << ",\n"
    << "  \"false_conjunction_pairs\": " << contradictions << ",\n"
    << "  \"nonaffine_conjunction_pairs\": " << nonaffine << ",\n"
    << "  \"min_sources_eligible\": " << (eligible ? min_eligible : 0) << ",\n"
    << "  \"min_sources_affine\": " << (affine ? min_affine : 0) << ",\n"
    << "  \"min_sources_false\": " << (contradictions ? min_contradiction : 0) << ",\n"
    << "  \"cross_strict_resolution_pairs\": " << cross_res_pairs << ",\n"
    << "  \"cross_strict_resolution_unique_outputs\": " << cross_resolvents.size() << ",\n"
    << "  \"min_sources_cross_strict_resolution\": "
    << (cross_res_pairs ? min_cross_res_sources : 0) << ",\n"
    << "  \"min_support_cross_strict_resolution\": "
    << (cross_res_pairs ? min_cross_res_support : 0) << ",\n"
    << "  \"cross_strict_resolution_support_at_most_three\": "
    << cross_res_support_at_most_three << ",\n"
    << "  \"cross_strict_resolution_by_output_support\": [";
  for (unsigned i = 0; i < cross_res_by_support.size(); ++i)
    std::cout << (i ? "," : "") << cross_res_by_support[i];
  std::cout << "],\n"
    << "  \"affine_examples\": [\n";
  for (size_t i = 0; i < examples.size(); ++i) {
    const auto& w = examples[i];
    const unsigned emask = unsigned(w.equation) & 0x7fffu;
    const unsigned erhs = (unsigned(w.equation) >> 15) & 1u;
    std::cout << "    {\"left_support\":" << vars_json(key_support(w.left))
      << ",\"left_table\":" << key_table(w.left)
      << ",\"right_support\":" << vars_json(key_support(w.right))
      << ",\"right_table\":" << key_table(w.right)
      << ",\"output_support\":" << vars_json(w.support)
      << ",\"output_table\":" << w.table
      << ",\"equation_mask\":" << vars_json(emask)
      << ",\"equation_rhs\":" << erhs
      << ",\"min_source_leaves\":" << w.min_sources << "}"
      << (i + 1 == examples.size() ? "\n" : ",\n");
  }
  std::cout << "  ],\n"
    << "  \"side_pair_tests\": {\"left_res\":" << lm.res_pairs
    << ",\"left_and\":" << lm.and_pairs << ",\"left_xor\":" << lm.xor_pairs
    << ",\"right_res\":" << rm.res_pairs << ",\"right_and\":" << rm.and_pairs
    << ",\"right_xor\":" << rm.xor_pairs << "},\n"
    << "  \"wall_seconds\": " << std::fixed << std::setprecision(6) << sec << ",\n"
    << "  \"max_rss_kib\": " << ru.ru_maxrss << ",\n"
    << "  \"status\": \"COMPUTATIONAL_EXACT_FINITE\"\n"
    << "}\n";
}
