# Testing and Design Ownership Policy

## Codex owns interactive testing

Codex is responsible for operating and testing the product in real execution environments. This includes:

- browser-based functional and visual testing;
- mobile, desktop, emulator, simulator, and installed-application testing;
- ADB-driven Android testing, log collection, screenshots, screen recordings, hierarchy dumps, layout snapshots, and package inspection;
- device-bridge, CLI, API, database, filesystem, and local-service interaction required to validate behavior;
- reproduction of bugs through actual user flows;
- collection of validation evidence and final interpretation of test results.

Interactive application use must not be delegated to Claude Code merely for convenience. It is generally too expensive and duplicates orchestration work Codex must validate independently anyway.

## Claude owns design-specialist work

Claude Code is preferred for scoped work where UI, UX, visual hierarchy, interaction design, component composition, accessibility presentation, or design-system fidelity is the primary quality concern.

Claude may:

- inspect supplied screenshots, screen recordings, layout snapshots, hierarchy dumps, design specifications, tokens, and component examples;
- compare observed UI evidence against an approved design direction or design system;
- identify visual, usability, consistency, spacing, typography, state, and interaction issues;
- propose or implement bounded UI/UX changes through a task contract;
- review Codex-collected evidence after implementation.

Claude must not launch, navigate, click through, install, operate, or independently test the application. Codex supplies the required evidence and executes every interactive validation step.

## Evidence handoff

When Claude is used for UI/UX or design review, Codex should provide the smallest sufficient evidence package, which may include:

- named screenshots for relevant states and viewport sizes;
- before-and-after captures;
- layout or accessibility hierarchy snapshots;
- exact reproduction steps;
- approved design references and acceptance criteria;
- observed deviations and known platform constraints.

Codex remains responsible for confirming that Claude's recommendations match actual runtime behavior and for re-testing after changes.

## Final accountability

Claude may provide specialist design judgement, but Codex owns:

- runtime truth;
- test execution;
- evidence integrity;
- regression checks;
- acceptance-criteria verification;
- the final completion decision and residual-risk report.
