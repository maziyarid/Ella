"""Verifier tests. All keys are generated here, in temporary directories, and discarded; all records are invented.
The user's keyring is never used: every gpg call gets an explicit temporary --homedir."""
import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

import attest_verify as av

GPG = shutil.which("gpg")
NOW = datetime(2026, 11, 4, 0, 0, 0, tzinfo=timezone.utc)
H1 = av.sha(b'{"id":"core:pref-tea","content":"invented"}')
H2 = av.sha(b'{"id":"core:pref-tea","content":"invented, corrected"}')
H3 = av.sha(b'{"id":"ppl:p-001","content":"invented person"}')


def entry(seq, action="approve", record_id="core:pref-tea", source_id="src:core", h=H1, **kw):
    e = {"seq": seq, "action": action, "record_id": record_id, "source_id": source_id, "record_sha256": h,
         "decision_ref": f"D-synthetic-{seq}", "issued_at": "2026-11-01T00:00:00Z"}
    if action != "withdraw":
        e["authority"] = "owner_approved"
    e.update(kw)
    return e


def reg(*entries) -> bytes:
    return b"".join(json.dumps(e, sort_keys=True).encode() + b"\n" for e in entries)


ANCHOR0 = {"latest_seq": 0, "prefix_sha256": av.sha(b"")}


class Keys:
    """Disposable keys in a private temporary home directory."""

    def __init__(self):
        self.home = tempfile.mkdtemp(prefix="ella-test-keys-")
        os.chmod(self.home, 0o700)
        self.base = [GPG, "--homedir", self.home, "--batch", "--no-tty", "--pinentry-mode", "loopback",
                     "--passphrase", ""]

    def run(self, *args, check=True):
        return subprocess.run(self.base + list(args), capture_output=True, check=check, timeout=60)

    def fpr_of(self, uid):
        out = self.run("--with-colons", "--list-keys", uid).stdout.decode().splitlines()
        return [ln.split(":")[9] for ln in out if ln.startswith("fpr:")][0]

    def gen(self, uid, usage="sign", expire="0", faked=None):
        extra = ["--faked-system-time", faked] if faked else []
        self.run(*extra, "--quick-gen-key", uid, "ed25519", usage, expire)
        return self.fpr_of(uid)

    def add_sign_subkey(self, fpr):
        self.run("--quick-add-key", fpr, "ed25519", "sign", "0")

    def export(self, fpr):
        return self.run("--export", fpr).stdout

    def sign(self, fpr, data, faked=None, armor=False, clearsign=False):
        d = Path(self.home) / "data.bin"
        s = Path(self.home) / "data.sig"
        d.write_bytes(data)
        if s.exists():
            s.unlink()
        extra = ["--faked-system-time", faked] if faked else []
        mode = ["--clearsign"] if clearsign else ["--detach-sign"]
        self.run(*extra, "--local-user", fpr,
                 *(["--armor"] if armor else []), "--output", str(s), *mode, str(d))
        return s.read_bytes()

    def close(self):
        subprocess.run(["gpgconf", "--homedir", self.home, "--kill", "all"], capture_output=True)
        shutil.rmtree(self.home, ignore_errors=True)


