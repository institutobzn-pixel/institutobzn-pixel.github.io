# Método Renda Digital — Página de Vendas

Página de vendas premium (dark, estética tech/IA) para o curso do professor **Tiago Cavalcanti**, construída a partir do briefing em PDF.

HTML + CSS + JavaScript puro, **sem frameworks nem bibliotecas pesadas**. Pronta para publicar.

## Estrutura

```
paginadevendas/
├── index.html          # Página completa (todas as seções + SEO/Schema)
├── css/styles.css      # Tema dark premium, glassmorphism, glow, responsivo
├── js/main.js          # Scroll reveal, partículas, contadores, acordeão, header
└── assets/
    ├── LEIA-ME.txt     # Instruções da foto
    ├── professor.jpg   # (você adiciona) foto do professor no Hero
    └── og-cover.jpg    # (opcional) imagem de compartilhamento social
```

## Como visualizar

Abra `index.html` no navegador, ou rode um servidor local:

```bash
python3 -m http.server 8000
# depois acesse http://localhost:8000
```

## O que você precisa personalizar

Os pontos abaixo estão marcados no código com `⚠️ EDITAR` (procure por esse texto):

| Item | Onde |
|------|------|
| **Foto do professor** | salvar em `assets/professor.jpg` |
| **Preço e link de checkout** | seção `#oferta` no `index.html` |
| **Depoimentos reais** | seção `#depoimentos` (não use fictícios em produção) |
| **Garantia** | seção `#garantia` (descreva as condições, se houver) |
| **Contato, redes e links legais** | rodapé |
| **Domínio / URLs** | tags SEO no `<head>` (canonical, Open Graph) |

## Características

- Copy 100% escrita em português do Brasil, tom ético (sem "dinheiro fácil").
- Seções: Hero, Dor, Solução, Benefícios, Conteúdo, Para quem é/não é, Professor, Diferenciais, Antes×Depois, Depoimentos, Oferta, Garantia, FAQ, CTA final, Rodapé.
- SEO: meta tags, Open Graph, Twitter Card, Schema.org (Course).
- Acessibilidade: skip link, ARIA, foco visível, contraste, `prefers-reduced-motion`.
- Performance: JS leve, `defer`, lazy loading, partículas com teto de densidade e pausa em aba oculta.
- Responsivo: desktop, tablet e mobile.
