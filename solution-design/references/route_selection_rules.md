# Route Selection Rules

Route selection must help the user understand trade-offs before framework design begins.

## Explain Each Route

For each candidate route, explain in chat:

- what the route does in professional terms
- a plain-language explanation
- required inputs and assumptions
- produced outputs
- algorithm modules or engineering modules
- implementation difficulty
- verification difficulty
- major risks and mitigation ideas

## Keep A Running Summary

During solution discussion, end every response with a latest-solution summary:

- selected or preferred main route
- retained comparison routes
- key assumptions
- expected Word depth or page target if known
- method difficulty preference if known
- open decisions

Then ask whether to use this solution direction to begin proposal framework design.

## Converge Without Overclaiming

Recommend one route only when the project objective and constraints support it. If the user has not confirmed the route, keep alternatives visible and ask one focused confirmation question.

## Confirmation Prompt

Use a concise confirmation question such as:

```text
当前方案方向总结如下：主线采用“路线 A”，保留“路线 B”作为对比，难度控制为中等，最终 Word 预计约 15 页。是否以这个方案方向开始设计正式方案框架？如果同意，我会先在对话中给出完整框架供你修改，不会立刻写入 confirmed_framework.md。
```

For English:

```text
Current solution summary: Route A is the main route, Route B is retained for comparison, the target difficulty is moderate, and the final Word proposal is expected to be about 15 pages. Should I start designing the formal proposal framework based on this direction? If yes, I will first show the full framework in chat for revision and will not write confirmed_framework.md yet.
```
