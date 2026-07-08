# homework-week1
# GitHub Repository File Scanner

## Description

This project is a simple Command Line Interface (CLI) application written in Python.

The application connects to the GitHub API using a Personal Access Token (PAT), retrieves the structure of a GitHub repository, and prints the list of all files in the repository.

## Features

- Connects to GitHub via REST API
- Uses GitHub Personal Access Token for authentication
- Automatically detects the repository's default branch
- Recursively retrieves all files from the repository
- Prints the file list to the console
- Handles common API errors

## Requirements

- Python 3.10+
- requests library
- GitHub Personal Access Token (PAT)

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/homework-week1.git
```

Navigate to the project folder:

```bash
cd homework-week1
```

Install dependencies:

```bash
pip install requests
```

## Configuration

Create an environment variable named `GITHUB_TOKEN` and set it to your GitHub Personal Access Token.

Example (Windows CMD):

```cmd
set GITHUB_TOKEN=your_personal_access_token
```

## Usage

Run the application:

```bash
python main.py <owner/repository>
```

Example:

```bash
python main.py octocat/Hello-World
```

or

```bash
python main.py psf/requests
```

## Example Output

```
Repository: psf/requests
Branch: main

Files:

README.md
LICENSE
setup.py
requests/__init__.py
requests/api.py
...
```

## Project Structure

```
homework-week1/
│
├── main.py
├── README.md
└── .gitignore
```

## Technologies

- Python
- GitHub REST API
- Requests

## Author

Khrystyna Struk
