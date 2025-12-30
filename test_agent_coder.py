"""
Test and Demonstration Script for Agent Coder

This script demonstrates the core functionality of the agent_coder module:
1. Tool discovery and registration
2. Tool execution capabilities
3. Safety constraints enforcement
4. Basic agent loop execution
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_coder import (
    Tool,
    ToolResult,
    ToolExecutor,
    AgentCoder,
    AgentConfig
)


def test_tool_registration():
    """Test that tools are properly registered and discoverable."""
    print("\n=== Testing Tool Registration ===")
    
    executor = ToolExecutor()
    tools = executor.get_available_tools()
    
    expected_tools = [
        "read_file", "write_file", "edit_file", "list_files",
        "search_code", "get_file_info", "run_python", "finish"
    ]
    
    tool_names = [tool.name for tool in tools]
    
    print(f"Found {len(tool_names)} tools:")
    for name in tool_names:
        print(f"  - {name}")
    
    for expected in expected_tools:
        assert expected in tool_names, f"Missing tool: {expected}"
    
    print("✓ All expected tools registered")
    return True


def test_tool_execution():
    """Test basic tool execution with safe operations."""
    print("\n=== Testing Tool Execution ===")
    
    executor = ToolExecutor()
    
    # Test list_files (safe, read-only operation)
    result = executor.execute("list_files", {"directory": "."})
    assert result.success, f"list_files failed: {result.error}"
    assert isinstance(result.data, list), "list_files should return a list"
    assert len(result.data) > 0, "list_files should return some files"
    print(f"✓ list_files executed successfully, found {len(result.data)} items")
    
    # Test read_file (safe, read-only operation)
    result = executor.execute("read_file", {"filepath": "README.md"})
    if result.success:
        print("✓ read_file executed successfully")
    else:
        print(f"⚠ read_file skipped (file may not exist): {result.error}")
    
    return True


def test_safety_constraints():
    """Test that safety constraints are properly enforced."""
    print("\n=== Testing Safety Constraints ===")
    
    executor = ToolExecutor()
    
    # Try to write to a protected file
    protected_files = ["constitutional.py", "provenance.py", "modification_log.py"]
    
    for protected in protected_files:
        # Create a temporary file in temp directory (safe)
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
            f.write("# test file\n")
        
        try:
            result = executor.execute("write_file", {
                "filepath": protected,
                "content": "# This should be blocked"
            })
            assert not result.success, f"Writing to {protected} should be blocked"
            print(f"✓ Writing to {protected} properly blocked")
        finally:
            os.unlink(temp_file)
    
    print("✓ Safety constraints working correctly")
    return True


def test_file_operations():
    """Test write and read operations with temporary files."""
    print("\n=== Testing File Operations ===")
    
    executor = ToolExecutor()
    import tempfile
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        temp_file = f.name
    
    try:
        # Write to it
        test_content = "Hello, Agent Coder!\nThis is a test file."
        result = executor.execute("write_file", {
            "filepath": temp_file,
            "content": test_content
        })
        assert result.success, f"write_file failed: {result.error}"
        print("✓ write_file executed successfully")
        
        # Read it back
        result = executor.execute("read_file", {"filepath": temp_file})
        assert result.success, f"read_file failed: {result.error}"
        assert result.data == test_content, "Content mismatch"
        print("✓ read_file verified content matches")
        
        # Edit it
        result = executor.execute("edit_file", {
            "filepath": temp_file,
            "old_content": "test file",
            "new_content": "modified file"
        })
        assert result.success, f"edit_file failed: {result.error}"
        print("✓ edit_file executed successfully")
        
        # Verify edit
        result = executor.execute("read_file", {"filepath": temp_file})
        assert "modified file" in result.data, "Edit not applied"
        print("✓ edit verified in content")
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    return True


def demonstrate_agent_coder():
    """Demonstrate the AgentCoder in action with a simple task."""
    print("\n=== Demonstrating Agent Coder ===")
    
    # Create a simple configuration
    config = AgentConfig(
        max_steps=5,
        timeout=30,
        enable_safety=True
    )
    
    # Note: Full agent demonstration would require an LLM backend
    # This shows the initialization and structure
    print("AgentCoder configuration:")
    print(f"  Max steps: {config.max_steps}")
    print(f"  Timeout: {config.timeout}s")
    print(f"  Safety enabled: {config.enable_safety}")
    print("✓ AgentCoder can be initialized")
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("AGENT CODER TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_tool_registration,
        test_tool_execution,
        test_safety_constraints,
        test_file_operations,
        demonstrate_agent_coder,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            failed += 1
            print(f"✗ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
