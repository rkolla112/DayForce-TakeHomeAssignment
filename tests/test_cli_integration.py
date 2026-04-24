import re
import subprocess
import sys


def test_app_starts_logs_department_and_exits_without_api_key(project_root):
    completed = subprocess.run(
        [sys.executable, "app.py"],
        cwd=project_root,
        input="exit\n",
        text=True,
        capture_output=True,
        check=True,
        timeout=10,
    )

    assert re.search(
        r"\[INFO\] Department selected: (Sales|Marketing|Engineering)",
        completed.stdout,
    )
    assert "Ask a question" in completed.stdout
    assert "Goodbye!" in completed.stdout
    assert completed.stderr == ""
