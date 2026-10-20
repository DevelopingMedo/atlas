#!/usr/bin/env python3
"""Langdock setup for OpenCode v2.0.27; Python 3.9+, standard library only.

Run manually: python3 install_langdock.py (Windows: py install_langdock.py).
Requires an installed OpenCode V2. Never reads or overwrites an existing .env.
"""

import copy
import getpass
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import warnings


BEGIN = "# >>> OpenCode Langdock >>>"
END = "# <<< OpenCode Langdock <<<"
API = "https://api.langdock.com"
PACKAGE = "@opencode/ai/providers/"
SECRET_RULE = """## Langdock: Secret-Schutz

Für alle Agents: .env und .env.* niemals lesen, durchsuchen, ausgeben, kopieren
oder committen, auch nicht über Shell, Skripte oder Subagents. API-Keys niemals
in Chat, Logs oder Werkzeugausgaben ausgeben. Keine Umgebungs-/Prozess-Dumps
und kein Shell-Tracing bei der Verwendung von Secrets. Diese Regel an alle
Subagents weitergeben. Nur die vom Nutzer eingerichteten Shell-Loader dürfen
.env zum Laden von LANGDOCK_API_KEY verwenden; Agents verwenden ausschließlich
die Umgebungsvariable zur Authentifizierung gegen https://api.langdock.com.
OpenCode bezieht den Key per {env:LANGDOCK_API_KEY}, nie als Klartext in JSON.
Den OpenCode-Dienst niemals aus einer seiner Agent-Sitzungen neu starten.
Read-Policies sind kein Sandbox-Schutz gegen beliebige Shell-Zugriffe.
"""


class SetupError(Exception):
    """A deliberately secret-free, user-facing error."""


def providers():
    """Snapshot of the 18 configured models; no credentials or local MCPs."""
    openai = {
        "gpt-6-luna": "GPT-6 Luna",
        "gpt-6.1-sol": "GPT-6.1 Sol",
        "gpt-6-astra": "GPT-6 Astra",
        "langdock-llama-3.3-70b-2": "Llama 3.3 70B",
        "mistral-large-4-0": "Mistral Large 4.0",
        "mistral-large-2512": "Mistral Large 2512",
    }
    claude = {
        "claude-sonnet-5": "Claude Sonnet 5",
        "claude-sonnet-5-default": "Claude Sonnet 5 Default",
        "claude-sonnet-5-5-default": "Claude Sonnet 5.5 Default",
        "claude-opus-5": "Claude Opus 5",
        "claude-opus-5-default": "Claude Opus 5 Default",
        "claude-opus-5-5": "Claude Opus 5.5",
        "claude-opus-5-5-default": "Claude Opus 5.5 Default",
        "claude-opus-4-8": "Claude Opus 4.8",
        "claude-opus-4-8-default": "Claude Opus 4.8 Default",
        "claude-haiku-5-5": "Claude Haiku 5.5",
    }
    google = {"gemini-4-argon": "Gemini 4 Argon", "gemini-3.8-flash": "Gemini 3.8 Flash"}
    result = {}
    for pid, name, package, endpoint, models in (
        ("langdock", "Langdock", "openai-compatible", "/openai/eu/v1", openai),
        ("langdock-anthropic", "Langdock Anthropic", "anthropic", "/anthropic/eu/v1", claude),
        ("langdock-google", "Langdock Google", "google", "/google/eu/v1beta", google),
    ):
        result[pid] = {
            "name": name, "env": ["LANGDOCK_API_KEY"], "package": PACKAGE + package,
            "settings": {"baseURL": API + endpoint, "apiKey": "{env:LANGDOCK_API_KEY}"},
            "models": {mid: {"name": label} for mid, label in models.items()},
        }
    for mid, model in result["langdock"]["models"].items():
        if mid.startswith("gpt-"):
            model.update(package=PACKAGE + "openai-compatible/responses", settings={"store": False})
    result["langdock"]["models"]["langdock-llama-3.3-70b-2"]["capabilities"] = {"input": ["text"]}
    return result


def parse_config(text):
    # Keep JSON strings intact while removing JSONC comments and trailing commas.
    text = re.sub(r'"(?:\\.|[^"\\])*"|//[^\r\n]*|/\*[\s\S]*?\*/',
                  lambda m: m[0] if m[0].startswith('"') else " ", text)
    text = re.sub(r'"(?:\\.|[^"\\])*"|,\s*(?=[}\]])',
                  lambda m: m[0] if m[0].startswith('"') else "", text)
    value = json.loads(text.lstrip("\ufeff"))
    if not isinstance(value, dict) or "provider" in value:
        raise SetupError("Eine native V2-Konfiguration mit 'providers' wird benötigt.")
    return value


