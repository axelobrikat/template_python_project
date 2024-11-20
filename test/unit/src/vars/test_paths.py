from src.vars.paths import ROOT

def test_ROOT():
    """test that ROOT path ends with project's name
    """
    assert str(ROOT).endswith("template_python_project")
