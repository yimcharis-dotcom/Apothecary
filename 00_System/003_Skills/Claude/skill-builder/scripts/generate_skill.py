#!/usr/bin/env python3
"""
Skill Generator - Creates a new Claude skill with guided structure

This script generates a complete skill directory structure based on provided
parameters. It's the primary tool used by the skill-builder skill to create
new skills programmatically.

Usage:
    python generate_skill.py --name "skill-name" --description "..." --output /path

Arguments:
    --name          Skill name in kebab-case (e.g., "data-analyzer")
    --description   Complete description including triggers
    --output        Directory where skill folder will be created
    --scripts       Comma-separated list of script names to create
    --references    Comma-separated list of reference doc names
    --assets        Comma-separated list of asset names
    --structure     Skill structure type: workflow, task, reference, or capabilities

Examples:
    # Basic skill
    python generate_skill.py --name "image-editor" \
        --description "Edit images..." --output ./skills

    # With resources
    python generate_skill.py --name "pdf-processor" \
        --description "Process PDFs..." --output ./skills \
        --scripts "rotate.py,merge.py" \
        --references "api_guide.md"
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


def title_case(name: str) -> str:
    """Convert kebab-case to Title Case."""
    return ' '.join(word.capitalize() for word in name.split('-'))


def generate_skill_md(name: str, description: str, structure: str, 
                      scripts: list, references: list, assets: list) -> str:
    """Generate the SKILL.md content based on parameters."""
    
    title = title_case(name)
    
    # Build the frontmatter — description must be quoted to handle colons/special chars
    # Also escape any double quotes in the description
    safe_desc = description.replace('"', "'")
    
    content = f"""---
name: {name}
description: "{safe_desc}"
---

# {title}

"""
    
    # Add structure-specific content
    if structure == "workflow":
        content += """## Overview

[Brief description of what this skill enables]

## Workflow

1. **[First Phase]** → [What happens]
2. **[Second Phase]** → [What happens]
3. **[Third Phase]** → [What happens]

## Phase 1: [First Phase Name]

[Detailed instructions for this phase]

## Phase 2: [Second Phase Name]

[Detailed instructions for this phase]

## Phase 3: [Third Phase Name]

[Detailed instructions for this phase]

"""
    elif structure == "task":
        content += """## Overview

[Brief description of what this skill enables]

## Quick Start

[Minimal example to get started quickly]

## Task Category 1

[Instructions for this category of tasks]

## Task Category 2

[Instructions for this category of tasks]

## Task Category 3

[Instructions for this category of tasks]

"""
    elif structure == "reference":
        content += """## Overview

[Brief description of what standards or guidelines this skill provides]

## Guidelines

[Core guidelines and principles]

## Specifications

[Detailed specifications]

## Usage Examples

[Examples showing how to apply the guidelines]

"""
    else:  # capabilities
        content += """## Overview

[Brief description of what this skill enables]

## Core Capabilities

### 1. [First Capability]

[Description and instructions]

### 2. [Second Capability]

[Description and instructions]

### 3. [Third Capability]

[Description and instructions]

"""
    
    # Add resources section if any resources are specified
    has_resources = scripts or references or assets
    
    if has_resources:
        content += "## Resources\n\n"
        
        if scripts:
            content += "### Scripts\n\n"
            for script in scripts:
                script_name = script.replace('.py', '')
                content += f"**{script}** - [Description of what this script does]\n\n"
                content += f"```bash\npython scripts/{script} [arguments]\n```\n\n"
        
        if references:
            content += "### References\n\n"
            for ref in references:
                ref_display = ref.replace('.md', '').replace('_', ' ').title()
                content += f"- [{ref_display}](references/{ref}) - [When to use this reference]\n"
            content += "\n"
        
        if assets:
            content += "### Assets\n\n"
            for asset in assets:
                content += f"- `assets/{asset}` - [What this asset is for]\n"
            content += "\n"
    
    return content


def generate_script_template(script_name: str, skill_name: str) -> str:
    """Generate a template Python script."""
    
    func_name = script_name.replace('.py', '').replace('-', '_')
    
    return f'''#!/usr/bin/env python3
"""
{script_name} - [Brief description]

Part of the {skill_name} skill.

Usage:
    python {script_name} [input] [output] [options]

Arguments:
    input   - [Description of input]
    output  - [Description of output]
    
Options:
    --option  [Description]
"""

import argparse
import sys


def {func_name}(input_path: str, output_path: str, **options):
    """
    [Function description]
    
    Args:
        input_path: Path to input file
        output_path: Path for output file
        **options: Additional options
        
    Returns:
        True if successful, False otherwise
    """
    # TODO: Implement the actual functionality
    print(f"Processing {{input_path}} -> {{output_path}}")
    
    # Example implementation:
    # 1. Load the input
    # 2. Process it
    # 3. Save the output
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="[Script description]",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output file path")
    # Add more arguments as needed
    
    args = parser.parse_args()
    
    success = {func_name}(args.input, args.output)
    
    if success:
        print("✅ Operation completed successfully")
        sys.exit(0)
    else:
        print("❌ Operation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''


def generate_reference_template(ref_name: str, skill_name: str) -> str:
    """Generate a template reference document."""
    
    title = ref_name.replace('.md', '').replace('_', ' ').replace('-', ' ').title()
    
    return f"""# {title}

Reference documentation for the {skill_name} skill.

## Overview

[Brief description of what this reference covers and when to consult it]

