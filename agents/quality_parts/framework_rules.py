FRAMEWORK_CHECK_RULES = """
FRAMEWORK CHECK

Verify the article contains AT MOST ONE memorable strategic framework.

Examples:

- Enterprise AI Maturity Model
- Execution Capability Stack
- Governance Layers
- Enterprise Decision Pyramid
- Autonomous Workforce Curve

PASS if exactly one framework is clearly presented, OR if the article
legitimately needs no framework and uses plain capability blocks instead.

FAIL if no framework exists AND the article's topic genuinely calls for one.

FAIL if TWO OR MORE named/acronym frameworks appear in the same
article, even if one is presented as primary and the other as
supporting — this includes cases where a second framework's steps
overlap conceptually with the first (e.g. one framework's stages
covering governance/runtime/sourcing while a second framework's
components cover the same three ideas under different names).
"""