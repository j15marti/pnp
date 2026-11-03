# Five-role math-formatting clarification

**User instruction: November 2, 2026, 20:40 PST, America/Los_Angeles.**

<!-- BEGIN LSPV5 FIVE_ROLE_MATH_FORMATTING_CLARIFICATION -->

Applies to all five existing PNP agents: General SAT Lower-Bound Lead, SAT-Circuit Reduction Builder, Hypergraph & Proof Certificates, Time-Space Resource Auditor, and Independent Proof Red Team.

## Markdown files

In every generated or revised `.md` artifact, use GitHub-compatible math. Enclose display equations in `$$` delimiters on separate lines, with blank lines around the display. Use `$...$` for inline math. Preserve the mathematical content and LaTeX commands.

Example file source:

```markdown
$$
\mathbb{E}R = 1 + \sum_{d=1}^{n} {n \choose d}\frac{r^d}{1+r^d}
$$
```

Do not put ordinary report equations in code fences; the fence above only demonstrates the required file syntax.

## Chat responses

Use normal rendered LaTeX in user-facing chat: `\(...\)` for inline mathematics and `\[...\]` for display mathematics. Do not carry the `.md`-specific dollar-delimiter instruction into chat, and do not show raw LaTeX or a code block unless the user requests the source.

Example chat source:

```latex
\[
\mathbb{E}R = 1 + \sum_{d=1}^{n} {n \choose d}\frac{r^d}{1+r^d}.
\]
```

## Scope and coordination

Apply this distinction on each agent's next report and chat response. This supersedes any interpretation that the earlier GitHub Markdown requirement also governed chat presentation. Ordinary `.tex` documents retain their existing LaTeX conventions.

This is a formatting-only clarification to the [active five-role research handoff](2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md). It changes no mathematical statement, scientific priority, task ID, title, enabled/paused state, schedule, or ownership. Publish the pointer in coordination issue #3, which all five roles are instructed to review.

<!-- END LSPV5 FIVE_ROLE_MATH_FORMATTING_CLARIFICATION -->
