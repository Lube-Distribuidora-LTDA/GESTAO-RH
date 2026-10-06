# BI de Absenteísmo RH — Lube Distribuidora

Sistema executivo de Business Intelligence e Gestão Estratégica de Absenteísmo e Frequência para Recursos Humanos da **Lube Distribuidora**.

---

## 🎯 Principais Recursos

- **Dashboard Executivo Dinâmico**: Visualização completa de KPIs, indicadores de ausências (Justificadas, Injustificadas, Folgas/BH, Treinamentos).
- **Integração Nativa com Supabase (PostgreSQL Cloud)**:
  - Leitura e gravação de ocorrências em alta velocidade.
  - Sincronização em tempo real via **WebSockets (Supabase Realtime)**.
  - Cadastro de novos registros via modal interativo com autocomplete de colaboradores, cargos e setores.
- **Importação de Planilhas Excel (.xlsx, .csv)**:
  - Processamento automatizado de novas bases com sincronização em lote (*bulk insert*) direto para a nuvem.
- **Exportação para Excel (.xlsx)**:
  - Download customizado dos dados filtrados com 1 clique.
- **Filtros Estratégicos & Atalhos Executivos**:
  - Filtro por mês, tipo de ausência, setor, cargo e colaborador.
  - Atalhos pré-configurados: *Foco Faltas Injustificadas*, *Pico Segundas-Feiras*, *Setor Crítico (ENTREGA)*, etc.
- **Dark Mode / Light Mode**: Interface moderna com Glassmorphism, responsiva e pronta para apresentações executivas.

---

## 🏗️ Estrutura do Projeto

```text
├── index.html                  # Ponto de entrada da aplicação para deploy no Vercel
├── Dashboard Absenteísmo.html  # Cópia do Dashboard com suporte a execução local
├── supabase-client.js          # Camada de comunicação com a API e Realtime do Supabase
├── supabase_schema.sql         # DDL completo do banco PostgreSQL (tabelas, views, triggers, RLS)
├── data.js                     # Fallback de dados para contingência offline
├── dashboard_dataset.json      # Dataset estruturado em JSON
├── lube-logo.png               # Logotipo oficial Lube Distribuidora
├── vercel.json                 # Configuração de rotas estáticas do Vercel
└── deploy_schema.ps1           # Script PowerShell para deploy de DDL no Supabase
```

---

## 🔒 Acesso

O sistema é protegido pela **Sentinela Lube**: só entra quem tem login no **Painel Lube** com permissão
para o RH Absenteísmo (slug `rh-absenteismo`). Quem não tem é levado para a tela de login do portal
(`https://painel-lube-distribuidora.vercel.app`); as rotas `/api/*` respondem 401.

- O guarda mora em `middleware.ts` + `sentinela-guarda.ts`, na raiz do repositório (Routing Middleware
  da Vercel, runtime nodejs). Não edite o `sentinela-guarda.ts` aqui: a cópia canônica fica no
  repositório do portal (`guarda/`).
- A exigência de login é ligada e desligada no painel da Sentinela (Configuração › exige login). Se a
  central não responder, o guarda continua fechado: só passa quem tem sessão válida do Painel Lube.
- Desde 2026-10-06 o "exige login" está **ligado** (`exige_login = true` em `sentinela.sistemas`),
  sem rotas públicas: sem sessão, a página vai para o portal (`/?abrir=rh-absenteismo`).
- Saúde do guarda: `https://rh-absentismo.vercel.app/.sentinela/saude`.
- O guarda protege o site e as rotas `/api/*`, não o acesso direto ao banco do Supabase.

---

## 🚀 Deploy no Vercel

1. Conecte sua conta do **Vercel** ao repositório GitHub `RH-absenteismo`.
2. O Vercel detectará automaticamente o arquivo `index.html` e `vercel.json`.
3. Clique em **Deploy**. A aplicação estará online instantaneamente com SSL e CDN global.

---

## 📊 Banco de Dados (Supabase PostgreSQL)

- **Projeto**: `RH Absenteísmo` (`jhznrwmwszpfogvbjnjx`)
- **Tabelas**:
  - `ocorrencias_absenteismo`
  - `colaboradores`
  - `setores`
  - `cargos`
  - `motivos_ausencia`
  - `historico_importacoes`
- **Views Analíticas**: `vw_kpis_absenteismo`, `vw_resumo_setor`, `vw_resumo_motivo`, `vw_resumo_dia_semana`, `vw_ranking_injustificadas`, `vw_evolucao_mensal`.