def merge_config(existing):
    config = copy.deepcopy(existing)
    config.setdefault("$schema", "https://opencode.ai/config.json")
    target = config.setdefault("providers", {})
    for pid, definition in providers().items():
        if pid in target and target[pid] != definition:
            raise SetupError("Bestehender Provider-Konflikt: " + pid + "; keine Änderung vorgenommen.")
        target[pid] = definition
    for field, action, prefix in (("permissions", "read", ""), ("policies", "tool.use", "read:")):
        owner = config if field == "permissions" else config.setdefault("experimental", {})
        rules = owner.setdefault(field, [])
        for pattern in ("*.env", "*.env.*"):
            rule = {"action": action, "resource": prefix + pattern, "effect": "deny"}
            rules[:] = [item for item in rules if item != rule] + [rule]
    return config


def read_regular(path):
    # This helper is never called for .env or any .env.* file.
    if path.name == ".env" or ".env." in path.name or path.name.endswith(".env"):
        raise SetupError("Secret-Dateien werden nicht gelesen.")
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise SetupError("Symlink oder nicht reguläre Zieldatei: " + str(path))
    if not path.exists():
        return None
    raw = path.read_bytes()
    return raw.decode("utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")


def block(text, content):
    text = text or ""
    if BEGIN in text or END in text:
        if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(BEGIN) > text.index(END):
            raise SetupError("Ungültiger Langdock-Markerblock; bitte zuerst manuell bereinigen.")
        start, stop = text.index(BEGIN), text.index(END) + len(END)
        return text[:start] + BEGIN + "\n" + content.rstrip() + "\n" + END + text[stop:]
    return text.rstrip("\n") + "\n\n" + BEGIN + "\n" + content.rstrip() + "\n" + END + "\n"


def ps_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def powershell(executable, command):
    result = subprocess.run(
        [executable, "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", command],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", timeout=30,
    )
    if result.returncode:
        raise SetupError("PowerShell-Schritt fehlgeschlagen; keine Secret-Ausgabe erfolgt.")
    return result.stdout.strip()


def shell_targets(home, secret, windows):
    if windows:
        executables = list(dict.fromkeys(filter(None, (shutil.which("powershell.exe"), shutil.which("pwsh.exe")))))
        if not executables:
            raise SetupError("PowerShell wurde nicht gefunden.")
        loader = f"""# Parse only the installer-owned assignment; never execute .env as PowerShell.
Set-PSDebug -Off
if (Test-Path -LiteralPath {ps_quote(secret)}) {{
    $ldValue = [IO.File]::ReadAllText({ps_quote(secret)}).Trim()
    if ($ldValue -match "^LANGDOCK_API_KEY='([A-Za-z0-9._~+/=-]+)'$") {{
        $env:LANGDOCK_API_KEY = $Matches[1]
    }}
    Remove-Variable ldValue, Matches -ErrorAction SilentlyContinue
}}"""
        paths = [Path(powershell(exe, "[Console]::OutputEncoding = [Text.UTF8Encoding]::new(); $PROFILE.CurrentUserAllHosts"))
                 for exe in executables]
        if any(not p.is_absolute() for p in paths):
            raise SetupError("PowerShell-Profilpfad konnte nicht ermittelt werden.")
        return {p: loader for p in paths}, executables[0]
    quoted = shlex.quote(str(secret))
    loader = f"""# Do not load secrets while shell tracing is enabled.
case $- in
  *x*) ;;
  *) if [ -r {quoted} ]; then
       . {quoted}
       export LANGDOCK_API_KEY
     fi ;;
esac"""
    login = next((home / p for p in (".bash_profile", ".bash_login", ".profile") if (home / p).exists()), home / ".profile")
    zdir = Path(os.environ.get("ZDOTDIR") or home).expanduser()
    return {p: loader for p in (home / ".bashrc", login, zdir / ".zshrc")}, None


def protect_windows(path, executable):
    powershell(executable, f"""$ErrorActionPreference = 'Stop'
$sid = [Security.Principal.WindowsIdentity]::GetCurrent().User
$acl = [Security.AccessControl.FileSecurity]::new()
$acl.SetOwner($sid)
$acl.SetAccessRuleProtection($true, $false)
$acl.AddAccessRule([Security.AccessControl.FileSystemAccessRule]::new($sid, 'FullControl', 'Allow'))
Set-Acl -LiteralPath {ps_quote(path)} -AclObject $acl""")


def create_secret(path, key, windows=False, executable=None):
    if not re.fullmatch(r"[A-Za-z0-9._~+/=-]+", key):
        raise SetupError("Der API-Key ist leer oder enthält unerlaubte Zeichen.")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        if windows:
            protect_windows(path, executable)  # Empty file first, then restrictive ACL, then key.
        else:
            os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            fd = None
            stream.write("LANGDOCK_API_KEY='" + key + "'\n")
    except BaseException:
        if fd is not None:
            os.close(fd)
        path.unlink(missing_ok=True)
        raise


