# Route Selection Rules

Route selection must help the user understand trade-offs before freezing the solution framework.

## Explain Each Route

For each candidate route, explain:

- what the route does in professional terms
- a plain-language explanation
- required inputs and assumptions
- produced outputs
- algorithm modules or engineering modules
- implementation difficulty
- verification difficulty
- major risks and mitigation ideas

## Converge Without Overclaiming

Recommend one route only when the project objective and constraints support it. If the user has not confirmed the route, keep alternatives visible and ask a focused confirmation question.

## Confirmation Prompt

Use a concise confirmation question such as:

```text
请确认本方案是否采用“路线 A”作为主线，并将“路线 B”作为可选对比路线。确认后我将基于该路线生成方案框架。
```

For English:

```text
Please confirm whether Route A should be used as the main route and Route B retained as an optional comparison route. After confirmation, I will generate the solution outline.
```
