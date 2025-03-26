# EMFlow (provisional name)

**EMFlow** is a Python-based automation tool designed to streamline the simulation workflow using the [EMsoft](https://github.com/EMsoft-org/EMsoft) electron microscopy software suite. It focuses on simplifying the generation of `.nml` configuration files, managing multiple simulation stages, and minimizing manual intervention.

---

## 🚀 Features

- Automatically generates valid `.nml` configuration files for each EMsoft program.
- Parameters are structured using Python `@dataclass`es for clarity and type safety.
- Supports multiple input types per program (`.nml`, `.json`, `.txt`, etc.).
- Enables fully automated, sequential execution of the EMsoft pipeline.

---

## 🛠 Structure (in progress)

```bash
emflow/
├── parameters.py         # Dataclass definitions for each simulation stage
├── base.py               # Core EMSoftProgram logic and NML generation
├── programs/
│   ├── emmcopencl.py     # EMMCOpenCL subclass
│   ├── emecpmaster.py    # EMECPmaster subclass
│   └── ...
└── main.py               # Orchestrates the full simulation flow
