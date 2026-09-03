#!/usr/bin/env python3
"""Guard the clean-room env contract in run_evals.py and run_triggers.py.

The eval result is only honest if nothing from the host shell leaks into the
subprocess. Both scripts carry their own build_case_env (they are
deliberately self-contained); this test pins the contract on both copies:
exactly PATH + fresh HOME + auth-var-only-when-set +
declared passthrough keys, nothing else.
Run with: uv run --with pytest -m pytest test_env_isolation.py
(or plain `uv run test_env_isolation.py` for a lightweight self-check).
"""
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import run_evals  # noqa: E402
import run_triggers  # noqa: E402

BUILDERS = [run_evals.build_case_env, run_triggers.build_case_env]

HOST_ENV = {
    "PATH": "/usr/bin:/bin",
    "HOME": "/Users/host",
    "RUNTIME_AUTH_TOKEN": "test-token-123",
    "AWS_SECRET_ACCESS_KEY": "host-secret-must-not-leak",
    "EXTRA_VAR": "extra",
}

HOME = Path("/tmp/eval-case/.home")


def test_minimal_env_keys():
    adapter = {"auth_env": "RUNTIME_AUTH_TOKEN"}
    for build in BUILDERS:
        env = build(adapter, HOME, HOST_ENV)
        assert set(env) == {"PATH", "HOME", "RUNTIME_AUTH_TOKEN"}, (build.__module__, env)
        assert env["PATH"] == HOST_ENV["PATH"]
        assert env["HOME"] == str(HOME), "HOME must be the fresh case home"
        assert env["RUNTIME_AUTH_TOKEN"] == "test-token-123"
        assert "AWS_SECRET_ACCESS_KEY" not in env, "host secrets leaked"


def test_auth_var_absent_when_unset():
    # Setting auth to "" breaks the runtime's OAuth fallback — the key must
    # be absent, never empty.
    adapter = {"auth_env": "RUNTIME_AUTH_TOKEN"}
    for host in ({}, {"RUNTIME_AUTH_TOKEN": ""}):
        for build in BUILDERS:
            env = build(adapter, HOME, {"PATH": "/bin", **host})
            assert "RUNTIME_AUTH_TOKEN" not in env, (build.__module__, env)


def test_no_adapter_still_minimal():
    for build in BUILDERS:
        env = build(None, HOME, HOST_ENV)
        assert set(env) == {"PATH", "HOME"}, env


def test_env_passthrough_only_declared_and_present():
    adapter = {"auth_env": "RUNTIME_AUTH_TOKEN",
               "env_passthrough": ["EXTRA_VAR", "NOT_SET_ON_HOST"]}
    for build in BUILDERS:
        env = build(adapter, HOME, HOST_ENV)
        assert env.get("EXTRA_VAR") == "extra"
        assert "NOT_SET_ON_HOST" not in env
        assert "AWS_SECRET_ACCESS_KEY" not in env


if __name__ == "__main__":
    test_minimal_env_keys()
    test_auth_var_absent_when_unset()
    test_no_adapter_still_minimal()
    test_env_passthrough_only_declared_and_present()
    print("ok: build_case_env contract holds in run_evals and run_triggers")
