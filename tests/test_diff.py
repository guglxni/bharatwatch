from bharatwatch.core.diff_engine import compute_diff

def test_diff_created():
    old = []
    new = [{"title": "A", "dept": "X"}]
    changes = compute_diff(old, new, ["title", "dept"])
    assert len(changes) == 1
    assert changes[0]["change_type"] == "created"

def test_diff_updated():
    old = [{"title": "A", "dept": "X"}]
    new = [{"title": "A", "dept": "Y"}]
    changes = compute_diff(old, new, ["title", "dept"])
    assert len(changes) == 1
    assert changes[0]["change_type"] == "updated"
