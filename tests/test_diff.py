from bharatwatch.core.diff_engine import compute_diff

def test_diff_created():
    old = []
    new = [{"title": "A", "dept": "X"}]
    changes = compute_diff(old, new, ["title", "dept"])
    assert len(changes) == 1
    assert changes[0]["change_type"] == "created"

def test_diff_updated():
    # "updated" fires when a NON-key field changes while the key stays the same.
    old = [{"title": "A", "dept": "X", "vacancies": "5"}]
    new = [{"title": "A", "dept": "X", "vacancies": "10"}]
    changes = compute_diff(old, new, ["title", "dept"])
    assert len(changes) == 1
    assert changes[0]["change_type"] == "updated"

def test_diff_key_field_change_is_create_plus_delete():
    # Changing a key field changes identity -> one created + one deleted.
    old = [{"title": "A", "dept": "X"}]
    new = [{"title": "A", "dept": "Y"}]
    changes = compute_diff(old, new, ["title", "dept"])
    types = sorted(c["change_type"] for c in changes)
    assert types == ["created", "deleted"]
