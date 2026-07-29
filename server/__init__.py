"""Skills Evaluation server package.

Puts the repo root on sys.path so `import refdata` resolves the same whether the
app is started by uvicorn, by pytest, or inside the container.
"""
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
