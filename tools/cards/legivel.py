# Gera os criativos legiveis para feed e story.
#
# O card original foi desenhado como cartaz: bonito em tamanho grande, ilegivel
# quando o Instagram reduz 1080px para os ~390px de largura de um celular.
# Tudo divide por 2,77 — o que era 15px virava 5px.
#
# Aqui o conteudo fica no essencial e o corpo minimo e de 33px, o que da ~12px
# na tela. As provas (best-seller, TEDx) viram uma linha so; o endereco tem
# area propria, marcada como "Noite 1" porque a segunda noite e online.
#
#   python3 legivel.py && node render.js

ESCALA_FEED = 1080 / 390   # como o feed reduz a imagem no celular
MINIMO_TELA = 12           # px na tela abaixo dos quais nao se le

ATIVOS = '../../assets'

CABECA = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />
<style>
  :root {{
    --black: #070708;
    --purple: #a855f7;
    --blue: #3b82f6;
    --cyan: #22d3ee;
    --grad: linear-gradient(115deg, var(--purple) 0%, var(--blue) 52%, var(--cyan) 100%);
    --muted: #b6bbc4;
    --font-sans: 'Inter', sans-serif;
    --font-display: 'Space Grotesk', sans-serif;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {W}px; height: {H}px; overflow: hidden; }}
  body {{
    font-family: var(--font-sans); background: var(--black); color: #fff;
    position: relative; -webkit-font-smoothing: antialiased;
  }}

  .grid {{
    position: absolute; inset: 0;
    background-image:
      linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
    background-size: 72px 72px;
    mask-image: radial-gradient(120% 90% at 20% 40%, #000 0%, transparent 72%);
  }}
  .glow-a {{
    position: absolute; width: 940px; height: 940px; border-radius: 50%;
    background: radial-gradient(circle, rgba(168,85,247,.32), transparent 66%);
    top: -340px; left: -320px;
  }}
  .glow-b {{
    position: absolute; width: 780px; height: 780px; border-radius: 50%;
    background: radial-gradient(circle, rgba(34,211,238,.20), transparent 66%);
    bottom: -300px; left: 140px;
  }}

  .photo {{
    position: absolute; top: 0; right: 0; width: {FOTO_W}px; height: {FOTO_H}px; overflow: hidden;
    -webkit-mask-image:
      linear-gradient(to right, transparent 0%, rgba(0,0,0,.35) 24%, #000 60%),
      linear-gradient(to bottom, #000 0%, #000 66%, transparent 97%);
    -webkit-mask-composite: source-in;
    mask-image:
      linear-gradient(to right, transparent 0%, rgba(0,0,0,.35) 24%, #000 60%),
      linear-gradient(to bottom, #000 0%, #000 66%, transparent 97%);
    mask-composite: intersect;
  }}
  .photo img {{
    width: 100%; height: 100%; object-fit: cover; object-position: 30% 14%;
    display: block; transform: translateX({FOTO_X}px);
  }}

  .frame {{
    position: absolute; inset: 0; z-index: 5;
    padding: {PAD};
    display: flex; flex-direction: column;
  }}

  /* Topo so com o selo de data: a logo desceu para o pe do card */
  .head {{ display: flex; align-items: center; justify-content: flex-end; }}
  .logo {{ height: {LOGO}px; width: auto; display: block; }}
  .date-chip {{
    display: inline-flex; align-items: center; gap: 12px;
    padding: {CHIP_PAD}; border-radius: 999px;
    background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.20);
    font-size: {F_DATA}px; font-weight: 700; letter-spacing: .05em; text-transform: uppercase;
    white-space: nowrap;
  }}
  .date-chip .dot {{
    width: 12px; height: 12px; border-radius: 50%;
    background: var(--cyan); box-shadow: 0 0 14px var(--cyan);
  }}

  .col {{ width: {COL}px; margin-top: {COL_TOP}px; }}

  .course {{
    font-family: var(--font-display); font-weight: 700; font-size: {F_TITULO}px;
    line-height: 1.02; letter-spacing: -.025em;
    background: var(--grad); -webkit-background-clip: text; background-clip: text; color: transparent;
  }}
  .speaker {{ margin-top: {GAP_SPK}px; }}
  .speaker .com {{ font-size: {F_COM}px; color: var(--muted); }}
  .speaker .nome {{
    display: block; font-family: var(--font-display); font-weight: 700;
    font-size: {F_NOME}px; line-height: 1.06; letter-spacing: -.02em; margin-top: 4px;
  }}
  .speaker .creds {{
    display: block; margin-top: {GAP_CRED}px; font-size: {F_CRED}px; font-weight: 600;
    color: var(--cyan); letter-spacing: .02em;
  }}

  .foot {{ margin-top: auto; padding-top: {GAP_FOOT}px; }}

  /* Tipografia, nao pilula: forma de botao dentro do criativo, logo acima do
     botao real do Meta, e tocada por engano e nao leva a lugar nenhum. */
  .bonus {{
    display: flex; align-items: center; gap: 16px;
    font-size: {F_BONUS}px; font-weight: 800; letter-spacing: -.015em;
    margin-bottom: {GAP_BONUS}px;
  }}
  .bonus .ic {{ font-size: {F_BONUS}px; line-height: 1; flex: none; }}
  .bonus .t {{
    background: var(--grad); -webkit-background-clip: text; background-clip: text;
    color: transparent;
  }}

  .days {{ display: flex; flex-direction: column; gap: {GAP_DIAS}px; }}
  .day {{ display: flex; align-items: baseline; gap: 16px; font-size: {F_DIA}px; letter-spacing: -.012em; }}
  .day .b {{ width: 14px; height: 14px; border-radius: 4px; flex: none; transform: translateY(-2px); }}
  .day.pres .b {{ background: var(--purple); box-shadow: 0 0 16px rgba(168,85,247,.9); }}
  .day.onl  .b {{ background: var(--cyan);   box-shadow: 0 0 16px rgba(34,211,238,.9); }}
  .day .n {{ font-family: var(--font-display); font-weight: 700; color: #fff; white-space: nowrap; }}
  .day .o {{ color: var(--muted); font-weight: 500; }}

  /* Local em area propria: e o que decide a ida de quem mora perto */
  .local {{ display: flex; align-items: flex-start; gap: {LOC_GAP}px; margin-top: {LOC_TOP}px; }}
  .local .ic {{ font-size: {LOC_IC}px; line-height: 1.1; flex: none; }}
  .local .txt {{ display: flex; flex-direction: column; }}
  .local .l1 {{
    font-family: var(--font-display); font-weight: 700; font-size: {LOC_L1}px;
    color: #fff; letter-spacing: -.015em;
  }}
  .local .l2 {{
    margin-top: 6px; font-size: {LOC_L2}px; line-height: 1.34;
    color: var(--muted); font-weight: 500;
  }}

  /* Assinatura no pe: contato a esquerda, logo a direita */
  .signoff {{ display: flex; align-items: center; gap: 28px; margin-top: {SIGN_TOP}px; }}
  .signoff .logo {{ margin-left: auto; }}

  .wa {{ display: flex; align-items: center; gap: {WA_GAP}px; }}
  .wa svg {{
    width: {WA_IC}px; height: {WA_IC}px; flex: none; color: #25D366;
    filter: drop-shadow(0 0 26px rgba(37,211,102,.55));
  }}
  .wa .txt {{ display: flex; flex-direction: column; line-height: 1.12; }}
  .wa .l1 {{
    font-family: var(--font-display); font-weight: 700; font-size: {WA_L1}px;
    color: #25D366; letter-spacing: -.015em;
  }}
  .wa .l2 {{
    font-family: var(--font-display); font-weight: 700; font-size: {WA_L2}px;
    color: #fff; letter-spacing: -.01em;
  }}
</style>
</head>
<body>
  <div class="grid"></div>
  <div class="glow-a"></div>
  <div class="glow-b"></div>
  <div class="photo"><img src="{ATIVOS}/professor.jpg.jpg" alt="" /></div>

  <div class="frame">
    <div class="head">
      <div class="date-chip"><span class="dot"></span> 31 ago e 1º set · 19h às 22h</div>
    </div>

    <div class="col">
      <h1 class="course">Como Gerar Renda<br/>pela Internet</h1>
      <div class="speaker">
        <span class="com">com</span>
        <span class="nome">Dr. Tiago Cavalcanti</span>
        <span class="creds">PhD · TEDx Speaker · Autor best-seller</span>
      </div>
    </div>

    <div class="foot">
{BONUS}      <div class="days">
        <div class="day pres"><span class="b"></span><span class="n">31/08</span><span class="o">presencial</span></div>
        <div class="day onl"><span class="b"></span><span class="n">01/09</span><span class="o">online e ao vivo</span></div>
      </div>
      <div class="local">
        <span class="ic">📍</span>
        <span class="txt">
          <span class="l1">Noite 1 · Instituto BZN</span>
          <span class="l2">Av. Baltazar de Oliveira Garcia, 430<br/>Porto Alegre/RS · com estacionamento</span>
        </span>
      </div>
      <div class="signoff">
{CTA}        <img class="logo" src="{ATIVOS}/logo-bzn.png.png" alt="Instituto BZN" />
      </div>
    </div>
  </div>
</body>
</html>
"""

WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
  '<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15'
  '-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475'
  '-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52'
  '.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207'
  '-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297'
  '-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487'
  '.709.306 1.262.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413'
  '.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 '
  '0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001'
  '-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c'
  '-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 '
  '5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 '
  '005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>'
  '</svg>')

CTA_WA = ('        <div class="wa">' + WA_SVG +
          '<span class="txt">'
          '<span class="l1">Inscrições pelo WhatsApp</span>'
          '<span class="l2">(51) 98986-6856</span>'
          '</span></div>\n')

BONUS_ACOMPANHANTE = '      <div class="bonus"><span class="ic">🎁</span><span class="t">Leve 1 acompanhante sem custo</span></div>\n'

# ------------------------------------------------------------------ pecas
# Sem CTA: para anuncio pago, onde o botao do Meta faz esse trabalho.
FEED = dict(
    ATIVOS=ATIVOS, W=1080, H=1350, FOTO_W=640, FOTO_H=1160, FOTO_X=88,
    PAD='92px 74px 208px', LOGO=58, CHIP_PAD='14px 26px', SUB_W=600,
    COL=690, COL_TOP=104,
    F_DATA=34, F_TITULO=74, F_SUB=44, F_COM=40, F_NOME=62, F_CRED=34, F_BONUS=46, F_DIA=44,
    GAP_SUB=24, GAP_SPK=28, GAP_CRED=14, GAP_BONUS=32, GAP_DIAS=20,
    LOC_GAP=16, LOC_TOP=26, LOC_IC=34, LOC_L1=36, LOC_L2=32,
    SIGN_TOP=24, GAP_FOOT=30,
    WA_GAP=0, WA_IC=1, WA_L1=1, WA_L2=1, CTA='', BONUS='',
)

STORY = dict(
    ATIVOS=ATIVOS, W=1080, H=1920, FOTO_W=690, FOTO_H=1300, FOTO_X=94,
    PAD='104px 76px 330px', LOGO=64, CHIP_PAD='15px 24px', SUB_W=630,
    COL=712, COL_TOP=240,
    F_DATA=34, F_TITULO=80, F_SUB=48, F_COM=42, F_NOME=66, F_CRED=36, F_BONUS=50, F_DIA=48,
    GAP_SUB=34, GAP_SPK=56, GAP_CRED=16, GAP_BONUS=46, GAP_DIAS=26,
    LOC_GAP=18, LOC_TOP=38, LOC_IC=38, LOC_L1=40, LOC_L2=34,
    SIGN_TOP=50, GAP_FOOT=58,
    WA_GAP=0, WA_IC=1, WA_L1=1, WA_L2=1, CTA='', BONUS=BONUS_ACOMPANHANTE,
)

# Com CTA: post organico, story do perfil e disparo em grupo, onde nao ha
# botao nativo. Nao usar em anuncio pago — telefone na imagem nao e clicavel.
FEED_WA = dict(FEED,
    PAD='96px 74px 176px', COL_TOP=76, GAP_BONUS=26,
    WA_GAP=20, WA_IC=56, WA_L1=34, WA_L2=46, CTA=CTA_WA)

STORY_WA = dict(STORY,
    PAD='130px 76px 330px', COL_TOP=200, GAP_BONUS=40,
    WA_GAP=24, WA_IC=70, WA_L1=38, WA_L2=56, CTA=CTA_WA)

PECAS = [
    ('feed-06-legivel.html',  FEED),
    ('story-06-legivel.html', STORY),
    ('feed-07-wa.html',       FEED_WA),
    ('story-07-wa.html',      STORY_WA),
]

if __name__ == '__main__':
    for nome, cfg in PECAS:
        open(nome, 'w', encoding='utf-8').write(CABECA.format(**cfg))
        print('gerado:', nome)

    print('\nmenor corpo por peca (px no card -> px na tela de 390):')
    for nome, cfg in PECAS:
        fontes = {k: v for k, v in cfg.items()
                  if (k.startswith('F_') or k.startswith('WA_L')) and isinstance(v, int) and v > 1}
        menor_k = min(fontes, key=fontes.get)
        tela = fontes[menor_k] / ESCALA_FEED
        marca = 'OK' if tela >= MINIMO_TELA else 'ABAIXO DO MINIMO'
        print(f'  {nome:24} {menor_k}={fontes[menor_k]}px -> {tela:.1f}px  {marca}')
