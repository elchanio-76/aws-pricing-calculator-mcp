# Implementation Plan: PyPI Publishing for AWS Pricing Calculator MCP Server

## Overview

This implementation plan provides step-by-step tasks for publishing the AWS Pricing Calculator MCP Server to PyPI as a cross-platform Python package. The tasks are organized to ensure proper configuration, validation, and testing before publishing.

## Tasks

- [x] 1. Create git worktree for PyPI publishing work
  - Check current branch: `git branch --show-current`
  - Create new worktree: `git worktree add ../aws-pricing-calculator-mcp-pypi -b pypi-publishing`
  - This creates a new branch `pypi-publishing` in a separate directory
  - All subsequent work should be done in the new worktree directory
  - Note: After completing all tasks, you can merge this branch back to main
  - _Requirements: N/A (workflow setup)_

- [x] 2. Update package configuration for PyPI publishing
  - Update `pyproject.toml` with the new package name `elchanio76-aws-pricing-calculator-mcp`
  - Verify all required metadata fields are present (name, version, description, author, license)
  - Ensure Python version requirement is set to `>=3.10`
  - Add "Operating System :: OS Independent" to classifiers
  - Verify entry point configuration for `aws-pricing-calculator-mcp` command
  - _Requirements: 1.1, 1.2, 1.4, 1.5, 2.5_

- [ ]* 2.1 Write property test for package metadata completeness
  - **Property 1: Package Metadata Completeness**
  - **Validates: Requirements 1.1**

- [ ]* 2.2 Write property test for dependency declaration
  - **Property 2: Dependency Declaration**
  - **Validates: Requirements 1.3**

- [ ]* 2.3 Write property test for project URLs presence
  - **Property 3: Project URLs Presence**
  - **Validates: Requirements 1.5**

- [x] 3. Update version information
  - Update version in `pyproject.toml` to `0.1.0`
  - Update `__version__` in `mcp_server/__init__.py` to match
  - Ensure version follows semantic versioning format (MAJOR.MINOR.PATCH)
  - _Requirements: 7.1, 7.3, 7.4_

- [ ]* 3.1 Write property test for version consistency
  - **Property 14: Version Consistency**
  - **Validates: Requirements 7.1, 7.5**

- [ ]* 3.2 Write property test for semantic versioning format
  - **Property 15: Semantic Versioning Format**
  - **Validates: Requirements 7.3**

