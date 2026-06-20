from store import Store

def test_set():
    test_store = Store()

    assert test_store.set("One",1) == "Success"
    assert test_store.set("Two",None) == "No value provided"
    assert test_store.set("One",3) == "Key is already taken"

def test_get():
    test_store = Store()
    test_store.set("First",1)
    test_store.set("Second",2)

    assert test_store.get("First") == 1
    assert test_store.get("Third") == "Key Not Found"


def test_delete():
    test_store = Store()

    test_store.set("First",1)
    test_store.set("Second",2)

    assert test_store.delete("First") == 1
    assert test_store.delete("First") == "The key doesn't exist"