# AwesomeLaTeX
Personally curated LaTeX macros and templates

在 `/Applications/Typora.app/Contents/Resources/TypeMark/index.html` 中添加

```javascript
MathJax.Hub.Config({
    skipStartupTypeset: true,
    jax: ["input/TeX", "output/SVG"],
    extensions: ["tex2jax.js", "toMathML.js"],
    TeX: {
        Macros: {/* 内容 */}
    }
})
```
