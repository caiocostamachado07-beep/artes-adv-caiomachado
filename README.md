# Artes do @adv.caiomachado
Repositório público usado pela rotina semanal de conteúdo (Claude + Metricool).
- `fotos/`: fotos do Caio (rodízio entre os temas)
- `fontes/`: Poppins e Lora (licença OFL)
- `render/post_foto.py`: gera o post foto 1080x1350 a partir de um JSON
- `arte/`: imagens geradas; o Metricool lê pelo endereço `https://raw.githubusercontent.com/caiocostamachado07-beep/artes-adv-caiomachado/main/arte/<arquivo>.png`
- foto16 a foto28 são em alta resolução (1122x1402) e podem ser usadas em capas e finais. foto11 a foto15 são menos nítidas: prefira para telas secundárias. Para rodízio, prefira foto01-10 e foto16-28 nas capas.

## Banco de imagens temáticas (Unsplash, automático)
- Para usar uma foto de domínio livre sobre o tema: busque com o conector Unsplash (search_photos, orientation portrait, query em inglês curta e específica; inclua "Brazil" quando fizer sentido), escolha a melhor e adicione em banco/pedidos.json um item {"tema","id","url","autor"} com url no formato https://images.unsplash.com/photo-XXXX?fm=jpg&w=1600&q=85 (pegue a base de urls.raw do resultado).
- Faça commit e push só do banco/pedidos.json: o GitHub Actions (.github/workflows/baixar-fotos.yml) baixa a imagem para banco/<tema>/<id>.jpg e faz commit (leva ~40 s). Depois rode git pull --rebase origin main.
- Nos JSON de render use "foto": "banco/<tema>/<id>.jpg". Escolha fotos em que o assunto esteja na parte de cima (a metade de baixo some no degradê); ajuste crop_y se precisar e OLHE o resultado.
- Mistura: capa com a foto do tema e a página final com foto do Caio (ou o contrário). O Reels e o post foto também aceitam banco/.

## Ideias guardadas para próximos conteúdos
- Voo atrasado/cancelado (ANAC 400/2016 e Res. 813/2026, válida a partir de 26/10/2026): o carrossel de 14/10 saiu sem foto do tema. Refazer em um próximo carrossel com foto pública de aeroporto/avião (Unsplash, "airport Brazil") na capa e foto do Caio na página final. Verificar de novo a regra vigente antes de publicar.

## Regras de conteúdo (atualizadas em 20/10/2026, pedido do Caio)
- **Reels suspensos.** Na sexta das semanas que antes tinham Reels (12/10, 26/10, 09/11... uma sim, outra não) entra um **post comum de imagem única** (render/post_foto.py), não carrossel.
- **Mais fotos públicas do que do Caio.** O estado das rotações está em `render/rotacao.json`:
  - Posts comuns: 3 com foto pública (banco/), 1 com foto do Caio, e repete.
  - Carrosséis: 2 com foto pública na capa, numa página do meio e no final; 1 com capa e final do Caio; 2 mesclando (capa pública + final do Caio; capa do Caio + final pública); repete.
  - Página do meio com foto: no JSON do carrossel, ponha `"foto": "banco/<tema>/<id>.jpg"` (e `crop_y` se precisar) na página, com 1 item curto e sem nota.
- **Áreas em rodízio por peça** (ver `areas` em rotacao.json): Consumidor, Previdenciário, Tributário e Imposto de Renda, Digital e LGPD, Consumidor, Previdenciário, Sucessório, Vizinhança, Compliance.
- **Fotos do Caio no carrossel (corrigido em 21/10/2026):** o gerador agora reduz a foto dele e deixa o rosto inteiro acima do texto; o degradê nunca pode cortar o rosto. Capa e final do mesmo carrossel devem ter **roupas/sessões diferentes** (ex.: não usar duas de "blazer bege"; compare os nomes dos arquivos). Sem numeração de páginas (o Instagram já mostra).

## Regra de fotos (atualizada em 11/11/2026, pedido do Caio) — SUBSTITUI as regras de fotos anteriores
- **NÃO usar mais fotos do Caio** (pasta fotos/) em nenhuma peça. Só fotos públicas do banco (Unsplash → banco/).
- **Post comum:** sempre foto pública do tema.
- **Carrossel com mais imagens:** capa, final e pelo menos 2 páginas do meio com foto (alternando página com foto e página só texto). Todas as fotos diferentes entre si e ligadas ao tema.
- Foto com pessoa: o rosto não pode ficar sob o texto/degradê; se ficar, troque a foto (prefira objetos, lugares e mãos).

## Estilos (aprovados em 11/11/2026) — alternar com o estilo atual
Ciclos em `render/rotacao.json` → `estilos` (um para post comum, outro para carrossel; avance o índice a cada peça).
Amostras: `render/amostras/estilos-7dias.json` e `render/amostras/claro-7dias.json` (imagens em `arte/amostra-*.png`).
- **atual**: post_foto.py / carrossel.py (fundo azul-marinho com foto grande).
- **claro**: carrossel_claro.py (fundo bege, títulos em pergunta, **negrito**; capa e final com foto pública).
- **moldura**: estilos.py, tela "moldura" (foto com cantos arredondados no alto, texto embaixo). Post comum = 1 tela moldura. Carrossel moldura = telas moldura (cada uma com foto diferente) + tela "final".
- **mito**: estilos.py, carrossel: "mito_capa" + 2 a 4 telas "mito" + 1 tela "moldura" no meio + "final".
- **lei**: estilos.py, tela "lei" (trecho literal da lei, conferido na fonte oficial, + "o que isso significa"). Post comum = 1 tela lei.
- **checklist**: estilos.py, tela "checklist" (4 a 5 itens + nota). Post comum = 1 tela checklist.
- **numero**: estilos.py, tela "numero" com foto pública no alto (ex.: "7 dias", "R$ 5 mil"). Post comum = 1 tela.
- **lei_checklist** (carrossel): "moldura" (capa) + "lei" + "moldura" + "checklist" + "final".
Em todos: só fotos públicas, convite "Fale comigo!" no rodapé, revisão de cada PNG antes de agendar. Post comum feito com estilos.py gera arte/<arquivo>-01.png (use essa URL).

### Estilos extras (aprovados em 11/11/2026, também no rodízio)
Amostras: `render/amostras/estilos-extras.json` (imagens `arte/amostra-extra-*.png`). Todos em estilos.py.
- **timeline** (3 a 4 marcos com prazos), **certo_errado** (3 itens por coluna), **pergunta** (rótulo padrão "PERGUNTA FREQUENTE"; use rotulo "ME PERGUNTARAM" só com pergunta real enviada pelo Caio), **juridiques** (termo + significado + exemplo), **tabela** (até 6 linhas), **fluxo** (2 a 3 perguntas Sim/Não + resultado). Post comum = 1 tela; foto dispensável.
- Carrosséis novos: **passo_a_passo** = "moldura" (capa) + "timeline" + "certo_errado" + "fluxo" ou "tabela" + "final"; **perguntas** = "moldura" (capa) + 2 a 3 telas "pergunta" + "juridiques" + "final".
- **mudou_lei**: fora do ciclo; só quando houver novidade legal real e recente (confirmada em fonte oficial ou grande veículo), no lugar do estilo da vez, sem avançar o ciclo.
