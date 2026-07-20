# Python grammar playbook

Use Python when it is the requested output surface or analysis is best expressed in a Python pipeline. Keep data transformation explicit and produce a static render that receives the same inspection as a browser chart.

## Declarative pattern

Use a declarative chart for explicit fields, transforms, and scales. Keep domain, baseline, marks, direct labels, and source/qualification visible in the output.

## ggplot-style pattern

```py
(ggplot(monthly, aes("month", "actual"))
 + geom_line()
 + geom_point()
 + labs(x="Month", y="Revenue (EUR)", title="Monthly revenue")
 + theme_minimal())
```

Use `geom_col()` only with a zero baseline. Use points/lines when a restricted domain is defensible and disclosed. Build small multiples with shared limits when panel comparison matters.

## Checks

- Validate input rows, transformations, and plotted values in code.
- Save a full-size and narrow render where delivery needs it.
- Run the portable specification linter and complete the same human rubric used for TypeScript charts.
