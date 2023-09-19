from optimalrotas.schedule import get_project_name_for_display, PROJECT_NAME_LEN_CHARS


def test_get_project_name_for_display_short():
    test_name = "10 chrlong"
    assert len(get_project_name_for_display(test_name)) == PROJECT_NAME_LEN_CHARS


def test_get_project_name_for_display_exact():
    test_name = "20 characters long i"
    assert len(get_project_name_for_display(test_name)) == PROJECT_NAME_LEN_CHARS


def test_get_project_name_for_display_long():
    test_name = "i'm 30 characters long exactly"
    assert len(get_project_name_for_display(test_name)) == PROJECT_NAME_LEN_CHARS