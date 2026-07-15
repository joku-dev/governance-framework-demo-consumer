import unittest

from demo_app import describe_release


class DescribeReleaseTests(unittest.TestCase):
    def test_describe_release_returns_demo_status(self) -> None:
        result = describe_release("demo-app", "0.1.0")

        self.assertEqual(result["name"], "demo-app")
        self.assertEqual(result["version"], "0.1.0")
        self.assertEqual(result["status"], "demo")

    def test_describe_release_rejects_empty_name(self) -> None:
        with self.assertRaises(ValueError):
            describe_release("", "0.1.0")


if __name__ == "__main__":
    unittest.main()
