#!/usr/bin/env python3
"""Gera projetos/*.html a partir dos dados abaixo. Rode: python3 gerar.py"""
import re, html
V = "7"  # versão do CSS: suba a cada mudança para furar o cache do navegador
idx = open("index.html").read()
ARQ = re.search(r'(<div class="arch">.*?</ol>)', idx, re.S).group(1)

P = [
 dict(slug="raio-x", nome="Raio-X Comercial", papel="dirigi", cat="ML + LLM · projeto de time (4 pessoas)",
  frase="Prepara a primeira reunião de um vendedor B2B com uma grande empresa, em minutos, usando só dado público. O LLM escreve o texto, mas não pode escrever nenhum número.",
  nums=[("595","empresas da CVM"),("384 mil","linhas contábeis"),("k = 4","silhueta corrigida"),("US$ 0,0008","por relatório")],
  capa=("raiox-thumb.jpg","Tela de teste, com empresas e números inventados: indicadores da empresa comparados com o grupo de empresas parecidas."),
  galeria=[("raiox-tela.jpg","A tela completa: resumo, perguntas para a reunião e empresas parecidas para prospectar. Todo número vem do dado; o texto vem do LLM.","")],
  links=[],
  blocos=[
   ("O problema","<p>Antes da primeira reunião com uma grande conta, o vendedor B2B passa horas juntando balanço, notícia e concorrente à mão, e mesmo assim chega sem saber o que perguntar.</p><p>A pergunta do projeto: dá para gerar esse preparo em minutos, só com dado aberto, sem a IA inventar número?</p>"),
   ("Dados","<ul><li>DFP da CVM (demonstrações financeiras padronizadas, dado aberto), de 2023 a 2025.</li><li>595 empresas e 384.591 linhas de contas, carregadas e modeladas em PostgreSQL.</li><li>Indicadores derivados: receita, crescimento em dois anos, margem EBIT, margem líquida, endividamento e ativo.</li></ul>"),
   ("Como funciona","<ol><li>O usuário escolhe a empresa e descreve o que vende.</li><li>O sistema calcula os indicadores e compara com o grupo de empresas parecidas.</li><li>O k-means define o grupo; os 5 vizinhos mais próximos viram sugestão de prospecção.</li><li>O LLM escreve o resumo e as perguntas para a reunião com <b>marcadores no lugar dos números</b>.</li><li>Um validador confere a saída e o código troca cada marcador pelo valor real. Se o texto citar um número que não veio do dado, ele é barrado.</li></ol>"),
   ("Decisão que mais importou","<p>A primeira clusterização deu silhueta de <b>0,77</b>, que parece ótima. Olhando os grupos, 567 das 595 empresas caíam num grupo só: a métrica estava boa e o resultado era inútil. Troquei para <b>k = 4</b>, com silhueta de 0,29 e grupos que fazem sentido de negócio. A lição: métrica sem olhar o dado engana.</p>"),
   ("Custo e qualidade","<ul><li>Cerca de US$ 0,0008 por relatório, com um modelo leve e saída estruturada.</li><li>259 testes automatizados no projeto do time.</li><li>Interface em Streamlit; entrega com Docker.</li></ul>"),
  ],
  fiz="Defini a regra de que o LLM não escreve número e o desenho do validador; escolhi e corrigi o k; desenhei a avaliação e a tela inicial; coordenei a minha parte.",
  dirigi="O código do ML, da camada de IA e do validador foi escrito com Claude Code sob a minha direção, revisado e testado por mim.",
  falta="Repositório privado do time (não posso abrir o código). Os pesos de comparação ainda não foram validados com vendedores reais.",
  tags=["Python","pandas","PostgreSQL","scikit-learn","LangChain","Streamlit","Docker"]),
 dict(slug="bike-store", nome="Bike Store: do caos no banco ao modelo estrela", papel="fiz", cat="SQL e modelagem",
  frase="Uma base de vendas com encoding corrompido, hierarquia com NULL e \"n/a\" contando como dado. Sem permissão de escrita, limpei tudo em views SQL, sem tocar na origem.",
  nums=[("~60 mil","linhas de vendas"),("18,4 mil","clientes"),("4","problemas silenciosos"),("95%","do lucro em bikes")],
  capa=("bike-modelo.jpg","Modelo estrela final: a fato de vendas no centro, dimensões de produtos, clientes e calendário. O BI lê só as views limpas."),
  links=[("Código SQL no GitHub","https://github.com/EduardoBrame/bike-store-sql"),("Artigo completo no Medium","https://medium.com/@galicianie/loja-de-bicicletas-analytics-do-caos-no-banco-de-dados-a-um-dashboard-de-neg%C3%B3cio-com-sql-e-power-eddb010e2efd")],
  blocos=[
   ("O problema","<p>A empresa queria saber onde ganhava receita, onde ganhava lucro e quem eram os clientes. Três perguntas simples, que nenhum relatório respondia com confiança porque a base tinha erros que não aparecem em consulta comum.</p>"),
   ("Os 4 problemas","<ol><li><b>Encoding corrompido:</b> 20 nomes com caracteres latinos quebrados (UTF-8 lido como Latin-1). Corrigido com REPLACE encadeado na view.</li><li><b>Hierarquia com NULL:</b> a categoria CO_PE voltava sem categoria e subcategoria, e os pedais sumiam dos relatórios. Corrigido com CTE + COALESCE + UNION ALL.</li><li><b>Datas como texto vazio:</b> 19 pedidos com data \"\" em vez de NULL, que quebram série temporal. Corrigido com checagem de comprimento.</li><li><b>\"n/a\" como valor:</b> passava em filtros IS NOT NULL e inflava contagens. Corrigido com NULLIF.</li></ol>"),
   ("Decisão de arquitetura","<p>Sem acesso de escrita à tabela original, toda a limpeza ficou em <b>views</b> no PostgreSQL. O Power BI conecta só nas views. Qualquer correção futura no SQL chega ao painel sem mexer no modelo.</p>"),
   ("Validações","<ul><li>Chaves sem duplicata nas dimensões e granularidade íntegra na fato (nenhum pedido + produto repetido).</li><li>sales_amount = quantity × price em 100% das linhas.</li><li>Nenhuma data de envio anterior à data do pedido; lead time médio de 7 dias.</li></ul>"),
   ("O que os dados disseram","<ul><li>95% do lucro vem de bicicletas, com risco concentrado em um modelo.</li><li>Acessórios são 18% dos pedidos, mas com 63% de margem contra 39% das bikes: cross-sell sobe a margem sem subir o volume.</li></ul>"),
  ],
  galeria=[("bike-encoding.jpg","Correção do encoding direto na view, sem descartar nenhum registro.","")],
  fiz="Todo o diagnóstico, as views SQL, a modelagem e a análise.", dirigi="",
  falta="Próximo passo de estudo: transformar as views em modelos dbt com testes (not_null, unique, relationships) e carga incremental.",
  tags=["PostgreSQL","SQL","Star Schema","DAX","Power BI"]),
 dict(slug="arvore-segura", nome="Árvore Segura Londrina", papel="dirigi", cat="Ingestão de dados públicos e geo",
  frase="Diz à Defesa Civil quais árvores de rua vistoriar primeiro, cruzando o inventário público da prefeitura com previsão de vento e fiação.",
  nums=[("41 mil","registros coletados"),("28,7 mil","árvores avaliadas"),("2.197","risco alto"),("415","mortas em pé")],
  capa=("arvore-mapa.jpg","O mapa funciona offline: indicadores, alerta de vento do dia, filtro por bairro e a fila de vistoria ordenada pela nota."),
  links=[("Abrir o mapa ao vivo","../demos/arvore-segura.html")],
  blocos=[
   ("O problema","<p>Em dia de temporal, árvores caem em fios, carros e casas. A cidade tem um inventário com dezenas de milhares de árvores, mas ninguém tem tempo de olhar tudo. A pergunta: por onde começar?</p>"),
   ("Ingestão","<ul><li>Fonte: Geoportal da Prefeitura de Londrina (API ArcGIS REST, dado aberto), mais a previsão de vento da Open-Meteo.</li><li>O servidor devolve no máximo 2.000 registros por consulta, então a coleta pagina com <code>resultOffset</code> até acabar.</li><li>Dos 41.077 registros, 12.383 (covas vazias e tocos) saem por uma regra explícita, documentada, e não por descarte silencioso.</li></ul>"),
   ("Nota de risco","<p>Nota = pontos de defeito × porte + fiação, uma simplificação do método ISA TRAQ, usado por arboristas. As árvores com maior nota formam a fila de vistoria.</p>"),
   ("Como eu levaria para produção","<ol><li>Transformar o script numa DAG agendada (Airflow ou similar).</li><li>Retry com backoff e checkpoint do último offset, para retomar se a API cair no meio.</li><li>Chave única por árvore, para a carga ser idempotente e incremental.</li><li>Checagem de contagem e de nulos a cada execução, com alerta se a fonte mudar.</li></ol>"),
  ],
  fiz="Defini o problema, as regras de descarte e a fórmula da nota, e conferi os números.", dirigi="Os scripts de coleta, a nota e o mapa foram escritos com Claude Code sob a minha direção.",
  falta="Os pesos da nota não foram calibrados com um técnico e o inventário é de 2018, com 18 bairros. É um protótipo de hackathon.",
  tags=["Python","pandas","shapely","ArcGIS REST","Open-Meteo"]),
 dict(slug="cerebro", nome="Cérebro: assistente 24 h na Azure", papel="dirigi", cat="Infra, agentes e custo",
  frase="Um assistente no WhatsApp que escolhe o modelo de IA pela dificuldade do pedido, usa as minhas ferramentas e pede confirmação antes de qualquer ação irreversível. Roda numa VM Linux sem porta de administração aberta.",
  nums=[("4","níveis de modelo"),("3","provedores com failover"),("12","achados de segurança corrigidos"),("2 min","sync da memória")],
  capa=None, links=[],
  blocos=[
   ("Arquitetura", "FULL"),
   ("O problema","<p>Eu queria usar IA no dia a dia sem abrir arquivos, sem pagar modelo caro para pergunta simples e sem deixar a IA fazer algo irreversível sozinha.</p>"),
   ("Decisões","<ul><li><b>Sem SSH público:</b> administração só por rede privada; emergência pelo run-command da Azure.</li><li><b>Modelo pequeno na triagem:</b> a maior parte dos pedidos não precisa do modelo caro. Cada resposta mostra modelo, tokens e custo.</li><li><b>Confirmação humana:</b> ação irreversível (evento com convidado, mudança de código) espera um \"sim\".</li><li><b>Revisão independente:</b> três agentes revisores (infra, segurança, UX). A revisão de segurança achou 12 problemas, corrigidos e testados antes de ligar.</li><li><b>Privacidade:</b> mensagem de terceiro é dado, nunca ordem; segredos ficam fora do código; nada das mensagens é publicado.</li></ul>"),
  ],
  fiz="A arquitetura, as regras de segurança e custo e os testes de aceitação.", dirigi="A implementação (Python, systemd, configuração da VM) foi feita com agentes de IA sob a minha direção.",
  falta="A infra foi criada pelo az CLI, não por Terraform; não há CI/CD nem alerta de queda; é uma VM só, em uma região; o failover foi testado em simulação. São exatamente os meus próximos 30 dias de estudo.",
  tags=["Azure","Linux","systemd","Caddy","Tailscale","Python","Git"]),
 dict(slug="varejo", nome="Varejo: uma regra explícita para cada sujeira", papel="fiz", cat="ETL e qualidade de dados",
  frase="12.575 transações com preço nulo, linhas fantasmas e produtos sem nome. Cada caso virou uma regra explícita antes de modelar.",
  nums=[("12.575","transações"),("628","linhas salvas"),("600+","nomes recuperados"),("604","fantasmas fora")],
  capa=("varejo-merge.jpg","Recuperação de nomes: merge por chave composta (categoria + preço) contra uma \"tabela da verdade\" de pares únicos. 609 de 609 linhas casaram."),
  links=[("Artigos no Medium","https://medium.com/@galicianie/")],
  blocos=[
   ("Os 4 problemas","<ol><li><b>Preço nulo (5%):</b> imputado por total ÷ quantidade, o valor exato da própria linha. 628 linhas preservadas.</li><li><b>Linhas fantasmas:</b> 604 registros só com preço, sem quantidade nem total. Excluídos para não distorcer o ticket médio.</li><li><b>Produto sem nome:</b> categoria + preço identificavam o item de forma única; virou chave composta para recuperar mais de 600 nomes.</li><li><b>Data solta:</b> calendário dimensional completo, necessário para comparação entre períodos.</li></ol>"),
   ("Estatística","<p>Outliers saíram do cálculo do ticket médio com μ±2σ, cerca de 5% das transações. Testei ±3σ antes: cobria 100% dos dados e não mudava nada.</p>"),
  ],
  galeria=[("varejo-modelo.jpg","Do arquivo plano ao modelo estrela: staging desligada da carga, fato de vendas e dimensões de itens e calendário.","")],
  fiz="Todo o ETL, a modelagem e a análise.", dirigi="",
  falta="Feito em Power Query. Hoje eu levaria as mesmas regras para SQL ou dbt, versionadas e testadas.",
  tags=["Power Query","Star Schema","DAX","estatística"]),
 dict(slug="drina", nome="DRINA: 3º lugar no SmartCities Hackathon", papel="fiz", cat="Produto e pitch · time de 5",
  frase="Toda a prefeitura num só contato de WhatsApp: o cidadão conta uma vez, por texto ou áudio, e todos os órgãos certos ficam sabendo.",
  nums=[("3º","lugar no hackathon"),("5","pessoas no time"),("20","serviços no protótipo Onde Resolvo"),("13/20","acertos só com regras")],
  capa=("drina-produto.jpg","Ilustração do produto com dados fictícios: a conversa no WhatsApp e o painel único da cidade, com a fila por prioridade."),
  links=[("Testar o Onde Resolvo","../demos/onde-resolvo.html")],
  blocos=[
   ("O problema","<p>Quem mais precisa da prefeitura (idosos, quem tem pouco tempo) não vai baixar oito aplicativos. E cada órgão recebe o mesmo problema várias vezes, sem saber que outro já recebeu.</p>"),
   ("A proposta","<p>Um contato só, no canal que a pessoa já usa. A IA transcreve, classifica e pergunta o que falta; um núcleo de unificação junta relatos repetidos, avisa todos os órgãos envolvidos e devolve o status. O mapa do briefing reaproveita os dados do Árvore Segura.</p>"),
   ("Onde Resolvo (protótipo funcional)","<p>O morador descreve o problema com as próprias palavras. Antes de qualquer análise, um filtro troca CPF, telefone e e-mail por [removido]. Depois um classificador indica um entre 20 serviços. A versão só com regras acertou 13 de 20 frases novas (65%); a versão com IA fica como opção.</p>"),
  ],
  galeria=[("drina-arquitetura.jpg","Arquitetura proposta: canais, conversa com IA, núcleo de unificação, órgãos e gestão.","full"),("onde-resolvo.jpg","Onde Resolvo: protótipo com filtro de dados pessoais antes da classificação.","full")],
  fiz="O pitch, o briefing e os scripts que geram as imagens do briefing.", dirigi="O protótipo Onde Resolvo foi construído com IA sob a minha direção.",
  falta="É uma proposta de hackathon: não há integração real com os sistemas da prefeitura.",
  tags=["produto","pitch","privacidade","classificação"]),
]

