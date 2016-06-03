from .context import event_client


def test_file_logging(tmpdir):
    file_path = str(tmpdir.join("hello.txt").realpath())

    ev = event_client.EventsLogger(file_path)
    ev.emit("test")
    ev.emit("test")

    assert open(file_path).read() == "test\ntest\n"
