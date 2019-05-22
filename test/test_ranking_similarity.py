import random

import pytest
from hypothesis import given, note, strategies as st

from socialchoice.ranking_similarity import num_inversions


def test_num_inversions():
    assert num_inversions([], []) == 0
    assert num_inversions([1], [1]) == 0
    assert num_inversions([1, 2], [1, 2]) == 0
    assert num_inversions([0, 1], [1, 0]) == 1
    assert num_inversions([1, 2], [2, 1]) == 1
    assert num_inversions([2, 1], [1, 2]) == 1
    assert num_inversions([1, 2, 3], [3, 2, 1]) == 3
    assert num_inversions([3, 2, 1], [1, 2, 3]) == 3


def test_num_inversions_assertion_error_if_different_sets():
    with pytest.raises(ValueError):
        num_inversions([1], [2])

    with pytest.raises(ValueError):
        num_inversions([3], [3, 4])

    with pytest.raises(ValueError):
        num_inversions([1, 2], [2])


@pytest.mark.hypothesis
@pytest.mark.slow
@given(st.lists(st.integers(), unique=True))
def test_inversions_between_list_and_inverse_triangle(lst):
    """The number of inversions between a list and it's inverse should be the `len(l)`th triangle number."""
    note(f"List: {lst}, reversed: {list(reversed(lst))}")
    assert num_inversions(lst, reversed(lst)) == (len(lst) * (len(lst) - 1)) // 2


@pytest.mark.hypothesis
@pytest.mark.slow
@given(st.lists(st.integers(), unique=True))
def test_no_inversions_identical_list(lst):
    note(f"List: {lst}")
    assert num_inversions(lst, lst) == 0


@pytest.mark.hypothesis
@pytest.mark.slow
@given(st.lists(st.integers(), unique=True))
def test_inversions_order_irrelevant(lst):
    lst1 = lst
    lst2 = random.sample(lst, len(lst))

    note(f"Lists: {lst1, lst2}")
    assert num_inversions(lst1, lst2) == num_inversions(lst2, lst1)
