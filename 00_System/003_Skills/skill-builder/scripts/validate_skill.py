#!/usr/bin/env python3
"""
Skill Validator - Validates Claude skill structure and content

Performs comprehensive validation of a skill directory to ensure it meets
all requirements before packaging.

Usage:
    python validate_skill.py /path/to/skill-directory

Checks performed:
    - SKILL.md exists and has valid YAML frontmatter
    - Required fields (name, description) are present
    - Name matches directory name and follows conventions
    - Description includes triggering information
    - Body length is reasonable
    - Referenced files exist
    - No prohibited files present
"""

import sys
import re
from pathlib import Path


class ValidationResult:
    """Container for validation results."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
    
    def add_error(self, message: str):
        self.errors.append(f"❌ ERROR: {message}")
    
    def add_warning(self, message: str):
        self.warnings.append(f"⚠️  WARNING: {message}")
    
    def add_info(self, message: str):
        self.info.append(f"ℹ️  INFO: {message}")
    
    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0
    
    def print_report(self):
        """Print the full validation report."""
        if self.errors:
            print("\n=== ERRORS (must fix) ===")
            for e in self.errors:
                print(e)
        
        if self.warnings:
            print("\n=== WARNINGS (should fix) ===")
            for w in self.warnings:
                print(w)
        
        if self.info:
            print("\n=== INFO ===")
            for i in self.info:
                print(i)
        
        print("\n" + "=" * 40)
        if self.is_valid:
            print("✅ VALIDATION PASSED")
            if self.warnings:
                print(f"   ({len(self.warnings)} warnings to consider)")
        else:
            print(f"❌ VALIDATION FAILED ({len(self.errors)} errors)")


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Parse YAML frontmatter from SKILL.md content.
    
    Returns:
        Tuple of (frontmatter_dict, body_content)
    """
    if not content.startswith('---'):
        return None, content
    
    # Find the closing ---
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return None, content
    
    frontmatter_text = content[3:end_match.start() + 3]
    body = content[end_match.end() + 3:]
    
    # Parse simple YAML (just key: value pairs)
    frontmatter = {}
    current_key = None
    current_value = []
    
    for line in frontmatter_text.split('\n'):
        # Check for new key
        key_match = re.match(r'^(\w+):\s*(.*)$', line)
        if key_match:
            # Save previous key if exists
            if current_key:
                frontmatter[current_key] = ' '.join(current_value).strip()
            current_key = key_match.group(1)
            current_value = [key_match.group(2)] if key_match.group(2) else []
        elif current_key and line.strip():
            # Continuation of multi-line value
            current_value.append(line.strip())
    
    # Save last key
    if current_key:
        frontmatter[current_key] = ' '.join(current_value).strip()
    
    return frontmatter, body


