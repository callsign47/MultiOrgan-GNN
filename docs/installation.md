# ORGANIX: Installation & Environment Setup

## 1. Prerequisites
- **Python**: Version 3.9, 3.10, or 3.11.
- **Operating System**: Linux, macOS, or Windows 10/11.
- **Hardware**: CPU or NVIDIA CUDA-enabled GPU (PyTorch 2.0+ compatible).

---

## 2. Environment Creation

It is strongly recommended to use a dedicated virtual environment or Conda environment:

```bash
# Using Python venv
python -m venv organix_env

# On Linux / macOS:
source organix_env/bin/activate

# On Windows (PowerShell):
.\organix_env\Scripts\Activate.ps1
```

---

## 3. Package Installation

### Option A: Install from Requirements
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Option B: Editable Package Installation
Install `organix` as an editable Python package:
```bash
pip install -e .
```

---

## 4. Verification

Verify that the environment and CLI are functional:

```bash
# Check CLI installation
organix verify

# Execute the 4-tier leakage control gate
organix gate

# Run the test suite
pytest tests/
# or
python -m unittest discover tests
```