HEAD = '''<!doctype html><html lang="pt-BR" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t} · Eduardo Bramé</title><meta name="description" content="{d}"><meta property="og:image" content="https://eduardobrame.github.io/assets/img/{og}">
<script>try{{var t=localStorage.getItem('tema');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="../assets/style.css?v={v}"></head><body>
<nav><div class="wrap"><a class="me" href="../">Eduardo Bramé</a><a href="../#projetos">Projetos</a><a class="ct" href="../#contato">Contato</a><button id="tema" aria-label="Alternar tema claro/escuro">◐</button></div></nav><main class="wrap">'''
FOOT = '''</main><footer><div class="wrap">Eduardo Bramé · Londrina-PR · 2026</div></footer>
<script>document.getElementById('tema').onclick=function(){var r=document.documentElement,n=r.dataset.theme==='light'?'dark':'light';r.dataset.theme=n;try{localStorage.setItem('tema',n)}catch(e){}};</script></body></html>'''
ROT = {"fiz":("p-fiz","Fiz"),"dirigi":("p-dirigi","Dirigi IA e validei")}

for i,p in enumerate(P):
    cls,lab = ROT[p["papel"]]
    og = (p["capa"] or ("arvore-thumb.jpg",))[0]
    o = [HEAD.format(t=p["nome"], d=html.escape(p["frase"]), og=og, v=V)]
    o.append(f'<a class="crumb" href="../#projetos">← Todos os projetos</a><header class="phero card {p["papel"]}" style="background:none;border:0;box-shadow:none;padding-left:0;padding-right:0"><span class="papel {cls}">{lab}</span><span class="cat">{p["cat"]}</span><h1>{p["nome"]}</h1><p class="lead">{p["frase"]}</p>')
    o.append('<div class="nums">'+"".join(f'<div><b>{a}</b>{b}</div>' for a,b in p["nums"])+'</div>')
    if p["links"]: o.append('<div class="acoes">'+"".join(f'<a class="btn{"" if k==0 else " sec"}" href="{u}">{t} →</a>' for k,(t,u) in enumerate(p["links"]))+'</div>')
    o.append('<div class="tags">'+"".join(f'<span class="tag">{t}</span>' for t in p["tags"])+'</div></header>')
    if p["capa"]: o.append(f'<figure class="capa"><img src="../assets/img/{p["capa"][0]}" alt="{html.escape(p["capa"][1])}" loading="eager"><figcaption>{p["capa"][1]}</figcaption></figure>')
    for t,b in p["blocos"]:
        if b == "FULL": o.append(f'<section class="bloco" id="sistema" style="display:block"><h2 style="margin-bottom:20px">{t}</h2>{ARQ}</section>')
        else: o.append(f'<section class="bloco"><h2>{t}</h2><div>{b}</div></section>')
    if p.get("galeria"):
        o.append('<section class="bloco"><h2>Imagens</h2><div class="gal">'+"".join(f'<figure class="{c}"><img src="../assets/img/{f}" alt="{html.escape(cap)}" loading="lazy"><figcaption>{cap}</figcaption></figure>' for f,cap,c in p["galeria"])+'</div></section>')
    pap = f'<div><span class="papel p-fiz">Fiz</span><p>{p["fiz"]}</p></div>' + (f'<div><span class="papel p-dirigi">Dirigi IA e validei</span><p>{p["dirigi"]}</p></div>' if p["dirigi"] else "")
    o.append(f'<section class="bloco"><h2>Meu papel</h2><div class="papeltxt">{pap}</div></section>')
    o.append(f'<section class="bloco"><h2>O que falta</h2><div><p>{p["falta"]}</p></div></section>')
    ant, prox = P[i-1], P[(i+1)%len(P)]
    o.append(f'<div class="prox"><a href="{ant["slug"]}.html">← Anterior<b>{ant["nome"]}</b></a><a href="{prox["slug"]}.html" style="text-align:right">Próximo →<b>{prox["nome"]}</b></a></div>')
    o.append(FOOT)
    open(f'projetos/{p["slug"]}.html','w').write("\n".join(o))
print("ok", len(P))
