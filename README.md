# GitHub Repository Analyzer Skills

This project contains custom **Gemini CLI Skills** for analyzing GitHub repositories.

The skills allow Gemini CLI to retrieve repository information through the **GitHub REST API** and generate a technical analysis of the project.

---

## Features

### GitHub Repository Reader

This skill is responsible for:

- connecting to a GitHub repository;
- retrieving repository metadata;
- determining the default branch;
- reading the repository structure;
- listing repository files;
- retrieving file contents when necessary.

The repository is accessed through the **GitHub REST API** without cloning it locally.

---

### Repository Analyzer

This skill analyzes the retrieved repository information and generates:

- project summary;
- technologies used;
- project structure;
- strengths;
- potential issues;
- recommendations for improvement.

The analysis is based only on the available repository context.

---

## Project Structure

```
.
├── .gemini
│   └── skills
│       ├── github-repository-reader
│       │   └── SKILL.md
│       └── repository-analyzer
│           └── SKILL.md
├── .gitignore
└── README.md
```

---

## Installation

1. Install Node.js.

2. Install Gemini CLI.

3. Clone the repository:

```bash
git clone https://github.com/khrystya-s/homework-week1.git
```

4. Open the project directory.

---

## Usage

Start Gemini CLI inside the project directory.

Example prompts:

```
Analyze this repository:
https://github.com/octocat/Hello-World
```

```
Analyze this repository:
https://github.com/psf/requests
```

```
Analyze this repository:
https://github.com/khrystya-s/rgr-os
```

Gemini automatically activates the appropriate skills and performs repository analysis.

---

## Technologies

- Gemini CLI
- GitHub REST API
- Markdown

---

## Author

Khrystyna Struk