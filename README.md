# 🔐 SecurePipe — DevSecOps Security Pipeline

![Pipeline](https://img.shields.io/badge/pipeline-GitHub%20Actions-blue)
![SAST](https://img.shields.io/badge/SAST-Bandit%20%7C%20Semgrep-orange)
![DAST](https://img.shields.io/badge/DAST-OWASP%20ZAP-red)
![Deps](https://img.shields.io/badge/deps-pip--audit-green)
![Docker](https://img.shields.io/badge/container-Docker-blue)

A fully automated DevSecOps pipeline that integrates **SAST**, **DAST**, and **dependency scanning** into a GitHub Actions CI/CD workflow for a containerized Python web application.

> Built to demonstrate secure software development lifecycle (SSDLC) practices — every push triggers automated security testing, and results are consolidated into a single security summary report.

---

## 🏗️ Architecture

```
Code Push / PR
      │
      ▼
┌─────────────────────────────────────────┐
│           GitHub Actions Pipeline        │
│                                         │
│  ┌──────────┐  ┌──────────────────┐    │
│  │  SAST    │  │ Dependency Scan  │    │
│  │ (Bandit  │  │  (pip-audit)     │    │
│  │ Semgrep) │  │                  │    │
│  └────┬─────┘  └────────┬─────────┘    │
│       │                 │              │
│       └────────┬────────┘              │
│                ▼                       │
│         ┌─────────────┐               │
│         │ Docker Build │               │
│         │  + Test      │               │
│         └──────┬───────┘               │
│                ▼                       │
│         ┌─────────────┐               │
│         │  DAST        │               │
│         │ (OWASP ZAP)  │               │
│         └──────┬───────┘               │
│                ▼                       │
│      ┌──────────────────┐             │
│      │ Security Summary │             │
│      │     Report       │             │
│      └──────────────────┘             │
└─────────────────────────────────────────┘
```

---

## 🛠️ Tools Used

| Category | Tool | Purpose |
|----------|------|---------|
| SAST | [Bandit](https://github.com/PyCQA/bandit) | Python-specific vulnerability detection |
| SAST | [Semgrep](https://semgrep.dev) | Multi-rule static analysis |
| Dependency Scan | [pip-audit](https://github.com/pypa/pip-audit) | CVE detection in Python dependencies |
| DAST | [OWASP ZAP](https://www.zaproxy.org/) | Runtime vulnerability scanning |
| Container | [Docker](https://docker.com) | App containerization |
| CI/CD | [GitHub Actions](https://github.com/features/actions) | Pipeline orchestration |

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Git

### Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/securepipe.git
cd securepipe

# Build and run with Docker Compose
docker compose up --build

# App runs at http://localhost:5000
```

### Run Security Scans Locally

```bash
# Install tools
pip install bandit pip-audit semgrep

# SAST
bandit -r app/

# Dependency scan
pip-audit -r app/requirements.txt

# DAST (requires running app)
docker compose up -d
docker compose --profile dast up zap
```

---

## 🔍 Intentional Vulnerabilities (for demo purposes)

This app contains **deliberate vulnerabilities** to showcase what the tools detect:

| Vulnerability | Location | Detected By |
|--------------|----------|-------------|
| Hardcoded secret | `app.py:8` | Bandit (B105) |
| SQL Injection | `/user` endpoint | Bandit (B608) + ZAP |
| Command Injection | `/ping` endpoint | Bandit (B602) |
| Outdated dependency | `Jinja2==3.0.0` | pip-audit |

> ✅ See the `fix/remediation` branch for the patched version with all vulnerabilities resolved.

---

## 📊 Pipeline Results

After each push, GitHub Actions generates:
- **SAST reports** (Bandit JSON + Semgrep JSON)
- **Dependency report** (pip-audit JSON)
- **ZAP DAST report** (HTML + JSON)
- **Consolidated security summary** (Markdown, posted to job summary)

---

## 📁 Project Structure

```
securepipe/
├── .github/
│   └── workflows/
│       └── devsecops.yml      # Main CI/CD pipeline
├── .zap/
│   └── rules.tsv              # ZAP rule suppressions
├── app/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Container definition
├── scripts/
│   └── generate_report.py     # Security report generator
├── tests/
│   └── test_app.py            # Unit tests
├── reports/                   # Generated reports (gitignored)
├── docker-compose.yml
└── README.md
```

---

## 🧠 Key Learnings

- **Shift-left security**: catching vulnerabilities in code *before* they reach production
- **Defense in depth**: no single tool catches everything — SAST + DAST + SCA together provide layered coverage
- **Pipeline-as-policy**: failing builds on critical findings enforces security as a hard requirement
- **Container security**: non-root users, minimal base images, health checks

---

## 📝 Blog Post

Read the full write-up: [How I Built a DevSecOps Pipeline That Catches Vulnerabilities Before They Reach Production](#)

---

## 👤 Author

**Saniya Bhaladare**  
M.S. Cybersecurity Engineering, University of Washington Bothell  
[LinkedIn](https://linkedin.com/in/saniyabhaladhare) | [Portfolio](https://saniyabhaladhare.me)
