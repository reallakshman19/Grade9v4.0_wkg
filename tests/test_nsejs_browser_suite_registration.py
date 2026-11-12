"""Guard mandatory Chromium-only suite without allowing a false-green pytest run."""
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]
CHROMIUM = ROOT / ".github/workflows/nsejs-wpe-parity-runtime.yml"
JOINT = ROOT / ".github/workflows/nsejs-wave2-joint-http.yml"
CASES = (
    ROOT / "browser_tests/test_nsejs_wpe_runtime_browser.py",
    ROOT / "browser_tests/test_nsejs_wpe_real_pilot_browser.py",
)


def test_browser_tests_have_dedicated_executable_ci_with_real_chromium():
    joint = JOINT.read_text("utf-8")
    runtime = CHROMIUM.read_text("utf-8")
    assert "python -m playwright install chromium" in joint
    assert "python -m playwright install chromium" in runtime
    assert "python -m pytest -v browser_tests/test_nsejs_wpe_runtime_browser.py browser_tests/test_nsejs_wpe_real_pilot_browser.py" in joint
    assert "python -m pytest -v browser_tests/test_nsejs_wpe_runtime_browser.py" in runtime
    for path in CASES:
        assert path.is_file()
        assert path.relative_to(ROOT).as_posix() in joint


def test_standard_qa_remains_unfiltered_and_chromium_is_separately_required():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text("utf-8"))
    assert project["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]
    workflow = (ROOT / ".github/workflows/qa.yml").read_text("utf-8")
    assert "qa_reproducibility.py run" in workflow
    assert "pytest_args" not in workflow
    assert "run: python -m pytest -q\n" not in workflow
    for path in CASES:
        code = path.read_text("utf-8")
        assert "from playwright.sync_api import sync_playwright" in code
        assert "pytest.skip(" not in code
        assert "pytest.mark.skip" not in code
        assert "pytest.mark.xfail" not in code
