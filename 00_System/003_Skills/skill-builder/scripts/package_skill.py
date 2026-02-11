#!/usr/bin/env python3
"""
Skill Packager - Creates distributable .skill files

Packages a validated skill directory into a .skill file (zip format)
that can be distributed and installed.

Usage:
    python package_skill.py /path/to/skill-directory [--output /path/to/output]

The script automatically validates the skill before packaging.
If validation fails, no package is created.
"""

import sys
import zipfile
from pathlib import Path

# Import the validator
from validate_skill import validate_skill


def package_skill(skill_path: str, output_dir: str = None) -> Path:
    """
    Package a skill directory into a .skill file.
    
    Args:
        skill_path: Path to the skill directory
        output_dir: Optional output directory (defaults to current directory)
        
    Returns:
        Path to created .skill file, or None if failed
    """
    skill_dir = Path(skill_path).resolve()
    skill_name = skill_dir.name
    
    # Validate first
    print("🔍 Validating skill before packaging...")
    print()
    
    result = validate_skill(skill_path)
    
    # Print validation summary
    if result.errors:
        print("=== Validation Errors ===")
        for e in result.errors:
            print(e)
        print()
        print("❌ Cannot package: fix validation errors first")
        return None
    
    if result.warnings:
        print("=== Validation Warnings ===")
        for w in result.warnings:
            print(w)
        print()
        print("Proceeding with warnings (consider fixing them)...")
        print()
    
    print("✅ Validation passed")
    print()
    
    # Determine output location
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()
    
    skill_filename = output_path / f"{skill_name}.skill"
    
    # Create the .skill file
    print(f"📦 Packaging skill...")
    
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through all files in the skill directory
            for file_path in skill_dir.rglob('*'):
                if file_path.is_file():
                    # Skip hidden files and common unwanted files
                    if any(part.startswith('.') for part in file_path.parts):
                        continue
                    if file_path.name in ['__pycache__', '.DS_Store', 'Thumbs.db']:
                        continue
                    if file_path.suffix == '.pyc':
                        continue
                    
                    # Calculate relative path for archive
                    # Include the skill directory name as the root
                    arcname = file_path.relative_to(skill_dir.parent)
                    
                    zipf.write(file_path, arcname)
                    print(f"   Added: {arcname}")
        
        # Get package stats
        package_size = skill_filename.stat().st_size
        size_str = f"{package_size / 1024:.1f} KB" if package_size > 1024 else f"{package_size} bytes"
        
        print()
        print(f"✅ Successfully created: {skill_filename}")
        print(f"   Size: {size_str}")
        print()
        print("The .skill file can now be:")
        print("  - Shared with others")
        print("  - Uploaded to a skill repository")
        print("  - Installed by extracting the contents")
        
        return skill_filename
        
    except Exception as e:
        print(f"❌ Error creating package: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py /path/to/skill-directory [--output /path]")
        print()
        print("Creates a distributable .skill file from a skill directory.")
        print()
        print("Options:")
        print("  --output PATH    Directory to save the .skill file (default: current)")
        print()
        print("Example:")
        print("  python package_skill.py ./my-skill --output ./dist")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    
    # Parse --output argument
    output_dir = None
    if '--output' in sys.argv:
        output_idx = sys.argv.index('--output')
        if output_idx + 1 < len(sys.argv):
            output_dir = sys.argv[output_idx + 1]
    
    print(f"📦 Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()
    
    result = package_skill(skill_path, output_dir)
    
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
