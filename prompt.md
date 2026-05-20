# Projeto A3 — Inteligência Artificial
## Universidade São Judas Tadeu

---

# Contexto do Projeto

Este projeto está sendo desenvolvido para a disciplina de Inteligência Artificial da Universidade São Judas Tadeu como parte da avaliação A3.

O objetivo principal é aplicar conceitos de aprendizado supervisionado utilizando um comitê de classificadores (ensemble) para resolver um problema de classificação baseado em dados reais.

O projeto será desenvolvido exclusivamente em Python utilizando um dataset público do Kaggle em formato CSV.

---

# Objetivo Acadêmico

O trabalho precisa obrigatoriamente contemplar:

- Pré-processamento de dados
- Análise exploratória (EDA)
- Modelagem supervisionada
- Pelo menos 3 classificadores individuais
- Construção de ensemble/comitê
- Avaliação de métricas
- Matriz de confusão
- Discussão crítica dos resultados

O projeto deve manter um nível acadêmico universitário, sem fugir do escopo proposto pela disciplina.

---

# Tema do Projeto

## Predição de Asteroides Potencialmente Perigosos para a Terra

O sistema utilizará Machine Learning para analisar características orbitais e físicas de asteroides e prever a possibilidade de um objeto ser considerado potencialmente perigoso para a Terra.

---

# Dataset

Dataset utilizado:
NASA JPL Small-Body Database (Kaggle CSV)

O projeto deve trabalhar prioritariamente em cima do dataset CSV já fornecido.

Evitar dependências externas excessivas ou arquiteturas complexas fora do escopo acadêmico.

---

# Tipo de Problema

Problema de:
- CLASSIFICAÇÃO SUPERVISIONADA

Objetivo:
- prever se um asteroide é potencialmente perigoso (PHA)

---

# Variável Target

## Target (y)

PHA — Potentially Hazardous Asteroid

Classes:
- 1 → Asteroide potencialmente perigoso
- 0 → Asteroide não perigoso

---

# Features Atuais

As principais variáveis utilizadas atualmente são:

- q
- ad
- H
- ma
- per
- e
- a
- i

Possíveis interpretações:
- velocidade orbital
- tamanho/magnitude
- excentricidade orbital
- período orbital
- inclinação orbital
- distância orbital

---

# Requisitos Obrigatórios da Faculdade

O projeto PRECISA conter:

## Pré-processamento
- tratamento de valores ausentes
- normalização/padronização
- encoding quando necessário

## Modelagem
Treinar pelo menos 3 modelos:
- KNN
- Naive Bayes
- SVM
- Árvores de decisão
- Redes neurais

## Ensemble
Criar um comitê de classificadores utilizando:
- hard voting
ou
- soft voting

## Métricas
Avaliar:
- Accuracy
- Precision
- Recall
- F1-score
- Matriz de confusão

---

# Estrutura Atual do Projeto

Atualmente o projeto já possui:

- carregamento do dataset
- análise exploratória básica
- tratamento de nulos
- imputação por mediana
- balanceamento de classes
- undersampling
- divisão treino/teste
- StandardScaler
- validação cruzada
- ensemble com VotingClassifier

---

# Modelos Implementados

## Classificadores Individuais
- KNN
- Gaussian Naive Bayes
- Decision Tree
- SVM
- MLPClassifier

## Ensemble
- Hard Voting
- Soft Voting

---

# Métricas Utilizadas

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

---

# Cuidados Importantes

## Data Leakage

Evitar utilizar features que entreguem diretamente o target.

Exemplo:
- MOID
- neo

Essas variáveis podem caracterizar vazamento de dados dependendo da abordagem utilizada.

---

# Dataset Desbalanceado

O dataset possui forte desbalanceamento entre:
- asteroides perigosos
- não perigosos

Portanto:
- accuracy isolada NÃO é suficiente
- recall possui alta importância

---

# Interpretação Importante

Neste problema:
- Falsos negativos são perigosos

Ou seja:
- um asteroide perigoso sendo classificado como seguro é um problema crítico

Por isso:
- recall deve receber atenção especial

---

# Objetivos Técnicos

O projeto deve:
- possuir código organizado
- possuir boa legibilidade
- possuir separação lógica das etapas
- possuir visualizações claras
- possuir análise crítica

---

# Melhorias Desejadas

O Claude pode sugerir melhorias como:

## EDA
- heatmaps
- correlação
- distribuição de classes
- boxplots
- histogramas

## Engenharia de Features
- orbital_risk
- orbital_diameter
- energy_proxy

## Ensemble
- weighted voting
- stacking
- comparação entre ensembles

## Visualizações
- feature importance
- PCA
- clustering visual
- ROC curve
- métricas comparativas

## Organização
Sugestões de modularização:
- /data
- /models
- /ensemble
- /evaluation
- /visualization
- /utils

---

# Limitações do Projeto

O projeto NÃO deve:
- virar uma arquitetura enterprise exagerada
- depender fortemente de APIs externas
- fugir do escopo acadêmico
- utilizar tecnologias fora de Python
- abandonar o dataset principal do Kaggle

---

# Objetivo Final

Queremos construir:
- um projeto tecnicamente sólido
- visualmente organizado
- academicamente correto
- profissional o suficiente para portfólio/GitHub
- mas ainda compatível com os requisitos universitários

---

# O que esperamos do Claude

Esperamos sugestões sobre:

- arquitetura do projeto
- melhorias técnicas
- melhorias de organização
- melhorias de visualização
- melhorias de ensemble
- melhorias de métricas
- possíveis otimizações
- storytelling técnico
- preparação para apresentação
- clareza do pipeline de Machine Learning

O Claude deve agir como um engenheiro de Machine Learning revisando um projeto universitário real.