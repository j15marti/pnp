#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <bitset>
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
  for (unsigned v = 0; v < 8; ++v) {
    if ((support >> v) & 1u) {
      idx |= ((assignment >> v) & 1u) << out;
      ++out;
    }
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
    for (unsigned v = 0; v < 8; ++v) {
      if ((union_support >> v) & 1u) {
        global |= ((a >> bit) & 1u) << v;
        ++bit;
      }
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
  for (unsigned a = 0; a < (1u << k); ++a) {
    if ((pc(a) & 1) == int(rhs)) table |= 1u << a;
  }
  return factor_code(mask, table);
}

static int affine_equation(U16 f) {
  const unsigned support = f & 255u, table = (f >> 8) & 255u;
  for (unsigned mask = 0; mask < 256; ++mask) {
    if (mask & ~support) continue;
    for (unsigned rhs = 0; rhs < 2; ++rhs) {
      U16 e = equation_code(mask, rhs);
      if (expand_table(equation_as_factor(e), support) == table) return int(e);
    }
  }
  return -1;
}

static int strict_resolve(U16 a, U16 b) {
  unsigned ap = a & 255u, an = (a >> 8) & 255u;
  unsigned bp = b & 255u, bn = (b >> 8) & 255u;
  unsigned piv = (ap & bn) | (an & bp);
  if (pc(piv) != 1) return -1;
  unsigned rp = (ap | bp) & ~piv;
  unsigned rn = (an | bn) & ~piv;
  if (rp & rn) return -1;
  return int(clause_code(rp, rn));
}

static U16 and_factor(U16 a, U16 b) {
  unsigned support = (a & 255u) | (b & 255u);
  unsigned table = expand_table(a, support) & expand_table(b, support);
  return factor_code(support, table);
}

static void add_factor(State& s, U16 f) {
  s.factors.push_back(f);
  s.conditions.push_back(f);
  int e = affine_equation(f);
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

static std::vector<U16> encode_side(bool right) {
  auto src = side(right);
  std::vector<int> vars;
  for (auto c : src) for (int x : c) vars.push_back(std::abs(x));
  std::sort(vars.begin(), vars.end());
  vars.erase(std::unique(vars.begin(), vars.end()), vars.end());
  std::vector<U16> out;
  for (auto c : src) {
    unsigned pos = 0, neg = 0;
    for (int x : c) {
      unsigned v = std::lower_bound(vars.begin(), vars.end(), std::abs(x)) - vars.begin();
      (x > 0 ? pos : neg) |= 1u << v;
    }
    out.push_back(clause_code(pos, neg));
  }
  return out;
}

struct Metrics {
  uint64_t partitions = 0, res_pairs = 0, and_pairs = 0, xor_pairs = 0;
  uint64_t equation_subsets = 0;
};

struct SideResult {
  State full;
  std::bitset<512> partition_sums;
  bool equation_subsets_exact;
};

static SideResult run_side(bool right, Metrics& metrics) {
  const auto src = encode_side(right);
  const unsigned n = src.size(), full = (1u << n) - 1;
  std::vector<State> dp(1u << n);
  for (unsigned i = 0; i < n; ++i) {
    dp[1u << i].clauses.push_back(src[i]);
    finalize(dp[1u << i]);
  }
  for (unsigned sz = 2; sz <= n; ++sz) {
    for (unsigned sub = 1; sub <= full; ++sub) {
      if (unsigned(pc(sub)) != sz) continue;
      State cur;
      for (unsigned a = (sub - 1) & sub; a; a = (a - 1) & sub) {
        unsigned b = sub ^ a;
        if (!b || a > b) continue;
        ++metrics.partitions;
        const State& A = dp[a]; const State& B = dp[b];
        metrics.res_pairs += uint64_t(A.clauses.size()) * B.clauses.size();
        for (U16 x : A.clauses) for (U16 y : B.clauses) {
          int z = strict_resolve(x, y);
          if (z >= 0) cur.clauses.push_back(U16(z));
        }
        metrics.and_pairs += uint64_t(A.conditions.size()) * B.conditions.size();
        for (U16 x : A.conditions) for (U16 y : B.conditions) {
          if (pc((x & 255u) | (y & 255u)) <= 3) add_factor(cur, and_factor(x,y));
        }
        metrics.xor_pairs += uint64_t(A.equations.size()) * B.equations.size();
        for (U16 x : A.equations) for (U16 y : B.equations)
          cur.equations.push_back(equation_code((x ^ y) & 255u, ((x >> 8) ^ (y >> 8)) & 1u));
      }
      finalize(cur);
      dp[sub] = std::move(cur);
    }
    std::cerr << (right ? "R" : "L") << " size=" << sz
              << " full_states=" << dp[full].clauses.size() << "/"
              << dp[full].factors.size() << "/" << dp[full].equations.size() << "\n";
  }
  for (unsigned sub = 1; sub <= full; ++sub)
    if (!dp[sub].equations.empty()) ++metrics.equation_subsets;
  bool exact_equation_subsets = true;
  std::array<U16,4> rows = {
    equation_code((1u<<0)|(1u<<2)|(1u<<3), right ? 0 : 1),
    equation_code((1u<<1)|(1u<<4)|(1u<<5), 0),
    equation_code((1u<<2)|(1u<<4)|(1u<<6), 0),
    equation_code((1u<<3)|(1u<<5)|(1u<<6), 0)
  };
  for (unsigned sub = 1; sub <= full; ++sub) {
    bool expected = false; U16 want = 0;
    for (unsigned gs = 1; gs < 16; ++gs) {
      unsigned sm = 0; U16 e = 0;
      for (unsigned g = 0; g < 4; ++g) if ((gs >> g) & 1u) {
        sm |= 15u << (4*g); e ^= rows[g];
      }
      if (sub == sm) { expected = true; want = e; break; }
    }
    if (expected) {
      if (dp[sub].equations.size() != 1 || dp[sub].equations[0] != want)
        exact_equation_subsets = false;
    } else if (!dp[sub].equations.empty()) exact_equation_subsets = false;
  }
  std::vector<std::bitset<512>> sums(1u << n);
  sums[0].set(0);
  for (unsigned mask = 1; mask <= full; ++mask) {
    const unsigned first = mask & -mask;
    for (unsigned block = mask; block; block = (block - 1) & mask) {
      if (!(block & first) || dp[block].equations.empty()) continue;
      const auto& prev = sums[mask ^ block];
      if (prev.none()) continue;
      for (U16 e : dp[block].equations)
        for (unsigned x = 0; x < 512; ++x) if (prev.test(x))
          sums[mask].set(x ^ e);
    }
  }
  return {std::move(dp[full]), sums[full], exact_equation_subsets};
}

static bool has(const std::vector<U16>& v, U16 x) {
  return std::binary_search(v.begin(), v.end(), x);
}

int main() {
  auto start = std::chrono::steady_clock::now();
  Metrics lm, rm;
  SideResult LR = run_side(false, lm);
  SideResult RR = run_side(true, rm);
  State& L = LR.full;
  State& R = RR.full;
  // In each remapping the bridge variable 15 is the highest local bit, bit 7.
  const U16 pos_unit = clause_code(1u << 7, 0);
  const U16 neg_unit = clause_code(0, 1u << 7);
  const U16 pos_eq = equation_code(1u << 7, 1);
  const U16 neg_eq = equation_code(1u << 7, 0);
  const U16 false_eq = equation_code(0, 1);
  const U16 false_factor = factor_code(0, 0);
  bool partition_contradiction = false;
  for (unsigned x = 0; x < 512; ++x)
    if (LR.partition_sums.test(x) && RR.partition_sums.test(x ^ 256u))
      partition_contradiction = true;
  rusage ru{}; getrusage(RUSAGE_SELF, &ru);
  double sec = std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout << "{\n"
    << "  \"run\": \"LSPV-5/REFEREE390 mixed source-once side closure\",\n"
    << "  \"scope\": \"historical RES+AND3+XOR, no LOCAL or DEF; 18-source full binary trees\",\n"
    << "  \"left\": {\"clauses\": " << L.clauses.size() << ", \"factors\": " << L.factors.size()
    << ", \"equations\": " << L.equations.size()
    << ", \"positive_unit_clause\": " << (has(L.clauses,pos_unit)?"true":"false")
    << ", \"positive_unit_equation\": " << (has(L.equations,pos_eq)?"true":"false")
    << ", \"false_equation\": " << (has(L.equations,false_eq)?"true":"false")
    << ", \"false_factor\": " << (has(L.factors,false_factor)?"true":"false")
    << ", \"equation_subsets\": " << lm.equation_subsets
    << ", \"equation_subsets_exact_internal_bundle_unions\": "
    << (LR.equation_subsets_exact ? "true" : "false")
    << ", \"partition_sums\": " << LR.partition_sums.count() << "},\n"
    << "  \"right\": {\"clauses\": " << R.clauses.size() << ", \"factors\": " << R.factors.size()
    << ", \"equations\": " << R.equations.size()
    << ", \"negative_unit_clause\": " << (has(R.clauses,neg_unit)?"true":"false")
    << ", \"negative_unit_equation\": " << (has(R.equations,neg_eq)?"true":"false")
    << ", \"false_equation\": " << (has(R.equations,false_eq)?"true":"false")
    << ", \"false_factor\": " << (has(R.factors,false_factor)?"true":"false")
    << ", \"equation_subsets\": " << rm.equation_subsets
    << ", \"equation_subsets_exact_internal_bundle_unions\": "
    << (RR.equation_subsets_exact ? "true" : "false")
    << ", \"partition_sums\": " << RR.partition_sums.count() << "},\n"
    << "  \"side_local_partition_contradiction\": "
    << (partition_contradiction ? "true" : "false") << ",\n"
    << "  \"pair_tests\": {\"left_res\": " << lm.res_pairs << ", \"left_and\": " << lm.and_pairs
    << ", \"left_xor\": " << lm.xor_pairs << ", \"right_res\": " << rm.res_pairs
    << ", \"right_and\": " << rm.and_pairs << ", \"right_xor\": " << rm.xor_pairs << "},\n"
    << "  \"wall_seconds\": " << sec << ",\n"
    << "  \"max_rss_kib\": " << ru.ru_maxrss << "\n"
    << "}\n";
}
