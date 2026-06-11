# Plano de Automação METTA — Roadmap Completo

**Responsável operacional:** Tamires Bala (COO)  
**Produto:** METTA Mentoria Estratégica  
**Objetivo:** Eliminar trabalho manual repetitivo e garantir que Simone e Dani foquem só no que importa — relação humana com as mentoradas.

---

## 🔴 Prioridade 1 — Já disponível (usar agora)

### 1. Checklist pós-encontro individual → DOCX automático
**Skill:** `/encontro-individual`  
**O que faz:** A partir das anotações/transcrição do encontro, gera automaticamente:
- DOCX com logo METTA, checkboxes clicáveis, tarefas por categoria
- Atualiza a página da mentorada no Notion
- Vincula o arquivo no Google Drive

**Como acionar:**
```
/encontro-individual
```
Informar: nome da mentorada, número do encontro, link do Drive com anotações.

**Template base:** `metta/templates/checklist_encontro_individual_template.docx`

---

### 2. Briefing diário de operações
**Skill:** `/briefing-diario`  
**O que faz:** Resume o status do METTA no dia — compromissos, tarefas pendentes, mentoradas em risco.

---

### 3. Onboarding de nova mentorada
**Skill:** `/metta-onboarding`  
**O que faz:** Prepara todo o material de boas-vindas para uma nova mentorada.

---

## 🟡 Prioridade 2 — Implementar esta semana

### 4. E-mail automático pós-encontro
**O que automatizar:**
- Após gerar o DOCX, enviar automaticamente por Gmail para a mentorada
- Assunto padrão: `METTA | Encontro Individual [Nº] — Seus compromissos da sessão`
- Anexar o DOCX + link do Notion

**Acrescentar ao skill `/encontro-individual` — passo 5.**

**E-mails:**
| Mentorada | E-mail |
|---|---|
| Ana Paula Monteiro | apcmonteiro55@hotmail.com |
| Ethel Pinella | (confirmar com Dani) |

---

### 5. Lembrete automático pré-encontro (48h antes)
**O que automatizar:**
- Verificar Google Calendar todo dia às 8h
- Se houver encontro em 48h → enviar e-mail/WhatsApp para a mentorada com:
  - Confirmação do horário
  - Link da reunião
  - Lembrete dos compromissos pendentes do encontro anterior

**Acionar:** Carla (Admin) verifica agenda e dispara o lembrete.

---

### 6. CRM — follow-up de tarefas não cumpridas
**O que automatizar:**
- No dia anterior ao próximo encontro, verificar o Notion
- Se alguma tarefa do encontro anterior ainda estiver `[ ]` → gerar alerta para Simone
- Simone decide se menciona na sessão ou envia mensagem de suporte

---

## 🟢 Prioridade 3 — Implementar este mês

### 7. Atualização automática do status no Notion
**O que automatizar:**
- Após cada encontro ser processado, marcar automaticamente como "Concluído" na tabela do Notion
- Atualizar a data do próximo encontro

**Páginas Notion:**
| Mentorada | ID Notion |
|---|---|
| Ana Paula | `373c8095-3f7d-8197-ae7c-e1abfc22765b` |
| Ethel | `373c8095-3f7d-81a9-ad53-c41cd981bb27` |

---

### 8. Relatório mensal automático por mentorada
**O que automatizar:**
- No último dia de cada mês, gerar PDF com:
  - Encontros realizados no mês
  - % de tarefas cumpridas
  - Próximos passos
- Enviar para Dani e Simone por e-mail

---

### 9. Pitch de vendas — geração automática de proposta personalizada
**O que automatizar:**
- Após reunião SPIN com lead, acionar skill de proposta
- Gerar PDF personalizado com nome do lead, especialidade e valores
- Enviar por e-mail com 1 clique

**Base:** slides de investimento do deck METTA (slides 13 e 14)

---

### 10. Controle financeiro — alertas de inadimplência
**O que automatizar:**
- Verificar planilha de recebíveis semanalmente
- Se pagamento > 5 dias em atraso → alertar Dani
- Gerar rascunho de e-mail de cobrança para aprovação

---

## 📋 Próximos passos imediatos

| # | Ação | Responsável | Prazo |
|---|---|---|---|
| 1 | Usar `/encontro-individual` no próximo encontro da Ana Paula | Dani/Simone | Próximo encontro |
| 2 | Confirmar e-mail da Ethel Pinella | Dani | Esta semana |
| 3 | Organizar Drive METTA (pastas por mentorada) | Dani + Tamires | Amanhã |
| 4 | Atualizar slides do pitch com versão Fernanda | Fernanda Lima | A combinar |
| 5 | Implementar e-mail automático pós-encontro | Claude + Dani | Esta semana |

---

## 🗂️ IDs e Referências

| Item | ID / Referência |
|---|---|
| Google Doc — Ana Paula | `1gUsTOZXwEEzG7t4Yi4dLEl4C7yNrd9tIfbB5ZG4xo5s` |
| Google Doc — Ethel | `1iZAvgASGo6OsdlBcL8rNiSdLw2HZ46ibz-r_rrk25A0` |
| Notion — Ana Paula | `373c8095-3f7d-8197-ae7c-e1abfc22765b` |
| Notion — Ethel | `373c8095-3f7d-81a9-ad53-c41cd981bb27` |
| Drive — Pasta METTA | `1Y2OH-ZX5KR2XDvJsjhu-3jn6D86a8ggd` |
| Logo METTA (Drive) | `1GM72AmIr9WBc6iHs7U-fkl-VrkS7p33B` |
| Template DOCX | `metta/templates/checklist_encontro_individual_template.docx` |
| Briefing design slides | `metta/briefings/briefing_design_slides_investimento.md` |