@unittest.skipIf(GPG is None, "gpg not installed; the tooling-missing tests below still run")
class SignatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = Keys()
        cls.owner = cls.k.gen("Synthetic Owner <owner@example.invalid>")
        cls.other = cls.k.gen("Synthetic Other <other@example.invalid>")
        cls.sub_primary = cls.k.gen("Synthetic Subkey Owner <sub@example.invalid>", usage="cert")
        cls.k.add_sign_subkey(cls.sub_primary)
        cls.expired = cls.k.gen("Synthetic Expired <exp@example.invalid>", expire="1d", faked="20200101T000000")
        cls.owner_pub = cls.k.export(cls.owner)
        cls.both_pub = cls.k.export(cls.owner) + cls.k.export(cls.other)

    @classmethod
    def tearDownClass(cls):
        cls.k.close()

    def verify(self, data, sig, pub=None, fpr=None, anchor=ANCHOR0, **kw):
        return av.verify_register(data, sig, self.owner_pub if pub is None else pub,
                                  self.owner if fpr is None else fpr, anchor, NOW, **kw)

    # --- signer and signature
    def test_trusted_signer_verified(self):
        data = reg(entry(1))
        r = self.verify(data, self.k.sign(self.owner, data))
        self.assertEqual(r["status"], "verified", r)
        self.assertEqual(r["signer_primary_fpr"], self.owner)
        self.assertEqual(av.owner_authority(r, "src:core", "core:pref-tea", H1), ("owner_approved", "ok"))

    def test_valid_signature_from_other_key_is_not_owner(self):
        data = reg(entry(1))
        sig = self.k.sign(self.other, data)
        r = self.verify(data, sig, pub=self.both_pub)          # the key is present and the signature is valid
        self.assertEqual((r["status"], r["reason"]), ("refused", "untrusted_signer"))
        self.assertEqual(av.owner_authority(r, "src:core", "core:pref-tea", H1)[0], None)

    def test_trusted_fpr_configured_but_signer_key_not_supplied(self):
        data = reg(entry(1))
        r = self.verify(data, self.k.sign(self.other, data))   # only the owner's public key is supplied
        self.assertEqual(r["status"], "refused")
        self.assertTrue(r["reason"].startswith("verification_failed"), r["reason"])

    def test_trusted_fpr_points_at_key_not_in_bundle(self):
        data = reg(entry(1))
        r = self.verify(data, self.k.sign(self.owner, data), fpr=self.other)
        self.assertEqual(r["reason"], "untrusted_signer")

    def test_signing_subkey_of_trusted_primary_accepted(self):
        data = reg(entry(1))
        r = self.verify(data, self.k.sign(self.sub_primary, data), pub=self.k.export(self.sub_primary),
                        fpr=self.sub_primary)
        self.assertEqual(r["status"], "verified", r)

    def test_configured_subkey_fingerprint_is_not_a_pin(self):
        data = reg(entry(1))
        sig = self.k.sign(self.sub_primary, data)
        out = self.k.run("--with-colons", "--list-keys", self.sub_primary).stdout.decode().splitlines()
        fprs = [ln.split(":")[9] for ln in out if ln.startswith("fpr:")]
        sub = [f for f in fprs if f != self.sub_primary][0]
        r = self.verify(data, sig, pub=self.k.export(self.sub_primary), fpr=sub)
        self.assertEqual(r["reason"], "untrusted_signer")

    def test_edited_verified_result_cannot_add_authority(self):
        data = reg(entry(1))
        r = self.verify(data, self.k.sign(self.owner, data))
        r["approvals"]["src:core\0core:other"] = {"record_sha256": H2, "authority": "owner_approved"}
        r["approvals"]["src:core\0core:pref-tea"] = {"record_sha256": H2, "authority": "owner_approved"}
        self.assertEqual(av.owner_authority(r, "src:core", "core:other", H2)[0], None)
        self.assertEqual(av.owner_authority(r, "src:core", "core:pref-tea", H2)[0], None)
        self.assertEqual(av.owner_authority(r, "src:core", "core:pref-tea", H1)[0], "owner_approved")
        forged = {k: v for k, v in r.items() if k != "_proof"}
        self.assertEqual(av.owner_authority(forged, "src:core", "core:pref-tea", H1), (None, "no_verified_register"))
        self.assertEqual(av.owner_authority(dict(r, _proof=object()), "src:core", "core:pref-tea", H1)[0], None)

    def test_altered_signed_bytes(self):
        data = reg(entry(1))
        sig = self.k.sign(self.owner, data)
        r = self.verify(data.replace(b"D-synthetic-1", b"D-synthetic-9"), sig)
        self.assertEqual((r["status"], r["reason"]), ("refused", "verification_failed:badsig"))

    def test_appended_entry_after_signing(self):
        data = reg(entry(1))
        sig = self.k.sign(self.owner, data)
        self.assertEqual(self.verify(data, sig)["status"], "verified")  # control: unchanged bytes
        longer = reg(entry(1), entry(2, record_id="ppl:p-001", source_id="src:people", h=H3))
        self.assertEqual(self.verify(longer, sig)["reason"], "verification_failed:badsig")

    def test_missing_or_garbage_signature(self):
        data = reg(entry(1))
        self.assertEqual(self.verify(data, None)["reason"], "signature_missing")
        self.assertEqual(self.verify(data, b"")["status"], "refused")
        self.assertEqual(self.verify(data, b"not a signature")["status"], "refused")

    def test_armored_detached_signature_accepted(self):
        data = reg(entry(1))
        self.assertEqual(self.verify(data, self.k.sign(self.owner, data, armor=True))["status"], "verified")

    def test_signature_of_other_bytes(self):
        data = reg(entry(1))
        other_sig = self.k.sign(self.owner, reg(entry(1, h=H2)))
        self.assertEqual(self.verify(data, other_sig)["reason"], "verification_failed:badsig")

    def test_expired_key(self):
        data = reg(entry(1))
        sig = self.k.sign(self.expired, data, faked="20200101T120000")
        r = self.verify(data, sig, pub=self.k.export(self.expired), fpr=self.expired)
        self.assertEqual(r["status"], "refused")
        self.assertEqual(r["reason"], "verification_failed:expkeysig")

    def test_garbage_public_key(self):
        data = reg(entry(1))
        r = self.verify(data, self.k.sign(self.owner, data), pub=b"garbage")
        self.assertEqual(r["status"], "refused")

    def test_user_keyring_not_consulted(self):
        data = reg(entry(1))
        sig = self.k.sign(self.owner, data)
        with mock.patch.dict(os.environ, {"GNUPGHOME": self.k.home}):  # a keyring that holds the other key too
            r = self.verify(data, self.k.sign(self.other, data), pub=self.owner_pub, fpr=self.owner)
        self.assertEqual(r["status"], "refused")
        self.assertEqual(self.verify(data, sig)["status"], "verified")

    def test_temporary_home_removed(self):
        before = set(Path(tempfile.gettempdir()).glob("ella-attest-gnupg-*"))
        data = reg(entry(1))
        self.verify(data, self.k.sign(self.owner, data))
        self.assertEqual(set(Path(tempfile.gettempdir()).glob("ella-attest-gnupg-*")), before)

    # --- record bytes
    def test_changed_record_bytes_lose_authority(self):
        data = reg(entry(1))
        r = self.verify(data, self.k.sign(self.owner, data))
        self.assertEqual(av.owner_authority(r, "src:core", "core:pref-tea", H2),
                         (None, "record_bytes_differ_from_approved_bytes"))
        self.assertEqual(av.owner_authority(r, "src:notebook", "core:pref-tea", H1), (None, "not_approved"))
        self.assertEqual(av.owner_authority(r, "src:core", "core:other", H1), (None, "not_approved"))

    # --- withdrawal and replacement (signed)
    def test_withdraw_then_reapprove(self):
        data = reg(entry(1), entry(2, "withdraw", supersedes_entry=1))
        r = self.verify(data, self.k.sign(self.owner, data))
        self.assertEqual(r["status"], "verified")
        self.assertEqual(av.owner_authority(r, "src:core", "core:pref-tea", H1), (None, "not_approved"))
        data2 = data + reg(entry(3))
        r2 = self.verify(data2, self.k.sign(self.owner, data2))
        self.assertEqual(av.owner_authority(r2, "src:core", "core:pref-tea", H1)[0], "owner_approved")

    def test_replace_binds_new_bytes_only(self):
        data = reg(entry(1), entry(2, "replace", h=H2, supersedes_entry=1))
        r = self.verify(data, self.k.sign(self.owner, data))
        self.assertEqual(av.owner_authority(r, "src:core", "core:pref-tea", H1)[0], None)
        self.assertEqual(av.owner_authority(r, "src:core", "core:pref-tea", H2)[0], "owner_approved")

    # --- rollback anchor
    def test_rollback_to_older_signed_register_refused(self):
        old = reg(entry(1))
        new = reg(entry(1), entry(2, "withdraw", supersedes_entry=1))
        anchor_after_new = av.anchor_for(new)
        r = self.verify(old, self.k.sign(self.owner, old), anchor=anchor_after_new)
        self.assertEqual(r["reason"], "rollback_detected:register_older_than_anchor")

    def test_fork_with_same_length_refused(self):
        a = reg(entry(1))
        b = reg(entry(1, h=H2))
        r = self.verify(b, self.k.sign(self.owner, b), anchor=av.anchor_for(a))
        self.assertEqual(r["reason"], "rollback_or_fork_detected:prefix_mismatch")

    def test_append_after_anchor_accepted(self):
        a = reg(entry(1))
        b = reg(entry(1), entry(2, record_id="ppl:p-001", source_id="src:people", h=H3))
        r = self.verify(b, self.k.sign(self.owner, b), anchor=av.anchor_for(a))
        self.assertEqual(r["status"], "verified")
        self.assertEqual(r["anchor_if_accepted"], av.anchor_for(b))

    def test_missing_or_malformed_anchor(self):
        data = reg(entry(1))
        sig = self.k.sign(self.owner, data)
        self.assertEqual(self.verify(data, sig, anchor=None)["reason"], "rollback_anchor_missing")
        for bad in ({"latest_seq": -1, "prefix_sha256": av.sha(b"")}, {"latest_seq": True, "prefix_sha256": av.sha(b"")},
                    {"latest_seq": 0}, {"latest_seq": 0, "prefix_sha256": "x", "extra": 1}, []):
            self.assertEqual(self.verify(data, sig, anchor=bad)["reason"], "anchor_malformed")

    # --- malformed or conflicting register content, correctly signed
    def assertRefusedSigned(self, data, prefix):
        r = self.verify(data, self.k.sign(self.owner, data))
        self.assertEqual(r["status"], "refused", r)
        self.assertTrue(r["reason"].startswith(prefix), r["reason"])
        self.assertEqual(r["approvals"], {})
        self.assertTrue(r["owner_approval_evidence"].startswith("none"))

    def test_signed_but_malformed(self):
        self.assertRefusedSigned(reg(entry(2)), "malformed:line_1_seq")
        self.assertRefusedSigned(b'{"seq": 1, "seq": 1}\n', "malformed:line_1_not_a_json_object")
        self.assertRefusedSigned(reg(entry(1))[:-1], "malformed:last_line_not_terminated")

    def test_signed_but_conflicting(self):
        self.assertRefusedSigned(reg(entry(1), entry(2, h=H2)), "conflict:entry_2_second_active_approval")


