"""Small opt-in OpenCode V2 runtime probe; no real model or personal config.

Usage: python3 tests/plan_permission_probe.py --opencode /absolute/path/to/opencode
Artifacts remain under work/agent-artifacts/pkg03/probe-*/ in this source copy.
"""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading


REPO = Path(__file__).resolve().parents[1]


class Fixture(BaseHTTPRequestHandler):
    """Only fixed tool calls: this is not a reasoning/model-quality test."""

    def log_message(self, *_):
        pass  # Never log headers or requests.

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        tools = {t["function"]["name"]: t["function"] for t in body.get("tools", [])}
        self.server.schemas.update(tools)
        results = sum(m.get("role") == "tool" for m in body.get("messages", []))
        if results < 2 and "read" in tools and self.server.tool_name in tools:
            tool = "read" if results == 0 else self.server.tool_name
            arguments = {"path": self.server.target}
            if tool == "edit":
                arguments.update(oldString="before", newString="after")
            elif tool == "write":
                arguments.update(content="after\n")
            if results == 1:
                self.server.calls += 1
            delta = {"role": "assistant", "tool_calls": [{
                "index": 0, "id": "call_fixture_" + str(results), "type": "function",
                "function": {"name": tool, "arguments": json.dumps(arguments)},
            }]}
            finish = "tool_calls"
        else:
            delta = {"role": "assistant", "content": "Synthetic fixture complete."}
            finish = "stop"
        chunks = [
            {"id": "fixture", "object": "chat.completion.chunk", "model": "fixture",
             "choices": [{"index": 0, "delta": delta, "finish_reason": None}]},
            {"id": "fixture", "object": "chat.completion.chunk", "model": "fixture",
             "choices": [{"index": 0, "delta": {}, "finish_reason": finish}],
             "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}},
        ]
        data = "".join("data: " + json.dumps(c) + "\n\n" for c in chunks)
        data += "data: [DONE]\n\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(data.encode())))
        self.end_headers()
        self.wfile.write(data.encode())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--opencode", required=True, type=Path)
    args = parser.parse_args()
    binary = args.opencode.resolve(strict=True)
    artifacts = REPO / "work/agent-artifacts/pkg03"
    artifacts.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="probe-", dir=artifacts))
    project = root / "project"
    config = root / "config/opencode"
    (config / "agents").mkdir(parents=True)
    project.mkdir()
    shutil.copyfile(REPO / "agents/Plan.md", config / "agents/Plan.md")
    # Deliberate allowlist, not a copy or dump of the process environment.
    env = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "HOME": str(root / "home"),
           "XDG_CONFIG_HOME": str(root / "config"), "XDG_CACHE_HOME": str(root / "cache"),
           "XDG_STATE_HOME": str(root / "state"), "XDG_DATA_HOME": str(root / "data"),
           "OPENCODE_CONFIG_DIR": str(config)}
    Path(env["HOME"]).mkdir()
    version = subprocess.run([str(binary), "--version"], env=env, cwd=project,
                             capture_output=True, text=True, timeout=15)
    assert version.returncode == 0, "version command failed"
    report = {"version": version.stdout.strip(), "artifact_root": str(root), "cases": []}
    server = ThreadingHTTPServer(("127.0.0.1", 0), Fixture)
    server.schemas = {}
    server.calls = 0
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    config_data = {
        "model": "fixture/fixed",
        "providers": {"fixture": {
            "name": "Local deterministic permission fixture", "env": [],
            "package": "@opencode/ai/providers/openai-compatible",
            "settings": {"baseURL": "http://127.0.0.1:" + str(server.server_port) + "/v1",
                         "apiKey": "synthetic-fixture-not-a-credential"},
            "models": {"fixed": {"name": "Fixed tool calls", "capabilities": {"tools": True}}},
        }},
    }
    (config / "opencode.json").write_text(json.dumps(config_data))
    allowed = ["docs/planning/tickets/task.md", "docs/planning/architecture/nested/design.md",
               "docs/planning/implementation/hints.md"]
    blocked = ["src/product.py", "README.md", "docs/planning/other.md",
               "docs/planning/tickets/config.json"]
    cases = [("allow-" + str(i), p, "edit", True) for i, p in enumerate(allowed)]
    cases += [("deny-" + str(i), p, "edit", False) for i, p in enumerate(blocked)]
    cases += [("allow-write", allowed[0], "write", True),
              ("deny-write", blocked[0], "write", False),
              ("deny-traversal", "docs/planning/tickets/../../../src/product.py", "edit", False),
              ("deny-absolute", str(project / blocked[0]), "edit", False)]
    try:
        for name, target, tool_name, permitted in cases:
            for p in allowed + blocked:
                path = project / p
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("before\n")
            server.target = target
            server.tool_name = tool_name
            calls_before = server.calls
            result = subprocess.run(
                [str(binary), "run", "--standalone", "--auto", "--agent", "Plan",
                 "--model", "fixture/fixed", "--format", "json",
                 "Synthetic permission probe: " + name],
                env=env, cwd=project, capture_output=True, text=True, timeout=60,
            )
            (root / (name + ".stdout.jsonl")).write_text(result.stdout)
            (root / (name + ".stderr.txt")).write_text(result.stderr)
            (root / "tool-schemas.json").write_text(json.dumps(server.schemas, indent=2))
            changed = [p for p in allowed + blocked if (project / p).read_text() != "before\n"]
            case = {"name": name, "exit": result.returncode, "tool_calls": server.calls - calls_before,
                    "tool": tool_name, "target": target,
                    "changed": changed, "expected": [target] if permitted else []}
            report["cases"].append(case)
            (root / "report.json").write_text(json.dumps(report, indent=2))
            assert result.returncode == 0, name + ": CLI failed; see " + str(root)
            assert case["tool_calls"] == 1, name + ": fixture tool not executed; see " + str(root)
            assert changed == case["expected"], name + ": wrong mutations; see " + str(root)
            for p in allowed + blocked:
                expected = "after\n" if p in case["expected"] else "before\n"
                assert (project / p).read_text() == expected, name + ": wrong file contents"
            if not permitted:
                states = [e["part"]["state"] for e in map(json.loads, result.stdout.splitlines())
                          if e.get("type") == "tool_use" and e["part"]["tool"] == tool_name]
                assert any(s.get("error") == "Permission denied: edit" for s in states), (
                    name + ": missing explicit edit-permission denial evidence"
                )
            print(name + ": PASS")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    print("Runtime permission probe passed; no real model behavior tested.")
    print("Evidence: " + str(root / "report.json"))


if __name__ == "__main__":
    main()
