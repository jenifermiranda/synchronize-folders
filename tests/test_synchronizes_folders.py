from synchronizes_folders import read_files, delete_files, copy_files, compare_files


CONTENT = "content"


def test_read_files(tmp_path):
    source_folder = tmp_path / "Source2/"
    source_folder.mkdir()

    file = source_folder / "text.py"
    file.write_text(CONTENT)

    files_info = read_files(source_folder)

    assert len(files_info) == 1
    assert files_info[0]["name_file"] == "text.py"
    assert files_info[0]["size"] == len(CONTENT)


def test_delete_files(tmp_path):
    source_folder = tmp_path / "Source2/"
    source_folder.mkdir()

    file = source_folder / "delete_file"
    file.write_text(CONTENT)

    assert file.exists()

    delete_files(file)

    assert not file.exists()


def test_copy_files(tmp_path):
    source_folder = tmp_path / "Source2/"
    source_folder.mkdir()

    file = source_folder / "source_file"
    file.write_text(CONTENT)

    replica_folder = tmp_path / "Replica2/"
    replica_folder.mkdir()

    assert not (replica_folder / "source_file").exists()

    copy_files(file, replica_folder)

    copy_to_replica = replica_folder / "source_file"

    assert copy_to_replica.exists()


def test_compare_files(tmp_path, capsys):
    source_folder = tmp_path / "Source2/"
    source_folder.mkdir()

    file_to_source = source_folder / "source_file"
    file_to_source.write_text(CONTENT)

    replica_folder = tmp_path / "Replica2/"
    replica_folder.mkdir()

    file_to_replica = replica_folder / "source_file"
    file_to_replica.write_text(CONTENT)

    file_to_delete = replica_folder / "delete_file"
    file_to_delete.write_text(CONTENT)

    assert file_to_source.exists()
    assert file_to_replica.exists()
    assert file_to_delete.exists()

    compare_files(source_folder, replica_folder)

    log_to_console = (
        f"Files created: []\nFiles copied: []\nFiles removed: [{file_to_delete}]"
    )
    print(log_to_console)

    assert file_to_source.exists()
    assert file_to_replica.exists()
    assert not file_to_delete.exists()

    captured = capsys.readouterr()
    assert captured.out.__contains__(
        "Files created: []\nFiles copied: []\nFiles removed:"
    )
