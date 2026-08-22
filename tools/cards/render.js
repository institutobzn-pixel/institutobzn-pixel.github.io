// Renderiza os criativos e mede cada texto no tamanho em que ele realmente
// aparece: o feed reduz 1080px para os ~390px de largura de um celular, entao
// tudo divide por 2,77. Reprova qualquer texto abaixo de 12px na tela.
//
//   NODE_PATH=/opt/node22/lib/node_modules node render.js

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const LARGURA_TELA = 390;
const MINIMO = 12;
// A linha de endereco e informacao de referencia — quem se interessa amplia ou
// clica. Ela pode ficar logo abaixo do piso sem prejudicar a mensagem.
const MINIMO_ENDERECO = 11.5;
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const PECAS = [
  ['feed-06-legivel.html',  'feed-06-legivel-1080x1350.png',  1080, 1350],
  ['story-06-legivel.html', 'story-06-legivel-1080x1920.png', 1080, 1920],
  ['feed-07-wa.html',       'feed-07-wa-1080x1350.png',       1080, 1350],
  ['story-07-wa.html',      'story-07-wa-1080x1920.png',      1080, 1920],
];

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  let reprovados = 0;

  for (const [src, out, W, H] of PECAS) {
    const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
    await page.goto('file://' + path.resolve(src));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(450);

    const vazando = await page.evaluate((H) => {
      const o = [];
      document.querySelectorAll('.frame *').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.height === 0) return;
        if (r.bottom > H + 1 || r.top < -1 || r.right > 1081 || r.left < -1) {
          o.push({ cls: el.className || el.tagName, top: Math.round(r.top), bottom: Math.round(r.bottom) });
        }
      });
      return o;
    }, H);

    const textos = await page.evaluate((args) => {
      const [W, LARGURA] = args;
      const escala = W / LARGURA;
      const vistos = [];
      document.querySelectorAll('.frame *').forEach(el => {
        const proprio = Array.from(el.childNodes)
          .filter(n => n.nodeType === 3 && n.textContent.trim())
          .map(n => n.textContent.trim()).join(' ');
        if (!proprio) return;
        const px = parseFloat(getComputedStyle(el).fontSize);
        vistos.push({ txt: proprio.slice(0, 34), px, tela: +(px / escala).toFixed(1) });
      });
      return vistos.sort((a, b) => a.tela - b.tela);
    }, [W, LARGURA_TELA]);

    // respiro real entre a ultima linha e a borda de baixo
    const respiro = await page.evaluate((H) => {
      const e = document.querySelector('.signoff') || document.querySelector('.local');
      return Math.round(H - e.getBoundingClientRect().bottom);
    }, H);

    console.log('\n=== ' + out + ' ===');
    console.log(vazando.length ? '  VAZANDO: ' + JSON.stringify(vazando) : '  layout: nada vazando');
    console.log('  respiro na borda de baixo: ' + respiro + 'px');
    const piso = t => (t.txt.startsWith('Av.') ? MINIMO_ENDERECO : MINIMO);
    const baixos = textos.filter(t => t.tela < piso(t));
    for (const t of textos) {
      console.log(`  ${t.tela >= piso(t) ? 'ok   ' : 'BAIXO'} ${String(t.px + 'px').padStart(6)} -> ${String(t.tela + 'px').padStart(7)}  "${t.txt}"`);
    }
    if (baixos.length || vazando.length) reprovados++;

    await page.screenshot({ path: out });
    await page.close();
  }

  await browser.close();
  console.log('\n' + (reprovados ? reprovados + ' peca(s) com problema' : 'todas as pecas aprovadas'));
  process.exit(reprovados ? 1 : 0);
})();
