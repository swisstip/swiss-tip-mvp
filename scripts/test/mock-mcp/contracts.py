"""Tool contracts of the mock server: re-exported from swisstip.core.contracts.

The models moved to packages/core on 12 September 2026 so that the mock and
the real server serve one contract. This module keeps the old import path and
the schema export command working:

    python scripts/test/mock-mcp/contracts.py --check docs/architecture/tool-contracts.schema.json
"""

import sys
from pathlib import Path

try:
    from swisstip.core.contracts import *  # noqa: F401,F403
    from swisstip.core.contracts import main, TOOL_CONTRACTS, TOOL_DESCRIPTIONS, tool_input_schema, tool_output_schema  # noqa: F401
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "packages/core/src"))
    from swisstip.core.contracts import *  # noqa: F401,F403
    from swisstip.core.contracts import main, TOOL_CONTRACTS, TOOL_DESCRIPTIONS, tool_input_schema, tool_output_schema  # noqa: F401

if __name__ == "__main__":
    raise SystemExit(main())
