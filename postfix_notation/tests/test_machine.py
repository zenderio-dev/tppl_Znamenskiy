from src.machine import evaluate


class TestExamples:
    def test_single_number(self):
        assert evaluate("42") == 42

    def test_addition(self):
        assert evaluate("2 3 +") == 5
