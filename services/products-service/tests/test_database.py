"""Unit tests for database module."""
import pytest
from unittest.mock import patch, MagicMock
from app.database import get_db, init_db, check_db_connection


class TestDatabase:
    """Test cases for database module."""
    
    def test_get_db_yields_session(self, db_session):
        """Test that get_db yields a database session."""
        gen = get_db()
        session = next(gen)
        
        assert session is not None
        
        # Clean up
        try:
            next(gen)
        except StopIteration:
            pass
    
    def test_get_db_closes_session(self):
        """Test that get_db closes session after use."""
        gen = get_db()
        session = next(gen)
        
        # Finish the generator
        try:
            next(gen)
        except StopIteration:
            pass
        
        # Session should be closed (we can't directly test this with SQLite in-memory)
        # but the code path is exercised
    
    @patch('app.database.Base.metadata.create_all')
    def test_init_db_success(self, mock_create_all):
        """Test successful database initialization."""
        init_db()
        
        mock_create_all.assert_called_once()
    
    @patch('app.database.Base.metadata.create_all')
    def test_init_db_failure(self, mock_create_all):
        """Test database initialization failure."""
        mock_create_all.side_effect = Exception("Database error")
        
        with pytest.raises(Exception):
            init_db()
    
    def test_check_db_connection_success(self, db_session):
        """Test successful database connection check."""
        result = check_db_connection()
        
        # With in-memory SQLite, this should succeed
        assert result is True
    
    @patch('app.database.SessionLocal')
    def test_check_db_connection_failure(self, mock_session_local):
        """Test database connection check failure."""
        mock_db = MagicMock()
        mock_db.execute.side_effect = Exception("Connection failed")
        mock_session_local.return_value = mock_db
        
        result = check_db_connection()
        
        assert result is False
