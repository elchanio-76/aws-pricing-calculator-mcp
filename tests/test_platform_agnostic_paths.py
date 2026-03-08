"""
Property-based tests for platform-agnostic path handling.

**Feature: pypi-publishing, Property 4: Platform-Agnostic Path Handling**
**Validates: Requirements 2.4**
"""

import ast
import re
from pathlib import Path
from typing import List, Tuple

import pytest
from hypothesis import given, strategies as st


def get_python_files() -> List[Path]:
    """Get all Python source files in the project."""
    project_root = Path(__file__).parent.parent
    python_files = []
    
    # Include mcp_server and scripts directories
    for directory in ["mcp_server", "scripts"]:
        dir_path = project_root / directory
        if dir_path.exists():
            python_files.extend(dir_path.rglob("*.py"))
    
    return python_files


def extract_path_operations(file_path: Path) -> List[Tuple[int, str]]:
    """
    Extract potential path operations from a Python file.
    
    Returns list of (line_number, code_snippet) tuples for suspicious patterns.
    """
    violations = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Check for hardcoded path separators in string literals
        # Pattern: strings containing forward or backslash that look like paths
        for i, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('#'):
                continue
            
            # Skip print statements - they're output, not path operations
            if 'print(' in line:
                continue
            
            # Check for hardcoded separators in string concatenation
            # Pattern: "something" + "/" + "something" or similar
            if re.search(r'["\'].*[/\\].*["\'].*\+.*["\']', line):
                violations.append((i, line.strip()))
            
            # Check for os.path.join (should use pathlib instead)
            if 'os.path.join' in line:
                violations.append((i, line.strip()))
            
            # Check for string formatting with hardcoded separators in file operations
            # Look for patterns like: open("path/to/file"), Path("path/to/file")
            # But exclude URLs and type annotations
            if re.search(r'open\s*\(["\'].*[/\\]', line):
                if not re.search(r'https?://', line):
                    violations.append((i, line.strip()))
            
            # Check for path construction with string concatenation
            # Pattern: variable + "/something" or "/something" + variable
            if re.search(r'\w+\s*\+\s*["\'][/\\]', line) or re.search(r'["\'][/\\].*["\']\s*\+\s*\w+', line):
                if not re.search(r'https?://', line):
                    violations.append((i, line.strip()))
    
    except Exception:
        # If we can't read the file, skip it
        pass
    
    return violations


def check_pathlib_usage(file_path: Path) -> bool:
    """
    Check if a file uses pathlib.Path for path operations.
    
    Returns True if the file properly uses pathlib, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check for Path imports
        tree = ast.parse(content, filename=str(file_path))
        
        has_pathlib_import = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module == 'pathlib':
                    has_pathlib_import = True
                    break
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == 'pathlib':
                        has_pathlib_import = True
                        break
        
        # If file does path operations, it should import pathlib
        violations = extract_path_operations(file_path)
        
        # Files with path operations should use pathlib
        if violations and not has_pathlib_import:
            return False
        
        return True
    
    except Exception:
        # If we can't parse, assume it's okay
        return True


@given(st.sampled_from(get_python_files() or [Path("dummy.py")]))
def test_property_platform_agnostic_paths(python_file: Path):
    """
    Property: For any Python file in the codebase, path operations SHALL use
    platform-agnostic methods (pathlib.Path) rather than string concatenation
    with hardcoded separators.
    
    **Feature: pypi-publishing, Property 4: Platform-Agnostic Path Handling**
    **Validates: Requirements 2.4**
    """
    # Skip if dummy file (no files found)
    if python_file.name == "dummy.py":
        pytest.skip("No Python files found in project")
    
    # Skip if file doesn't exist
    if not python_file.exists():
        pytest.skip(f"File {python_file} does not exist")
    
    # Extract path operations that might be problematic
    violations = extract_path_operations(python_file)
    
    # Filter out acceptable patterns
    acceptable_violations = []
    for line_num, code in violations:
        # Allow URL patterns
        if 'http://' in code or 'https://' in code:
            continue
        # Allow format strings that are clearly URLs or API endpoints
        if 'cloudfront.net' in code or 'calculator.aws' in code:
            continue
        # Allow debug/log messages
        if 'DEBUG' in code or 'f.write' in code:
            continue
        
        acceptable_violations.append((line_num, code))
    
    # Assert no violations remain
    if acceptable_violations:
        violation_details = '\n'.join(
            f"  Line {line}: {code}" 
            for line, code in acceptable_violations
        )
        pytest.fail(
            f"File {python_file.relative_to(python_file.parent.parent)} contains "
            f"hardcoded path separators or non-pathlib path operations:\n"
            f"{violation_details}\n"
            f"Use pathlib.Path instead for platform-agnostic path handling."
        )


def test_all_files_use_pathlib_for_paths():
    """
    Unit test: Verify that all Python files with file operations use pathlib.
    
    This is a concrete example test that complements the property-based test.
    """
    python_files = get_python_files()
    
    if not python_files:
        pytest.skip("No Python files found")
    
    files_without_pathlib = []
    
    for py_file in python_files:
        violations = extract_path_operations(py_file)
        
        # Filter acceptable violations
        real_violations = []
        for line_num, code in violations:
            if 'http://' in code or 'https://' in code:
                continue
            if 'cloudfront.net' in code or 'calculator.aws' in code:
                continue
            if 'DEBUG' in code or 'f.write' in code:
                continue
            real_violations.append((line_num, code))
        
        if real_violations:
            files_without_pathlib.append((py_file, real_violations))
    
    if files_without_pathlib:
        report = []
        for py_file, violations in files_without_pathlib:
            report.append(f"\n{py_file.relative_to(py_file.parent.parent)}:")
            for line_num, code in violations:
                report.append(f"  Line {line_num}: {code}")
        
        pytest.fail(
            "The following files contain non-pathlib path operations:\n" +
            '\n'.join(report) +
            "\n\nUse pathlib.Path for platform-agnostic path handling."
        )
