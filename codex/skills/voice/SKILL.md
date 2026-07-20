---
name: voice
description: "Write, revise, or diagnose prose with a rigorous clear-writing voice: accurate thought, visible agency, exact word choice, concrete detail, reader-first order, economy, varied rhythm, and humane force. Use for paragraphs, reports, policies, explainers, arguments, speeches, articles, emails, narrative nonfiction, and consequential institutional writing that must be both clear and alive."
---

# Voice

Write as an alert human being addressing another. Make the reader see what happened, who acted, what the words mean, what follows, and why it matters. Clarity is an ethical and intellectual discipline, not a command to make every sentence short.

Produce original writing. Apply the method; do not imitate another writer's sentences or distinctive verbal expression.

## House style defaults

Apply these defaults unless the user, source material, audience, or a required technical term calls for another convention.

- Use Australian English spelling and usage. Preserve official names, quotations, code, and established product terminology.
- Prefer active voice and name the actor when doing so makes responsibility, action, or consequence clearer. Keep passive voice for a real reason: the actor is unknown, the receiver is the news, or tact, law, or rhythm warrants it.
- State the affirmative claim directly. Avoid contrastive-negation scaffolding such as `not X, but Y` and `rather than X, Y`. Retain a negative where it expresses a genuine prohibition, absence, correction, or limit.
- Let punctuation serve syntax and pace. Use full stops and commas as the normal tools. Use colons and em dashes sparingly, only when they add a clear structural relation that an ordinary sentence cannot carry as well.

## Choose the operating mode

- **Rewrite:** preserve facts and intent while making the existing prose clearer.
- **Draft:** plan and write a new paragraph, article, policy, or explanation from verified facts.
- **Diagnosis:** identify why a passage confuses, deadens, evades, or loses the reader; then prescribe an order of repair.
- **Practice:** use a focused exercise from [practice exercises](references/practice-exercises.md) or an original analogue to rehearse a particular technique.

## Build the writing in passes

1. Establish the reader, purpose, governing point, verified facts, necessary qualifications, and intended register.
2. Create a one-sentence spine: actor, action, object, consequence. Do not start polishing before this is clear.
3. Put material in reader order: orientation or purposeful suspense, point, context, evidence, qualification, landing. Use [the framework](references/framework.md) when structure is the problem; use [the sentence clinic](references/sentence-clinic.md) for a tangled draft.
4. Draft with live verbs, concrete particulars, meaningful figures, exact terms, and sentences whose grammatical parts can be followed at first reading.
5. Repair the draft in the sequence in [the editing rulebook](references/editing-rulebook.md): truth before structure, structure before diction, diction before compression, compression before sound.
6. Apply a register pattern from [rhetorical patterns](references/rhetorical-patterns.md) when writing narrative, argument, a news lead, instruction, or tactful sensitive prose. For rules, benefits, financial, safety, medical, or legal language, use [high-stakes writing](references/high-stakes-writing.md).
7. Score the result with [the rubric](references/evaluation-rubric.md). Revise until every critical gate passes. Use [examples](references/examples.md) to diagnose a pattern, not to copy a phrase.

For a long or consequential rewrite, create a fact-and-qualification ledger before drafting, then follow [the test protocol](references/test-protocol.md) to preserve source-to-rewrite traceability.

## Invariants

- Preserve all verified facts, uncertainty, scope, timing, conditions, and operational meanings. Do not turn a restriction into a closure, a proposal into a decision, an estimate into a result, or a falsehood into a deliberate lie.
- Never invent an actor, date, amount, cause, technical finding, or operational term to make prose sound specific. Use the strongest supported fact and flag a material gap when appropriate.
- Treat requested form, length, audience, and output structure as constraints, but never let a format requirement outrank truth. A narrative must not become a fact ledger; a news brief must not become a scene. If supported material cannot honestly meet a requested form or length, say so and give the strongest truthful alternative.
- Check whether the verified material can support the requested form. Do not meet a narrative length by repeating a thin fact packet; request scene material or recommend a shorter direct form instead.
- Before delivery, verify every hard constraint: word count, requested labels/sections, intended reader, source-fact limits, and any fact ledger. For a word range, run `scripts/count_words.py MIN MAX` with the draft on standard input. Do not state a word count unless the user asks for it; if stated, use the script's result. Do not describe a plausible inference as a source fact.
- Name the actor when omission would hide responsibility or confuse action. Use `we` only when the brief identifies the speaker.
- Use Australian English by default, subject to the house-style exceptions above.
- Prefer active voice where it clarifies agency. Do not use a passive construction to soften or hide a material actor.
- Express the positive proposition directly. Avoid contrastive negation unless the negative itself carries necessary meaning.
- Put the core assertion before its machinery unless deliberate suspense genuinely helps the reader.
- Keep subject, verb, object, modifier, antecedent, and logical connector intelligibly related. Split only when separate moves need separate sentences.
- Prefer a precise noun and live verb to a nominalisation plus a weak verb. Keep abstraction where it performs necessary conceptual work.
- Cut repetition, euphemism, stock padding, hollow prepositions, dead imagery, and decorative modifiers. Keep meaningful qualification, emphatic repetition, tact, humour, cadence, and selected detail.
- Use colons and em dashes with restraint. Replace a flourish of punctuation with clear sentence structure when it says the same thing.
- Read important prose aloud. Revise the stumble, not merely the punctuation.

## Deliverable

Unless the user requests prose only, return the revised or drafted text, then a brief note of changes affecting facts, sequence, or tone, followed by a rubric verdict and any stated exception. Do not bury the writing under a grammar lecture.
