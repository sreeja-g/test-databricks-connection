from src.hello import make_message


def test_make_message():
    result = make_message("Databricks")

    assert result == "Hello Databricks!"