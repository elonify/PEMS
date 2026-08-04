# GOVERNANCE.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Project governance  

---

## 1. Purpose

Defines ownership, decision rights, change control, contribution rules, release authority, and documentation control for PEMS.

---

## 2. Roles

| Role | Responsibility |
|------|----------------|
| Project Owner | Final authority on scope, releases, Golden Master approval |
| Architecture Owner | Architecture integrity; ADR acceptance |
| Validation Owner | Validation methodology, tolerances, release validation sign-off |
| Implementation Engineer | Module implementation and unit tests |
| Reviewer | PR / change review against architecture and validation |

One person may hold multiple roles on a small team.

---

## 3. Documentation Control

- Active suite = Documentation Baseline **v2.1** only.  
- Changes to governance/architecture require Project Owner acknowledgement for material items.  
- `docs/archive/` holds superseded material; clearly LEGACY; never authoritative.  
- Cross-references must use current paths under `docs/`.  
- Version label **v2.1** appears on active core documents.

---

## 4. Change Control

### 4.1 Software change

```text
Proposal → Architecture impact → Spec update → Implementation
→ Tests → Workbook validation (if calc) → Review → Merge → Tracker/Changelog
```

### 4.2 Golden Master change

```text
Receive workbook → Identity + checksum → Diff → Impacted modules
→ Update mapping & specs → Update expected datasets → Implement
→ Full regression → Archive validation evidence → Approve new Golden Master
```

### 4.3 Technology change

Must be recorded as an Architectural Decision (see ARCHITECTURAL_DECISIONS.md) before widespread use.

---

## 5. Branch Strategy

```text
main
develop
feature/<module>
release/<version>
hotfix/<issue>
```

Only validated code merges to `main`.

---

## 6. Release Authority

A release requires:

- regression pass  
- no open critical validation failures  
- documentation current  
- workbook version recorded  
- validation reports archived  
- technical, validation, architecture, and Project Owner approval  

Release packaging: see BUILD_AND_DEPLOYMENT.md and release checklist therein.

---

## 7. Contribution Policy

Integrated from former CONTRIBUTING guidance:

1. Read MASTER_IMPLEMENTATION_DIRECTIVE, architecture plan, SYSTEM_DESIGN, VALIDATION_FRAMEWORK, CODING_AGENT_WORKFLOW.  
2. Preserve workbook fidelity and architecture.  
3. Include tests and validation.  
4. Update docs when behaviour or structure changes.  
5. Use conventional commits.  

PR checklist:

- [ ] Architecture compliant  
- [ ] Workbook validated (if applicable)  
- [ ] Unit tests pass  
- [ ] Regression pass (if applicable)  
- [ ] Documentation updated  
- [ ] Commit messages follow convention  

---

## 8. Quality Gates by Phase

No phase is complete until implementation, validation, documentation, and testing criteria for that phase are met (PROJECT_ROADMAP / IMPLEMENTATION_SEQUENCE).

---

## 9. Dispute Resolution

1. Prefer higher document in the authority hierarchy.  
2. Prefer Golden Master for numeric/business behaviour.  
3. Escalate to Project Owner when hierarchy does not resolve the issue.  
4. Record lasting decisions in ARCHITECTURAL_DECISIONS.md.

---

## 10. Security and IP

- Do not commit secrets.  
- Project assets remain proprietary until a license is declared by the Project Owner.  
- Validate external inputs; never trust raw user/import data without validation.