- [x] 4. Verify cross-platform path handling
  - Audit all file operations in `mcp_server/` and `scripts/` directories
  - Ensure all path operations use `pathlib.Path` instead of string concatenation
  - Replace any hardcoded path separators (`/` or `\`) with platform-agnostic methods
  - _Requirements: 2.4_

- [x] 4.1 Write property test for platform-agnostic path handling
  - **Property 4: Platform-Agnostic Path Handling**
  - **Validates: Requirements 2.4**

- [x] 5. Update MANIFEST.in for distribution files
  - Verify MANIFEST.in includes README.md and LICENSE
  - Ensure all necessary source files are included
  - Add any missing patterns for package data
  - _Requirements: 3.3, 3.4_

- [ ]* 5.1 Write property test for critical files inclusion
  - **Property 7: Critical Files Inclusion**
  - **Validates: Requirements 3.4**

- [ ]* 5.2 Write property test for required files in distribution
  - **Property 16: Required Files in Distribution**
  - **Validates: Requirements 8.2**

- [ ] 6. Update .gitignore for security
  - Ensure .gitignore includes `.pypirc` to prevent committing API tokens
  - Add patterns for `dist/`, `build/`, and `*.egg-info/` directories
  - Verify no sensitive files are tracked
  - _Requirements: 9.2_

- [ ]* 6.1 Write unit test for security configuration
  - **Property 17: Security Configuration**
  - **Validates: Requirements 9.2**

- [ ] 7. Install build tools
  - Install `build` package: `pip install build`
  - Install `twine` package: `pip install twine`
  - Verify installations are successful
  - _Requirements: 3.1_

- [ ] 8. Build package distributions
  - Clean previous builds: `rm -rf dist/ build/ *.egg-info`
  - Build wheel and source distributions: `python -m build`
  - Verify both `.whl` and `.tar.gz` files are created in `dist/` directory
  - Check that filenames include correct package name and version
  - _Requirements: 3.2, 3.3_

- [ ]* 8.1 Write property test for dual distribution generation
  - **Property 5: Dual Distribution Generation**
  - **Validates: Requirements 3.2**

- [ ]* 8.2 Write property test for source files inclusion
  - **Property 6: Source Files Inclusion**
  - **Validates: Requirements 3.3**

- [ ] 9. Validate package with twine
  - Run `twine check dist/*` to validate package metadata and structure
  - Fix any errors or warnings reported by twine
  - Ensure validation passes without issues
  - _Requirements: 3.5, 8.1_

- [ ]* 9.1 Write property test for package validation
  - **Property 8: Package Validation**
  - **Validates: Requirements 3.5, 8.1**

- [ ] 10. Test local installation
  - Create a clean virtual environment: `python -m venv test_env`
  - Activate the environment
  - Install the built wheel: `pip install dist/*.whl`
  - Verify package imports successfully: `python -c "import mcp_server; print(mcp_server.__version__)"`
  - Test entry point is available: `which aws-pricing-calculator-mcp` (Unix) or `where aws-pricing-calculator-mcp` (Windows)
  - Test entry point executes: `aws-pricing-calculator-mcp --help` (if help flag supported)
  - Deactivate and remove test environment
  - _Requirements: 5.1, 5.3, 5.4, 5.5_

- [ ]* 10.1 Write property test for entry point availability
  - **Property 9: Entry Point Availability**
  - **Validates: Requirements 5.3, 8.4**

- [ ]* 10.2 Write property test for dependency installation
  - **Property 10: Dependency Installation**
  - **Validates: Requirements 5.4**

- [ ]* 10.3 Write property test for package importability
  - **Property 11: Package Importability**
  - **Validates: Requirements 5.5, 7.4**

- [ ] 11. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Update README.md with PyPI installation instructions
  - Add installation section with `pip install elchanio76-aws-pricing-calculator-mcp`
  - Add installation section with `uvx elchanio76-aws-pricing-calculator-mcp`
  - Include usage examples for the MCP server
  - Add publishing process documentation for maintainers
  - Include troubleshooting section for common issues
  - Add section on creating and securing PyPI API tokens
  - Include CI/CD integration examples (GitHub Actions)
  - Update Kiro configuration examples to use new package name
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 9.4, 10.4_

- [ ]* 12.1 Write property test for documentation completeness
  - **Property 12: Documentation Completeness**
  - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**

- [ ]* 12.2 Write property test for README in package metadata
  - **Property 13: README in Package Metadata**
  - **Validates: Requirements 6.5**

- [ ]* 12.3 Write property test for token documentation
  - **Property 18: Token Documentation**
  - **Validates: Requirements 9.4**

- [ ]* 12.4 Write property test for CI/CD documentation
  - **Property 19: CI/CD Documentation**
  - **Validates: Requirements 10.4**

- [ ] 13. Update LICENSE file
  - Replace `[Your Name]` placeholder with actual copyright holder name
  - Verify year is correct (2026)
  - Ensure LICENSE is included in distribution
  - _Requirements: 1.1_

- [ ] 14. Create PyPI account and API token
  - Create account on https://pypi.org (if not already created)
  - Navigate to Account Settings → API tokens
  - Create API token with appropriate scope (project-specific recommended)
  - Save token securely (it will only be shown once)
  - _Requirements: 4.1, 9.1_

- [ ] 15. Configure PyPI credentials
  - Create `~/.pypirc` file with PyPI and TestPyPI configurations
  - Add API tokens to the configuration file
  - Set file permissions to 600: `chmod 600 ~/.pypirc`
  - Verify `.pypirc` is in `.gitignore`
  - _Requirements: 9.1, 9.2_

- [ ] 16. Test upload to TestPyPI
  - Upload to TestPyPI: `twine upload --repository testpypi dist/*`
  - Verify upload was successful
  - Check package page on https://test.pypi.org/project/elchanio76-aws-pricing-calculator-mcp/
  - Verify README renders correctly on TestPyPI
  - _Requirements: 4.4_

- [ ] 17. Test installation from TestPyPI
  - Create clean virtual environment
  - Install from TestPyPI: `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ elchanio76-aws-pricing-calculator-mcp`
  - Note: `--extra-index-url` needed for dependencies not on TestPyPI
  - Verify package imports and entry point works
  - Test basic functionality
  - _Requirements: 5.1, 5.2_

- [ ] 18. Checkpoint - Verify TestPyPI installation
  - Ensure TestPyPI installation works correctly, ask the user if questions arise.

- [ ] 19. Prepare release commit and tag
  - Commit all changes: `git add -A && git commit -m "Prepare release v0.1.0"`
  - Create git tag: `git tag v0.1.0`
  - Push commit: `git push origin pypi-publishing`
  - Push tag: `git push origin v0.1.0`
  - _Requirements: 7.2_

- [ ] 20. Upload to production PyPI
  - Rebuild package to ensure clean build: `rm -rf dist/ && python -m build`
  - Validate package: `twine check dist/*`
  - Upload to PyPI: `twine upload dist/*`
  - Verify upload was successful
  - _Requirements: 4.2, 4.3_

- [ ] 21. Verify production PyPI release
  - Visit https://pypi.org/project/elchanio76-aws-pricing-calculator-mcp/
  - Verify package metadata displays correctly
  - Verify README renders correctly
  - Check that version number is correct
  - Verify all project URLs work
  - _Requirements: 5.1_

- [ ] 22. Test installation from production PyPI
  - Create clean virtual environment
  - Install from PyPI: `pip install elchanio76-aws-pricing-calculator-mcp`
  - Verify package imports successfully
  - Test entry point: `aws-pricing-calculator-mcp --help`
  - Test with uvx: `uvx elchanio76-aws-pricing-calculator-mcp`
  - Verify all dependencies installed correctly
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 23. Create GitHub release
  - Navigate to https://github.com/elchanio-76/aws-pricing-calculator-mcp/releases/new
  - Select tag `v0.1.0`
  - Set release title: "v0.1.0 - Initial PyPI Release"
  - Add release notes describing the changes and features
  - Attach distribution files (optional): wheel and source distribution
  - Publish release
  - _Requirements: 7.2_

- [ ] 24. Test cross-platform installation (manual)
  - Test installation on Windows (if available)
  - Test installation on macOS (if available)
  - Test installation on Linux
  - Verify entry point works on all platforms
  - Document any platform-specific issues
  - _Requirements: 2.1, 2.2, 2.3_

- [ ] 25. Create GitHub Actions workflow for automated publishing (optional)
  - Create `.github/workflows/publish.yml` file
  - Configure workflow to trigger on release publication
  - Add steps for building and uploading to PyPI
  - Add `PYPI_API_TOKEN` to GitHub repository secrets
  - Test workflow by creating a test release
  - _Requirements: 10.1, 10.2, 10.3_

- [ ] 26. Merge pypi-publishing branch to main
  - Switch back to main worktree directory
  - Merge the branch: `git checkout main && git merge pypi-publishing`
  - Push to remote: `git push origin main`
  - Remove the worktree: `git worktree remove ../aws-pricing-calculator-mcp-pypi`
  - Delete the branch (optional): `git branch -d pypi-publishing`
  - _Requirements: N/A (workflow cleanup)_

- [ ] 27. Final checkpoint - Verify complete publishing workflow
  - Ensure all tests pass, ask the user if questions arise.
  - Verify package is installable from PyPI on all platforms
  - Confirm documentation is complete and accurate
  - Verify GitHub release is created with proper tags

## Notes

- Tasks marked with `*` are optional test tasks and can be skipped for faster implementation
- Each task references specific requirements for traceability
- Checkpoints ensure validation at key milestones
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Manual testing on multiple platforms is recommended before final release
- TestPyPI testing is highly recommended to catch issues before production release
- Keep API tokens secure and never commit them to version control
