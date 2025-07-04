#!/bin/bash

# ==============================================================================
# Script de Demonstração para a API Personal Trainer
#
# Este script executa um fluxo completo de ponta a ponta:
# 1. Registra um treinador e um aluno.
# 2. Faz login com o treinador e testa o acesso baseado em papéis.
# 3. O treinador cria um treino para o aluno.
# 4. O aluno faz login e verifica o treino que lhe foi atribuído.
# ==============================================================================

# --- Configurações e Funções Auxiliares ---
BASE_URL="http://localhost:8000"

# Cores para um output mais legível
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Sem Cor

# Função para imprimir cabeçalhos e separar os passos da demo
print_header() {
    echo -e "\n${YELLOW}=======================================================================${NC}"
    echo -e "${YELLOW} $1 ${NC}"
    echo -e "${YELLOW}=======================================================================${NC}"
}

# --- Início da Demonstração ---

# 1. REGISTRO DE USUÁRIOS
print_header "PASSO 1: REGISTRANDO UM TREINADOR E UM ALUNO"

echo "Registrando Treinador 'prof_oak'..."
curl -s -X POST "${BASE_URL}/auth/register" \
-H "Content-Type: application/json" \
-d '{"username": "prof_oak", "password": "password123", "role": "trainer"}' | jq .

echo -e "\nRegistrando Aluno 'ash_ketchum'..."
# Capturamos o ID do aluno da resposta JSON para usar mais tarde
STUDENT_ID=$(curl -s -X POST "${BASE_URL}/auth/register" \
-H "Content-Type: application/json" \
-d '{"username": "ash_ketchum", "password": "password123", "role": "student"}' | jq '.id')

if [ -z "$STUDENT_ID" ] || [ "$STUDENT_ID" == "null" ]; then
    echo -e "${RED}Falha ao obter o ID do aluno. Verifique se a API está de pé. Abortando.${NC}"
    exit 1
fi
echo "Aluno 'ash_ketchum' criado com ID: $STUDENT_ID"


# 2. LOGIN E TESTE DE AUTORIZAÇÃO (TREINADOR)
print_header "PASSO 2: TREINADOR FAZ LOGIN E TESTA ACESSO"

echo "Fazendo login como Treinador 'prof_oak'..."
TRAINER_TOKEN=$(curl -s -X POST "${BASE_URL}/auth/login" \
-H "Content-Type: application/json" \
-d '{"username": "prof_oak", "password": "password123"}' | jq -r '.access_token')

if [ -z "$TRAINER_TOKEN" ] || [ "$TRAINER_TOKEN" == "null" ]; then
    echo -e "${RED}Falha ao obter o token do treinador. Abortando.${NC}"
    exit 1
fi
echo -e "${GREEN}Login do treinador bem-sucedido!${NC}"

echo -e "\nTestando acesso ao dashboard do TREINADOR (deve funcionar)..."
curl -s -X GET "${BASE_URL}/trainer/dashboard" -H "Authorization: Bearer $TRAINER_TOKEN" | jq .

echo -e "\nTestando acesso ao dashboard do ALUNO com token de treinador (deve falhar com 403)..."
# CORREÇÃO: Removido o pipe para jq, pois a resposta de erro pode não ser JSON puro
curl -s -X GET "${BASE_URL}/student/dashboard" -H "Authorization: Bearer $TRAINER_TOKEN" -w "\nHTTP Status: %{http_code}\n"


# 3. TREINADOR CRIA UM TREINO
print_header "PASSO 3: TREINADOR CRIA UM TREINO PARA O ALUNO"

echo "Criando treino 'Jornada de Kanto' para o aluno com ID $STUDENT_ID..."
curl -s -X POST "${BASE_URL}/workouts/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $TRAINER_TOKEN" \
-d '{
    "name": "Jornada de Kanto",
    "description": "Foco em cardio e resistência para a Liga Indigo.",
    "start_date": "2025-07-04",
    "end_date": "2025-08-04",
    "student_id": '$STUDENT_ID'
}' | jq .


# 4. ALUNO FAZ LOGIN E VERIFICA SEUS TREINOS
print_header "PASSO 4: ALUNO FAZ LOGIN E VERIFICA SEUS TREINOS"

echo "Fazendo login como Aluno 'ash_ketchum'..."
STUDENT_TOKEN=$(curl -s -X POST "${BASE_URL}/auth/login" \
-H "Content-Type: application/json" \
-d '{"username": "ash_ketchum", "password": "password123"}' | jq -r '.access_token')

if [ -z "$STUDENT_TOKEN" ] || [ "$STUDENT_TOKEN" == "null" ]; then
    echo -e "${RED}Falha ao obter o token do aluno. Abortando.${NC}"
    exit 1
fi
echo -e "${GREEN}Login do aluno bem-sucedido!${NC}"

echo -e "\nAluno busca por seus treinos (deve encontrar 'Jornada de Kanto')..."
curl -s -X GET "${BASE_URL}/workouts/me" -H "Authorization: Bearer $STUDENT_TOKEN" | jq .


print_header "DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO"