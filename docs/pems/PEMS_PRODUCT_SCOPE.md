# PEMS — Product Scope & Cross-Chat Handoff Instructions

## 1. Purpose

This document is the broader PEMS product-scope and continuity handoff. It complements, but does not replace, phase-specific implementation handoffs such as:

`docs/phase1h/PHASE1H_CHAT_HANDOFF.md`

The purpose is to preserve the broader PEMS product vision, architecture, domain scope, analytical capabilities, decision-support requirements, deployment strategy, reporting requirements, and governance principles across ChatGPT conversations.

This document should be treated as a product-scope/architecture continuity artifact. It is not a substitute for authoritative source code, specifications, workbook evidence, audit files, tests, or phase-specific implementation state.

---

## 2. Product Identity

PEMS is intended to become a comprehensive Petroleum Economics Modelling and decision-support platform.

PEMS is not merely an Excel replacement, charting application, or desktop calculator.

The broader product scope encompasses:

- petroleum economic modelling;
- production and development economics;
- fiscal modelling;
- asset and project evaluation;
- investment evaluation;
- bid-round evaluation;
- scenario analysis;
- sensitivity analysis;
- probabilistic/Monte Carlo analysis;
- portfolio analysis and optimization;
- project screening and selection;
- reporting and decision documentation;
- visualization;
- auditability and traceability;
- API-based integration;
- enterprise deployment;
- user-facing diagnostics, help and AI-assisted explanation.

---

## 3. Core Architectural Principle

The PEMS Economic Engine is the product core.

Presentation clients must not contain independent economic implementations.

The intended architecture is:

    Users
      |
      +----------------+----------------+----------------+
      |                |                |
    Desktop           Web              API
      |                |                |
      +----------------+----------------+
                       |
                       v
              Application / Service Layer
                     RunService
                       |
                       v
               PEMS Economic Engine
                       |
          +------------+------------+
          |            |            |
      Production     Fiscal      Economics
        Engine       Engine       Engine
          |            |            |
          +------------+------------+
                       |
                       v
             Authoritative Result DTOs
                       |
          +------------+------------+
          |            |            |
        Charts       Reports     Analytics
                       |
                       v
                Decision Support

The same authoritative calculation/result layer should serve:

- PySide6 desktop;
- future web UI;
- API clients;
- batch processing;
- Monte Carlo;
- scenario analysis;
- sensitivity analysis;
- portfolio optimization;
- reporting.

---

## 4. Application / Service Layer

PEMS should preserve separation between:

1. UI/presentation;
2. application/service orchestration;
3. domain/economic engines;
4. authoritative result DTOs;
5. presentation/reporting/analytics.

The application/service layer, including the intended RunService pattern, should orchestrate calculations without embedding the underlying economic formulas in the UI.

A conceptual execution flow is:

    PEMS UI
       |
       v
    RunService
       |
       +--> validation
       |
       +--> production calculation
       |
       +--> fiscal calculation
       |
       +--> cash-flow calculation
       |
       +--> economics calculation
       |
       v
    Authoritative Results DTO
       |
       +--> charts
       +--> tables
       +--> reports
       +--> Monte Carlo
       +--> sensitivity
       +--> portfolio analytics

---

## 5. Multi-Client and Deployment Strategy

PEMS is intended to be server-capable and API-first.

Target clients/deployment modes include:

### Desktop

A rich engineering/economic-analysis client, initially compatible with the Python/PySide6 direction.

### Web

A browser-based client consuming the same application/service and economic engine.

### API

An API interface for:

- external applications;
- enterprise systems;
- automated workflows;
- batch evaluations;
- integrations;
- future PEMS clients.

### Deployment

PEMS should be capable of:

- local desktop deployment;
- internal enterprise server;
- private cloud;
- on-premise enterprise;
- hybrid deployment.

The architecture must therefore avoid assumptions that all calculation state and processing permanently reside in a single desktop application.

---

## 6. Petroleum Economics Engine

The core deterministic calculation chain should support, as applicable:

    Inputs
      |
    Reservoir / Production assumptions
      |
    Production profile
      |
    Prices
      |
    Revenue
      |
    CAPEX
      |
    OPEX
      |
    Royalty
      |
    Taxes
      |
    Government / Contractor economics
      |
    Cash flow
      |
    Discounting
      |
    NPV / IRR / economic indicators

The calculation engine is the authoritative source for economic values.

Presentation code must not recreate formulas merely to produce charts, reports or dashboards.

---

## 7. Fiscal Framework

PEMS should be extensible beyond a single country or fiscal regime.

The intended abstraction is:

    Country
       |
    Fiscal Regime
       |
    Contract / Licence Type
       |
    Fiscal Terms
       |
    Economic Calculation

The fiscal architecture should support, as applicable:

- different countries;
- different petroleum fiscal regimes;
- PSCs;
- concessionary systems;
- PIA-based regimes;
- royalty systems;
- tax systems;
- contractual variations;
- regimes where particular fiscal clauses are omitted or configured differently.

The architecture should avoid scattering country-specific formulas throughout the core engine.

---

## 8. Royalty and Tax Extensibility

Royalty support should accommodate different structures, including:

- fixed royalty;
- sliding-scale royalty;
- jumping-scale royalty;
- other configured/contractual royalty structures.

Tax support should accommodate different regimes and rates rather than permanently hard-coding one tax formula.

Nigeria-specific PIA 2021 modelling remains an important implementation domain, including applicable:

- royalty;
- tax;
- hydrocarbon tax;
- cost recovery;
- production-sharing;
- concessionary;
- contractual/fiscal-transition logic.

PSC-to-concessionary conversion and related Nigerian asset evaluations are also within the broader domain scope where applicable.

---

## 9. Petroleum / Asset / Project Use Cases

PEMS should support economic evaluation across:

- petroleum assets;
- fields;
- development projects;
- investment opportunities;
- acquisition opportunities;
- bid-round opportunities;
- alternative development concepts;
- contractual/fiscal alternatives.

Existing Nigerian modelling work and examples such as OML 20, OML 56, OML 65 and NUPRC bid-round evaluations are use cases/evidence of application, not justification for hard-coding those assets into PEMS.

---

## 10. Scenario Analysis

PEMS should support controlled scenario analysis.

Examples include:

- Low Case;
- Base Case;
- High Case;
- Scenario A/B/C;
- user-defined scenarios.

Scenario variables may include:

- production;
- prices;
- CAPEX;
- OPEX;
- fiscal assumptions;
- development schedule;
- reserves;
- recovery assumptions.

Scenario outputs must originate from authoritative scenario calculations/results.

Presentation code must not invent scenario series.

---

## 11. Sensitivity Analysis

PEMS should ultimately support:

- one-way sensitivity;
- two-way sensitivity;
- multi-variable sensitivity;
- tornado analysis;
- sensitivity matrices;
- parameter-impact analysis.

Sensitivity calculations belong in the appropriate analytical/model layer.

Charts should consume authoritative sensitivity result DTOs.

The Phase 1H STOIIP/GIIP sensitivity charts are currently blocked/deferred where the required authoritative sensitivity DTO structures do not yet exist.

---

## 12. Probabilistic / Monte Carlo Analysis

PEMS should provide probabilistic analysis comparable conceptually to tools such as @RISK or Crystal Ball.

The capability should support uncertainty in inputs such as:

- oil price;
- gas price;
- production;
- CAPEX;
- OPEX;
- reserves;
- start-up date;
- recovery factor;
- fiscal assumptions.

Potential distributions include, where appropriate:

- triangular;
- normal;
- lognormal;
- uniform;
- PERT;
- discrete;
- user-defined distributions.

Potential outputs include:

- NPV distributions;
- IRR distributions;
- P10/P50/P90;
- probability of positive NPV;
- probability of achieving a hurdle rate;
- risk distributions;
- tornado/sensitivity relationships.

Monte Carlo should repeatedly invoke the authoritative economic engine rather than implement a second economic model.

---

## 13. Portfolio Analysis & Optimization

Portfolio Analysis & Optimization is a major PEMS capability.

PEMS must explicitly classify projects as:

- Mutually Exclusive (ME); or
- Non-Mutually Exclusive (NME)

before portfolio selection/optimization.

This classification is a standing product requirement.

### 13.1 Mutually Exclusive Projects

ME projects are competing alternatives where only the appropriate alternative(s) within a defined mutually exclusive group may be selected.

Examples include alternative development concepts.

PEMS should:

- identify the ME group;
- evaluate alternatives against one another;
- apply appropriate ranking/selection logic;
- enforce the mutual-exclusion constraint;
- incorporate capital-budget and other applicable constraints.

### 13.2 Non-Mutually Exclusive Projects

NME projects can potentially be selected independently, subject to constraints.

PEMS should use screening based on user-defined:

- priorities;
- thresholds;
- strategic criteria;
- financial criteria;
- technical criteria;
- risk criteria;
- capital constraints;
- dependencies.

Only qualifying projects should proceed to portfolio consideration.

### 13.3 Critical Rule

PEMS must not apply one universal ranking method indiscriminately to ME and NME projects.

The classification must influence the selection/optimization workflow.

---

## 14. Capital-Budget Constrained Optimization

Portfolio optimization should support constraints such as:

- maximum available CAPEX;
- minimum NPV;
- minimum IRR;
- production targets;
- risk limits;
- strategic requirements;
- project dependencies;
- ME constraints;
- timing constraints.

Potential objectives include:

- maximize NPV;
- maximize IRR or value-related metrics;
- maximize value per capital;
- maximize production;
- minimize risk;
- maximize strategic score;
- user-selected objective functions.

---

## 15. Modern Portfolio Theory Concepts

Where analytically appropriate, PEMS should support Modern Portfolio Theory concepts, including:

- expected return/value;
- risk;
- covariance/correlation;
- diversification;
- risk-adjusted selection;
- efficient-frontier concepts.

The portfolio engine should be capable of recognizing correlated project outcomes, including common exposure to:

- commodity prices;
- fiscal assumptions;
- geography;
- development assumptions;
- market assumptions.

---

## 16. Project Screening

Portfolio analysis should have a screening stage before optimization.

Potential screening criteria include:

- NPV threshold;
- IRR threshold;
- payout;
- capital requirement;
- production target;
- reserves;
- strategic importance;
- technical readiness;
- risk;
- fiscal attractiveness;
- development timing;
- corporate priorities.

The screening framework is particularly important for NME projects.

---

## 17. Project Domain Requirements for ME/NME

The project domain should eventually represent selection relationships explicitly.

Conceptually:

    Project
      |
      +-- project_id
      +-- name
      +-- project_type
      +-- selection_class
      |      +-- MUTUALLY_EXCLUSIVE
      |      +-- NON_MUTUALLY_EXCLUSIVE
      |
      +-- exclusive_group_id
      +-- dependencies
      +-- constraints
      +-- economic_results

The exact implementation should follow the authoritative domain specification when created; this conceptual structure must not be treated as an already-implemented schema.

---

## 18. Bid and Investment Evaluation

PEMS should support bid-level and investment decision workflows, including:

- bid economics;
- economic ranking;
- fiscal comparison;
- asset-level evaluation;
- bidder/project comparison;
- competing scenarios;
- NBO support;
- LOI support;
- decision documentation.

NUPRC bid-round work is a significant application domain.

---

## 19. Reporting

PEMS should ultimately generate professional reports from authoritative results.

Target report classes include:

- economic evaluation reports;
- project evaluation reports;
- bid evaluation reports;
- NBO documents;
- LOI support documents;
- portfolio reports;
- sensitivity reports;
- Monte Carlo reports;
- management summaries;
- technical/economic appendices.

Reports must consume authoritative calculation results rather than reproduce economic formulas independently.

---

## 20. Traceability and Auditability

A core PEMS principle is:

    Where did this number come from?

Users should be able to trace a result through the calculation chain.

For example:

    NPV
      |
    Cash Flow
      |
    Tax / Royalty
      |
    Revenue
      |
    Production
      |
    Input Assumption

Traceability should be available wherever practical and should preserve links between inputs, calculations, DTO outputs and presentation/reporting results.

---

## 21. Calculation Trace

PEMS should support a calculation-trace/debugging layer.

A result should eventually be explainable in terms of its authoritative calculation chain rather than appearing as a black-box number.

Example:

    Revenue = Production × Price
    Royalty = ...
    Taxable Income = ...
    Tax = ...
    Contractor Cash Flow = ...
    Discounted Cash Flow = ...
    NPV = ...

The exact formula presentation must reflect the authoritative engine implementation.

---

## 22. Model-Health Diagnostics

PEMS should provide model-health diagnostics for issues such as:

- missing required inputs;
- inconsistent year keys;
- invalid assumptions;
- missing result maps;
- fiscal configuration conflicts;
- production inconsistencies;
- incomplete scenarios;
- incompatible portfolio constraints;
- invalid dependencies;
- unavailable authoritative outputs.

Diagnostics should distinguish, where appropriate:

- ERROR;
- WARNING;
- INFO.

---

## 23. Actionable Errors

PEMS errors should be understandable and actionable.

Avoid exposing low-level implementation errors as the primary user experience.

Instead of only reporting an internal exception, PEMS should explain:

1. what failed;
2. what data/condition caused it;
3. what component is affected;
4. what the user should check or do next.

---

## 24. AI-Assisted User Support

PEMS may include an AI assistance layer around the deterministic engine.

AI can assist with:

- model navigation;
- error explanation;
- calculation explanation;
- fiscal-term explanation;
- sensitivity interpretation;
- Monte Carlo interpretation;
- portfolio-result interpretation;
- user guidance;
- identification of suspicious/incomplete inputs.