def save(path, text, mode=0o600, executable=None, encoding="utf-8"):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".langdock-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding=encoding, newline="\n") as stream:
            if executable:
                protect_windows(Path(temporary), executable)
            stream.write(text)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def verify_opencode():
    executable = shutil.which("opencode")
    if not executable:
        raise SetupError("Bitte zuerst OpenCode V2 installieren und in PATH verfügbar machen.")
    result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=15)
    if result.returncode or not re.search(r"\bv?2\.\d+\.\d+\b", result.stdout):
        raise SetupError("OpenCode V2 wird benötigt; --version konnte V2 nicht bestätigen.")


def install(home=None, windows=None):
    home = home or Path.home()
    windows = os.name == "nt" if windows is None else windows
    config_dir = Path(os.environ.get("OPENCODE_CONFIG_DIR") or
                      Path(os.environ.get("XDG_CONFIG_HOME") or home / ".config") / "opencode").expanduser().absolute()
    secret = config_dir / ".env"
    if secret.exists() or secret.is_symlink():
        raise SetupError(".env existiert bereits. Sie wird weder gelesen noch überschrieben.")
    verify_opencode()
    configs = [p for p in (config_dir / "opencode.json", config_dir / "opencode.jsonc") if p.exists() or p.is_symlink()]
    if len(configs) > 1:
        raise SetupError("opencode.json und opencode.jsonc existieren beide; bitte zuerst zusammenführen.")
    config_path = configs[0] if configs else config_dir / "opencode.json"
    old = read_regular(config_path)
    updated = merge_config(parse_config(old) if old is not None else {})
    targets, executable = shell_targets(home, secret, windows)
    plan = {config_path: (old, json.dumps(updated, indent=2, ensure_ascii=False) + "\n")}
    targets[config_dir / "AGENTS.md"] = SECRET_RULE
    for path, content in targets.items():
        previous = read_regular(path)
        plan[path] = (previous, block(previous, content))
    ignore = config_dir / ".gitignore"
    previous = read_regular(ignore)
    plan[ignore] = (previous, block(previous, ".env\n.env.*\n*.langdock.bak"))
    for path, (previous, _) in plan.items():
        if previous is not None and (path.with_name(path.name + ".langdock.bak").exists() or
                                     path.with_name(path.name + ".langdock.bak").is_symlink()):
            raise SetupError("Ein .langdock.bak-Backup existiert bereits; bitte zuerst manuell sichern.")
    print("Langdock: 18 Modelle für OpenCode V2. Bestehende andere Provider, MCPs und Agents bleiben erhalten.")
    with warnings.catch_warnings():
        warnings.simplefilter("error", getpass.GetPassWarning)
        key = getpass.getpass("Langdock API-Key (verdeckt): ")
    config_dir.mkdir(parents=True, exist_ok=True)
    create_secret(secret, key, windows, executable)
    del key
    try:
        for path, (previous, updated_text) in plan.items():
            mode = stat.S_IMODE(path.stat().st_mode) if previous is not None else 0o600
            encoding = "utf-8-sig" if windows and path.suffix == ".ps1" else "utf-8"
            if previous is not None:
                save(path.with_name(path.name + ".langdock.bak"), previous, executable=executable, encoding=encoding)
            save(path, updated_text, mode, executable, encoding)
    except BaseException:
        # Preserve .env; reruns must never overwrite it. Backups allow manual recovery.
        raise SetupError("Setup unvollständig. Bereits ersetzte Dateien sind als *.langdock.bak gesichert; .env bleibt geschützt.") from None
    print("Installiert. API-Key nur in .env; keine Dienst-Neustarts ausgeführt.")
    print("Neue " + ("PowerShell" if windows else "Bash/Zsh") + " öffnen, dann: opencode service restart")
    print("Anschließend OpenCode öffnen und /models verwenden. Neustart NICHT in einer Agent-Sitzung ausführen.")
    if windows:
        print("Windows: gilt für PowerShell, nicht CMD. Falls die lokale ExecutionPolicy Profile blockiert, muss der Nutzer diese freigeben.")


if __name__ == "__main__":
    try:
        install()
    except SetupError as error:
        print("Abbruch: " + str(error), file=sys.stderr)
        sys.exit(1)
    except (getpass.GetPassWarning, EOFError, KeyboardInterrupt):
        print("Abbruch: verdeckte Eingabe in einem interaktiven Terminal erforderlich.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as error:
        print(f"Abbruch: ungültiges JSON/JSONC in Zeile {error.lineno}, Spalte {error.colno}.", file=sys.stderr)
        sys.exit(1)
    except Exception:
        # No traceback, locals, key, or subprocess output in error messages.
        print("Setup abgebrochen. Keine Secrets ausgegeben. Voraussetzung: OpenCode V2, keine bestehende .env, keine widersprüchlichen Provider/Backups und beschreibbare Dateien.", file=sys.stderr)
        sys.exit(1)
