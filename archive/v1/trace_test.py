#!/usr/bin/env python3
"""Trace execution to find where the error occurs."""

import sys
import traceback

sys.stderr = sys.stdout  # Redirect stderr to stdout

print("Step 1: Starting test")

try:
    print("Step 2: Importing asyncio")
    import asyncio
    print("Step 3: Imported asyncio")
    
    print("Step 4: Setting up mocks")
    from unittest.mock import Mock, AsyncMock
    
    mock_driver = Mock()
    mock_driver.verify_connectivity = AsyncMock(return_value=None)
    mock_driver.close = AsyncMock(return_value=None)
    
    mock_session = Mock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    mock_driver.session = Mock(return_value=mock_session)
    
    mock_result = Mock()
    mock_result.consume = AsyncMock(return_value=None)
    
    async def mock_run(query, **kwargs):
        mock_result.single = AsyncMock(return_value={"count": 0})
        mock_result.data = AsyncMock(return_value=[])
        return mock_result
    
    mock_session.run = mock_run
    
    mock_neo4j = Mock()
    mock_neo4j.AsyncGraphDatabase = Mock()
    mock_neo4j.AsyncGraphDatabase.driver = Mock(return_value=mock_driver)
    sys.modules['neo4j'] = mock_neo4j
    print("Step 5: Mocks ready")
    
    print("Step 6: Importing graph_connectivity")
    from graph_connectivity import GraphConnectivity
    print("Step 7: GraphConnectivity imported")
    
    print("Step 8: Creating instance")
    config = {
        "neo4j_uri": "bolt://localhost:7687",
        "neo4j_user": "neo4j",
        "neo4j_password": "password"
    }
    connectivity = GraphConnectivity(config)
    print("Step 9: Instance created")
    
    print("Step 10: Running async connect")
    async def test():
        status = await connectivity.connect()
        print(f"Step 11: Connected = {status.is_connected}")
        return status
    
    result = asyncio.run(test())
    print(f"Step 12: Test complete, connected={result.is_connected}")
    
    print("\nSUCCESS: All steps completed!")
    
except Exception as e:
    print(f"ERROR at step: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
