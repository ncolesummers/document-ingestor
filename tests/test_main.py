from document_ingestor import main


def test_main_output(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from document-ingestor!" in captured.out
