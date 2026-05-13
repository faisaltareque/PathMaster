"""
Tests for pathmaster module.

These tests cover all public functions: add_path, add_parent, and list_files.
Follows TDD principles: tests define expected behavior first.
"""

import os
import sys
import pathlib
import tempfile
import shutil
from unittest import mock

import pytest

from pathmaster import add_path, add_parent, list_files


# ─────────────────────────────────────────────
# Test Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    directory = tempfile.mkdtemp()
    yield directory
    shutil.rmtree(directory)


@pytest.fixture
def populated_dir(temp_dir):
    """Create a temporary directory with some files."""
    for name in ["file1.txt", "file2.py", "file3.md"]:
        filepath = os.path.join(temp_dir, name)
        with open(filepath, "w") as f:
            f.write(f"content of {name}")
    yield temp_dir


@pytest.fixture
def nested_dir(temp_dir):
    """Create a temporary directory with nested subdirectories and files."""
    subdir = os.path.join(temp_dir, "subdir")
    os.makedirs(subdir)
    with open(os.path.join(temp_dir, "root_file.txt"), "w") as f:
        f.write("root")
    with open(os.path.join(subdir, "nested_file.txt"), "w") as f:
        f.write("nested")
    yield temp_dir


# ─────────────────────────────────────────────
# Tests for add_path
# ─────────────────────────────────────────────

class TestAddPath:
    """Tests for the add_path function."""

    def test_add_valid_new_path(self, temp_dir):
        """Adding a new valid path should insert it into sys.path."""
        original_path = sys.path.copy()
        resolved = str(pathlib.Path(temp_dir).resolve())
        add_path(temp_dir)
        assert resolved in sys.path
        # Verify it was inserted at position 0
        assert sys.path[0] == resolved

    def test_add_existing_path_no_duplicate(self, temp_dir):
        """Adding a path that's already in sys.path should not duplicate it."""
        resolved = str(pathlib.Path(temp_dir).resolve())
        add_path(temp_dir)
        add_path(temp_dir)
        count = sys.path.count(resolved)
        assert count == 1

    def test_add_nonexistent_path(self, temp_dir):
        """Adding a non-existent path should not modify sys.path."""
        fake_path = os.path.join(temp_dir, "nonexistent")
        original_path = sys.path.copy()
        add_path(fake_path)
        assert sys.path == original_path

    def test_add_file_not_directory(self, temp_dir):
        """Adding a file (not directory) should not modify sys.path."""
        filepath = os.path.join(temp_dir, "some_file.txt")
        with open(filepath, "w") as f:
            f.write("test")
        original_path = sys.path.copy()
        add_path(filepath)
        assert sys.path == original_path

    def test_add_path_with_relative_input(self, temp_dir):
        """Adding a path with relative input should resolve to absolute."""
        original_path = sys.path.copy()
        add_path(temp_dir)
        # The resolved absolute path should be in sys.path
        resolved = pathlib.Path(temp_dir).resolve()
        assert str(resolved) in sys.path

    def test_add_path_prints_success_message(self, temp_dir):
        """Adding a valid new path should print a success message."""
        with mock.patch("builtins.print") as mock_print:
            add_path(temp_dir)
            mock_print.assert_any_call(
                f"✅ Successfully added '{pathlib.Path(temp_dir).resolve()}' to sys.path."
            )

    def test_add_path_prints_already_exists_message(self, temp_dir):
        """Adding an existing path should print an info message."""
        add_path(temp_dir)  # First add
        with mock.patch("builtins.print") as mock_print:
            add_path(temp_dir)  # Second add
            mock_print.assert_any_call(
                f"ℹ️ Path '{pathlib.Path(temp_dir).resolve()}' is already in sys.path."
            )

    def test_add_path_prints_warning_for_nonexistent(self, temp_dir):
        """Adding a nonexistent path should print a warning message."""
        fake_path = os.path.join(temp_dir, "fake_nonexistent_dir_xyz")
        with mock.patch("builtins.print") as mock_print:
            add_path(fake_path)
            mock_print.assert_any_call(
                f"⚠️ Warning: Path '{pathlib.Path(fake_path).resolve()}' does not exist or is not a directory."
            )


# ─────────────────────────────────────────────
# Tests for add_parent
# ─────────────────────────────────────────────

class TestAddParent:
    """Tests for the add_parent function."""

    def test_add_parent_default(self, temp_dir):
        """add_parent() with default levels=1 should add immediate parent."""
        # Create a subdir inside temp_dir, then add_parent from inside it
        subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(subdir)
        # Change to subdir temporarily
        original_cwd = os.getcwd()
        try:
            os.chdir(subdir)
            add_parent()  # levels=1 by default
            parent_path = str(pathlib.Path(temp_dir).resolve())
            assert parent_path in sys.path
        finally:
            os.chdir(original_cwd)

    def test_add_parent_levels_2(self, temp_dir):
        """add_parent(levels=2) should add grandparent directory."""
        # Create: temp_dir / level1 / level2
        level1 = os.path.join(temp_dir, "level1")
        level2 = os.path.join(level1, "level2")
        os.makedirs(level2)
        original_cwd = os.getcwd()
        try:
            os.chdir(level2)
            add_parent(levels=2)
            parent_path = str(pathlib.Path(temp_dir).resolve())
            assert parent_path in sys.path
        finally:
            os.chdir(original_cwd)

    def test_add_parent_levels_0(self, temp_dir):
        """add_parent(levels=0) should add the current directory."""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            add_parent(levels=0)
            assert str(pathlib.Path(temp_dir).resolve()) in sys.path
        finally:
            os.chdir(original_cwd)

    def test_add_parent_too_many_levels(self, temp_dir):
        """Going up more levels than available should not crash."""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            # Should not raise an exception
            add_parent(levels=100)
        except Exception as e:
            pytest.fail(f"add_parent(levels=100) raised unexpected exception: {e}")
        finally:
            os.chdir(original_cwd)

    def test_add_parent_prints_success(self, temp_dir):
        """Adding a parent should print a success message."""
        subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(subdir)
        original_cwd = os.getcwd()
        try:
            os.chdir(subdir)
            with mock.patch("builtins.print") as mock_print:
                add_parent()
                # Should have printed the success message
                assert any("✅" in str(call) for call in mock_print.call_args_list)
        finally:
            os.chdir(original_cwd)

    def test_add_parent_wont_duplicate(self, temp_dir):
        """Calling add_parent multiple times should not create duplicates."""
        subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(subdir)
        original_cwd = os.getcwd()
        try:
            os.chdir(subdir)
            add_parent()
            add_parent()
            add_parent()
            parent_path = str(pathlib.Path(temp_dir).resolve())
            count = sys.path.count(parent_path)
            assert count == 1
        finally:
            os.chdir(original_cwd)


