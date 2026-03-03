import PyInstaller.__main__
import shutil
import os

def build():
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    print("🚀 Building Executable (onedir mode)...")
    print("   This may take a few minutes.")

    PyInstaller.__main__.run([
        'run_main.py',
        '--name=AI_XRay_Assistant',
        '--onedir',       # Folder output (safer for Torch/Streamlit)
        '--clean',
        '--noconfirm',
        
        # Include main app file
        '--add-data=app.py;.',
        
        # Include config
        '--add-data=.streamlit/config.toml;.streamlit',
        
        # Hidden imports for Streamlit & dependencies
        '--hidden-import=streamlit',
        '--hidden-import=streamlit.web.cli',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=torch',
        '--hidden-import=torchvision',
        '--hidden-import=PIL',
        '--hidden-import=altair',
        '--hidden-import=torchxrayvision',
        '--hidden-import=skimage',
        '--hidden-import=sklearn',
        
        # Collect all metadata/files for complex packages
        '--collect-all=streamlit',
        '--collect-all=altair',
        '--collect-all=torchxrayvision',
        '--collect-all=skimage',
    ])

    print("\n✅ Build Complete!")
    print("   Executable is at: dist/AI_XRay_Assistant/AI_XRay_Assistant.exe")
    print("\n⚠️  IMPORTANT: You must copy the 'models' folder into 'dist/AI_XRay_Assistant/'")
    print("   The executable expects the models to be in the same directory.")

if __name__ == "__main__":
    try:
        import PyInstaller
        build()
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        os.system("pip install pyinstaller")
        build()
