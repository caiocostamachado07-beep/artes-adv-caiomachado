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