# ─────────────────────────────────────────────
# Tests for list_files
# ─────────────────────────────────────────────

class TestListFiles:
    """Tests for the list_files function."""

    def test_list_files_returns_list(self, populated_dir):
        """list_files should return a list."""
        result = list_files(populated_dir)
        assert isinstance(result, list)

    def test_list_files_files_count(self, populated_dir):
        """list_files should return all files in the directory."""
        result = list_files(populated_dir)
        assert len(result) == 3

    def test_list_files_returns_filenames_only(self, populated_dir):
        """By default, list_files should return just filenames (not paths)."""
        result = list_files(populated_dir)
        for item in result:
            assert "/" not in item and "\\" not in item

    def test_list_files_filenames_are_strings(self, populated_dir):
        """list_files should return a list of strings."""
        result = list_files(populated_dir)
        assert all(isinstance(f, str) for f in result)

    def test_list_files_includes_specific_file(self, populated_dir):
        """list_files should include specific files we created."""
        result = list_files(populated_dir)
        assert "file1.txt" in result
        assert "file2.py" in result
        assert "file3.md" in result

    def test_list_files_excludes_subdirectories(self, nested_dir):
        """list_files should not include subdirectories."""
        result = list_files(nested_dir)
        assert "subdir" not in result

    def test_list_files_absolute_path(self, populated_dir):
        """list_files(absolute_path=True) should return full paths."""
        result = list_files(populated_dir, absolute_path=True)
        for item in result:
            assert pathlib.Path(item).is_absolute()
            assert pathlib.Path(item).exists()

    def test_list_files_absolute_path_count(self, populated_dir):
        """list_files with absolute_path=True should return same count."""
        result = list_files(populated_dir, absolute_path=True)
        assert len(result) == 3

    def test_list_files_relative_vs_absolute(self, populated_dir):
        """Relative and absolute results should reference same files."""
        relative = set(list_files(populated_dir, absolute_path=False))
        absolute = list_files(populated_dir, absolute_path=True)
        absolute_filenames = {pathlib.Path(p).name for p in absolute}
        assert relative == absolute_filenames

    def test_list_files_nonexistent_directory(self, temp_dir):
        """list_files for a nonexistent directory should return empty list."""
        fake_dir = os.path.join(temp_dir, "does_not_exist_xyz")
        result = list_files(fake_dir)
        assert result == []

    def test_list_files_is_file_not_directory(self, temp_dir):
        """list_files given a file path should return empty list."""
        filepath = os.path.join(temp_dir, "a_file.txt")
        with open(filepath, "w") as f:
            f.write("test")
        result = list_files(filepath)
        assert result == []

    def test_list_files_empty_directory(self, temp_dir):
        """list_files on empty directory should return empty list."""
        result = list_files(temp_dir)
        assert result == []

    def test_list_files_prints_warning_for_invalid(self, temp_dir):
        """list_files for invalid path should print a warning."""
        fake_dir = os.path.join(temp_dir, "not_a_dir_xyz")
        with mock.patch("builtins.print") as mock_print:
            list_files(fake_dir)
            mock_print.assert_any_call(
                f"⚠️ Warning: '{fake_dir}' is not a valid directory."
            )

    def test_list_files_sorted_not_required(self, populated_dir):
        """list_files does not guarantee ordering (relies on filesystem order)."""
        # This is a negative test — we just verify we get the right count
        # without asserting order (order is filesystem-dependent)
        result = list_files(populated_dir)
        assert len(result) == 3


# ─────────────────────────────────────────────
# Integration Tests
# ─────────────────────────────────────────────

class TestIntegration:
    """Integration tests that exercise multiple functions together."""

    def test_add_path_and_list_files(self, temp_dir):
        """Adding a path and then listing files from it."""
        # Create a file in temp_dir
        test_file = os.path.join(temp_dir, "integration_test.txt")
        with open(test_file, "w") as f:
            f.write("integration")
        
        add_path(temp_dir)
        files = list_files(temp_dir)
        assert "integration_test.txt" in files

    def test_add_parent_and_list_files(self, temp_dir):
        """Adding parent directory and then listing files."""
        # Create: temp_dir / subdir / subsubdir
        subsubdir = os.path.join(temp_dir, "subdir", "subsubdir")
        os.makedirs(subsubdir)
        test_file = os.path.join(temp_dir, "parent_file.txt")
        with open(test_file, "w") as f:
            f.write("parent")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(subsubdir)
            add_parent(levels=2)
            parent_path = str(pathlib.Path(temp_dir).resolve())
            assert parent_path in sys.path
            files = list_files(temp_dir)
            assert "parent_file.txt" in files
        finally:
            os.chdir(original_cwd)
