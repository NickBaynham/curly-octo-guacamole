from typing import List, Any, Callable
import traceback


class SoftAssert:
    """Soft assertion utility that collects failures without stopping the test."""
    
    def __init__(self):
        self.failures: List[str] = []
    
    def assert_true(self, condition: bool, message: str = "Condition should be True"):
        """Soft assert that condition is True."""
        if not condition:
            failure_msg = f"❌ SOFT ASSERT FAILED: {message}"
            self.failures.append(failure_msg)
            print(failure_msg)
    
    def assert_false(self, condition: bool, message: str = "Condition should be False"):
        """Soft assert that condition is False."""
        if condition:
            failure_msg = f"❌ SOFT ASSERT FAILED: {message}"
            self.failures.append(failure_msg)
            print(failure_msg)
    
    def assert_equal(self, actual: Any, expected: Any, message: str = None):
        """Soft assert that actual equals expected."""
        if actual != expected:
            msg = message or f"Expected {expected}, but got {actual}"
            failure_msg = f"❌ SOFT ASSERT FAILED: {msg}"
            self.failures.append(failure_msg)
            print(failure_msg)
    
    def assert_not_equal(self, actual: Any, expected: Any, message: str = None):
        """Soft assert that actual does not equal expected."""
        if actual == expected:
            msg = message or f"Expected not {expected}, but got {actual}"
            failure_msg = f"❌ SOFT ASSERT FAILED: {msg}"
            self.failures.append(failure_msg)
            print(failure_msg)
    
    def assert_in(self, item: Any, container: Any, message: str = None):
        """Soft assert that item is in container."""
        if item not in container:
            msg = message or f"Expected {item} to be in {container}"
            failure_msg = f"❌ SOFT ASSERT FAILED: {msg}"
            self.failures.append(failure_msg)
            print(failure_msg)
    
    def assert_not_in(self, item: Any, container: Any, message: str = None):
        """Soft assert that item is not in container."""
        if item in container:
            msg = message or f"Expected {item} to not be in {container}"
            failure_msg = f"❌ SOFT ASSERT FAILED: {msg}"
            self.failures.append(failure_msg)
            print(failure_msg)
    
    def assert_is_none(self, value: Any, message: str = None):
        """Soft assert that value is None."""
        if value is not None:
            msg = message or f"Expected None, but got {value}"
            failure_msg = f"❌ SOFT ASSERT FAILED: {msg}"
            self.failures.append(failure_msg)
            print(failure_msg)
    
    def assert_is_not_none(self, value: Any, message: str = None):
        """Soft assert that value is not None."""
        if value is None:
            msg = message or "Expected not None, but got None"
            failure_msg = f"❌ SOFT ASSERT FAILED: {msg}"
            self.failures.append(failure_msg)
            print(failure_msg)
    
    def assert_custom(self, condition: bool, message: str):
        """Custom soft assert with custom message."""
        if not condition:
            failure_msg = f"❌ SOFT ASSERT FAILED: {message}"
            self.failures.append(failure_msg)
            print(failure_msg)
    
    def assert_all(self):
        """Raise an exception if any soft assertions failed."""
        if self.failures:
            print(f"\n🚨 {len(self.failures)} SOFT ASSERTION(S) FAILED:")
            for failure in self.failures:
                print(f"  {failure}")
            raise AssertionError(f"{len(self.failures)} soft assertion(s) failed")
    
    def get_failures(self) -> List[str]:
        """Get list of all failures."""
        return self.failures.copy()
    
    def clear_failures(self):
        """Clear all failures."""
        self.failures.clear()
    
    def has_failures(self) -> bool:
        """Check if there are any failures."""
        return len(self.failures) > 0 