"""
Compatibility shim for numpy._core module
This fixes issues when loading models saved with newer numpy versions
"""
import sys

# Patch sys.modules BEFORE importing numpy
# This ensures pickle can find numpy._core when unpickling
try:
    import numpy.core as _core_module
    # Create the _core module in sys.modules so pickle can import it
    sys.modules['numpy._core'] = _core_module
    # Also create submodules
    if hasattr(_core_module, 'multiarray'):
        sys.modules['numpy._core.multiarray'] = _core_module.multiarray
    if hasattr(_core_module, 'umath'):
        sys.modules['numpy._core.umath'] = _core_module.umath
    if hasattr(_core_module, '_multiarray_umath'):
        sys.modules['numpy._core._multiarray_umath'] = _core_module._multiarray_umath
except Exception as e:
    print(f"Warning: Could not set up numpy compatibility: {e}")

# Now import numpy and patch the attribute
try:
    import numpy
    if not hasattr(numpy, '_core'):
        numpy._core = sys.modules.get('numpy._core', _core_module)
except:
    pass

