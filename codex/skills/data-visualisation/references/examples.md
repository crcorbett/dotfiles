# Examples

## 1. Ranked comparison with explanatory labels

**Question:** Which practice areas had the highest median time to resolution in FY2025, and how stable is that ordering?

**Grammar:** completed matters -> calculate median, interval, and sample count -> raw points + interval + direct text -> aligned position on a zero-day scale -> ordered rows -> labels for sample count, source, and exclusion rule.

**Why it passes:** Individual matters and a summary support macro/micro reading; a shared scale makes ranking inspectable; the interval shows variation.

**Failing version:** Five isolated medians, no sample count/spread, and a hidden 40-day baseline. It exaggerates magnitude and strips out evidence needed to evaluate the order.

## 2. Release-date time series without causal overclaim

**Question:** How did checkout conversion differ by device through 2025 around a 15 July redesign?

**Grammar:** month-device rows -> rate from numerator/eligible sessions -> line + point + release rule -> common time/rate scales -> direct endpoint labels -> annotation that July has mixed exposure and the view is descriptive.

**Why it passes:** Full calendar, common rate scale, denominator, and mixed treatment remain visible. The release is context, not proof.

**Failing version:** A cropped before/after bar pair claiming the redesign lifted conversion. It confounds time, traffic mix, and treatment.

## 3. Small multiples for repeated comparison

**Question:** Did each region's monthly revenue pattern change from 2024 to 2025?

**Grammar:** region-month rows -> calendar alignment -> line marks -> common y and month domains -> one panel per region -> direct labels plus common events.

**Why it passes:** Constant design turns panels into controlled comparisons; shared domains prevent a quiet panel looking as volatile as a high-variance panel.

**Colour check:** If the decision concerns one region against the whole, use neutral regional traces, a dark aggregate/reference, and one accent for the selected region. Many categorical hues are justified only when tracing each series across views is necessary.

## 4. Dense table-graphic for exact decisions

**Question:** Which experiment arms have a practically meaningful difference, with intervals and sample sizes?

**Grammar:** arm estimates -> calculate interval and rank -> table with decimal-aligned values + dot/interval column -> common effect scale -> direct comparator rule -> source, confidence level, and model note.

**Why it passes:** Exact lookup and pattern recognition coexist; words, values, and marks share one reading surface.

**Failing version:** A colourful donut of point estimates. It cannot support precise reading or show uncertainty.

## 5. Spatial evidence without misleading area

**Question:** Where are reported incidents concentrated after accounting for population exposure?

**Grammar:** geocoded incidents + population denominator -> rate and uncertainty -> points/grid cells or labelled rate map -> geographic coordinate -> optional time panels -> reporting-quality limits.

**Why it passes:** It avoids allowing large empty administrative areas to dominate visual magnitude, and makes the denominator visible.

**Failing version:** A filled county map of raw counts. Geographic area, not the quantity of interest, becomes dominant.

## 6. Editorial focus-plus-context ranking

**Question:** How does a selected country's maternal-mortality rate compare with peer countries and a regional median?

**Grammar:** country-rate rows -> sort and calculate median -> ordered neutral dots -> common rate scale -> selected country in one non-valenced accent + dark median rule -> direct values, source, denominator, and year.

**Why it passes:** Every country remains available for comparison, while one accent carries a necessary question-specific focus. The median is a data-built benchmark.

**Failing version:** Every country receives a different hue even though all are directly labelled and no group is analytically focal.

## 7. Dense scatter with an editorial finding

**Question:** Which metro areas are unusual in the relationship between rent burden and vacancy rate?

**Grammar:** metro rows -> validate population threshold -> muted semi-transparent points -> common x/y scales + quiet references -> direct labels only for named outliers -> source and non-causal qualification.

**Why it passes:** Context points reveal density while labels make a few decision-relevant observations inspectable. A fit is descriptive unless stronger design supports inference.

**Failing version:** Opaque multi-colour dots with a categorical legend for every region. It obscures density and makes readers decode irrelevant categories.

## 8. Dual-scale challenge

**Question:** Did fuel price and commuter trips change together over time?

**Grammar:** month-series rows -> first try aligned panels and indexed lines -> only if dual axis remains necessary, record rationale, direct axis/series association, zero-alignment assessment, and alternative view.

**Why it passes:** The comparison does not rely on a forced correlation; scale relationship remains inspectable.

**Failing version:** Two unrelated axes stretched until their lines appear to move together, with a title implying one series drove the other.

## 9. Route narrative that retains place and sequence

**Question:** Where in a morning delivery route do late handoffs accumulate, and does their order suggest a recurring bottleneck?

**Grammar:** stop-time-delay rows -> order by scheduled stop and calculate exposure-adjusted late rate -> connected route with directly labelled stop sequence + aligned delay-by-stop strip -> geographic coordinate and ordered stop index -> direct labels for salient stops, route coverage, and reporting limitation.

**Why it passes:** The route connection and sequence are both evidence, while the aligned strip gives an exact common-scale comparison. A reader can recover location, order, and local delay without guessing from colour.

**Failing version:** Pins in different colours on a base map. The reader cannot tell route order, compare delays, or distinguish a real bottleneck from differing stop volume.

## 10. Honest handling of an extreme value

**Question:** How do branch approval rates compare when one branch is far above the rest?

**Grammar:** branch-rate rows -> retain common percentage scale or use a main comparison plus clearly labelled detail panel -> ordered dots with direct values -> explicit domain and any range omission -> neutral branches plus one question-relevant accent.

**Why it passes:** It does not use an invisible broken axis to amplify small differences. If an exceptional-value detail is needed, the reader sees the scale change and the original common-scale comparison remains available.

**Failing version:** A broken y-axis without a discontinuity marker or omitted-range label. It creates a sharper apparent gap while concealing the scale change.
