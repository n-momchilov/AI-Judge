import json
import sys
import types
from pathlib import Path

import pytest

if 'ollama' not in sys.modules:
    stub_module = types.ModuleType('ollama')

    class _StubClient:
        def __init__(self, *_, **__):
            pass

        def generate(self, *_, **__):
            raise RuntimeError('Stub client should be replaced in tests')

    stub_module.Client = _StubClient
    sys.modules['ollama'] = stub_module

from gdpr_knowledge_base import GDPRKnowledgeBase
from gdpr_judge import GDPRJudge

DATA_DIR = Path('data')

def test_knowledge_base_assets_exist():
    for filename in [
        'gdpr_articles.json',
        'gdpr_chunks.jsonl',
        'gdpr_tfidf.npz',
        'gdpr_vectorizer.joblib',
        'gdpr_chunks_index.json',
    ]:
        assert (DATA_DIR / filename).exists(), f"Missing knowledge base asset: {filename}"

def test_retrieval_returns_expected_article():
    kb = GDPRKnowledgeBase(DATA_DIR)
    results = kb.retrieve('child consent for profiling under gdpr', top_k=3)
    assert results, 'Expected at least one retrieval result'
    articles = {result.article for result in results}
    assert 'Article 8' in articles or 'Article 7' in articles

def test_judge_attaches_supporting_passages():
    class DummyClient:
        def generate(self, model, prompt, options):
            return {
                'response': json.dumps({
                    'issue': 'Test issue',
                    'applicable_articles': ['Article 6'],
                    'legal_requirements': ['Requirement'],
                    'compliance_checklist': ['Checklist'],
                    'risk_assessment': 'Low risk',
                    'recommendations': ['Recommendation'],
                    'confidence_score': 0.9,
                })
            }

    judge = GDPRJudge()
    judge.client = DummyClient()

    analysis = judge.analyze_gdpr_compliance(
        'We process employee health data with explicit consent for wellness monitoring.',
        context={'legal_basis': 'Consent'},
    )

    assert analysis.supporting_passages, 'Expected supporting passages when knowledge base is available'
    for passage in analysis.supporting_passages:
        assert passage.get('article'), 'Passage missing article metadata'
        assert passage.get('text'), 'Passage missing text content'
