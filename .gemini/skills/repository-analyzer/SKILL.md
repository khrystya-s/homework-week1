---
name: repository-analyzer
description: >
  Use this skill whenever the user asks to analyze a software repository,
  summarize its structure, identify technologies, detect potential issues,
  or generate technical documentation.
---

# Purpose

Use this skill whenever:

- the user asks to analyze a repository;
- the user requests a project summary;
- the user wants to identify technologies;
- the user asks for strengths and weaknesses;
- the user requests recommendations;
- a repository report needs to be generated.

This skill analyzes repository information.
It does not retrieve data directly from GitHub.

---

# Inputs

Receive repository context from another skill, including:

- repository metadata;
- directory structure;
- file list;
- contents of important files.

Priority files include:

- README.md
- requirements.txt
- pyproject.toml
- package.json
- Dockerfile
- compose.yaml
- main.py
- app.py
- source files
- documentation

---

# Instructions

When this skill is selected:

1. Understand the project purpose.
2. Identify technologies and dependencies.
3. Describe the project structure.
4. Highlight strengths.
5. Detect potential issues supported by the available context.
6. Suggest realistic improvements.
7. Generate structured output.

---

# Output

Generate a JSON object containing:

- summary
- technologies
- strengths
- issues
- recommendations

Also generate a Markdown report containing:

- Project Summary
- Technologies
- Project Structure
- Strengths
- Potential Issues
- Recommendations

Save the results as:

- `output/analysis.json`
- `output/report.md`

---

# Constraints

Use only the provided repository context.

Do not:

- fabricate information;
- assume technologies that are not present;
- report unsupported issues.

Recommendations should be practical, technically justified, and based on the available repository data.