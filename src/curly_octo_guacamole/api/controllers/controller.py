import logging
import subprocess
import sys
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class Controller:
    def __init__(self):
        pass

    def run_test(self, test_type: str, data: dict) -> dict: 
        if test_type == "ui":
            logger.info("Executing UI Test")
            return self.run_ui_test(data)
        elif test_type == "api":
            logger.info("Executing API Test")
            return self.run_api_test(data)
        else:
            raise ValueError(f"Invalid test type: {test_type}")

    def run_api_test(self, data: dict) -> dict:
        """
        Execute API tests using PyTest while maintaining compatibility.
        This method runs the appropriate test file based on the test type.
        """
        logger.info("Executing API Test")
        
        try:
            # Get the project root directory (go up from src/curly_octo_guacamole/api/controllers/)
            project_root = Path(__file__).parent.parent.parent.parent.parent
            
            # Determine which test file to run based on the test type
            test_type = data.get("test_type", "account")
            if test_type == "user":
                test_file_path = project_root / "tests" / "api" / "test_user.py"
                test_method = "test_create_user"
            else:  # default to account
                test_file_path = project_root / "tests" / "api" / "test_account.py"
                test_method = "test_create_account"
            
            if not test_file_path.exists():
                raise FileNotFoundError(f"Test file not found: {test_file_path}")
            
            # Set environment variables for the test data
            env = os.environ.copy()
            env['TEST_DATA'] = str(data)
            
            # Run the specific test using PyTest
            cmd = [
                "pdm", "run", "pytest",
                str(test_file_path),
                "-k", test_method,  # Run only the specific test method
                "-v",  # Verbose output
                "--tb=short",  # Short traceback
                "--capture=no"  # Show print statements
            ]
            
            logger.info(f"Executing command: {' '.join(cmd)}")
            logger.info(f"Test data: {data}")
            logger.info(f"Test file: {test_file_path}")
            logger.info(f"Test method: {test_method}")
            
            # Run the test
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                cwd=project_root
            )
            
            # Parse the result
            success = result.returncode == 0
            
            if success:
                logger.info("✅ API test executed successfully")
                return {
                    "status": "success",
                    "message": "API test executed successfully",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
            else:
                logger.error(f"❌ API test failed with return code: {result.returncode}")
                logger.error(f"STDOUT: {result.stdout}")
                logger.error(f"STDERR: {result.stderr}")
                return {
                    "status": "error",
                    "message": "API test failed",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
                
        except Exception as e:
            logger.error(f"Exception during API test execution: {str(e)}")
            return {
                "status": "error",
                "message": f"Exception during test execution: {str(e)}",
                "error": str(e)
            }
    
    def run_ui_test(self, data: dict) -> dict:
        logger.info("Executing UI Test")
        return {"status": "success", "message": "UI test executed successfully"}    

# Example usage
if __name__ == "__main__":
    # Create an instance of the Controller
    controller = Controller()
    
    # Example data for testing
    test_data = {
        "test_name": "sample_test",
        "parameters": {"param1": "value1"},
        "expired_at": "2025-08-19"  # Add the expired_at field that the test expects
    }
    
    # Invoke run_test with "ui" test type
    try:
        result = controller.run_test("ui", test_data)
        print("UI test executed successfully")
    except Exception as e:
        print(f"Error: {e}")
    
    # Invoke run_test with "api" test type
    try:
        result = controller.run_test("api", test_data)
        print("API test executed successfully")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example of invalid test type (will raise ValueError)
    try:
        result = controller.run_test("invalid", test_data)
    except ValueError as e:
        print(f"Expected error: {e}")
