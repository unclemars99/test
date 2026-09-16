# E001 — Strict Ultrasonic Process Token Validation

## P

Does an explicit physical-stage representation improve cross-equipment process transfer compared with ordinary time-coordinate representations?

## Setup

A strict two-domain comparison was built under matched material/polarity/recipe context. Each domain contributed about 5k unlabeled production waveforms. No proprietary identifiers or raw data are stored in this repository.

The physical structure was frozen as:

`P1 -> Gap -> P2`

Baselines:

- Fixed whole-wave representation
- Generic masked SSL
- Process-stage representation
- Shuffled-stage negative control

## Evidence

Representative cross-domain results:

- Fixed PCA: ~0.781 mean process-state Spearman
- Process + duration PCA: ~0.869
- Shuffled Process: ~0.604
- Generic masked SSL: ~0.771
- Process masked SSL: ~0.844
- Shuffled Process masked SSL: ~0.829

Future-time results kept the same direction; process-stage representations remained stronger than generic baselines.

## Decision

**Process-stage structure: SUPPORTED on this ultrasonic-welding domain pair.**

This result does not imply that a fully shared latent state has been learned. Equipment identity remains highly decodable from the representation.

## N

Move from the question “Does Process Token help?” to “How should process state and equipment context be separated?”