## Table of Contents

1. [Section 1](#section-1)
2. [Section 2](#section-2)
3. [Section 3](#section-3)

## Section 1

[Detailed content]

### Subsection 1.1

[Content]

### Subsection 1.2

[Content]

## Section 2

[Detailed content]

## Section 3

[Detailed content]

## Quick Reference

| Item | Description | Example |
|------|-------------|---------|
| [Item 1] | [Description] | [Example] |
| [Item 2] | [Description] | [Example] |
| [Item 3] | [Description] | [Example] |
"""


def generate_skill(name: str, description: str, output_dir: str,
                   structure: str = "workflow",
                   scripts: list = None, 
                   references: list = None,
                   assets: list = None) -> Path:
    """
    Generate a complete skill directory structure.
    
    Args:
        name: Skill name in kebab-case
        description: Complete skill description
        output_dir: Parent directory for the skill
        structure: Type of structure (workflow, task, reference, capabilities)
        scripts: List of script filenames to create
        references: List of reference doc filenames
        assets: List of asset filenames/directories
        
    Returns:
        Path to created skill directory
    """
    scripts = scripts or []
    references = references or []
    assets = assets or []
    
    # Create skill directory
    skill_dir = Path(output_dir) / name
    
    if skill_dir.exists():
        print(f"❌ Error: Directory already exists: {skill_dir}")
        return None
        
    skill_dir.mkdir(parents=True)
    print(f"✅ Created skill directory: {skill_dir}")
    
    # Generate and write SKILL.md
    skill_md_content = generate_skill_md(
        name, description, structure, scripts, references, assets
    )
    (skill_dir / "SKILL.md").write_text(skill_md_content)
    print("✅ Created SKILL.md")
    
    # Create scripts directory and files
    if scripts:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir()
        for script in scripts:
            script_content = generate_script_template(script, name)
            script_path = scripts_dir / script
            script_path.write_text(script_content)
            script_path.chmod(0o755)
            print(f"✅ Created scripts/{script}")
    
    # Create references directory and files
    if references:
        refs_dir = skill_dir / "references"
        refs_dir.mkdir()
        for ref in references:
            ref_content = generate_reference_template(ref, name)
            (refs_dir / ref).write_text(ref_content)
            print(f"✅ Created references/{ref}")
    
    # Create assets directory
    if assets:
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir()
        for asset in assets:
            # Create placeholder file or directory
            asset_path = assets_dir / asset
            if '.' in asset:
                # It's a file
                asset_path.write_text(f"# Placeholder for {asset}\n\n[Replace with actual content]")
            else:
                # It's a directory
                asset_path.mkdir()
                (asset_path / ".gitkeep").touch()
            print(f"✅ Created assets/{asset}")
    
    print(f"\n✅ Skill '{name}' generated successfully!")
    print(f"   Location: {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the [bracketed placeholders]")
    print("2. Implement the actual logic in any generated scripts")
    print("3. Fill in reference documentation")
    print("4. Replace asset placeholders with actual files")
    print("5. Validate with: python validate_skill.py " + str(skill_dir))
    print("6. Package with: python package_skill.py " + str(skill_dir))
    
    return skill_dir


def main():
    parser = argparse.ArgumentParser(
        description="Generate a new Claude skill structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic workflow skill
    python generate_skill.py --name "data-analyzer" \\
        --description "Analyze CSV data..." --output ./skills

    # Task-based skill with scripts
    python generate_skill.py --name "image-editor" \\
        --description "Edit images..." --output ./skills \\
        --structure task \\
        --scripts "resize.py,rotate.py,convert.py"

    # Reference skill with documentation
    python generate_skill.py --name "brand-guidelines" \\
        --description "Brand standards..." --output ./skills \\
        --structure reference \\
        --references "colors.md,typography.md,logos.md" \\
        --assets "logo.png,fonts/"
        """
    )
    
    parser.add_argument(
        "--name", required=True,
        help="Skill name in kebab-case (e.g., 'data-analyzer')"
    )
    parser.add_argument(
        "--description", required=True,
        help="Complete description including when to use the skill"
    )
    parser.add_argument(
        "--output", required=True,
        help="Directory where skill folder will be created"
    )
    parser.add_argument(
        "--structure", default="workflow",
        choices=["workflow", "task", "reference", "capabilities"],
        help="Skill structure type (default: workflow)"
    )
    parser.add_argument(
        "--scripts",
        help="Comma-separated list of script names (e.g., 'process.py,validate.py')"
    )
    parser.add_argument(
        "--references",
        help="Comma-separated list of reference docs (e.g., 'api.md,guide.md')"
    )
    parser.add_argument(
        "--assets",
        help="Comma-separated list of assets (e.g., 'template.docx,images/')"
    )
    
    args = parser.parse_args()
    
    # Parse comma-separated lists
    scripts = [s.strip() for s in args.scripts.split(',')] if args.scripts else []
    references = [r.strip() for r in args.references.split(',')] if args.references else []
    assets = [a.strip() for a in args.assets.split(',')] if args.assets else []
    
    print(f"🚀 Generating skill: {args.name}")
    print(f"   Structure: {args.structure}")
    print(f"   Output: {args.output}")
    print()
    
    result = generate_skill(
        name=args.name,
        description=args.description,
        output_dir=args.output,
        structure=args.structure,
        scripts=scripts,
        references=references,
        assets=assets
    )
    
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
