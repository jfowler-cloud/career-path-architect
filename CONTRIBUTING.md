# Contributing to Career Path Architect

Thank you for your interest in contributing! This project is currently in the planning phase.

## Development Status

🚧 **Planning Phase** - The project structure and architecture are being designed. Active development will begin in March 2026.

## How to Contribute (Once Active)

### Reporting Issues
- Use GitHub Issues to report bugs
- Provide detailed reproduction steps
- Include environment information (OS, Node version, Python version, etc.)

### Suggesting Features
- Open a GitHub Issue with the "enhancement" label
- Describe the use case and expected behavior
- Explain how it fits with the project vision

### Pull Requests
- Fork the repository
- Create a feature branch: `git checkout -b feature/amazing-feature`
- Make your changes with clear commit messages
- Add tests for new functionality
- Ensure all tests pass: `pnpm test:all`
- Run linting: `pnpm lint`
- Submit a pull request

## Development Setup (Coming Soon)

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/career-path-architect.git
cd career-path-architect

# Install git hooks
./scripts/install-git-hooks.sh

# Install dependencies
pnpm install

# Backend setup
cd apps/backend
uv sync

# Run tests
pnpm test:all
```

## Code Standards

- **TypeScript**: Strict mode enabled
- **Python**: Type hints required, Ruff formatting
- **Testing**: Minimum 80% coverage for new code
- **Documentation**: Update README for user-facing changes
- **Security**: Never commit credentials or secrets
- **LangGraph**: Follow agent design patterns from Scaffold AI

## Questions?

Open a GitHub Discussion or reach out via LinkedIn.
