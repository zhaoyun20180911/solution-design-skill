# Markdown Math Rules

Use Markdown math notation in formal proposal source files.

## Rules

- Inline mathematical variables use `$...$`.
- Display formulas use `$$...$$`.
- Subscripts, superscripts, hats, bars, matrices, sets, norms, fractions, and roots must be marked as math.
- Greek letters must be marked as math, such as `$\\alpha$`, `$\\theta$`, and `$\\sigma$`.
- Error metrics, statistical metrics, and algorithm variables should be marked when used as variables.
- Do not mark ordinary English words, software names, unit names, or natural-language phrases as formulas.

## Chinese Example

Correct:

```text
系统状态向量记为 $x(k)$，观测向量记为 $z(k)$，状态转移矩阵记为 $F(k)$。
```

Incorrect:

```text
系统状态向量记为 x(k)，观测向量记为 z(k)。
```

## English Example

Correct:

```text
The state vector is denoted as $x(k)$, the observation vector as $z(k)$, and the transition matrix as $F(k)$.
```

Use `scripts/check_markdown_math.py` to flag likely unmarked variables.