class RegisterParsingTests(unittest.TestCase):
    """Structure and conflict rules, independent of gpg."""

    def parse(self, *entries):
        return av.parse_register(reg(*entries))

    def test_field_rules(self):
        cases = {
            "seq_bool": entry(True), "seq_str": entry("1"), "seq_zero": entry(0),
            "action": entry(1, action="delete"), "hash": entry(1, h="sha256:abc"),
            "hash_upper": entry(1, h=H1.upper()), "authority_low": entry(1, authority="ella_observed"),
            "authority_missing": {k: v for k, v in entry(1).items() if k != "authority"},
            "unknown_field": entry(1, note="x"), "missing_field": {k: v for k, v in entry(1).items() if k != "decision_ref"},
            "empty_id": entry(1, record_id=""), "nul_in_source": entry(1, source_id="src:core\x00a"),
            "ctrl_in_record": entry(1, record_id="core:\x1btea"), "ts": entry(1, issued_at="2026-11-01"),
            "expiry_ts": entry(1, expires_at="tomorrow"), "supersedes_on_approve": entry(1, supersedes_entry=1),
        }
        for name, e in cases.items():
            with self.subTest(name):
                entries, why = self.parse(e)
                self.assertIsNone(entries, name)
                self.assertTrue(why.startswith("malformed"), why)

    def test_withdraw_shapes(self):
        for e2 in (entry(2, "withdraw"), entry(2, "withdraw", supersedes_entry=2),
                   entry(2, "withdraw", supersedes_entry=1, authority="owner_approved")):
            with self.subTest(e2=e2):
                self.assertIsNone(self.parse(entry(1), e2)[0])

    def test_blank_line_and_non_utf8_and_non_object(self):
        self.assertIsNone(av.parse_register(reg(entry(1)) + b"\n")[0])
        self.assertEqual(av.parse_register(reg(entry(1)).replace(b"\n", b"\r\n"))[1], "malformed:line_1_whitespace_or_cr")
        self.assertIsNone(av.parse_register(b" " + reg(entry(1)))[0])
        self.assertIsNone(av.parse_register(b"\xff\xfe\n")[0])
        self.assertIsNone(av.parse_register(b"[1]\n")[0])
        self.assertEqual(av.parse_register(b""), ([], "ok"))

    def resolve(self, *entries):
        parsed, why = self.parse(*entries)
        self.assertIsNotNone(parsed, why)
        return av.resolve(parsed, NOW)

    def test_conflicts(self):
        cases = {
            "second_active": (entry(1), entry(2, h=H2)),
            "withdraw_twice": (entry(1), entry(2, "withdraw", supersedes_entry=1), entry(3, "withdraw", supersedes_entry=1)),
            "withdraw_mismatch_hash": (entry(1), entry(2, "withdraw", h=H2, supersedes_entry=1)),
            "withdraw_of_withdraw": (entry(1), entry(2, "withdraw", supersedes_entry=1), entry(3, "withdraw", supersedes_entry=2)),
            "replace_same_bytes": (entry(1), entry(2, "replace", supersedes_entry=1)),
            "replace_across_sources": (entry(1), entry(2, "replace", source_id="src:people", h=H2, supersedes_entry=1)),
            "replace_retired": (entry(1), entry(2, "replace", h=H2, supersedes_entry=1), entry(3, "replace", h=H3, supersedes_entry=1)),
            "replace_onto_active": (entry(1), entry(2, record_id="core:b", h=H3),
                                    entry(3, "replace", record_id="core:b", h=H2, supersedes_entry=1)),
            "replace_renames_record": (entry(1), entry(2, "replace", record_id="core:other", h=H2, supersedes_entry=1)),
        }
        for name, es in cases.items():
            with self.subTest(name):
                granted, why, _ = self.resolve(*es)
                self.assertIsNone(granted)
                self.assertTrue(why.startswith("conflict"), why)

    def test_expiry_and_future(self):
        g, _, notes = self.resolve(entry(1, expires_at="2026-11-02T00:00:00Z"))
        self.assertEqual((g, notes["expired"]), ({}, 1))
        g, _, notes = self.resolve(entry(1, issued_at="2027-01-01T00:00:00Z"))
        self.assertEqual((g, notes["not_yet_valid"]), ({}, 1))
        g, _, _ = self.resolve(entry(1, expires_at="2027-01-01T00:00:00Z"))
        self.assertIn("src:core\0core:pref-tea", g)

    def test_replace_chain(self):
        g, why, notes = self.resolve(entry(1), entry(2, "replace", h=H2, supersedes_entry=1),
                                     entry(3, "replace", h=H3, supersedes_entry=2))
        self.assertEqual(why, "ok")
        self.assertEqual(g["src:core\0core:pref-tea"]["record_sha256"], H3)
        self.assertEqual(notes["replaced"], 2)


