# BUILD_AND_DEPLOYMENT.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Build, test, package, and release specification  

---

## 1. Purpose

Defines how PEMS is built, tested, packaged, and released.

Consistent with TECHNOLOGY_STACK (Python, PyInstaller-class packaging) and GOVERNANCE release authority.

---

## 2. Development Environment (Phase 0)

- CPython version pinned (see TECHNOLOGY_STACK)  
- Virtual environment  
- Dependency lockfile  
- Install: project in editable mode when scaffolding exists  
- Pre-commit / lint / format tools as adopted  

---

## 3. Build

| Artifact | Description |
|----------|-------------|
| Source tree | `src/pems` |
| Tests | `tests/` |
| Docs | `docs/` |

Build commands will be recorded here when scaffolding lands (e.g. `python -m build` or project-specific). Until then, Phase 0 creates the skeleton and fills exact commands.

---

## 4. Automated Tests

| Suite | Location | When |
|-------|----------|------|
| Unit | `tests/unit` | Every commit / PR |
| Integration | `tests/integration` | PR / merge |
| Regression | `tests/regression` | PR / release |
| Validation / workbook compare | `tests/validation` | Module complete / release |

CI pipeline (when configured) must run unit + regression at minimum before release tags.

---

## 5. Packaging

### 5.1 Desktop freeze

- **PyInstaller-class** (or ADR-approved equivalent)  
- Produce Windows executable  
- Portable package option  

### 5.2 Installer

- Windows installer under `installer/`  
- Include configuration defaults, documentation package, validation package (as required by release)  

### 5.3 Signing

Digital signing when Project Owner requires for distribution.

### 5.4 Auto-update

Future; not required for first production parity release.

---

## 6. Performance Targets (from tracker heritage)

| Metric | Target |
|--------|--------|
| Application startup | < 5 s (typical hardware, TBD baseline machine) |
| Core calculation (non-MC) | < 2 s typical project |
| Chart render | < 100 ms typical series |

Tune only after correctness.

---

## 7. Release Checklist

### Documentation

- [ ] README updated  
- [ ] Architecture / design current  
- [ ] Validation framework current  
- [ ] Roadmap / sequence / tracker current  
- [ ] Changelog updated  

### Validation

- [ ] Unit tests passed  
- [ ] Integration tests passed  
- [ ] Regression tests passed  
- [ ] Workbook validation passed  
- [ ] Validation reports archived  
- [ ] Workbook version recorded  

### Packaging

- [ ] Windows executable built  
- [ ] Installer created  
- [ ] Configuration packaged  
- [ ] Documentation included  

### QA

- [ ] Manual testing complete  
- [ ] Performance verified  
- [ ] Memory acceptable  
- [ ] Error logs reviewed  

### Version control

- [ ] Git tag created  
- [ ] Release branch merged  
- [ ] Repository synchronized  

### Approvals

- [ ] Technical  
- [ ] Validation  
- [ ] Architecture  
- [ ] Project Owner  

**Status:** READY FOR RELEASE only when all applicable items checked.

---

## 8. Deployment Model

v1: standalone desktop install / portable run. No mandatory server.

Future cloud deployment is out of scope for parity baseline.

---

## 9. Configuration at Deploy

Default tolerances and paths installed; user overrides in user config directory (CONFIGURATION.md).

---

## 10. Rollback

Retain previous installer and Git tag; Golden Master version used for that release recorded in CHANGELOG / release notes.
