from setuptools import setup, find_packages
import subprocess
import sys
import os

def install_fip():
    """Install fip if not already available"""
    try:
        # Check if fip is already available
        subprocess.run(["fip", "--help"], check=True, capture_output=True)
        print("✅ fip already installed")
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    print("📦 Installing fip (clipboard utility)...")
    
    # Use the official one-line installer from the fip repository
    try:
        subprocess.run([
            "sh", "-c", 
            "curl -fsSL https://raw.githubusercontent.com/Blakemagne/fip/main/install.sh | sh"
        ], check=True)
        print("✅ fip installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Could not install fip automatically: {e}")
        print("💡 Manual installation:")
        print("   curl -fsSL https://raw.githubusercontent.com/Blakemagne/fip/main/install.sh | sh")

# Install fip during setup
install_fip()

setup(
    name="otw-cli",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "otw=otw.cli:main"
        ]
    },
    author="Blakemagne",
    description="CLI companion for OverTheWire wargames",
    python_requires=">=3.7",
    # Note: fip is installed automatically during setup
)
