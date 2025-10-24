from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gneiss-engine",
    version="0.2.0",
    author="Gneiss-Engine Contributors",
    author_email="your.email@example.com",
    description="A rock-solid, high-performance Python core for metamorphic image manipulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gneiss-engine",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/gneiss-engine/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.8,<3.13",
    install_requires=[
        "Pillow>=9.0.0,<10.0.0",  # Using Pillow for image processing
        "Pillow-SIMD>=9.0.0; platform_machine == 'x86_64'",
        "tqdm>=4.62.0",   # For progress bars
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "isort>=5.9.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
            "types-Pillow",
        ],
    },
)