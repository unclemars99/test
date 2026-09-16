# D009 — Bounded-window sampling for very large ADR tables

## Context

A first-pass ADR proxy collector attempted to retrieve high-ADR samples from a very large production table using a global filter plus `ORDER BY ... LIMIT`. The database resource group rejected the query because the sort/filter plan exceeded the query-memory limit.

## Decision

For ADR proxy experiments, do not use full-table counts or global ordering as part of the primary sampling path.

Use bounded chronological windows instead:

1. fix the study population and study time range first;
2. query small time windows independently;
3. use a small `LIMIT` per window and no global `ORDER BY`;
4. preserve both electrode polarities but match references within the same device/process context;
5. obtain one low-ADR reference per high-ADR sample from progressively wider local time windows;
6. if time-nearest selection is needed, retrieve a small unsorted candidate set and choose nearest in Python rather than sorting a large relation in the database.

## Rationale

This changes only data-access mechanics, not the scientific hypothesis. It reduces database load, avoids memory-intensive global sorts, and naturally produces a time-distributed sample instead of selecting one dense region of a massive table.

## Scientific boundary

ADR remains a waveform-derived anomaly proxy, not independent teardown/pull-test quality truth. It is suitable for testing representation sensitivity to high-confidence waveform anomalies, not for claiming direct physical-quality validation.