class FailClosedWithoutVerification(unittest.TestCase):
    def test_no_trusted_fingerprint(self):
        data = reg(entry(1))
        for fpr, reason in ((None, "no_trusted_signer_configured"), ("", "trusted_fingerprint_invalid"),
                            ("ABCD", "trusted_fingerprint_invalid"), ("Z" * 40, "trusted_fingerprint_invalid"),
                            (12345, "trusted_fingerprint_invalid")):
            r = av.verify_register(data, b"sig", b"key", fpr, ANCHOR0, NOW)
            self.assertEqual(r["reason"], reason)

    def test_missing_inputs(self):
        f = "A" * 40
        self.assertEqual(av.verify_register(None, b"s", b"k", f, ANCHOR0, NOW)["reason"], "register_missing")
        self.assertEqual(av.verify_register(b"", None, b"k", f, ANCHOR0, NOW)["reason"], "signature_missing")
        self.assertEqual(av.verify_register(b"", b"s", None, f, ANCHOR0, NOW)["reason"], "trusted_public_key_missing")

    def test_tool_missing(self):
        r = av.verify_register(reg(entry(1)), b"s", b"k", "A" * 40, ANCHOR0, NOW, gpg_binary="/nonexistent/gpg")
        self.assertEqual(r["reason"], "verification_tool_missing")
        with mock.patch.object(av.shutil, "which", return_value=None):
            r = av.verify_register(reg(entry(1)), b"s", b"k", "A" * 40, ANCHOR0, NOW)
        self.assertEqual(r["reason"], "verification_tool_missing")

    def _fake(self, body):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, True)
        p = Path(d) / "gpg"
        p.write_text("#!/bin/sh\n" + body)
        p.chmod(p.stat().st_mode | stat.S_IXUSR)
        return str(p)

    def test_tool_failures(self):
        fpr = "A" * 40
        good = f'echo "[GNUPG:] GOODSIG X u"; echo "[GNUPG:] VALIDSIG {fpr} 2026-11-01 0 0 4 0 22 10 00 {fpr}"'
        cases = {
            "nonzero_exit_even_with_good_status": f'case "$*" in *--verify*) {good}; exit 1;; esac; exit 0',
            "import_fails": "exit 2",
            "no_status": 'exit 0',
            "two_signatures": f'case "$*" in *--verify*) {good}; {good};; esac; exit 0',
            "bad_and_good": f'case "$*" in *--verify*) {good}; echo "[GNUPG:] BADSIG X u";; esac; exit 0',
            "text_signature_class": f'case "$*" in *--verify*) echo "[GNUPG:] GOODSIG X u"; '
                                    f'echo "[GNUPG:] VALIDSIG {fpr} d 0 0 4 0 22 10 01 {fpr}";; esac; exit 0',
            "hang": 'case "$*" in *--verify*) sleep 30;; esac; exit 0',
        }
        for name, body in cases.items():
            with self.subTest(name), mock.patch.object(av, "GPG_TIMEOUT_S", 1):
                r = av.verify_register(reg(entry(1)), b"s", b"k", fpr, ANCHOR0, NOW, gpg_binary=self._fake(body))
                self.assertEqual(r["status"], "refused", name)
                self.assertEqual(r["approvals"], {})

    def test_timeout_kills_the_whole_process_group(self):
        marker = Path(tempfile.mkdtemp()) / "child-alive"
        self.addCleanup(shutil.rmtree, marker.parent, True)
        body = f'case "$*" in *--verify*) (sleep 3; touch {marker}) & sleep 30;; esac; exit 0'
        with mock.patch.object(av, "GPG_TIMEOUT_S", 1):
            r = av.verify_register(reg(entry(1)), b"s", b"k", "A" * 40, ANCHOR0, NOW, gpg_binary=self._fake(body))
        self.assertEqual(r["reason"], "verification_failed:timeout")
        import time
        time.sleep(3.5)
        self.assertFalse(marker.exists(), "a child of the verification tool outlived the timeout")

    def test_owner_authority_requires_verified_result(self):
        fake = {"status": "refused", "approvals": {"src:core\0core:pref-tea": {"record_sha256": H1, "authority": "owner_approved"}}}
        self.assertEqual(av.owner_authority(fake, "src:core", "core:pref-tea", H1), (None, "no_verified_register"))
        self.assertEqual(av.owner_authority(None, "src:core", "core:pref-tea", H1), (None, "no_verified_register"))
        self.assertEqual(av.owner_authority({"status": "VERIFIED"}, "s", "r", H1), (None, "no_verified_register"))


if __name__ == "__main__":
    unittest.main()
