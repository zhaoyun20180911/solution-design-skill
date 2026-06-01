# Route Selection Rules

Route selection must help the user understand trade-offs before saving the confirmed framework anchor.

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

Recommend one route only when the project objective and constraints support it. If the user has not confirmed the route, keep alternatives visible and ask one focused confirmation question.

## Confirmation Prompt

Use a concise confirmation question such as:

```text
请确认本方案是否采用“路线 A”作为主线，并将“路线 B”作为可选对比路线。确认后我会把已确认路线、模块边界、指标体系和方案章节框架保存到 confirmed_framework.md。
```

For English:

```text
Please confirm whether Route A should be used as the main route and Route B retained as an optional comparison route. After confirmation, I will save the confirmed route, module boundaries, metric system, and proposal framework in confirmed_framework.md.
```
