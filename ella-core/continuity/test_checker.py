"""Deterministic tests for the continuity checker. Stdlib only.

Run from ella-core/continuity/:
    python3 -m unittest -v test_checker
(pytest also collects this file: python3 -m pytest -q test_checker.py)
"""
import builtins
import copy
import json
import socket
import unittest
from pathlib import Path
from unittest import mock

import checker

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
ZWNJ = "\u200c"


def load(name):
    path = next(FIXTURES.glob(f"{name}_*.json"))
    return json.loads(path.read_text(encoding="utf-8"))


def run(fixture):
    rep = checker.assemble(fixture, FIXTURES)
    return rep, checker.compare(rep, fixture["expected"])


def by_id(fixture, rid):
    return next(r for r in fixture["records"] if r["id"] == rid)


class FixturePack(unittest.TestCase):
    def test_every_fixture_passes(self):
        paths = sorted(FIXTURES.glob("*.json"))
        self.assertGreaterEqual(len(paths), 15)
        for path in paths:
            with self.subTest(fixture=path.name):
                _, fails = checker.run_fixture(path)
                self.assertEqual(fails, [])

    def test_fixtures_are_synthetic_and_record_text_is_qalam_clean(self):
        for path in sorted(FIXTURES.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(fixture=path.name):
                self.assertIs(data["synthetic"], True)
                for rec in data["records"]:
                    self.assertNotIn(ZWNJ, rec["content"])
                    self.assertTrue(all(ZWNJ not in t for t in rec["topics"]))
                    self.assertTrue(rec["provenance"]["source_ref"].startswith("fixture://")
                                    if "provenance" in rec else True)

    def test_each_fixture_declares_forbidden_conclusions(self):
        for path in sorted(FIXTURES.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(fixture=path.name):
                self.assertTrue(data["expected"].get("forbidden"))

    def test_example_manifest_is_valid(self):
        m = json.loads((HERE / "manifest.example.json").read_text(encoding="utf-8"))
        self.assertEqual(checker.validate_manifest(m), [])

    def test_deterministic(self):
        for path in sorted(FIXTURES.glob("*.json")):
            a, _ = checker.run_fixture(path)
            b, _ = checker.run_fixture(path)
            self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

    def test_non_synthetic_fixture_is_refused(self):
        path = next(FIXTURES.glob("F01_*.json"))
        data = json.loads(path.read_text(encoding="utf-8"))
        data["synthetic"] = False
        with mock.patch.object(checker, "load_json", return_value=data):
            rep, fails = checker.run_fixture(path)
        self.assertIsNone(rep)
        self.assertTrue(fails)


class SideEffects(unittest.TestCase):
    def test_no_network_and_no_writes(self):
        real_open = builtins.open

        def read_only_open(file, mode="r", *args, **kwargs):
            if any(flag in mode for flag in "wax+"):
                raise AssertionError(f"checker tried to write {file}")
            return real_open(file, mode, *args, **kwargs)

        def no_net(*args, **kwargs):
            raise AssertionError("checker tried to open a network connection")

        before = {p: p.stat().st_mtime_ns for p in HERE.rglob("*") if p.is_file()}
        with mock.patch("builtins.open", read_only_open), \
                mock.patch.object(socket, "socket", no_net), \
                mock.patch.object(socket, "create_connection", no_net):
            for path in sorted(FIXTURES.glob("*.json")):
                checker.run_fixture(path)
        after = {p: p.stat().st_mtime_ns for p in HERE.rglob("*") if p.is_file()}
        self.assertEqual({k: v for k, v in before.items() if "__pycache__" not in str(k)},
                         {k: v for k, v in after.items() if "__pycache__" not in str(k)})


class MutationsMustBite(unittest.TestCase):
    """Each mutation changes one input. The original expectations must then fail,
    and the new report must show the contract-correct behavior."""

    def test_lower_authority_correction_does_not_win(self):
        fx = load("F04")
        by_id(fx, "core:correction-recoverable")["authority"] = "ella_inferred"
        rep, fails = run(fx)
        self.assertTrue(fails)
        self.assertEqual(rep["applied"], {"status:fx-task-7": "epi:claim-blocked-terminal"})
        self.assertIn(("supersession_lacks_authority",
                       ("core:correction-recoverable", "epi:claim-blocked-terminal")),
                      [(u["type"], tuple(u["ids"])) for u in rep["unresolved"]])

    def test_equal_authority_slot_conflict_applies_neither(self):
        fx = load("F10")
        by_id(fx, "nb:infer-date-fa")["authority"] = "owner_approved"
        fx["observed"]["authority_attestations"]["nb:infer-date-fa"] = "owner_approved"  # attested, not self-claimed
        rep, _ = run(fx)
        self.assertNotIn("pref:date_format", rep["applied"])
        self.assertEqual({s["role"] for s in rep["selected"]}, {"contested"})

    def test_prior_receipt_never_counts_as_current(self):
        fx = load("F03")
        fx["observed"].pop("fresh_checks")
        fx["observed"]["boot_id"] = "fx-boot-0001"  # even the same boot ID
        rep, _ = run(fx)
        self.assertEqual(rep["capabilities"]["account:ella"], "unverified_requires_fresh_check")
        self.assertFalse(rep["environment_ready"])
        self.assertTrue(all(p["counts_as_current"] is False for p in rep["prior_receipts"]))

    def test_environment_ready_only_when_every_check_passes_now(self):
        fx = load("F02")
        caps = [c["capability"] for c in checker.resolve_manifest(fx["manifest"], FIXTURES)["environment_checks"]]
        fx["observed"]["fresh_checks"] = {c: True for c in caps}
        rep, _ = run(fx)
        self.assertTrue(rep["environment_ready"])
        fx["observed"]["fresh_checks"][caps[0]] = False
        rep, _ = run(fx)
        self.assertFalse(rep["environment_ready"])

    def test_fresh_index_still_yields_to_authoritative_record(self):
        fx = load("F14")
        by_id(fx, "idx:tea-summary")["derived_from"]["sha256"] = "sha256:fx-core-r13"
        rep, _ = run(fx)
        self.assertEqual([s["id"] for s in rep["selected"]], ["core:pref-tea-v2"])
        self.assertIn(("idx:tea-summary", "authoritative_preferred"),
                      [(o["id"], o["reason"]) for o in rep["omitted"]])

    def test_valid_unexpired_approval_is_history_not_authority(self):
        fx = load("F07")
        by_id(fx, "epi:approval-push-02")["approval"]["env_binding"]["boot_id"] = "fx-boot-0002"
        rep, _ = run(fx)
        sel = {s["id"]: s for s in rep["selected"]}
        self.assertEqual(sel["epi:approval-push-02"]["label"], "historical_authorization_receipt")
        self.assertEqual(rep["authority_from_memory"], [])

    def test_uninspected_evidence_stays_reported(self):
        fx = load("F05")
        by_id(fx, "epi:report-tp-with-evidence")["provenance"]["evidence"][0]["inspected"] = False
        rep, fails = run(fx)
        self.assertTrue(fails)
        sel = {s["id"]: s for s in rep["selected"]}
        self.assertEqual(sel["epi:report-tp-with-evidence"]["label"], "reported_unverified")

    def test_relabelled_simulation_is_caught(self):
        fx = load("F11")
        by_id(fx, "epi:body-sim-01")["reality"] = "observed"
        _, fails = run(fx)
        self.assertTrue(any("forbidden" in f for f in fails))

    def test_missing_source_records_cannot_appear(self):
        fx = load("F06")
        fx["records"].append({**copy.deepcopy(fx["records"][0]), "id": "ppl:ghost", "store": "people",
                              "source_id": "src:people", "topics": ["tea"]})
        rep, _ = run(fx)
        self.assertIn(("ppl:ghost", "source_missing"), [(o["id"], o["reason"]) for o in rep["omitted"]])

    def test_tampered_expectation_is_detected(self):
        fx = load("F01")
        fx["expected"]["selected"].append("nb:note-weather")
        _, fails = run(fx)
        self.assertTrue(fails)


def omitted(rep):
    return [(o["id"], o["reason"]) for o in rep["omitted"]]


def unresolved(rep):
    return [(u["type"], tuple(u["ids"])) for u in rep["unresolved"]]


class AuthorityIsNotSelfAsserted(unittest.TestCase):
    """Review finding 1: a record must not gain priority by labelling itself."""

    def test_self_labelled_owner_approval_does_not_win(self):
        fx = load("F10")
        by_id(fx, "nb:infer-date-fa")["authority"] = "owner_approved"  # claim only
        rep, _ = run(fx)
        self.assertEqual(rep["applied"], {"pref:date_format": "core:pref-date-fa-v2"})
        sel = {s["id"]: s for s in rep["selected"]}
        self.assertEqual(sel["nb:infer-date-fa"]["authority"], "ella_inferred")
        self.assertEqual(sel["nb:infer-date-fa"]["claimed_authority"], "owner_approved")

    def test_unattested_record_cannot_supersede(self):
        fx = load("F04")
        del fx["observed"]["authority_attestations"]["core:correction-recoverable"]
        rep, fails = run(fx)
        self.assertTrue(fails)
        self.assertNotIn("core:correction-recoverable", rep["applied"].values())
        self.assertIn(("supersession_lacks_authority",
                       ("core:correction-recoverable", "epi:claim-blocked-terminal")), unresolved(rep))
        sel = {s["id"]: s for s in rep["selected"]}
        self.assertIn("authority_unattested", sel["core:correction-recoverable"]["flags"])

    def test_attestation_can_lower_but_never_raise_a_claim(self):
        fx = load("F04")
        fx["observed"]["authority_attestations"]["epi:claim-blocked-terminal"] = "owner_approved"
        rep, _ = run(fx)
        self.assertEqual(rep["applied"], {"status:fx-task-7": "core:correction-recoverable"})

    def test_every_report_declares_the_trust_boundary(self):
        for path in sorted(FIXTURES.glob("*.json")):
            rep, _ = checker.run_fixture(path)
            with self.subTest(fixture=path.name):
                self.assertEqual(rep["trust"]["live_memory_use"], "not_permitted")


class ChangedSourcesAreNotSilentlyTrusted(unittest.TestCase):
    """Review finding 2: a hash mismatch needs reconciliation or an accepted revision."""

    def test_unaccepted_change_holds_records_back(self):
        fx = load("F14")
        del fx["observed"]["accepted_revisions"]
        rep, fails = run(fx)
        self.assertTrue(fails)
        self.assertEqual(rep["selected"], [])
        self.assertIn(("core:pref-tea-v2", "source_changed_unreconciled"), omitted(rep))
        self.assertIn(("source_revision_unreconciled", ("src:core",)), unresolved(rep))
        self.assertIn("src:core", [g["source_id"] for g in rep["gaps"]])
        status = {i["id"]: i["status"] for i in rep["integrity"]}
        self.assertEqual(status["src:core"], "changed_unreconciled")

    def test_accepted_revision_must_name_the_observed_hash(self):
        fx = load("F14")
        fx["observed"]["accepted_revisions"]["src:core"] = "sha256:fx-core-r99"
        rep, _ = run(fx)
        self.assertIn(("core:pref-tea-v2", "source_changed_unreconciled"), omitted(rep))

    def test_accepted_revision_is_reported_as_such(self):
        rep, fails = run(load("F14"))
        self.assertEqual(fails, [])
        self.assertEqual({i["id"]: i["status"] for i in rep["integrity"]}["src:core"], "accepted_revision")


class BudgetAndIdentityValidation(unittest.TestCase):
    """Review finding 3: negative tests."""

    def test_bad_record_token_counts_are_rejected(self):
        for bad in (-5, 0, True, False, 2.5, "20", None):
            fx = load("F01")
            by_id(fx, "core:pref-tea")["tokens"] = bad
            rep, _ = run(fx)
            with self.subTest(tokens=bad):
                self.assertIn(("core:pref-tea", "invalid_record"), omitted(rep))
                self.assertNotIn("core:pref-tea", [s["id"] for s in rep["selected"]])
                self.assertGreaterEqual(rep["tokens_used"], 0)

    def test_tokens_of_refuses_bad_values(self):
        for bad in (-1, True):
            with self.subTest(tokens=bad), self.assertRaises(ValueError):
                checker.tokens_of({"tokens": bad, "content": "x"})

    def test_negative_tokens_cannot_buy_budget(self):
        fx = load("F13a")
        fx["records"][0]["tokens"] = -100000
        rep, _ = run(fx)
        self.assertIn((fx["records"][0]["id"], "invalid_record"), omitted(rep))
        self.assertLessEqual(rep["tokens_used"],
                             checker.resolve_manifest(fx["manifest"], FIXTURES)["context_budget_tokens"])

    def test_bad_profile_tokens_and_budget_in_manifest(self):
        m = json.loads((HERE / "manifest.example.json").read_text(encoding="utf-8"))
        for bad in (-300, True, 0):
            mm = copy.deepcopy(m)
            mm["profiles"][0]["tokens"] = bad
            mm["context_budget_tokens"] = True if bad is True else mm["context_budget_tokens"]
            errs = checker.validate_manifest(mm)
            with self.subTest(tokens=bad):
                self.assertTrue(any(e.startswith("bad_profile_tokens") for e in errs))
                if bad is True:
                    self.assertIn("bad_budget", errs)

    def test_duplicate_record_ids_select_neither_copy(self):
        fx = load("F01")
        twin = copy.deepcopy(by_id(fx, "core:pref-tea"))
        twin["content"] = "Synthetic: a different body under the same ID."
        fx["records"].append(twin)
        rep, fails = run(fx)
        self.assertTrue(fails)
        self.assertNotIn("core:pref-tea", [s["id"] for s in rep["selected"]])
        self.assertEqual(omitted(rep).count(("core:pref-tea", "duplicate_record_id")), 2)
        self.assertIn(("duplicate_record_id", ("core:pref-tea",)), unresolved(rep))

    def test_record_store_must_match_registered_source_store(self):
        fx = load("F01")
        by_id(fx, "core:pref-tea")["store"] = "people"  # source src:core is registered as core
        rep, _ = run(fx)
        self.assertIn(("core:pref-tea", "store_source_mismatch"), omitted(rep))

    def test_equal_authority_two_way_cycle_resolves_nothing(self):
        fx = load("F10")
        by_id(fx, "core:pref-date-fa-v1")["supersedes"] = ["core:pref-date-fa-v2"]
        rep, fails = run(fx)
        self.assertTrue(fails)
        ids = {s["id"]: s for s in rep["selected"]}
        self.assertIn("core:pref-date-fa-v1", ids)
        self.assertIn("core:pref-date-fa-v2", ids)
        self.assertEqual(ids["core:pref-date-fa-v1"]["role"], "contested")
        self.assertNotIn("pref:date_format", rep["applied"])
        self.assertIn(("supersession_cycle", ("core:pref-date-fa-v1", "core:pref-date-fa-v2")), unresolved(rep))
        self.assertFalse(any(h["accepted"] for h in rep["correction_history"]))

    def test_equal_authority_three_way_cycle_resolves_nothing(self):
        fx = load("F10")
        nb = by_id(fx, "nb:infer-date-fa")
        nb["authority"] = "owner_approved"
        fx["observed"]["authority_attestations"]["nb:infer-date-fa"] = "owner_approved"
        by_id(fx, "core:pref-date-fa-v1")["supersedes"] = ["nb:infer-date-fa"]
        nb["supersedes"] = ["core:pref-date-fa-v2"]
        rep, _ = run(fx)
        self.assertEqual(len(rep["selected"]), 3)
        self.assertIn(("supersession_cycle", ("core:pref-date-fa-v1", "core:pref-date-fa-v2", "nb:infer-date-fa")),
                      unresolved(rep))
        self.assertEqual(rep["applied"], {})

    def test_unequal_cycle_keeps_the_higher_authority_correction(self):
        fx = load("F04")
        by_id(fx, "epi:claim-blocked-terminal")["supersedes"] = ["core:correction-recoverable"]
        rep, _ = run(fx)
        self.assertEqual(rep["applied"], {"status:fx-task-7": "core:correction-recoverable"})
        self.assertNotIn("supersession_cycle", [u["type"] for u in rep["unresolved"]])


class ManifestRules(unittest.TestCase):
    def base(self):
        return json.loads((HERE / "manifest.example.json").read_text(encoding="utf-8"))

    def test_missing_field(self):
        m = self.base()
        del m["privacy"]
        self.assertIn("missing_field:privacy", checker.validate_manifest(m))

    def test_derived_index_cannot_be_authoritative(self):
        m = self.base()
        m["derived_indexes"][0]["authoritative"] = True
        self.assertTrue(any(e.startswith("derived_index_claims_authority") for e in checker.validate_manifest(m)))

    def test_p0_must_never_drop(self):
        m = self.base()
        m["load_order"][0]["never_drop"] = False
        self.assertIn("p0_must_be_never_drop", checker.validate_manifest(m))

    def test_key_material_value(self):
        m = self.base()
        m["unresolved_questions"][0]["question"] = "-----BEGIN RSA PRIVATE KEY-----"
        self.assertTrue(any(e.startswith("key_material") for e in checker.validate_manifest(m)))


class Normalization(unittest.TestCase):
    def test_persian_forms(self):
        self.assertEqual(checker.norm("تاريخ\u200cها"), "تاریخ ها")
        self.assertEqual(checker.norm("كتاب ۱۲۳ ٤٥"), "کتاب 123 45")
        self.assertEqual(checker.norm("  Tea  "), "tea")

    def test_bilingual_equivalents(self):
        eq = checker.Equivalents({"date_format": ["date", "تاریخ"]})
        self.assertIn("date", eq.expand("تاريخ\u200cها"))


if __name__ == "__main__":
    unittest.main()
