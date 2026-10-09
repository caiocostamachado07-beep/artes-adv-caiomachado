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
