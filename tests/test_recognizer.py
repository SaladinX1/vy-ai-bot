from vision import recognizer

def test_extract_text():
    text = recognizer.extract_text_from_image("images/sample.png")
    assert isinstance(text, str)

def test_detect_element():
    found = recognizer.detect_element("images/sample.png", "Connexion")
    assert isinstance(found, bool)