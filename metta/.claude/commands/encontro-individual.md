# Skill: Processar Encontro Individual METTA

**Acionamento:** `/encontro-individual`

Processa a transcrição de um encontro individual mensal de mentorada METTA, gera PDF com visual METTA oficial, atualiza o Google Doc cumulativo e envia por WhatsApp/e-mail.

## O que fazer quando acionado

Peça à Dani as informações abaixo se não foram fornecidas no comando:
1. **Nome da mentorada** (ex: Ana Paula Monteiro / Ethel Pinella)
2. **Número do encontro** (ex: 4º, 5º...)
3. **Link do Google Drive** com as anotações/transcrição do encontro

## Passo a passo

### 1. Ler a transcrição
- Acesse o arquivo no Google Drive pelo link fornecido
- Leia a seção "Próximas etapas" e "Detalhes" do documento do Gemini
- Extraia TODOS os to-dos atribuídos à mentorada

### 2. Organizar os to-dos por categoria
Agrupe as tarefas nas categorias existentes ou crie novas se necessário:
- 💰 Finanças & Gestão
- 🩺 Operacional & Clínico
- 🤖 Tecnologia & IA
- 📋 Documentação & Compliance
- 📚 Desenvolvimento Pessoal

Para cada tarefa inclua:
- Título objetivo em negrito
- Descrição detalhada do que fazer (1-2 linhas)

### 3. Gerar PDF com visual METTA oficial

Use o script Python `/tmp/gerar_checklist_metta.py` como base. Substitua as variáveis:

```python
NOME = "[Nome da mentorada]"
ESPECIALIDADE = "[Especialidade]"
ENCONTRO_NUM = "[Nº]º"
DATA = "[DD de Mês de AAAA]"
TEMA = "[Tema da sessão]"
RESUMO = "[Resumo da sessão]"
TAREFAS = [
    ("💰 FINANÇAS & GESTÃO", [
        ("Título da tarefa", "Descrição detalhada."),
    ]),
    # ... demais categorias
]
OUTPUT = "/tmp/METTA_Checklist_[Nome]_[N]Encontro.pdf"
```

Visual obrigatório:
- Cabeçalho **preto** com METTA em letras ouro (`#C9963A`), "T" em branco
- Subtítulo "MENTORIA ESTRATÉGICA" em ouro
- Checkboxes ☐ em ouro para cada tarefa
- Assinatura: "Simone Farah & Danielle Magalhães / Mentoria METTA — Fletic"

Execute: `python3 /tmp/gerar_checklist_metta.py` → envia o PDF resultante por WhatsApp e e-mail.

### 4. Atualizar o Google Doc da mentorada
Arquivo no Drive: `METTA — Encontros Individuais — [Nome da Mentorada]`

- Localize a seção `[Será preenchido após o encontro]` correspondente ao número do encontro
- Substitua pelo bloco completo com: data, tema da sessão, resumo e checklist de tarefas
- Mantenha os encontros futuros como placeholders

### 4. Atualizar o Notion
- Acesse a página da mentorada em: METTA → Encontros Individuais → Turma 1 — 2026 → [Nome]
- Marque o encontro como "Concluído" na tabela de status

### 5. Enviar por e-mail à mentorada
Use o Gmail para enviar o documento atualizado.

**Para Ana Paula Monteiro:** apcmonteiro55@hotmail.com
**Para Ethel Pinella:** (confirmar e-mail)

Assunto: `METTA | Encontro Individual [Nº] — Seus compromissos da sessão`

Corpo do e-mail:
```
Olá, [Nome]!

Ótima sessão hoje! 🙌

Segue em anexo o documento com os compromissos que combinamos. Você pode marcar cada item conforme for avançando.

Qualquer dúvida, estamos por aqui.

Abraços,
Simone Farah & Danielle Magalhães
Mentoria METTA — Fletic
```

Anexar o Google Doc exportado como PDF (baixar do Drive e anexar).

## IDs importantes

| Item | ID / Referência |
|---|---|
| Google Doc — Ana Paula | `1gUsTOZXwEEzG7t4Yi4dLEl4C7yNrd9tIfbB5ZG4xo5s` |
| Google Doc — Ethel | `1iZAvgASGo6OsdlBcL8rNiSdLw2HZ46ibz-r_rrk25A0` |
| Notion — Ana Paula | `373c8095-3f7d-8197-ae7c-e1abfc22765b` |
| Notion — Ethel | `373c8095-3f7d-81a9-ad53-c41cd981bb27` |
| Drive — Pasta METTA | `1Y2OH-ZX5KR2XDvJsjhu-3jn6D86a8ggd` |
