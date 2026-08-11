# BioHackathon 2026 Project Brief

## Official listing

**Title:** St. Jude AI and Data Learning Assistant: Personalized Guidance Using
The Turing Way and Institutional Knowledge

**Submitters:** Ty Michael, Computational Biology, and Saikat Nandi, St. Jude
Graduate School

**Summary:** This project will build an AI-powered learning assistant that helps
users discover training resources related to data science, AI, software
development, and reproducible research. The assistant will combine content from
The Turing Way with curated institutional resources and deliver role-aware
recommendations through a conversational interface. The system is designed to
support learners across a wide range of expertise and professional backgrounds.

**Benefit:** Personalized navigation of educational resources can improve
onboarding, knowledge discovery, and AI literacy across the institution. By
reducing barriers to finding relevant guidance, the platform supports
self-directed learning and broader adoption of data science best practices. The
framework also demonstrates how open educational resources can be integrated
with institutional knowledge.

**Tools:** LLMs, Python, vector databases, GitHub, retrieval-augmented
generation frameworks, and St. Jude MyGPT where appropriate.

**Test data:** The Turing Way, public educational resources, and approved
institutional materials.

## Challenge

Biomedical research increasingly depends on AI, data science, software,
reproducibility, open science, cloud computing, and collaborative practices.
Useful training already exists, but it is distributed across public and
internal GitHub repositories, Confluence, wikis, and other formats. Non-experts
often lack the time and vocabulary needed to locate the right guidance.

New learners may not know:

- where to begin;
- which resources suit their role or experience;
- how institutional guidance relates to broader reproducible-research practice;
- what to learn at the current stage of a project; or
- how to navigate rapidly changing AI and data-science ecosystems.

Participants will prototype an assistant that combines The Turing Way,
St. Jude-created training materials, and approved institutional resources. The
72-hour scope is deliberately limited to a curated corpus, persona-aware
recommendations, reusable skills, and a conversational demonstration rather
than a production deployment.

## Intended users

- Researchers and research teams
- Technical staff
- Program managers, administrators, and operations teams
- Trainees and students
- Research software engineers
- Data scientists and AI practitioners
- Educators and trainers

## Expected outputs

- A structured resource corpus with public and approved institutional sources
- A lightweight retrieval workflow with measurable baseline behavior
- Persona definitions and recommendation logic
- A polished conversational prototype
- Example user journeys and evaluation cases
- Plug-and-play MCP and Agent Skill documentation
- A retroactive best-practices skill that guides incremental modernization of
  existing research codebases
- Documentation for sustainability after the event

## Success criteria

The demonstration should show that a user can:

1. Ask a natural-language learning question.
2. Select or describe a professional persona and experience level.
3. Receive relevant resources with visible citations.
4. Receive an ordered learning path rather than only free-form prose.
5. Use a skill-driven workflow such as retroactive best practices.
6. Install or connect the released MCP server and skills from a modern AI
   coding client with minimal technical setup.

A stretch goal is a learner profile or avatar that reflects completed topics
without pretending to measure competence solely from chat history.

## Data boundaries

No PHI or patient-level clinical data is needed. The project uses public,
de-identified, or explicitly approved educational material. Resource owners and
institutional stakeholders must approve internal sources before they are added.

## Longer-term impact

The project may support faster onboarding, more equitable access to knowledge,
cross-disciplinary collaboration, and reuse of existing educational resources.
Because The Turing Way is open, the resulting patterns may also help other
research organizations combine institutional guidance with open educational
ecosystems.
