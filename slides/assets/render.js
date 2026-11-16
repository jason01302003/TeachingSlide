/* 共用的顯示程式：Markdown（marked）＋ LaTeX（KaTeX）＋ [[Wiki 連結]] ＋ 圖表區塊。
   簡報與 wiki.html 都用這一份。 */
(function () {
  const PALETTE = ['#0f766e', '#b45309', '#4338ca', '#be185d', '#15803d', '#0369a1', '#7c3aed', '#a16207'];
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function math(tex, display) {
    try { return katex.renderToString(tex, { displayMode: display, throwOnError: false }); }
    catch (e) { return '<code>' + esc(tex) + '</code>'; }
  }

  /* 甘特圖：{rows:[{label, bars:[{job,start,end,group?}]}], caption} */
  function gantt(d) {
    const jobs = [...new Set(d.rows.flatMap(r => r.bars.map(b => b.job)))];
    const end = Math.max(...d.rows.flatMap(r => r.bars.map(b => b.end)));
    const W = 860, L = 70, rowH = 46, top = 8, H = top + d.rows.length * rowH + 30;
    const x = t => L + t * (W - L - 12) / end;
    let s = `<svg class="diagram" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(d.caption || '甘特圖')}">`;
    for (let t = 0; t <= end; t++) {
      s += `<line x1="${x(t)}" y1="${top}" x2="${x(t)}" y2="${H - 24}" class="grid"/>`;
      if (end <= 24 || t % 2 === 0) s += `<text x="${x(t)}" y="${H - 8}" class="tick">${t}</text>`;
    }
    d.rows.forEach((r, i) => {
      const y = top + i * rowH + 5;
      s += `<text x="${L - 12}" y="${y + 22}" class="rowlabel">${esc(r.label)}</text>`;
      r.bars.forEach(b => {
        const c = PALETTE[(b.group ? b.group - 1 : jobs.indexOf(b.job)) % PALETTE.length];
        s += `<rect x="${x(b.start) + 1}" y="${y}" width="${x(b.end) - x(b.start) - 2}" height="${rowH - 12}" rx="5" fill="${c}"/>`;
        s += `<text x="${(x(b.start) + x(b.end)) / 2}" y="${y + 22}" class="barlabel">${esc(b.job)}</text>`;
      });
    });
    s += '</svg>';
    return `<figure>${s}${d.caption ? `<figcaption>${esc(d.caption)}</figcaption>` : ''}</figure>`;
  }

  /* 資源水位圖：{v0, steps:[{job,alpha,beta,before,during,after}], caption} */
  function levels(d) {
    const max = Math.max(d.v0, ...d.steps.flatMap(s => [s.before, s.after]));
    const W = 860, L = 56, H = 250, top = 22, bot = 44, n = d.steps.length;
    const x = i => L + i * (W - L - 20) / n, y = v => top + (H - top - bot) * (1 - v / max);
    let s = `<svg class="diagram" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(d.caption || '資源水位圖')}">`;
    for (let v = 0; v <= max; v++) {
      s += `<line x1="${L}" y1="${y(v)}" x2="${W - 20}" y2="${y(v)}" class="grid"/><text x="${L - 10}" y="${y(v) + 5}" class="rowlabel">${v}</text>`;
    }
    let path = `M ${x(0)} ${y(d.steps[0].before)}`;
    d.steps.forEach((st, i) => {
      const c = PALETTE[i % PALETTE.length];
      s += `<rect x="${x(i) + 3}" y="${H - bot + 8}" width="${x(i + 1) - x(i) - 6}" height="26" rx="5" fill="${c}"/>`;
      s += `<text x="${(x(i) + x(i + 1)) / 2}" y="${H - bot + 26}" class="barlabel">${esc(st.job)}（−${st.alpha}，+${st.beta}）</text>`;
      path += ` L ${x(i)} ${y(st.during)} L ${x(i + 1)} ${y(st.during)} L ${x(i + 1)} ${y(st.after)}`;
      s += `<text x="${(x(i) + x(i + 1)) / 2}" y="${y(st.during) - 8}" class="tick">${st.during}</text>`;
      s += `<circle cx="${x(i + 1)}" cy="${y(st.after)}" r="4" class="dot"/><text x="${x(i + 1) - 4}" y="${y(st.after) - 9}" class="tick strong">${st.after}</text>`;
    });
    s += `<circle cx="${x(0)}" cy="${y(d.steps[0].before)}" r="4" class="dot"/><text x="${x(0) + 6}" y="${y(d.steps[0].before) - 9}" class="tick strong">${d.steps[0].before}</text>`;
    s += `<path d="${path}" class="level"/></svg>`;
    return `<figure>${s}${d.caption ? `<figcaption>${esc(d.caption)}</figcaption>` : ''}</figure>`;
  }

  /* opts.link(target, label) 回傳 [[連結]] 的 href；opts.cite(sourceId) 回傳來源標註的 href（可省略）。 */
  window.renderMarkdown = function (src, opts) {
    opts = opts || {};
    const stash = [];
    const keep = html => { stash.push(html); return '⟦' + (stash.length - 1) + '⟧'; };

    src = src.replace(/```(\w*)\n([\s\S]*?)```/g, (m, lang, code) => {
      if (lang === 'gantt' || lang === 'levels') {
        try { return '\n\n' + keep((lang === 'gantt' ? gantt : levels)(JSON.parse(code))) + '\n\n'; }
        catch (e) { return '\n\n' + keep('<pre class="err">圖表資料有誤：' + esc(e.message) + '</pre>') + '\n\n'; }
      }
      return '\n\n' + keep('<pre><code>' + esc(code) + '</code></pre>') + '\n\n';
    });
    src = src.replace(/`([^`\n]+)`/g, (m, code) => keep('<code>' + esc(code) + '</code>'));
    src = src.replace(/\$\$([\s\S]+?)\$\$/g, (m, tex) => keep(math(tex.trim(), true)));
    src = src.replace(/\$([^$\n]+?)\$/g, (m, tex) => keep(math(tex, false)));
    src = src.replace(/\[\[([^\]|#\\]+)(?:\\?\|([^\]]*))?\]\]/g, (m, target, label) => {
      const t = target.trim();
      const text = label || (opts.title ? opts.title(t) : t);
      return keep(`<a class="wikilink" href="${esc(opts.link ? opts.link(t) : '#' + t)}">${esc(text)}</a>`);
    });
    src = src.replace(/\[((?:DO|EJOR|JOSH|TSWJ)\d{4})(\s+[^\]\[]*)?\]/g, (m, id, where) => {
      const label = esc(id + (where || ''));
      return keep(opts.cite ? `<a class="cite" href="${esc(opts.cite(id))}">${label}</a>` : `<span class="cite">${label}</span>`);
    });

    let html = marked.parse(src, { gfm: true, breaks: false });
    html = html.replace(/<p>⟦(\d+)⟧<\/p>/g, (m, i) => stash[+i]);
    for (let pass = 0; pass < 3; pass++) html = html.replace(/⟦(\d+)⟧/g, (m, i) => stash[+i]);
    html = html.replace(/<blockquote>\s*<p><strong>待確認<\/strong>/g, '<blockquote class="todo"><p><strong>待確認</strong>');
    return html.replace(/<table>/g, '<div class="tablewrap"><table>').replace(/<\/table>/g, '</table></div>');
  };
})();
