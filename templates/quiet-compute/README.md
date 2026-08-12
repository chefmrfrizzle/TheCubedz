# Quiet Compute local templates

These files are forms, not evidence. Copy them outside the repository, replace every template value with an observed or reviewed value, and seal the result locally.

```bash
research-core quiet seal-passport templates/quiet-compute/PASSPORT-ROUND-0.template.json --output work/PASSPORT-ROUND-0.json
research-core quiet seal-measurement templates/quiet-compute/MEASUREMENT.template.json --output work/MEASUREMENT.json
```

The included hashes and measurements are synthetic placeholders chosen only to make the structure machine-testable. They must never be submitted as an experiment.
