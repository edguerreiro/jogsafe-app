import streamlit as st

# Função para calcular pace (min/km) a partir do tempo e distância
def calcular_pace(tempo, distancia_km):
    if tempo == "Não possuo":
        return "Pace padrão"
    try:
        h, m, s = map(int, tempo.split(':'))
        total_minutos = h * 60 + m + s / 60
        pace = total_minutos / distancia_km
        minutos = int(pace)
        segundos = int((pace - minutos) * 60)
        return f"{minutos}:{segundos:02d} min/km"
    except:
        return "Pace inválido"

# Título
st.title('JogSafe - Seu Plano de Corrida Personalizado')

# Coleta de informações do usuário
idade = st.number_input("Qual é a sua idade?", min_value=10, max_value=100, step=1)
peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, step=0.1)
altura = st.number_input("Altura (cm)", min_value=100, max_value=250, step=1)

# Nível de atividade
nivel_atividade = st.radio(
    "Qual o seu nível atual de atividade física?",
    ('Sedentário', 'Mínimo', 'Moderado', 'Regular', 'Avançado')
)

# Quantos dias já corre por semana?
dias_corrida = st.radio(
    "Quantos dias na semana você já pratica corrida?",
    ('Não pratico', '1 dia', '2 a 3 dias', '4 a 6 dias', '7 dias')
)

# Dias disponíveis para correr
dias_disponiveis = st.multiselect(
    "Quais dias da semana você tem disponíveis para seu novo plano de corrida?",
    ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
)

# Alimentação
habitos_alimentacao = st.radio(
    "Como você julga seus hábitos de alimentação?",
    ('Não penso nisso', 'Fast-food/Ultraprocessados', 'Alimentação equilibrada', 
     'Não planejo, mas faço 3 refeições', 'Planejo 3 refeições saudáveis', 'Acompanhamento nutricional')
)

# Objetivo
objetivo = st.radio(
    "Qual o seu objetivo com o JogSafe?",
    ('Corrida de 1 a 3 km', 'Corrida de até 5 km', 'Pretendo correr até 10 km', 'Correr maratonas longas')
)

# Tempo para atingir o objetivo
tempo_objetivo = st.radio(
    "Em quanto tempo pretende atingir seu objetivo?",
    ('Até 1 mês', 'Até 3 meses', 'Até 6 meses', 'Não tenho certeza')
)

# Recordes pessoais
st.write("Insira seus recordes pessoais:")
recorde_5k_tempo = st.text_input("Qual o seu recorde pessoal nos 5km? (Exemplo: 00:25:00)")
recorde_5k_nao_possui = st.checkbox("Não possuo recorde nos 5km")

recorde_3k_tempo = st.text_input("Qual o seu recorde pessoal nos 3km? (Exemplo: 00:15:00)")
recorde_3k_nao_possui = st.checkbox("Não possuo recorde nos 3km")

recorde_10k_tempo = st.text_input("Qual o seu recorde pessoal nos 10km? (Exemplo: 00:50:00)")
recorde_10k_nao_possui = st.checkbox("Não possuo recorde nos 10km")

# Sugestão de pace com base nos recordes pessoais
pace_5k = calcular_pace(recorde_5k_tempo if not recorde_5k_nao_possui else "Não possuo", 5)
pace_3k = calcular_pace(recorde_3k_tempo if not recorde_3k_nao_possui else "Não possuo", 3)
pace_10k = calcular_pace(recorde_10k_tempo if not recorde_10k_nao_possui else "Não possuo", 10)

# Botão para gerar o plano
if st.button('Gerar Plano de Corrida'):
    st.write(f"### Plano Semanal para {objetivo}")
    st.write(f"**Dias disponíveis para treino**: {', '.join(dias_disponiveis)}")

    st.write(f"**Sugestões de pace com base nos seus recordes pessoais:**")
    st.write(f"5 km: {pace_5k}")
    st.write(f"3 km: {pace_3k}")
    st.write(f"10 km: {pace_10k}")

    # Função para gerar plano baseado nos dias selecionados
    def gerar_plano(dias_disponiveis, objetivo, pace_5k, pace_10k):
        treino_semana = []

        if objetivo == 'Corrida de 1 a 3 km':
            plano = 'Plano para melhorar resistência em curtas distâncias.'
        elif objetivo == 'Corrida de até 5 km':
            plano = 'Plano focado em ritmo e resistência para 5 km.'
        elif objetivo == 'Pretendo correr até 10 km':
            plano = 'Plano para correr 10 km com foco em ritmo e volume.'
        else:
            plano = 'Plano de longo prazo para maratonas.'

        # Geração de um plano simples para 4 semanas
        for semana in range(1, 5):
            treino_semana.append(f"### Semana {semana}: {objetivo}")
            dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
            treinos = [
                f"*Intervalado*: Aquecimento: 10 min trote leve. 6x 400m em ritmo forte ({pace_5k}) com descanso de 1 min.",
                "*Corrida leve*: 5 km em ritmo confortável.",
                f"*Ritmado*: 4 km em ritmo constante (70% do máximo, {pace_10k}).",
                "*Corrida leve*: 6 km em ritmo confortável.",
                "*Longo*: 8 km em ritmo confortável."
            ]
            
            dia_treino = 0
            for dia in dias_disponiveis:
                if dia_treino < len(treinos):
                    treino_semana.append(f"{dia} - {treinos[dia_treino]}")
                    dia_treino += 1
            treino_semana.append("---")

        return treino_semana

    # Chama a função para gerar o plano baseado nos dias selecionados
    plano_final = gerar_plano(dias_disponiveis, objetivo, pace_5k, pace_10k)

    # Exibe o plano gerado
    for treino in plano_final:
        st.write(treino)
