#!/usr/bin/env python3
"""Thin client for Coohom's (the product the user's request spelled
"Cohoom") Open API / B2B render service — https://open.coohom.com/ .

Coohom's Open Platform is partner-gated: endpoint paths, the signing
scheme, and the exact request/response fields are only published to
approved partners at https://developer.coohom.com/reference after you
apply at https://www.coohom.com/b2b/api. This module intentionally does
NOT hardcode endpoint paths it cannot verify — instead it reads them from
a small JSON config the partner fills in from their own onboarding docs,
and it enforces the one structural detail Coohom documents publicly on
https://www.coohom.com/helpcenter/api-design-standard : every response is
wrapped as {"c": <int>, "result": <payload>, "count"/"totalCount"/"hasMore"
for lists}, where c == 0 means success.

Usage:
    python coohom_client.py status --config coohom_endpoints.json
    python coohom_client.py call create_design --config coohom_endpoints.json --body '{"name": "living-room"}'

Config file shape (fill in from your partner API reference):
{
  "base_url": "https://<issued-by-coohom>",
  "app_key": "env:COOHOM_APP_KEY",
  "app_secret": "env:COOHOM_APP_SECRET",
  "endpoints": {
    "sso": "/path/from/your/partner/docs",
    "create_design": "/path/from/your/partner/docs",
    "upload_model": "/path/from/your/partner/docs",
    "start_render": "/path/from/your/partner/docs",
    "get_render_status": "/path/from/your/partner/docs"
  }
}
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


class CoohomConfigError(Exception):
    pass


def _resolve(value):
    """Allow config values like 'env:COOHOM_APP_KEY' to pull from the environment
    instead of putting secrets in a checked-in JSON file."""
    if isinstance(value, str) and value.startswith("env:"):
        var = value[4:]
        resolved = os.environ.get(var)
        if not resolved:
            raise CoohomConfigError(f"Config references ${var} but it is not set in the environment.")
        return resolved
    return value


def load_config(path):
    if not os.path.isfile(path):
        raise CoohomConfigError(
            f"Config file not found: {path}. Coohom's Open API is partner-gated — apply for access at "
            "https://www.coohom.com/b2b/api, then copy the real base_url and endpoint paths from "
            "https://developer.coohom.com/reference into a config with this module's shape (see --help)."
        )
    with open(path) as fh:
        cfg = json.load(fh)
    for required in ("base_url", "endpoints"):
        if required not in cfg:
            raise CoohomConfigError(f"Config is missing required key: {required}")
    return cfg


def status(config_path):
    try:
        cfg = load_config(config_path)
    except CoohomConfigError as exc:
        return {"configured": False, "reason": str(exc)}
    missing_creds = [k for k in ("app_key", "app_secret") if not cfg.get(k)]
    unset_endpoints = [name for name, path in cfg["endpoints"].items() if not path or "your/partner/docs" in path]
    return {
        "configured": not missing_creds and not unset_endpoints,
        "base_url": cfg["base_url"],
        "missing_credentials": missing_creds,
        "unfilled_endpoints": unset_endpoints,
    }


def call(config_path, endpoint_name, body=None, method="POST"):
    cfg = load_config(config_path)
    if endpoint_name not in cfg["endpoints"]:
        raise CoohomConfigError(
            f"Unknown endpoint '{endpoint_name}'. Known keys in config: {list(cfg['endpoints'])}"
        )
    path = cfg["endpoints"][endpoint_name]
    if not path or "your/partner/docs" in path:
        raise CoohomConfigError(
            f"Endpoint '{endpoint_name}' has not been filled in with a real path from your Coohom partner docs."
        )

    url = cfg["base_url"].rstrip("/") + path
    app_key = _resolve(cfg.get("app_key"))
    app_secret = _resolve(cfg.get("app_secret"))
    if not app_key or not app_secret:
        raise CoohomConfigError(
            "app_key/app_secret are not set. Coohom SSO/signing requires credentials issued during partner "
            "onboarding — see https://developer.coohom.com/reference for the exact signing scheme, then set "
            "COOHOM_APP_KEY / COOHOM_APP_SECRET in the environment."
        )

    payload = json.dumps(body or {}).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        # NOTE: Coohom's actual auth header name/signing algorithm is defined
        # in the partner-only reference. Replace this placeholder header with
        # whatever your partner docs specify before relying on this in production.
        "X-Coohom-App-Key": app_key,
    }
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        return {"ok": False, "http_status": exc.code, "body": exc.read().decode(errors="replace")}
    except urllib.error.URLError as exc:
        return {"ok": False, "error": str(exc.reason)}

    # Coohom's documented envelope: {"c": 0-success/other-error, "result": ...}
    ok = raw.get("c") == 0
    return {"ok": ok, "code": raw.get("c"), "result": raw.get("result"), "raw": raw}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status", help="Check whether the Coohom config/credentials are filled in")
    p_status.add_argument("--config", required=True)

    p_call = sub.add_parser("call", help="Call a configured Coohom endpoint")
    p_call.add_argument("endpoint")
    p_call.add_argument("--config", required=True)
    p_call.add_argument("--body", default="{}", help="JSON request body")
    p_call.add_argument("--method", default="POST")

    args = parser.parse_args()
    try:
        if args.command == "status":
            print(json.dumps(status(args.config), indent=2))
        elif args.command == "call":
            body = json.loads(args.body)
            print(json.dumps(call(args.config, args.endpoint, body, args.method), indent=2))
    except CoohomConfigError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
