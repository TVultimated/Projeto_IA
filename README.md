# Previsão de Estado do Telemóvel com Machine Learning

## 📱 Visão Geral
Este projeto utiliza Random Forest para prever o estado de um telemóvel – "desligar", "silenciar" ou "não alterar" – com base em dados sensoriais simulados, incluindo localização, nível de ruído, movimento e orientação do dispositivo. O objetivo é automatizar decisões do dispositivo em ambientes críticos, melhorando a experiência do utilizador e reduzindo interrupções.

### Características Principais
- Previsão de estado baseada em dados sensoriais
- Modelo Random Forest otimizado
- Análise completa de métricas de desempenho
- Dataset sintético balanceado com 9.000 amostras

## 🗂️ Estrutura do Projeto
```
📁 Projeto_IA/
├── 📄 baseline.py               # Modelos baseline para comparação
├── 📄 config.json               # Parâmetros de configuração
├── 📄 dataset_sintetico.csv     # Dataset com 9.000 amostras
├── 📄 geração_dataset.py        # Gerador de dados sintéticos
├── 📄 modelo.py                 # Implementação do Random Forest
├── 📄 README.md                 # Documentação
└── 📄 requirements.txt          # Dependências
```

## 🚀 Guia de Início Rápido

### Pré-requisitos
- Python
- pip (gerenciador de pacotes Python)
- Git

### Instalação e Execução

1. **Clone o repositório**
```bash
git clone https://github.com/TVultimated/Projeto_IA.git
cd Projeto_IA
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Gere o dataset sintético**
```bash
python geração_dataset.py
```

4. **Execute o modelo**
```bash
python modelo.py
```

## 📊 Características do Dataset

### Variáveis de Entrada
- **Localização**: Nome do local
- **Nível de Ruído**: Medição em decibéis
- **Categoria de Ruído**: Silencio, moderado, ruidoso
- **Movimento**: Acelerómetro (x, y, z)
- **Orientação**: Giroscópio (x, y, z)
- **Estado da orientação**: Virado para cima, Virado para baixo
- **Estado do movimento**: Estatico, movimento lento, movimento rapido

### Classes de Saída (Estado)
- Desligar
- Silenciar
- Não Alterar

## 📈 Avaliação do Modelo

### Métricas Principais
### Relatório de Classificação, contendo:
- **Exatidão**: Percentagem de previsões corretas
- **Precisão**: Capacidade de identificar corretamente estados positivos
- **Recall**: Capacidade de identificar todos os estados relevantes
- **F1-Score**: Média harmônica entre precisão e recall

### Visualizações
- Matriz de Confusão
- Curvas ROC
- Gráfico de Importância das Features

## 👥 Equipa
- Carolina Guerreiro (30011061)
- Diogo Costa (30011282)
- Guilherme Fernandes (30010398)
- Tomás Viana (30010623)

## 📄 Licença
Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

Desenvolvido como projeto da disciplina de Inteligência Artificial
Universidade Autónoma de Lisboa, 2024
Professor Orientador: Sérgio Ferreira