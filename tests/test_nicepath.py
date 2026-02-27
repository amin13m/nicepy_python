# tests/test_nicepath_full.py
import pytest
from nicepy.nicepath.core import NicePath
from nicepy.nicepath.exceptios import PathNotFoundError, NotAFileError
from pathlib import Path

@pytest.fixture
def temp_dir(tmp_path):
    """Fixture for a temporary NicePath directory"""
    return NicePath(tmp_path)

def test_file_operations(temp_dir):
    # Write
    file = temp_dir / "test.txt"
    file.write("Hello World")
    assert file.exists
    assert file.is_file
    assert file.read() == "Hello World"

    # Append
    file.append("!!!")
    assert file.read() == "Hello World!!!"

    # Parent
    assert file.parent.exists
    assert file.parent.is_dir

    # Size
    assert file.size > 0

def test_mkdir_and_delete(temp_dir):
    folder = temp_dir / "folder"
    folder.mkdir()
    assert folder.exists
    assert folder.is_dir

    folder.delete()
    assert not folder.exists

def test_copy_and_move(temp_dir):
    src = temp_dir / "source.txt"
    src.write("Copy Me")
    dest = temp_dir / "dest.txt"

    # Copy
    src.copy_to(dest)
    assert dest.exists
    assert dest.read() == "Copy Me"
    assert src.exists  # original still exists

    # Move
    moved = src.move_to(temp_dir / "moved.txt")
    assert moved.exists
    assert not src.exists

def test_tree_and_search(temp_dir):
    # Create files
    (temp_dir / "a.txt").write("a")
    (temp_dir / "b.log").write("b")
    (temp_dir / "sub").mkdir()
    (temp_dir / "sub" / "c.txt").write("c")

    tree_output = temp_dir.tree()
    assert "a.txt" in tree_output
    assert "sub" in tree_output
    assert "c.txt" in tree_output

    # Search by suffix
    results = temp_dir.search(suffix=".txt")
    assert len(results) == 2
    for f in results:
        assert f.suffix == ".txt"

    # Search by name_contains
    results2 = temp_dir.search(name_contains="b")
    assert any("b.log" in str(f.path) for f in results2)

def test_properties(temp_dir):
    file = temp_dir / "file.txt"
    file.write("data")
    assert file.name == "file.txt"
    assert file.stem == "file"
    assert file.suffix == ".txt"
    assert file.parent.exists
    assert file.is_file
    assert not file.is_dir
    assert file.size > 0
    assert file.created_at
    assert file.modified_at

def test_errors(temp_dir):
    non_file = temp_dir / "folder"
    non_file.mkdir()
    with pytest.raises(NotAFileError):
        non_file.read()

    missing = temp_dir / "missing.txt"
    with pytest.raises(PathNotFoundError):
        missing.read()

def test_logAll(temp_dir):
    file = temp_dir / "logall.txt"
    (temp_dir / "x.txt").write("x")
    (temp_dir / "y.txt").write("y")

    output = temp_dir.logAll(file_output=file, search_suffix=".txt")
    # The file should now exist and contain both tree and search results
    assert file.exists
    text = file.read()
    assert "Tree Structure" in text
    assert "Search Results" in text
    assert "x.txt" in text
    assert "y.txt" in text



# -------------------------
# Tree and Search
# -------------------------
def test_tree_and_search(temp_dir):
    # Setup multiple files
    (temp_dir / "apple.py").write("a")
    (temp_dir / "banana.txt").write("b")
    (temp_dir / "cherry.py").write("c")
    (temp_dir / "venv" / "ignore.py").write("ignore")  # should be ignored

    # Tree
    tree_str = temp_dir.tree()
    assert "apple.py" in tree_str
    assert "banana.txt" in tree_str

    # Search by suffix
    py_files = temp_dir.search(suffix=".py")
    assert all(f.suffix == ".py" for f in py_files)
    assert any(f.name == "apple.py" for f in py_files)

# -------------------------
# logAll with safety limits
# -------------------------
def test_logAll_safety(temp_dir):
    # Create many files
    for i in range(600):
        (temp_dir / f"file{i}.txt").write(f"content {i}")

    output_file = temp_dir / "log.txt"
    log_text = temp_dir.logAll(
        file_output=output_file,
        search_suffix=".txt",
        max_files=500,             # safety limit
        max_total_size=10_000_000, # 10 MB
    )

    # Check file created
    assert output_file.exists
    assert "file0.txt" in log_text
    assert "Safety Limit" in log_text

# -------------------------
# copy, move, delete
# -------------------------
def test_copy_move_delete(temp_dir):
    file = temp_dir / "original.txt"
    file.write("data")

    # Copy
    copy_file = temp_dir / "copy.txt"
    file.copy_to(copy_file)
    assert copy_file.exists
    assert copy_file.read() == "data"

    # Move
    moved_file = temp_dir / "moved.txt"
    file.move_to(moved_file)
    assert not file.exists
    assert moved_file.exists
    assert moved_file.read() == "data"

    # Delete
    moved_file.delete()
    assert not moved_file.exists

# -------------------------
# Error handling
# -------------------------
def test_errors(temp_dir):
    missing = temp_dir / "missing.txt"
    with pytest.raises(PathNotFoundError):
        missing.read()

    with pytest.raises(NotAFileError):
        temp_dir.read()

# -------------------------
# Operator overloads
# -------------------------
def test_operator_overloads(temp_dir):
    new_file = temp_dir / "operator.txt"
    new_file.write("op")

    assert isinstance(temp_dir / "operator.txt", NicePath)
    assert (temp_dir / "operator.txt").read() == "op"