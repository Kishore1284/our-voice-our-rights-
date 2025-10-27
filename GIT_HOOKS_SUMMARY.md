# Git Hooks Summary

This repository uses Git hooks to maintain code quality and prevent regressions. All hooks are cross-platform compatible and work on both Windows (PowerShell) and Unix-like systems (Bash).

## Hooks Overview

### 1. pre-commit
**Trigger**: Before each commit  
**Location**: `.git/hooks/pre-commit`  
**Purpose**: Format code, lint, and build validation

**Steps**:
1. If `frontend/package.json` changed:
   - Regenerates `package-lock.json`
   - Stages the updated lockfile
2. For frontend changes:
   - 🧹 Runs Prettier formatting
   - 🔍 Runs ESLint
   - 🏗️ Builds the project
3. Aborts commit if any step fails

**Commands**:
```bash
# Format
npm run format  # prettier --write "src/**/*.{js,jsx,ts,tsx,json,css,scss,html}"

# Lint
npm run lint   # eslint . --ext .js,.jsx,.ts,.tsx

# Build
npm run build  # vite build
```

### 2. pre-push
**Trigger**: Before each push  
**Location**: `.git/hooks/pre-push`  
**Purpose**: Run lightweight unit tests

**Steps**:
1. Frontend Tests (if Vitest exists):
   ```bash
   cd frontend
   npm run test -- --run --timeout=5000
   ```

2. Backend Tests (if pytest exists):
   ```bash
   cd backend
   pytest -q --maxfail=1 --disable-warnings
   ```

### 3. commit-msg
**Trigger**: After commit message is edited  
**Location**: `.husky/commit-msg`  
**Purpose**: Enforce conventional commit format

**Format**:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- chore: Maintenance tasks
- ci: CI/CD changes
- test: Test-related changes

## OS Compatibility

### Windows
- Uses PowerShell (pwsh) for native Windows path handling
- Permissions set via `icacls`
- Detects Windows via `$IsWindows` or MSYS/Cygwin checks

### Unix-like (Linux/macOS)
- Uses Bash for native Unix path handling
- Permissions set via `chmod +x`
- Native path resolution via `dirname`/`pwd`

## Additional Tools

### Prettier Configuration
Location: `.prettierrc`
```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "es5"
}
```

### Commitlint Configuration
Location: `commitlint.config.js`
```js
module.exports = { extends: ['@commitlint/config-conventional'] };
```

## Developer Setup

1. **Hook Installation**:
   - Hooks are version controlled and installed automatically
   - Pre-commit and pre-push hooks in `.git/hooks/`
   - Commit message hook via Husky in `.husky/`

2. **Dependencies**:
   ```bash
   # Root dependencies (commit linting)
   npm install

   # Frontend dependencies
   cd frontend
   npm install
   ```

3. **IDE Integration**:
   - VS Code users: Install the ESLint and Prettier extensions
   - Enable "Format on Save" for best experience