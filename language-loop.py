#!/usr/bin/env python3
"""Offline, bounded qualification of the controlled language loop; stdlib only.

Run against the exact CLI/HUD bytes being qualified. All mutation stays inside a
fresh temporary world. The JSON receipt distinguishes unavailable from failed.
This does not qualify GF, statistical models, open-domain semantics, or code
equivalence; its named fragment is deliberately narrower.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

EN = "Socrates is human. All humans are mortal."
IT = "Socrate è un uomo. Tutti gli uomini sono mortali."
FORMAL = "Human(socrates); forall x: Human(x) -> Mortal(x)"


def digest(path):
    value = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            value.update(chunk)
    return value.hexdigest()


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--physis", default=shutil.which("physis"))
    parser.add_argument("--hud", default=shutil.which("physis-hud"))
    args = parser.parse_args()
    receipt = {"fragment": "controlled-language-closed-loop/1", "grounded": False,
               "backends": "native controlled grammar; no GF/Z3/model claimed", "checks": []}
    binaries = {}
    for name, candidate in (("physis", args.physis), ("hud", args.hud)):
        if not candidate or not Path(candidate).is_file() or not os.access(candidate, os.X_OK):
            receipt["status"] = "UNVERIFIABLE"
            receipt["reason"] = f"required executable unavailable: {name} ({candidate!r})"
            print(json.dumps(receipt, ensure_ascii=False, indent=2))
            return 2
        binaries[name] = str(Path(candidate).resolve())
    receipt["binaries"] = {name: {"path": path, "sha256": digest(path)} for name, path in binaries.items()}

    with tempfile.TemporaryDirectory(prefix="physis-language-loop-") as directory:
        root = Path(directory)
        env = dict(os.environ, PHYSIS_STORE_DIR=str(root / ".physis-next"),
                   PHYSIS_MCP_SURFACE="area:language", PHYSIS_MCP_COMPACT="0")

        def command(argv, ok=True):
            result = subprocess.run(argv, cwd=root, env=env, text=True,
                                    capture_output=True, timeout=30, check=False)
            require((result.returncode == 0) == ok,
                    f"unexpected exit {result.returncode}: {result.stderr or result.stdout}")
            return result.stdout

        def call(action, source=None, language=None, extra=(), ok=True):
            argv = [binaries["physis"], "--json", "language", "--path", str(root), action]
            if source is not None:
                argv.append(source)
            if language:
                argv += ["--language", language]
            argv += list(extra)
            return json.loads(command(argv, ok))

        def check(name, operation):
            try:
                operation()
            except (AssertionError, ValueError, KeyError, OSError, subprocess.TimeoutExpired) as error:
                receipt["checks"].append({"name": name, "status": "FAIL", "reason": str(error)})
            else:
                receipt["checks"].append({"name": name, "status": "PASS"})

        def oracle():
            atom = {"kind": "atom", "atom": {"predicate": "Human", "term": {"kind": "entity", "id": "socrates"}, "negated": False}}
            rule = {"kind": "for_all", "variable": "v0",
                    "antecedent": {"predicate": "Human", "term": {"kind": "variable", "id": "v0"}, "negated": False},
                    "consequent": {"predicate": "Mortal", "term": {"kind": "variable", "id": "v0"}, "negated": False}}
            ids = []
            for source, language in ((EN, "en"), (IT, "it"), (FORMAL, "formal")):
                result = call("normalize", source, language)
                require(result["normalized"] == [atom, rule], f"{language}: oracle differs")
                require(result["analysis"]["complete"], f"{language}: incomplete")
                ids.append(result["analysis"]["id"])
            require(len(set(ids)) == 3, "source provenance collapsed across languages")
            require(not (root / ".physis-next/observations.jsonl").exists(), "read loop wrote observations")
        check("independent_three_form_oracle_and_read_only", oracle)

        def deduction():
            result = call("infer", FORMAL, "formal")
            require(result["complete"] and not result["grounded"], "wrong inference status")
            require(len(result["proofs"]) == 1, "expected one conditional derivation")
            proof = result["proofs"][0]
            require(proof["conclusion"]["predicate"] == "Mortal", "wrong conclusion")
            require(proof["premise"] and proof["rule"] and proof["substitution"] == {"v0": "socrates"}, "missing proof lineage")
            for source in ("Human(socrates)", "forall x: Human(x) -> Mortal(x)"):
                require(not call("infer", source, "formal")["proofs"], "missing premise still licenses conclusion")
        check("conditional_inference_and_missing_premise_controls", deduction)

        def gaps():
            partial = call("inspect", "Socrates is human. Some humans are mortal.", "en")
            require(not partial["complete"] and partial["diagnostics"], "unsupported syntax silently accepted")
            limited = call("infer", FORMAL, "formal", ("--steps", "1"))
            require(not limited["complete"] and limited["steps"] <= 1, "budget falsely claims fixed point")
            for source in ("All humans are not mortal.", "He is human."):
                require(not call("inspect", source, "en")["complete"], "ambiguous reference/scope guessed")
        check("explicit_semantic_gaps_and_resource_limit", gaps)

        def contradiction():
            result = call("infer", FORMAL + "; not Mortal(socrates)", "formal")
            require(len(result["contradictions"]) == 1, "contradiction absent")
            signs = {fact["negated"] for fact in result["facts"] if fact["predicate"] == "Mortal"}
            require(signs == {False, True}, "one polarity erased")
            require({fact["predicate"] for fact in result["facts"]} == {"Human", "Mortal"}, "contradiction exploded")
        check("contradiction_retention_without_explosion", contradiction)

        def roundtrip():
            lines = call("linearize", FORMAL, "formal", ("--target-language", "it"))["lines"]
            compared = call("compare", FORMAL, extra=("; ".join(lines), "--language-a", "formal", "--language-b", "it"))
            require(compared["status"] == "normalized_equal", "linearization lost meaning")
            reversed_rule = "Human(socrates); forall x: Mortal(x) -> Human(x)"
            different = call("compare", FORMAL, extra=(reversed_rule, "--language-a", "formal", "--language-b", "formal"))
            require(different["status"] == "different", "implication direction erased")
        check("linearization_roundtrip_and_direction_control", roundtrip)

        def lifecycle():
            first = call("ingest", EN, "en")
            source_id = first["record"]["analysis"]["id"]
            proof_id = first["record"]["inference"]["proofs"][0]["id"]
            require(first["observations_added"] == 1, "ingestion did not append")
            require(call("ingest", EN, "en")["observations_added"] == 0, "duplicate ingestion appended")
            require(call("explain", proof_id)["analysis"]["id"] == source_id, "restart lost proof source")
            second = call("ingest", IT, "it")
            second_proof = second["record"]["inference"]["proofs"][0]["id"]
            require(second_proof != proof_id, "proof provenance collapsed")
            require(call("withdraw", source_id)["withdrawn"], "withdrawal failed")
            require(call("explain", proof_id, ok=False)["code"] == "not_found", "withdrawn proof still active")
            require(call("explain", second_proof)["analysis"]["source_language"] == "it", "unrelated active evidence erased")
        check("canonical_ingest_dedupe_restart_and_selective_withdrawal", lifecycle)

        def wire():
            requests = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
                {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
                    "name": "physis.language.infer", "arguments": {"source": EN, "language": "en"}}},
            ]
            result = subprocess.run([binaries["physis"], "serve", "--stdio", "--path", str(root)],
                                    input="".join(json.dumps(r) + "\n" for r in requests),
                                    cwd=root, env=env, text=True, capture_output=True, timeout=30, check=False)
            require(result.returncode == 0, f"MCP transport failed: {result.stderr}")
            replies = {r["id"]: r for r in map(json.loads, result.stdout.splitlines()) if "id" in r}
            names = {t["name"] for t in replies[2]["result"]["tools"]}
            require("physis.language.infer" in names, "language tools absent from area catalogue")
            response = replies[3]["result"]
            require(not response["isError"] and len(response["structuredContent"]["proofs"]) == 1, "wire inference differs")
        check("real_native_mcp_stdio_roundtrip", wire)

        def hud():
            text = command([binaries["hud"], "--snapshot", "--path", str(root), "--view=language:it " + IT])
            require("Mortal(socrates)" in text and "grounded=false" in text and "premise" in text, "HUD loses proof/grounding distinction")
        check("exact_hud_bytes_render_language_evidence", hud)

    receipt["status"] = "PASS" if receipt["checks"] and all(c["status"] == "PASS" for c in receipt["checks"]) else "FAIL"
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