AI must not silently replace or alter the deterministic economic engine.

Authoritative calculations remain deterministic and traceable.

---

## 25. Authoritative DTO Principle — PEMS-Wide

The Phase 1H presentation rule should be elevated to a broader PEMS architectural principle:

    Calculation Engine
          |
          v
    Authoritative Result DTO
          |
      +---+---+---+---+
      |   |   |   |   |
     UI Charts Reports Analytics API

Consumers must not recreate authoritative economics.

This applies not only to charts, but eventually to:

- dashboards;
- reports;
- portfolio analytics;
- Monte Carlo;
- sensitivity visualization;
- API output;
- other presentation/decision-support layers.

If a required output is not represented faithfully by an authoritative DTO, the correct response is to add or locate the authoritative model output, not to manufacture it in the consumer layer.

---

## 26. Workbook Relationship

The Excel workbook is an important source of semantic/reference evidence during migration and validation.

The long-term direction is:

    Workbook
       |
    Semantic Mapping / Evidence
       |
    PEMS Domain Model
       |
    PEMS Economic Engine
       |
    Authoritative DTOs
       |
    Clients / Charts / Reports

Workbook formulas and chart behavior must not be blindly duplicated into presentation code.

Where workbook semantics are authoritative for a specific implementation task, they must be reconciled against the audit/specification and current code reality.

---

## 27. Workbook Parity

PEMS development should distinguish:

- architecture implemented;
- semantic mapping established;
- implementation authorized;
- implementation completed;
- model/DTO dependencies completed;
- UI integrated;
- workbook parity validated;
- release-ready.

Passing automated tests does not by itself establish workbook parity.

---

## 28. Product Milestones

The broader PEMS development can be viewed through:

### Milestone A — Architecture
Core structures and separation are established.

### Milestone B — Domain/Semantic Mapping
Authoritative domain and workbook mappings are established where required.

### Milestone C — Authorization
Implementation scope is explicitly authorized.

### Milestone D — Implementation
Authorized capabilities are implemented.

### Milestone E — Model/DTO Completion
Missing authoritative outputs are added at the correct calculation/model layer.

### Milestone F — UI/Client Integration
Clients consume authoritative services/results.

### Milestone G — Validation / Workbook Parity
Rendered and serialized behavior is validated against authoritative evidence.

### Milestone H — Release
Regression, audit reconciliation, documentation, deployment and release controls are complete.

---

## 29. Governance and Information Hierarchy

When information conflicts, use this order of authority:

1. Explicit current PO direction for scope/authorization.
2. Authoritative audit/specification/workbook evidence for specific chart/model semantics.
3. Current repository code and DTO definitions for implementation reality.
4. Current tests and verification output for behavioral evidence.
5. This product-scope handoff for synthesized product continuity.
6. Conversation history for working context only.

This handoff must never override an authoritative source.

---

## 30. Phase-Specific Work Must Remain Separate

The broader product scope must not cause unrelated work to be started automatically.

For Phase 1H specifically:

- use `docs/workbook/semantic_mapping/CHART_MAPPING_AUDIT.csv` as chart-audit authority;
- preserve presentation-only DTO projection;
- preserve all Phase 1H blockers/deferred boundaries;
- do not invent DTO fields;
- do not invent workbook mappings;
- do not claim workbook parity prematurely.

The Phase 1H handoff remains the canonical current-state document for that phase.

---

## 31. Phase 1H Current-State Reference

At the time of this broader scope handoff:

- five core chart families are implemented;
- current verification baseline is 49 passed with 1 pre-existing slow-mark warning;
- the staged slice contains five files;
- no commit had been performed according to the Phase 1H handoff;
- Production Profile is blocked by missing PP cumulative DTO support;
- Equity CashFlow is blocked by missing annual/cumulative equity DNCF DTO support;
- STOIIP/GIIP sensitivity charts are deferred/blocked by missing sensitivity DTOs;
- OML123 scenario is blocked by missing scenario DTO;
- Prod_Summary chart #1 / column C is semantically unresolved;
- Analysis/sensitivity/Monte Carlo chart work remains deferred;
- FLGT HCDT gas/NDDC gas inclusion must follow authoritative chart evidence.

See the Phase 1H handoff for exact implementation state and evidence.

---

## 32. Continuation Rules for New ChatGPT Conversations

When this file is uploaded into a new conversation, use the following operating instruction:

