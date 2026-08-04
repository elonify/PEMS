# CONFIGURATION.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Configuration specification  

---

## 1. Purpose

Defines configuration surfaces for PEMS: what is configurable, where it lives, and hard rules about what configuration must never contain.

---

## 2. Hard Rules

- Configuration **must never** contain business calculation logic or fiscal formulas.  
- Calculation behaviour comes from Golden Master-derived code and domain rules.  
- Secrets must not be stored in source control.  
- Tolerances for validation are configuration, not hard-coded magic numbers in random modules.  

---

## 3. Configuration Categories

| Category | Examples | Typical location |
|----------|----------|------------------|
| Application | theme, language, recent files, window state | user config dir |
| Paths | default project dir, workbook path, export dir | user/app config |
| Units preferences | display units | user/project |
| Fiscal defaults | template keys only, not formulas | templates / project |
| Validation tolerances | absolute/relative epsilons by value class | app config + project override policy |
| Logging | level, file path | app config |
| Performance | Monte Carlo default iterations (cap) | app/project |
| Feature flags | experimental UI (if any) | app config |

---

## 4. Tolerance Configuration (required)

Central policy consumed by ValidationService:

| Value class | Policy |
|-------------|--------|
| Integers / counts | Exact match (tolerance 0) unless documented |
| Money / financial floats | Configurable absolute and/or relative |
| Percentages / rates | Configurable |
| General floats | Configurable |

Defaults must be documented when first implemented and versioned with validation datasets.

---

## 5. Project vs Application Scope

| Scope | Contents |
|-------|----------|
| Application | UI preferences, global paths, default tolerances |
| Project | Unit system, currency, template identity, scenario list |
| Scenario | Economic/risk parameters specific to case |

---

## 6. File Layout (logical)

```text
config/
  app.defaults.*
  tolerances.defaults.*
docs/workbook/   # not config — Golden Master assets
```

Exact format open with ADR-0009 / implementation (JSON/TOML/YAML acceptable if consistent).

---

## 7. Loading Order

```text
Built-in defaults → Installation config → User config → Project config → Scenario overrides
```

Later wins if allowed by policy.

---

## 8. Configuration Service

`ConfigurationService` loads/merges settings; exposes typed accessors; validates config schema on load.

---

## 9. Audit

Material config used in a validation run should be recorded in validation reports (tolerance profile id/version).
