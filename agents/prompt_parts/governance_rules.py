GOVERNANCE_RULES = """
==================================================
GOVERNANCE, SECURITY & REGULATORY COVERAGE
==================================================

When the article’s topic intersects with data handling, AI deployment, cloud infrastructure, or enterprise AI operations, include governance and regulatory context where relevant. Do not force governance content into articles where it does not naturally fit.

WHEN TO APPLY GOVERNANCE CONTEXT:

Apply governance coverage when the article covers:
- AI infrastructure deployment decisions (cloud, hybrid, on-prem).
- Data platform strategy (training data, vector databases, feature stores).
- Enterprise AI adoption in regulated industries (finance, healthcare, government, energy).
- Multi-cloud or cross-border data movement.
- AI model access, audit trails, or accountability.
- Autonomous AI systems with consequential outputs.

==================================================
REGULATORY FRAMEWORKS — APPLY WHEN INTERSECTING
==================================================

EU AI ACT

The EU AI Act classifies AI systems by risk level. High-risk systems (those used in hiring, credit scoring, healthcare, law enforcement, or critical infrastructure) require:
- Conformity assessments and registration before deployment.
- Human oversight mechanisms that can intervene or override outputs.
- Comprehensive audit logs traceable to individual decisions.
- Training data documentation including source, scope, and bias testing.
- Transparency disclosures to users when AI is making consequential decisions.

Enterprises with EU operations or EU-resident users must assess whether their AI deployments qualify as high-risk under the Act. Multi-cloud or hybrid AI architectures do not reduce regulatory obligation — data processing location and output consequence determine classification.

DATA SOVEREIGNTY & RESIDENCY LAWS

Data sovereignty requirements restrict where data can be stored, processed, and transmitted. Key contexts:
- GDPR (EU): Personal data of EU residents must remain within the EU unless adequacy decisions or standard contractual clauses apply. Training AI on EU-resident personal data without lawful basis is a violation regardless of infrastructure location.
- China PIPL / Data Security Law: Cross-border transfer of Chinese citizen data requires government security assessments for sensitive categories.
- Regional AI regulations: India, Brazil, Canada, and others are enacting AI-specific data rules that may conflict with a single-cloud-region strategy.

Enterprise implication: organizations cannot design AI infrastructure on pure cost or latency criteria. Data residency constraints determine which cloud regions, which provider zones, and which orchestration patterns are legally permissible.

HIPAA (U.S. HEALTHCARE)

When AI processes Protected Health Information (PHI):
- AI providers must sign Business Associate Agreements (BAAs).
- PHI used in training, fine-tuning, or inference must remain within HIPAA-compliant infrastructure.
- Logging and audit trails for AI-processed PHI are required.
- Automated AI decisions affecting patient care require human oversight.

Not all cloud AI services offer HIPAA BAAs. Enterprises using general-purpose LLMs for clinical applications must verify HIPAA compliance at the model, hosting, and data pipeline layers.

SOC 2 TYPE II

SOC 2 Type II certification requires audited controls for:
- Security: access controls to AI models, APIs, and training infrastructure.
- Availability: uptime SLAs for AI-dependent production systems.
- Confidentiality: ensuring model outputs do not leak sensitive inputs.
- Processing Integrity: verifiable, repeatable AI outputs for audited business processes.

AI platform engineering teams must include SOC 2 control mapping in their model serving, orchestration, and monitoring architectures.

FINANCIAL SERVICES AI REGULATION

- SR 11-7 (U.S. Federal Reserve): Model Risk Management guidance applies to AI models used in credit, trading, fraud detection, and customer decisions. Requires independent model validation, challenger models, and documentation of assumptions and limitations.
- MAS AI/Data Ethics Framework (Singapore): Requires explainability, fairness testing, and human oversight for AI in financial decisions.
- DORA (EU Digital Operational Resilience Act): Applies to AI systems that financial institutions rely on for critical operations — requires third-party risk management for cloud AI providers.

==================================================
ENTERPRISE SECURITY PERIMETER
==================================================

AI infrastructure introduces new attack surfaces that traditional security perimeters were not designed to handle:

MODEL ACCESS CONTROLS
- API keys and model endpoints must be treated as high-value credentials.
- Rate limiting, IP allowlisting, and mTLS authentication are baseline requirements for production AI APIs.
- Prompt injection attacks (manipulating model behavior via crafted inputs) require input validation and output filtering at the API gateway layer.

DATA PIPELINE SECURITY
- Training data pipelines must enforce the same access controls as production data — a data pipeline breach enables model poisoning.
- Vector database security is often overlooked: embeddings can be reverse-engineered to approximate source data, creating confidentiality exposure.
- Feature stores and model registries require versioning and audit trails to meet model risk management standards.

NETWORK ISOLATION
- Enterprises handling regulated data should run inference workloads in dedicated VPCs or private cloud environments, not shared public endpoints.
- Multi-cloud AI orchestration (SkyPilot, Ray) must be configured to respect network isolation boundaries — cross-cloud traffic routing can inadvertently bypass security perimeter controls.

AUDIT TRAILS FOR AI
- Every consequential AI decision (credit approval, content moderation, resource allocation) requires a tamper-evident log including input, model version, output, timestamp, and the human or system that reviewed or acted on it.
- Log retention periods for AI decisions in regulated industries often exceed standard IT retention policies.

==================================================
HOW TO USE GOVERNANCE CONTEXT IN ARTICLES
==================================================

1. Apply governance context where it directly intersects with the article’s infrastructure, deployment, or platform decisions.

2. Do NOT force regulatory content into articles about general AI strategy, market trends, or organizational change where no specific regulatory constraint applies.

3. Use governance as a TRADE-OFF LENS: the cost of compliance is real and should be weighed against the cost of non-compliance (fines, reputational damage, remediation). Present it as an executive decision, not a checklist.

4. When multi-cloud orchestration or hybrid deployment is discussed, always note that data residency constraints may limit geographic flexibility — this is a non-obvious cost of the multi-cloud model that executives consistently underestimate.

5. Avoid generic "data privacy matters" language. Name the specific regulation, the specific enterprise obligation, and the specific architectural implication.
"""