def validate_skill(skill_path: str) -> ValidationResult:
    """
    Validate a skill directory.
    
    Args:
        skill_path: Path to the skill directory
        
    Returns:
        ValidationResult with all findings
    """
    result = ValidationResult()
    skill_dir = Path(skill_path).resolve()
    
    # === Check 1: Directory exists ===
    if not skill_dir.exists():
        result.add_error(f"Skill directory not found: {skill_dir}")
        return result
    
    if not skill_dir.is_dir():
        result.add_error(f"Path is not a directory: {skill_dir}")
        return result
    
    skill_name = skill_dir.name
    
    # === Check 2: Naming conventions ===
    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$', skill_name):
        result.add_error(
            f"Skill name '{skill_name}' must be kebab-case "
            "(lowercase letters, digits, hyphens; no leading/trailing hyphens)"
        )
    
    if len(skill_name) > 64:
        result.add_error(f"Skill name too long ({len(skill_name)} chars, max 64)")
    
    # === Check 3: SKILL.md exists ===
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        result.add_error("SKILL.md not found in skill directory")
        return result
    
    # === Check 4: Parse and validate SKILL.md ===
    content = skill_md_path.read_text()
    frontmatter, body = parse_frontmatter(content)
    
    if frontmatter is None:
        result.add_error("SKILL.md must start with YAML frontmatter (---)")
        return result
    
    # === Check 5: Required frontmatter fields ===
    if 'name' not in frontmatter:
        result.add_error("Frontmatter missing required field: name")
    elif frontmatter['name'] != skill_name:
        result.add_error(
            f"Frontmatter name '{frontmatter['name']}' "
            f"doesn't match directory name '{skill_name}'"
        )
    
    if 'description' not in frontmatter:
        result.add_error("Frontmatter missing required field: description")
    else:
        desc = frontmatter['description']
        
        # Check description quality
        if len(desc) < 50:
            result.add_warning(
                f"Description seems short ({len(desc)} chars). "
                "Include both what the skill does AND when to use it."
            )
        
        if '[TODO' in desc or '[todo' in desc:
            result.add_error("Description contains unfilled [TODO] placeholder")
        
        # Check for trigger indicators
        trigger_phrases = ['use when', 'trigger', 'use for', 'use this', 'when the user']
        has_trigger = any(phrase in desc.lower() for phrase in trigger_phrases)
        if not has_trigger:
            result.add_warning(
                "Description should explain WHEN to use the skill "
                "(e.g., 'Use when the user asks to...')"
            )
    
    # Check for prohibited fields
    prohibited = ['version', 'author', 'date', 'license']
    for field in prohibited:
        if field in frontmatter and field != 'license':
            result.add_warning(
                f"Frontmatter contains '{field}' - only 'name' and 'description' are used"
            )
    
    # === Check 6: Body content ===
    body_lines = body.strip().split('\n')
    
    if len(body_lines) > 500:
        result.add_warning(
            f"SKILL.md body is {len(body_lines)} lines (recommended: <500). "
            "Consider moving detailed content to references/"
        )
    
    if '[TODO' in body or '[todo' in body:
        todo_count = body.lower().count('[todo')
        result.add_warning(f"Body contains {todo_count} unfilled [TODO] placeholder(s)")
    
    # === Check 7: Verify referenced files exist ===
    # Find references in markdown links
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(link_pattern, body):
        link_text, link_path = match.groups()
        
        # Skip external URLs
        if link_path.startswith(('http://', 'https://', '#')):
            continue
        
        # Check if internal file exists
        referenced_file = skill_dir / link_path
        if not referenced_file.exists():
            result.add_error(f"Referenced file not found: {link_path}")
    
    # === Check 8: Check for prohibited files ===
    prohibited_files = [
        'README.md', 'readme.md',
        'CHANGELOG.md', 'changelog.md',
        'INSTALLATION.md', 'installation.md',
        'QUICK_REFERENCE.md',
        '.git', '.gitignore',
        'package.json', 'requirements.txt'
    ]
    
    for item in skill_dir.iterdir():
        if item.name in prohibited_files:
            result.add_warning(
                f"Skill contains '{item.name}' - skills should only contain "
                "SKILL.md and resource directories (scripts/, references/, assets/)"
            )
    
    # === Check 9: Validate scripts if present ===
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.glob("*.py"):
            script_content = script.read_text()
            
            # Check for placeholder content
            if 'TODO: Implement' in script_content or 'TODO: Add' in script_content:
                result.add_warning(f"Script {script.name} contains TODO placeholders")
            
            # Check for basic structure
            if 'def main' not in script_content and '__main__' not in script_content:
                result.add_info(
                    f"Script {script.name} has no main() function - "
                    "may not be directly executable"
                )
    
    # === Check 10: Validate references if present ===
    refs_dir = skill_dir / "references"
    if refs_dir.exists():
        for ref in refs_dir.glob("*.md"):
            ref_content = ref.read_text()
            lines = ref_content.split('\n')
            
            if len(lines) > 100 and '## Table of Contents' not in ref_content:
                result.add_info(
                    f"Reference {ref.name} is {len(lines)} lines - "
                    "consider adding a Table of Contents"
                )
    
    # === Summary info ===
    result.add_info(f"Skill name: {skill_name}")
    result.add_info(f"SKILL.md: {len(body_lines)} lines")
    
    if scripts_dir.exists():
        script_count = len(list(scripts_dir.glob("*")))
        result.add_info(f"Scripts: {script_count} files")
    
    if refs_dir.exists():
        ref_count = len(list(refs_dir.glob("*")))
        result.add_info(f"References: {ref_count} files")
    
    assets_dir = skill_dir / "assets"
    if assets_dir.exists():
        asset_count = len(list(assets_dir.glob("*")))
        result.add_info(f"Assets: {asset_count} files/directories")
    
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_skill.py /path/to/skill-directory")
        print("\nValidates a skill directory structure and content.")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    
    print(f"🔍 Validating skill: {skill_path}")
    print()
    
    result = validate_skill(skill_path)
    result.print_report()
    
    sys.exit(0 if result.is_valid else 1)


if __name__ == "__main__":
    main()