> Continue the PEMS project from this Product Scope & Cross-Chat Handoff. Treat this document as the broader PEMS product-scope and architecture continuity baseline. Do not assume that every capability described here is already implemented. Distinguish product requirements, current implementation, planned capability, blocked work, and deferred work. Treat authoritative repository code, DTO definitions, specifications, workbook evidence and audit files as higher authority than this handoff when they conflict.
>
> For phase-specific implementation work, use the relevant phase handoff as the current-state authority. For Phase 1H, use `docs/phase1h/PHASE1H_CHAT_HANDOFF.md` and `docs/workbook/semantic_mapping/CHART_MAPPING_AUDIT.csv`.
>
> Preserve the PEMS architecture: Economic Engine → authoritative DTOs → application/service layer → clients/presentation/analytics. Do not put economic calculations into presentation code.
>
> Preserve the Portfolio Analysis & Optimization rule: classify projects explicitly as Mutually Exclusive (ME) or Non-Mutually Exclusive (NME) before selection/optimization. Use appropriate competitive selection/ranking and capital-budget optimization for ME alternatives; use screening against user-defined priorities, thresholds, strategic criteria and constraints for NME projects. Do not apply one universal ranking method to both.
>
> Do not invent DTO fields, calculations, fiscal formulas, workbook mappings, scenario outputs or parity claims. If a required authoritative output is missing, identify the dependency and escalate it to the correct model/domain layer.
>
> Use focused execution commands where appropriate:
>
> `STATUS` — current state across product/phase, implementation, audit, tests, Git and blockers.
>
> `STATUS DELTA` — changes since the last checkpoint.
>
> `NEXT` — one highest-priority evidence-backed action.
>
> `AUDIT` — reconcile implementation against the authoritative audit/specification.
>
> `VERIFY` — perform relevant tests, compile/checks, staging and validation.
>
> `BLOCKERS` — report only issues preventing the next meaningful action.
>
> `DECISION` — record a decision, rationale, authority/evidence and consequence.
>
> `CHECKPOINT` — capture the current project state for continuity.
>
> `HANDOFF` — generate an updated cross-chat handoff.
>
> `STOP` — stop implementation and report state/blockers without making further code changes.

---

## 33. Do Not List

Do not:

- treat PEMS as only an Excel/chart replacement;
- couple economic calculations to a UI;
- create separate economic implementations for charts, reports, Monte Carlo or optimization;
- hard-code one country/fiscal regime into the entire engine;
- assume one royalty or tax formula applies universally;
- apply one portfolio-selection method to ME and NME projects;
- treat ME alternatives as independently selectable projects;
- optimize NME projects without appropriate screening;
- invent missing authoritative DTO outputs in presentation/analytics code;
- manufacture cumulative values from annual values when the authoritative cumulative result is absent;
- manufacture equity economics by scaling unrelated project economics;
- infer scenario outputs without authoritative scenario results;
- claim workbook parity merely because tests pass;
- allow AI assistance to silently change authoritative deterministic economics.

---

## 34. Recommended Canonical Documentation Structure

Preferred project documentation structure:

    docs/
    |
    +-- pems/
    |   +-- PEMS_PRODUCT_SCOPE.md
    |   +-- PEMS_ARCHITECTURE.md
    |   +-- PEMS_DOMAIN_MODEL.md
    |   +-- PEMS_ROADMAP.md
    |
    +-- phase1h/
    |   +-- PHASE1H_CHAT_HANDOFF.md
    |
    +-- workbook/
        +-- semantic_mapping/
            +-- CHART_MAPPING_AUDIT.csv

Maintain one canonical product-scope document rather than creating multiple versions such as:

    PEMS_SCOPE_v1.md
    PEMS_SCOPE_v2.md
    PEMS_SCOPE_FINAL.md
    PEMS_SCOPE_FINAL2.md

Use Git history for historical versions.

---

## 35. Scope Status Discipline

Every major capability should eventually be classified as one of:

- REQUIRED — product requirement;
- IMPLEMENTED — implemented in authoritative code;
- AUTHORIZED — explicitly authorized for implementation;
- IN PROGRESS — active implementation;
- BLOCKED — cannot proceed because an authoritative dependency is missing;
- DEFERRED — intentionally postponed;
- VALIDATED — independently validated;
- RELEASED — included in a released product version.

Do not use "implemented" as a synonym for "validated" or "release-ready".

---

## 36. Final Continuity Principle

The objective of this handoff is to preserve the distinction between:

    What PEMS is
    +
    What PEMS should become
    +
    What is currently implemented
    +
    What is currently authorized
    +
    What is blocked/deferred
    +
    What has actually been validated

A future ChatGPT conversation must not collapse these into a single status.

PEMS should continue to be developed as a modular, auditable, extensible petroleum economics and decision-support platform whose deterministic economic engine remains the authoritative source of economic truth.
