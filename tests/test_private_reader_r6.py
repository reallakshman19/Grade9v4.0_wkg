"""Synthetic R6 identity, content-revision and fail-closed integration controls."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from private_reader_r6 import question_key, revise, transform, RUNTIME
from private_reader_integration import build

from test_private_reader_integration import fixture


def test_scoped_legacy_identity_is_not_global():
    q1 = {'topic': 'OPTICS', 'source_id': 'EX-SAME', 'id': 'Q1'}
    q2 = {**q1, 'topic': 'MAGNETISM'}
    assert question_key(q1) != question_key(q2)
    assert question_key(q1) == 'OPTICS::EX-SAME::Q1'


def test_attempt_revision_tracks_question_and_actual_figure_bytes():
    q = {'topic': 'OPTICS', 'source_id': 'EX-SAME', 'id': 'Q1',
         'stem': 'Synthetic only', 'options': ['a', 'b'],
         'answer': 'a', 'source_figures': ['a.svg']}
    media = {'a.svg': '<svg><rect width="1"/></svg>'}
    original = revise(q, media)
    assert original == revise(dict(q), dict(media))
    for changed in ({**q, 'answer': 'b'}, {**q, 'options': ['b', 'a']},
                    {**q, 'stem': 'Different synthetic question'}):
        assert revise(changed, media) != original
    assert revise(q, {'a.svg': '<svg><rect width="2"/></svg>'}) != original
    assert revise(q, {}) != original


def test_r6_template_mismatch_fails_closed():
    with pytest.raises(ValueError, match='R6_EXPECTED_RUNTIME_ANCHOR_MISMATCH'):
        transform('<!doctype html><html><head></head><body>'
                  '<script id="wpe-data" type="application/json">'
                  '{"questions":[]}</script></body></html>')


def test_builder_rejects_r6_when_synthetic_legacy_template_is_incompatible(tmp_path):
    root, manifest, out = fixture(tmp_path)
    with pytest.raises(ValueError, match='R6_EXPECTED_RUNTIME_ANCHOR_MISMATCH'):
        build(root, out, manifest, r6=True)
    assert not out.exists()


def test_storage_runtime_declares_revision_scoped_attempts():
    for token in ('g9:private:practice:v3:', 'SAVED_LOCAL', 'UNSAVED',
                  'firstAttempt', 'helpEvents', 'localStorage.setItem',
                  'data.version === 3', 'data.revision === revision'):
        assert token in RUNTIME
