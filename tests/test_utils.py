import os
from streamlit_examples.utils.streamlit import cache_files
from streamlit.runtime.uploaded_file_manager import (
    UploadedFile,
    UploadedFileRec,
    FileURLsProto,
)


def create_file(name, test_data):
    file_id = f"{name}_file_id"
    type = "text/plain"
    record = UploadedFileRec(file_id=file_id, name=name, type=type, data=test_data)
    file_urls = FileURLsProto()
    return UploadedFile(record=record, file_urls=file_urls)


def test_cache_file():
    tc = [
        {
            "test": "test one file",
            "files": [create_file("test.pdf", b"test content")],
            "expected": [b"test content"],
        },
        {
            "test": "test two files",
            "files": [
                create_file("test.pdf", b"test content"),
                create_file("test2.pdf", b"test content 2"),
            ],
            "expected": [b"test content", b"test content 2"],
        },
    ]

    for test in tc:
        filepaths = cache_files(test["files"])
        assert len(filepaths) == len(test["files"])
        for i in range(len(filepaths)):
            assert os.path.exists(filepaths[i])
            with open(filepaths[i], "rb") as f:
                assert f.read() == test["expected"][i]
            os.remove(filepaths[i])
