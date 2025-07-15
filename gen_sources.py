#!/usr/bin/env python3
"""
Generate source files for Bazel build.
This script replaces the CMake custom commands for generating headers and sources.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_python_script(script_path, args, cwd=None):
    """Run a Python script with the given arguments."""
    cmd = [sys.executable, str(script_path)] + args
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script_path}:")
        print(result.stderr)
        sys.exit(1)
    return result.stdout


def generate_diagnostics(script_dir, build_dir, source_dir, include_dir):
    """Generate diagnostic headers."""
    script_path = script_dir / "diagnostic_gen.py"
    diagnostics_txt = script_dir / "diagnostics.txt"
    
    args = [
        "--outDir", str(build_dir),
        "--srcDir", str(source_dir),
        "--incDir", str(include_dir),
        "--diagnostics", str(diagnostics_txt)
    ]
    
    run_python_script(script_path, args)


def generate_syntax(script_dir, build_dir):
    """Generate syntax headers and sources."""
    script_path = script_dir / "syntax_gen.py"
    syntax_txt = script_dir / "syntax.txt"
    
    args = [
        "--dir", str(build_dir),
        "--syntax", str(syntax_txt)
    ]
    
    run_python_script(script_path, args)


def generate_version(source_dir, build_dir, version_major, version_minor, version_patch, version_hash):
    """Generate version source file."""
    version_in = source_dir / "util" / "VersionInfo.cpp.in"
    version_out = build_dir / "VersionInfo.cpp"
    
    with open(version_in, 'r') as f:
        content = f.read()
    
    content = content.replace("@SLANG_VERSION_MAJOR@", str(version_major))
    content = content.replace("@SLANG_VERSION_MINOR@", str(version_minor))
    content = content.replace("@SLANG_VERSION_PATCH@", str(version_patch))
    content = content.replace("@SLANG_VERSION_HASH@", str(version_hash))
    
    with open(version_out, 'w') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Generate source files for Bazel build")
    parser.add_argument("--build-dir", type=Path, required=True, help="Build directory")
    parser.add_argument("--source-dir", type=Path, required=True, help="Source directory")
    parser.add_argument("--include-dir", type=Path, required=True, help="Include directory")
    parser.add_argument("--script-dir", type=Path, required=True, help="Script directory")
    parser.add_argument("--version-major", type=int, default=8, help="Major version")
    parser.add_argument("--version-minor", type=int, default=1, help="Minor version")
    parser.add_argument("--version-patch", type=int, default=0, help="Patch version")
    parser.add_argument("--version-hash", type=str, default="bazel", help="Version hash")
    
    args = parser.parse_args()
    
    # Create build directory
    args.build_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate diagnostics
    generate_diagnostics(args.script_dir, args.build_dir, args.source_dir, args.include_dir)
    
    # Generate syntax
    generate_syntax(args.script_dir, args.build_dir)
    
    # Generate version
    generate_version(args.source_dir, args.build_dir, args.version_major, 
                    args.version_minor, args.version_patch, args.version_hash)


if __name__ == "__main__":
    main()