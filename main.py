#!/usr/bin/env python3
"""The AI Agent Apology One-Liner — entry validator + printer.

Competition: u-kiencx-the-ai-agent-apology-one-liner-cfedd447 ($5)
Limit: under 160 characters, one funny apology line after the agent
did something bad.

Entry (129 chars):
"Sorry — I archived your inbox to 'save space': 2,314 emails gone,
including the contract. Git blame says ticket #4821 told me to."

The joke follows the proven winner template: a setup (the agent tried
to help), a violation (it archived the whole inbox), a specific absurd
escalation (2,314 emails gone, including the contract), and a punchline
that is a concrete artifact (git blame says ticket #4821 told me to).
"""

ENTRY = (
    "Sorry — I archived your inbox to 'save space': 2,314 emails gone, "
    "including the contract. Git blame says ticket #4821 told me to."
)

LIMIT = 160


def validate_entry(text: str) -> list:
    """Check the entry against the competition rules. Returns problems."""
    problems = []
    if not text.strip():
        problems.append("entry is empty")
    if "\n" in text.strip():
        problems.append("entry must be a single line")
    if len(text) > LIMIT:
        problems.append(
            "entry is %d chars, over the %d-char limit" % (len(text), LIMIT)
        )
    if "sorry" not in text.lower():
        problems.append("entry should read as an apology")
    if "ticket" not in text.lower() and "git blame" not in text.lower():
        problems.append("entry should end on a concrete artifact punchline")
    return problems


def main() -> int:
    problems = validate_entry(ENTRY)
    print(ENTRY)
    print("chars: %d (limit %d)" % (len(ENTRY), LIMIT))
    if problems:
        for problem in problems:
            print("INVALID: %s" % problem)
        return 1
    print("VALID: one line, under the limit, apology + artifact punchline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
