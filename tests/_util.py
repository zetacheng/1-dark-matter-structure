"""Anchor + mutation-discrimination helpers (not a test module).

Every numeric anchor is paired with a committed *discrimination* check: a value
perturbed by more than the tolerance must be rejected by that tolerance. This
proves the tolerance discriminates rather than passing anything (Task 6.3a).
Tolerances are numerical and justified at each call site — never byte-identity,
because cross-platform float reduction order makes byte-identity unachievable.
"""


def within(value, expected, tol):
    return abs(value - expected) <= tol


def check_anchor(value, expected, tol, bump_rel, label):
    """Assert value≈expected within tol, AND that a bump_rel perturbation is rejected."""
    assert within(value, expected, tol), (
        f"{label}: {value!r} not within {tol} of {expected!r}"
    )
    # Discrimination: perturbing the real value by bump_rel must leave the tol band.
    perturbed = value * (1 + bump_rel)
    assert not within(perturbed, expected, tol), (
        f"{label}: tolerance {tol} fails to reject a {bump_rel:+.1%} perturbation "
        f"({perturbed!r} still within {tol} of {expected!r}) — tolerance too loose"
    )
    assert abs(bump_rel * value) > tol, (
        f"{label}: chosen bump {bump_rel} is not larger than tol {tol}"
    )


def check_count(value, expected, label):
    """Exact integer anchor; discrimination = an off-by-one is caught."""
    assert value == expected, f"{label}: {value} != {expected}"
    assert (value + 1) != expected and (value - 1) != expected, (
        f"{label}: off-by-one not discriminated"
    )
