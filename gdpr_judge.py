#!/usr/bin/env python3
"""
AI GDPR Judge - A specialized AI assistant for GDPR compliance and EU law
Designed to provide accurate legal analysis with minimal hallucination
"""

import ollama
import json
import re
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

from gdpr_knowledge_base import GDPRKnowledgeBase, RetrievalResult
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalArea(Enum):
    GDPR = "GDPR"
    DATA_PROTECTION = "Data Protection"
    PRIVACY = "Privacy"
    CONSENT = "Consent"
    DATA_BREACH = "Data Breach"
    RIGHTS = "Data Subject Rights"
    PROCESSING = "Data Processing"
    TRANSFERS = "Data Transfers"

@dataclass
class LegalPrecedent:
    case_name: str
    court: str
    year: int
    key_points: List[str]
    gdpr_articles: List[str]
    relevance_score: float

@dataclass
class LegalAnalysis:
    issue: str
    applicable_articles: List[str]
    legal_requirements: List[str]
    compliance_checklist: List[str]
    risk_assessment: str
    recommendations: List[str]
    precedents: List[LegalPrecedent]
    confidence_score: float
    supporting_passages: List[Dict[str, Any]] = field(default_factory=list)

class GDPRJudge:
    """
    AI Judge specialized in GDPR and EU data protection law
    """
    
    def __init__(self, model_name: str = "llama3.1:8b"):
        self.model_name = model_name
        self.client = ollama.Client()
        self.gdpr_knowledge = self._load_gdpr_knowledge()
        self.legal_precedents = self._load_legal_precedents()
        try:
            self.knowledge_base = GDPRKnowledgeBase()
        except FileNotFoundError as exc:
            logger.warning("GDPR knowledge base unavailable: %s", exc)
            self.knowledge_base = None
        
    def _load_gdpr_knowledge(self) -> Dict:
        """Load comprehensive GDPR knowledge base"""
        return {
            "articles": {
                "Article 5": "Principles relating to processing of personal data",
                "Article 6": "Lawfulness of processing",
                "Article 7": "Conditions for consent",
                "Article 8": "Conditions applicable to child's consent",
                "Article 9": "Processing of special categories of personal data",
                "Article 12": "Transparent information and communication",
                "Article 13": "Information to be provided where personal data collected from data subject",
                "Article 14": "Information to be provided where personal data not obtained from data subject",
                "Article 15": "Right of access by the data subject",
                "Article 16": "Right to rectification",
                "Article 17": "Right to erasure ('right to be forgotten')",
                "Article 18": "Right to restriction of processing",
                "Article 19": "Notification obligation regarding rectification or erasure",
                "Article 20": "Right to data portability",
                "Article 21": "Right to object",
                "Article 22": "Automated individual decision-making",
                "Article 25": "Data protection by design and by default",
                "Article 32": "Security of processing",
                "Article 33": "Notification of a personal data breach to the supervisory authority",
                "Article 34": "Communication of a personal data breach to the data subject",
                "Article 35": "Data protection impact assessment",
                "Article 44": "General principle for transfers",
                "Article 45": "Transfers on the basis of an adequacy decision",
                "Article 46": "Transfers subject to appropriate safeguards",
                "Article 47": "Binding corporate rules",
                "Article 48": "Transfers or disclosures not authorised by Union law",
                "Article 49": "Derogations for specific situations",
                "Article 77": "Right to lodge a complaint with a supervisory authority",
                "Article 78": "Right to an effective judicial remedy against a supervisory authority",
                "Article 79": "Right to an effective judicial remedy against a controller or processor",
                "Article 80": "Representation of data subjects",
                "Article 82": "Right to compensation and liability",
                "Article 83": "General conditions for imposing administrative fines",
                "Article 84": "Penalties"
            },
            "principles": [
                "Lawfulness, fairness and transparency",
                "Purpose limitation",
                "Data minimisation",
                "Accuracy",
                "Storage limitation",
                "Integrity and confidentiality",
                "Accountability"
            ],
            "legal_basis": [
                "Consent",
                "Contract",
                "Legal obligation",
                "Vital interests",
                "Public task",
                "Legitimate interests"
            ],
            "data_subject_rights": [
                "Right to be informed",
                "Right of access",
                "Right to rectification",
                "Right to erasure",
                "Right to restrict processing",
                "Right to data portability",
                "Right to object",
                "Rights related to automated decision making"
            ]
        }
    
    def _load_legal_precedents(self) -> List[LegalPrecedent]:
        """Load key GDPR legal precedents and case law"""
        return [
            LegalPrecedent(
                case_name="Google Spain SL, Google Inc. v Agencia Española de Protección de Datos",
                court="CJEU",
                year=2014,
                key_points=[
                    "Established 'right to be forgotten'",
                    "Search engines are data controllers",
                    "Right to delisting from search results"
                ],
                gdpr_articles=["Article 17", "Article 4(7)"],
                relevance_score=0.95
            ),
            LegalPrecedent(
                case_name="Schrems v Data Protection Commissioner",
                court="CJEU",
                year=2015,
                key_points=[
                    "Invalidated Safe Harbor agreement",
                    "Established adequacy requirements for third countries",
                    "Emphasized fundamental rights protection"
                ],
                gdpr_articles=["Article 45", "Article 46", "Article 44"],
                relevance_score=0.90
            ),
            LegalPrecedent(
                case_name="Schrems II",
                court="CJEU",
                year=2020,
                key_points=[
                    "Invalidated Privacy Shield",
                    "Standard Contractual Clauses require case-by-case assessment",
                    "Third country surveillance laws must be considered"
                ],
                gdpr_articles=["Article 45", "Article 46", "Article 44"],
                relevance_score=0.95
            ),
            LegalPrecedent(
                case_name="Weltimmo s.r.o. v Nemzeti Adatvédelmi és Információszabadság Hatóság",
                court="CJEU",
                year=2015,
                key_points=[
                    "Established establishment criteria",
                    "Controllers can be subject to GDPR even outside EU",
                    "Economic activity test for establishment"
                ],
                gdpr_articles=["Article 3", "Article 4(7)"],
                relevance_score=0.85
            ),
            LegalPrecedent(
                case_name="Google LLC v CNIL",
                court="CJEU",
                year=2019,
                key_points=[
                    "Right to be forgotten applies globally",
                    "Balancing fundamental rights",
                    "Territorial scope of delisting"
                ],
                gdpr_articles=["Article 17", "Article 3"],
                relevance_score=0.80
            )
        ]
    
    def analyze_gdpr_compliance(self, scenario: str, context: Dict = None) -> LegalAnalysis:
        """
        Analyze a scenario for GDPR compliance
        """
        try:
            # Create comprehensive prompt for legal analysis
            retrieved_passages = []
            if getattr(self, "knowledge_base", None):
                try:
                    retrieved_passages = self.knowledge_base.retrieve(scenario, top_k=5)
                except Exception as retrieval_error:
                    logger.warning("Retrieval failed: %s", retrieval_error)
                    retrieved_passages = []
            prompt = self._create_legal_analysis_prompt(scenario, context, retrieved_passages)
            
            # Get AI response
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.1,  # Low temperature for legal accuracy
                    "top_p": 0.9,
                    "top_k": 40
                }
            )
            
            # Parse response
            analysis = self._parse_legal_response(response['response'], scenario, retrieved_passages)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in legal analysis: {e}")
            return self._create_fallback_analysis(scenario, retrieved_passages)
    
    def _create_legal_analysis_prompt(self, scenario: str, context: Dict = None, retrieved_passages: Optional[List[RetrievalResult]] = None) -> str:
        """Create a comprehensive prompt for legal analysis"""
        
        gdpr_articles_text = "\n".join([
            f"{article}: {description}" 
            for article, description in self.gdpr_knowledge["articles"].items()
        ])
        
        precedents_text = "\n".join([
            f"- {p.case_name} ({p.court}, {p.year}): {', '.join(p.key_points[:2])}"
            for p in self.legal_precedents[:5]
        ])
        
        retrieved_passages = retrieved_passages or []
        retrieval_section = "\n".join(
            f"{idx + 1}. {passage.article} - {passage.title or 'No title'}\n{passage.text}"
            for idx, passage in enumerate(retrieved_passages[:5])
        ) if retrieved_passages else 'No direct GDPR passages retrieved; rely on statutory text and core principles.'

        return f"""You are an expert GDPR legal judge and compliance specialist. Analyze the following scenario for GDPR compliance.

GDPR ARTICLES REFERENCE:
{gdpr_articles_text}

KEY LEGAL PRECEDENTS:
{precedents_text}

GDPR PRINCIPLES:
{', '.join(self.gdpr_knowledge['principles'])}

LEGAL BASIS FOR PROCESSING:
{', '.join(self.gdpr_knowledge['legal_basis'])}

DATA SUBJECT RIGHTS:
{', '.join(self.gdpr_knowledge['data_subject_rights'])}

RELEVANT GDPR PASSAGES (retrieved):
{retrieval_section}

SCENARIO TO ANALYZE:
{scenario}

CONTEXT: {context or 'No additional context provided'}

Please provide a comprehensive legal analysis in the following JSON format:
{{
    "issue": "Brief description of the main legal issue",
    "applicable_articles": ["Article X", "Article Y"],
    "legal_requirements": ["Requirement 1", "Requirement 2"],
    "compliance_checklist": ["Check 1", "Check 2"],
    "risk_assessment": "Assessment of compliance risks",
    "recommendations": ["Recommendation 1", "Recommendation 2"],
    "confidence_score": 0.85
}}

Focus on:
1. Specific GDPR articles that apply
2. Legal requirements that must be met
3. Compliance checklist for the scenario
4. Risk assessment and potential violations
5. Practical recommendations
6. Reference to relevant case law where applicable

Be precise, cite specific articles, and avoid speculation. If uncertain, state limitations clearly."""

    def _parse_legal_response(self, response: str, scenario: str, retrieved_passages: Optional[List[RetrievalResult]] = None) -> LegalAnalysis:
        """Parse AI response into structured legal analysis"""
        retrieved_passages = retrieved_passages or []
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract information from text
                    data = self._extract_info_from_text(response)
            else:
                # If no JSON found, extract information from text
                data = self._extract_info_from_text(response)
            
            # Find relevant precedents
            relevant_precedents = self._find_relevant_precedents(scenario)
            supporting_context = [
                {
                    "article": passage.article,
                    "title": passage.title,
                    "chapter": passage.chapter,
                    "section": passage.section,
                    "text": passage.text,
                    "score": round(passage.score, 4),
                }
                for passage in retrieved_passages
            ]

            return LegalAnalysis(
                issue=data.get("issue", "Analysis completed"),
                applicable_articles=data.get("applicable_articles", ["Article 5", "Article 6"]),
                legal_requirements=data.get("legal_requirements", ["Ensure lawful basis for processing"]),
                compliance_checklist=data.get("compliance_checklist", ["Review data processing activities"]),
                risk_assessment=data.get("risk_assessment", "Manual review recommended"),
                recommendations=data.get("recommendations", ["Consult with legal expert"]),
                precedents=relevant_precedents,
                confidence_score=data.get("confidence_score", 0.7),
                supporting_passages=supporting_context
            )
            
        except Exception as e:
            logger.error(f"Error parsing legal response: {e}")
            return self._create_fallback_analysis(scenario, retrieved_passages)
    
    def _extract_info_from_text(self, response: str) -> Dict:
        """Extract information from text response when JSON parsing fails"""
        data = {
            "issue": "GDPR compliance analysis",
            "applicable_articles": [],
            "legal_requirements": [],
            "compliance_checklist": [],
            "risk_assessment": "Analysis completed",
            "recommendations": [],
            "confidence_score": 0.6
        }
        
        # Extract articles mentioned
        article_pattern = r'Article\s+(\d+)'
        articles = re.findall(article_pattern, response)
        if articles:
            data["applicable_articles"] = [f"Article {art}" for art in articles[:5]]
        
        # Extract key points
        lines = response.split('\n')
        requirements = []
        recommendations = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('{') and not line.startswith('}'):
                if any(keyword in line.lower() for keyword in ['must', 'required', 'obligation']):
                    requirements.append(line)
                elif any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'should']):
                    recommendations.append(line)
        
        data["legal_requirements"] = requirements[:5]
        data["recommendations"] = recommendations[:5]
        data["compliance_checklist"] = requirements[:3]  # Use requirements as checklist
        
        return data
    
    def _find_relevant_precedents(self, scenario: str) -> List[LegalPrecedent]:
        """Find relevant legal precedents based on scenario keywords"""
        keywords = scenario.lower().split()
        relevant = []
        
        for precedent in self.legal_precedents:
            score = 0
            for keyword in keywords:
                if keyword in precedent.case_name.lower():
                    score += 0.3
                if any(keyword in point.lower() for point in precedent.key_points):
                    score += 0.2
            
            if score > 0.1:
                precedent.relevance_score = min(score, 1.0)
                relevant.append(precedent)
        
        return sorted(relevant, key=lambda x: x.relevance_score, reverse=True)[:3]
    
    def _create_fallback_analysis(self, scenario: str, retrieved_passages: Optional[List[RetrievalResult]] = None) -> LegalAnalysis:
        """Create fallback analysis when AI response fails"""
        supporting_context = [
            {
                "article": passage.article,
                "title": passage.title,
                "chapter": passage.chapter,
                "section": passage.section,
                "text": passage.text,
                "score": round(passage.score, 4),
            }
            for passage in (retrieved_passages or [])
        ]
        return LegalAnalysis(
            issue="Unable to complete analysis due to technical error",
            applicable_articles=["Article 5", "Article 6"],
            legal_requirements=["Ensure lawful basis for processing", "Implement data protection principles"],
            compliance_checklist=["Review data processing activities", "Assess legal basis", "Implement safeguards"],
            risk_assessment="Unable to assess - manual review recommended",
            recommendations=["Consult with legal expert", "Review GDPR compliance framework"],
            precedents=[],
            confidence_score=0.1,
            supporting_passages=supporting_context
        )
    
    def get_article_explanation(self, article: str) -> str:
        """Get detailed explanation of a specific GDPR article"""
        if article in self.gdpr_knowledge["articles"]:
            return f"{article}: {self.gdpr_knowledge['articles'][article]}"
        return f"Article {article} not found in knowledge base"
    
    def check_data_processing_lawfulness(self, purpose: str, data_types: List[str], 
                                       legal_basis: str) -> Dict:
        """Check if data processing is lawful under GDPR"""
        prompt = f"""
        Analyze if the following data processing is lawful under GDPR Article 6:
        
        Purpose: {purpose}
        Data Types: {', '.join(data_types)}
        Claimed Legal Basis: {legal_basis}
        
        Available legal bases: {', '.join(self.gdpr_knowledge['legal_basis'])}
        
        Provide analysis in JSON format:
        {{
            "is_lawful": true/false,
            "reasoning": "Explanation",
            "alternative_basis": ["suggested alternatives"],
            "requirements": ["specific requirements to meet"]
        }}
        """
        
        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={"temperature": 0.1}
            )
            
            json_match = re.search(r'\{.*\}', response['response'], re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            logger.error(f"Error in lawfulness check: {e}")
        
        return {
            "is_lawful": False,
            "reasoning": "Unable to analyze - manual review required",
            "alternative_basis": [],
            "requirements": ["Consult legal expert"]
        }

def main():
    """Main function for testing the GDPR Judge"""
    judge = GDPRJudge()
    
    # Example usage
    scenario = """
    A company wants to collect customer email addresses for marketing purposes 
    without explicit consent, claiming legitimate interest as the legal basis.
    They plan to store the data for 5 years and share it with third-party 
    marketing partners.
    """
    
    print("AI GDPR Judge - Legal Analysis")
    print("=" * 50)
    print(f"Scenario: {scenario.strip()}")
    print("\nAnalyzing...")
    
    analysis = judge.analyze_gdpr_compliance(scenario)
    
    print(f"\nIssue: {analysis.issue}")
    print(f"\nApplicable Articles: {', '.join(analysis.applicable_articles)}")
    print(f"\nLegal Requirements:")
    for req in analysis.legal_requirements:
        print(f"  - {req}")
    print(f"\nCompliance Checklist:")
    for check in analysis.compliance_checklist:
        print(f"  - {check}")
    print(f"\nRisk Assessment: {analysis.risk_assessment}")
    print(f"\nRecommendations:")
    for rec in analysis.recommendations:
        print(f"  - {rec}")
    print(f"\nConfidence Score: {analysis.confidence_score:.2f}")

if __name__ == "__main__":
    main()
