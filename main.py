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

import re

ENTRY = (
    "Sorry — I archived your inbox to 'save space': 2,314 emails gone, "
    "including the contract. Git blame says ticket #4821 told me to."
)

LIMIT = 160

# The joke must SHOW the disaster, not just tell the judge it happened:
# a concrete bad action, a concrete consequence, a specific number,
# a named object, and a punchline that is a checkable artifact.
ACTION_VERBS = ("archived", "deleted", "sent", "shipped", "emailed", "wiped")
CONSEQUENCE_WORDS = ("gone", "missing", "wide open", "lost", "down")
NAMED_OBJECTS = ("inbox", "contract", "database", "login", "production")


def validate_entry(text: str) -> list:
    """Check the entry against the competition rules. Returns problems."""
    problems = []
    stripped = text.strip()
    if not stripped:
        problems.append("entry is empty")
        return problems
    if "\n" in stripped:
        problems.append("entry must be a single line")
    if len(text) > LIMIT:
        problems.append(
            "entry is %d chars, over the %d-char limit" % (len(text), LIMIT)
        )
    # 1. Apology up front: the line must open on the apology, not bury it.
    if not re.match(r"(?i)sorry\b", stripped):
        problems.append("entry must open with the apology ('Sorry …')")
    # 2. Shows, not tells: a concrete bad action the agent did.
    if not any(re.search(r"(?i)\b%s\b" % verb, stripped) for verb in ACTION_VERBS):
        problems.append("entry must show a concrete bad action (archived/deleted/…)")
    # 3. A concrete consequence, not a vague regret.
    if not any(word in stripped.lower() for word in CONSEQUENCE_WORDS):
        problems.append("entry must show a concrete consequence (gone/missing/…)")
    # 4. A specific number — the escalation must be measurable.
    if not re.search(r"\d{1,3}(,\d{3})+", stripped):
        problems.append("entry must carry a specific number (e.g. 2,314)")
    # 5. A named object that was harmed.
    if not any(re.search(r"(?i)\b%s\b" % obj, stripped) for obj in NAMED_OBJECTS):
        problems.append("entry must name the object that was harmed")
    # 6. Punchline must be a checkable artifact: git blame + ticket #N.
    if not re.search(r"(?i)git blame", stripped):
        problems.append("punchline must name git blame")
    if not re.search(r"ticket #\d+", stripped):
        problems.append("punchline must cite a ticket number (ticket #N)")
    # 7. Narrative order: apology → bad action → specific number → artifact
    #    punchline. A joke that cites the ticket before the disaster lands flat.
    positions = {}
    apology_m = re.search(r"(?i)\bsorry\b", stripped)
    if apology_m:
        positions["apology"] = apology_m.start()
    action_m = None
    for verb in ACTION_VERBS:
        m = re.search(r"(?i)\b%s\b" % verb, stripped)
        if m and (action_m is None or m.start() < action_m.start()):
            action_m = m
    if action_m:
        positions["action"] = action_m.start()
    number_m = re.search(r"\d{1,3}(,\d{3})+", stripped)
    if number_m:
        positions["number"] = number_m.start()
    artifact_m = re.search(r"(?i)git blame", stripped)
    if artifact_m:
        positions["artifact"] = artifact_m.start()
    order = ["apology", "action", "number", "artifact"]
    present = [name for name in order if name in positions]
    for earlier, later in zip(present, present[1:]):
        if positions[earlier] >= positions[later]:
            problems.append(
                "joke out of order: %s must come before %s" % (earlier, later)
            )
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
    # Self-test: the validator must reject entries that break each rule.
    bad_cases = {
        "no apology up front": "I archived your inbox, 2,314 emails gone, git blame ticket #4821.",
        "no concrete action": "Sorry — something bad happened to your inbox, ticket #4821.",
        "no specific number": "Sorry — I archived your inbox, emails gone, git blame ticket #4821.",
        "no artifact punchline": "Sorry — I archived your inbox: 2,314 emails gone, including the contract.",
        "two lines": "Sorry — I archived your inbox.\n2,314 emails gone, git blame ticket #4821.",
        "wrong order (ticket before action)": "Sorry — git blame ticket #4821: I archived your inbox, 2,314 emails gone.",
    }
    for name, bad in bad_cases.items():
        if not validate_entry(bad):
            print("SELF-TEST FAILED: %r should have been rejected (%s)" % (bad, name))
            return 1
    print("SELF-TEST: %d bad entries rejected as expected" % len(bad_cases))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
