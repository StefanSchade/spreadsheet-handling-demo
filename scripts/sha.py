import subprocess
def current_sha(short=True):
    args = ["git", "rev-parse", "--short", "HEAD"] if short else ["git", "rev-parse", "HEAD"]
    return subprocess.check_output(args, text=True).strip()
