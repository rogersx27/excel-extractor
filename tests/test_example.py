"""Tests de ejemplo."""
import pytest


def test_example():
    """Test de ejemplo básico."""
    assert 1 + 1 == 2


def test_example_with_fixture(tmp_path):
    """Test de ejemplo usando fixture de pytest."""
    # tmp_path es un directorio temporal proporcionado por pytest
    test_file = tmp_path / "test.txt"
    test_file.write_text("contenido de prueba")

    assert test_file.read_text() == "contenido de prueba"


class TestExample:
    """Clase de tests de ejemplo."""

    def test_method_example(self):
        """Test method de ejemplo."""
        result = "hello".upper()
        assert result == "HELLO"

    def test_another_example(self):
        """Otro test de ejemplo."""
        my_list = [1, 2, 3]
        assert len(my_list) == 3
        assert 2 in my_list
