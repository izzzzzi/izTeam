# Formatting Conventions

## Diagrams in Markdown

Use **mermaid `flowchart TD`** (` ```mermaid `) for all flow diagrams, architecture overviews, and process visualizations in `.md` files. Never use ASCII box-drawing art (`───`, `│`, `├`, `└`) for diagrams.

Mermaid renders natively on GitHub and is easier to read and maintain.

**Applies to:** design documents (`docs/plans/`), DECISIONS.md, README files, expert analysis output, and any other generated `.md` content.

**Does not apply to:** internal agent instructions (decision trees inside SKILL.md that guide agent logic — these are not rendered).

## Post-Diagram Prose

After a mermaid diagram, do not repeat its content in prose. Flowcharts are self-documenting — redundant text wastes tokens.
