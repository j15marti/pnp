# Governance note: main.tex placeholder clobber

- Failure: f786a273 reduced root `main.tex` to 28 bytes; 46affd0a ("Restore...") wrote the 34-byte literal `THE_FULL_CORRECT_CONTENT_FROM_FILE`. Cause: a tool call passed a placeholder string instead of file content.
- Repair: `main.tex` restored from 0f94eb28 (23077 bytes) plus one comment line. Rollback: `git revert` this commit.
- Not repaired: the Grok 4.7 reviews' earlier finding that the body is not the reconciled MERGEGUARD1 root body and does not compile. That needs LSPV-5.
- Status: P vs NP OPEN. No scientific claims changed.
- Prevention: automations that edit main.tex should check size and `\end{document}` before pushing.
