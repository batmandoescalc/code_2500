#!/usr/bin/env python3
"""
Create a Python 3.14 virtual environment for this course repository.

Usage:
    python3.14 setup_python314_environment.py

Optional:
    python3.14 setup_python314_environment.py --venv discrete_math_env
    python3.14 setup_python314_environment.py --python /path/to/python3.14

Standard-library modules (random, math, collections, fractions, re, itertools)
are included with Python and do not need to be installed.
"""

import argparse
import subprocess
import sys
from pathlib import Path

PACKAGES = [
    "matplotlib",
    "matplotlib-venn",
    "numpy",
    "scipy",
    "pandas<3",
    "ipywidgets",
    "ipython",
]

def default_python() -> str:
    if sys.platform == "win32":
        return "python"
    else:
        return "python3.14"
    

def run(command):
    """Run a command and stop if it fails."""
    print("+", " ".join(str(part) for part in command), flush=True)
    subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Create a Python 3.14 virtual environment and install course packages."
    )
    parser.add_argument(
        "--python",
        default=default_python(),
        help="Python 3.14 executable (default: python3.14 or python on Windows).",
    )
    parser.add_argument(
        "--venv",
        default="_2500_venv",
        help="Virtual-environment directory (default: .venv).",
    )
    args = parser.parse_args()

    repo_dir = Path(__file__).resolve().parent
    venv_dir = Path(args.venv)
    if not venv_dir.is_absolute():
        venv_dir = repo_dir / venv_dir

    # Verify that the requested interpreter is Python 3.14.
    version_code = (
        "import sys; "
        "print(f'Using Python {sys.version_info.major}.{sys.version_info.minor}'); "
        "sys.exit(0 if sys.version_info[:2] == (3, 14) else 1)"
    )
    try:
        run([args.python, "-c", version_code])
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(
            "\nCould not verify Python 3.14. Install Python 3.14 or pass its "
            "executable path with --python.",
            file=sys.stderr,
        )
        raise SystemExit(1) from error

    # Create the environment if it does not already exist.
    if not (venv_dir / "pyvenv.cfg").exists():
        run([args.python, "-m", "venv", str(venv_dir)])
    else:
        print(f"Using existing virtual environment: {venv_dir}")

    # Locate the environment's Python executable.
    if sys.platform == "win32":
        env_python = venv_dir / "Scripts" / "python.exe"
    else:
        env_python = venv_dir / "bin" / "python"

    run([str(env_python), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(env_python), "-m", "pip", "install", *PACKAGES])

    # Verify third-party imports and report installed versions.
    check_code = (
        "import matplotlib, matplotlib_venn, numpy, scipy, pandas, ipywidgets, IPython; "
        "print('All third-party imports successful'); "
        "print('matplotlib:', matplotlib.__version__); "
        "print('matplotlib-venn:', matplotlib_venn.__version__); "
        "print('numpy:', numpy.__version__); "
        "print('scipy:', scipy.__version__); "
        "print('pandas:', pandas.__version__); "
        "print('ipywidgets:', ipywidgets.__version__); "
        "print('IPython:', IPython.__version__)"
    )
    run([str(env_python), "-c", check_code])

    print("\nEnvironment setup complete.")
    print(f"Environment directory: {venv_dir}")
    print("\nActivate it with:")
    if sys.platform == "win32":
        print(f'  "{venv_dir}\\Scripts\\activate"')
    else:
        try:
            relative_venv = venv_dir.relative_to(repo_dir)
            activation_path = f"./{relative_venv}/bin/activate"
        except ValueError:
            activation_path = str(venv_dir / "bin" / "activate")
        print(f"  source {activation_path}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(
            f"\nSetup failed (command exited with status {error.returncode}).",
            file=sys.stderr,
        )
        sys.exit(error.returncode)
