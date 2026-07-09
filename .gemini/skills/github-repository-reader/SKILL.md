---
name: github-repository-reader
description: >
  Use this skill whenever the user asks to inspect, explore, summarize,
  or retrieve information from a GitHub repository. This skill accesses
  the repository through the GitHub REST API instead of using a local clone.
---

# Purpose

Use this skill whenever:

- the user wants to inspect a GitHub repository;
- the user asks for the project structure;
- the user wants a list of repository files;
- the user requests file contents;
- another skill requires repository information.

Always retrieve information directly from GitHub.

Never rely on a local copy of the repository.

---

# Inputs

Accept any of the following formats:

- `owner/repository`
- `https://github.com/owner/repository`
- `https://github.com/owner/repository.git`

Normalize every input to:

`owner/repository`

---

# Authentication

Use a GitHub Personal Access Token if available.

Check for:

1. `GITHUB_TOKEN`
2. `GH_TOKEN`

If no token is available and the repository is public,
continue without authentication.

Never expose or print authentication tokens.

---

# Instructions

When this skill is selected:

1. Retrieve repository metadata.
2. Determine the default branch.
3. Retrieve the complete repository tree recursively.
4. Separate files from directories.
5. Retrieve file contents if requested.
6. Return structured repository information.

---

# Output

Return repository information including:

- repository name
- owner
- default branch
- directory structure
- file list

If requested, also return the contents of specific files.

---

# Error Handling

If the repository cannot be accessed:

- explain the reason;
- include the GitHub API error message;
- do not invent missing information.

---

# Constraints

Always use the GitHub REST API.

Do not:

- clone repositories;
- inspect the local filesystem;
- execute Git commands;
- fabricate repository contents.

This skill is responsible only for retrieving repository information.
Repository analysis should be performed by another skill.