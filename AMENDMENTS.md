# AMENDMENTS — Protocolo Constitucional de Mudança do Atlas

Este arquivo define o único procedimento válido para emendar o Atlas.
Qualquer alteração fora deste protocolo é nula.

## Definições

- **Proposta de Emenda**: conjunto imutável de mudanças no Atlas, expresso como diff assinado.
- **Root Constitucional**: hash raiz do estado selado do Atlas.
- **Janela Constitucional**: período de tempo previamente declarado para deliberação e assinatura.
- **Quórum Criptográfico**: conjunto mínimo de assinaturas válidas exigidas para aprovação.
- **Evidência de Inclusão**: prova de inclusão Merkle das mudanças no snapshot proposto.

## Requisitos Obrigatórios

Uma emenda só é válida se **todas** as condições abaixo forem satisfeitas:

1. **Hash da Proposta**
   - O diff completo deve ser hashado com algoritmo imutável e declarado publicamente.
2. **Janela Temporal**
   - A janela deve ser registrada antes do início da coleta de assinaturas.
3. **Quórum Criptográfico**
   - O quórum mínimo deve ser atendido com assinaturas verificáveis.
4. **Evidência Anexada**
   - Todas as evidências exigidas por leis e invariantes afetados devem estar anexadas.
5. **Merkle Inclusion**
   - Deve existir prova de inclusão Merkle do diff no snapshot proposto.
6. **Nova Root Assinada**
   - O novo Root Constitucional deve ser assinado pelo quórum requerido.
7. **Compatibilidade de Escopo**
   - A emenda não pode expandir o escopo do Atlas além do definido no REGIME.md.

## Procedimento

1. **Anunciar Proposta**
   - Publicar o hash da proposta e o diff completo.
2. **Abrir Janela Constitucional**
   - Declarar início e fim da janela temporal.
3. **Recolher Evidências**
   - Anexar evidências exigidas por leis e invariantes afetados.
4. **Assinaturas**
   - Coletar assinaturas até atingir o quórum criptográfico.
5. **Selagem**
   - Gerar o snapshot, a prova Merkle e o novo Root Constitucional.
6. **Registro**
   - Registrar a emenda aprovada em `signatures/` com data, hash e quórum.

## Invalidade

Qualquer passo omitido ou fora da ordem invalida a emenda.
Emendas inválidas não geram novo Root Constitucional.
