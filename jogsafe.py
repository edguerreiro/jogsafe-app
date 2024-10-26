import streamlit as st
import math
from datetime import datetime, timedelta

# Funções auxiliares
def calcular_frequencia_cardiaca_maxima(idade):
    return 220 - idade

def calcular_zonas_fc(fc_max):
    return {
        'Zona 1 (50-60%)': (fc_max * 0.5, fc_max * 0.6),
        'Zona 2 (60-70%)': (fc_max * 0.6, fc_max * 0.7),
        'Zona 3 (70-80%)': (fc_max * 0.7, fc_max * 0.8),
        'Zona 4 (80-90%)': (fc_max * 0.8, fc_max * 0.9),
        'Zona 5 (90-100%)': (fc_max * 0.9, fc_max)
    }

def calcular_nivel_atleta(idade, peso, altura, nivel_atividade, dias_corrida, recordes):
    imc = peso / ((altura/100) ** 2)
    
    pontos = 0
    
    nivel_scores = {
        'Sedentário': 0,
        'Mínimo': 2,
        'Moderado': 4,
        'Regular': 6,
        'Avançado': 8
    }
    pontos += nivel_scores[nivel_atividade]
    
    dias_scores = {
        'Não pratico': 0,
        '1 dia': 2,
        '2 a 3 dias': 4,
        '4 a 6 dias': 6,
        '7 dias': 8
    }
    pontos += dias_scores[dias_corrida]
    
    # Pontos extras baseados em recordes
    if recordes['5k'] and recordes['5k'] < '00:25:00':
        pontos += 3
    if recordes['3k'] and recordes['3k'] < '00:15:00':
        pontos += 2
    if recordes['10k'] and recordes['10k'] < '00:50:00':
        pontos += 4
    
    return {
        'pontuacao': pontos,
        'imc': imc,
        'nivel': 'Iniciante' if pontos < 6 else 'Intermediário' if pontos < 12 else 'Avançado'
    }

def gerar_dicas_prevencao_lesoes(nivel_atleta, imc):
    dicas_base = [
        "Sempre faça aquecimento antes dos treinos",
        "Hidrate-se bem antes, durante e após os treinos",
        "Use tênis adequados para corrida e troque-os a cada 500-800km",
        "Respeite os dias de descanso do programa"
    ]
    
    if imc > 25:
        dicas_base.extend([
            "Comece devagar e aumente o volume gradualmente",
            "Considere treinos alternados com caminhada",
            "Priorize superfícies mais macias como grama ou terra"
        ])
    
    if nivel_atleta == 'Avançado':
        dicas_base.extend([
            "Inclua exercícios de força 2-3x por semana",
            "Faça alongamento dinâmico antes e estático depois",
            "Considere massagem ou foam rolling para recuperação"
        ])
    
    return dicas_base

def calcular_pace_recomendado(nivel_atleta, objetivo):
    paces = {
        'Iniciante': {
            'leve': '7:30-8:00',
            'moderado': '7:00-7:30',
            'forte': '6:30-7:00'
        },
        'Intermediário': {
            'leve': '6:30-7:00',
            'moderado': '6:00-6:30',
            'forte': '5:30-6:00'
        },
        'Avançado': {
            'leve': '5:30-6:00',
            'moderado': '5:00-5:30',
            'forte': '4:30-5:00'
        }
    }
    return paces[nivel_atleta]

def gerar_plano_treino(dias_disponiveis, objetivo, nivel_info, tempo_objetivo):
    nivel = nivel_info['nivel']
    paces = calcular_pace_recomendado(nivel, objetivo)
    
    # Base de treinos por nível
    treinos = {
        'Iniciante': {
            'semana1': {
                'intervalado': f"Aquecimento: 5 min caminhada\n6x (1 min corrida pace {paces['moderado']} + 2 min caminhada)",
                'leve': f"20 min corrida pace {paces['leve']}",
                'longo': "30 min caminhada rápida alternando com trote"
            },
            'semana4': {
                'intervalado': f"Aquecimento: 10 min trote\n8x (2 min corrida pace {paces['forte']} + 1 min caminhada)",
                'leve': f"30 min corrida pace {paces['leve']}",
                'longo': f"40 min corrida pace {paces['leve']}"
            }
        },
        'Intermediário': {
            'semana1': {
                'intervalado': f"Aquecimento: 10 min + 8x 400m pace {paces['forte']}",
                'leve': f"5 km pace {paces['leve']}",
                'longo': f"6 km pace {paces['leve']}"
            },
            'semana4': {
                'intervalado': f"Aquecimento: 15 min + 10x 400m pace {paces['forte']}",
                'leve': f"7 km pace {paces['leve']}",
                'longo': f"10 km pace {paces['leve']}"
            }
        },
        'Avançado': {
            'semana1': {
                'intervalado': f"Aquecimento: 15 min + 12x 400m pace {paces['forte']}",
                'leve': f"8 km pace {paces['leve']}",
                'longo': f"12 km pace {paces['leve']}"
            },
            'semana4': {
                'intervalado': f"Aquecimento: 20 min + 15x 400m pace {paces['forte']}",
                'leve': f"10 km pace {paces['leve']}",
                'longo': f"15 km pace {paces['leve']}"
            }
        }
    }
    
    # Gerar progressão entre semana 1 e 4
    plano_completo = []
    nivel_atual = treinos[nivel]
    
    for semana in range(1, 5):
        # Interpolar entre semana 1 e 4
        fator_progressao = (semana - 1) / 3
        treinos_semana = []
        
        for dia in dias_disponiveis[:3]:  # Limita a 3 treinos por semana
            if len(treinos_semana) == 0:
                tipo = 'intervalado'
            elif len(treinos_semana) == 1:
                tipo = 'leve'
            else:
                tipo = 'longo'
                
            # Interpolar entre semana 1 e 4
            treino_base = nivel_atual['semana1'][tipo]
            treino_final = nivel_atual['semana4'][tipo]
            
            treinos_semana.append(f"{dia}: {treino_base if semana <= 2 else treino_final}")
        
        plano_completo.append(treinos_semana)
    
    return plano_completo

def gerar_recomendacoes_nutricao(habitos_alimentacao, objetivo, nivel_atleta):
    recomendacoes_base = {
        'Não penso nisso': [
            "Comece registrando suas refeições diárias",
            "Estabeleça 3 refeições principais com horários regulares",
            "Hidrate-se com 2-3L de água diariamente",
            "Inclua uma fonte de proteína em cada refeição principal"
        ],
        'Fast-food/Ultraprocessados': [
            "Substitua gradualmente ultraprocessados por alimentos in natura",
            "Inclua frutas e verduras em pelo menos 2 refeições",
            "Prepare mais refeições em casa",
            "Escolha lanches naturais como frutas e oleaginosas"
        ],
        'Alimentação equilibrada': [
            "Mantenha o bom trabalho com alimentação balanceada",
            "Ajuste carboidratos conforme intensidade dos treinos",
            "Considere suplementação de vitamina D e ferro (consulte um profissional)",
            "Prepare lanches pré e pós-treino com carboidratos e proteínas"
        ]
    }
    
    recomendacoes = recomendacoes_base.get(habitos_alimentacao, ["Consulte um nutricionista para um plano personalizado"])
    
    # Adiciona recomendações específicas baseadas no nível
    if nivel_atleta == 'Avançado':
        recomendacoes.extend([
            "Considere periodização nutricional alinhada aos treinos",
            "Monitore a ingestão de eletrólitos em treinos longos",
            "Planeje refeições de recuperação pós-treinos intensos"
        ])
    
    return recomendacoes

# Interface principal
col1, col2, col3 = st.columns([1,1,1])

with col2:

    st.image('jogsafe-logo.png', width=200, use_column_width=False)
    
st.markdown("<h1 style='text-align: center;'>JogSafe</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Seu Plano de Corrida Personalizado</h3>", unsafe_allow_html=True)

# Criação de abas
tab1, tab2, tab3 = st.tabs(["Informações Básicas", "Histórico de Corrida", "Preferências de Treino"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        idade = st.number_input("Qual é a sua idade?", min_value=10, max_value=100, step=1)
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, step=0.1)
        altura = st.number_input("Altura (cm)", min_value=100, max_value=250, step=1)
    
    with col2:
        nivel_atividade = st.radio(
            "Qual o seu nível atual de atividade física?",
            ('Sedentário', 'Mínimo', 'Moderado', 'Regular', 'Avançado')
        )
        
        habitos_alimentacao = st.radio(
            "Como você julga seus hábitos de alimentação?",
            ('Não penso nisso', 'Fast-food/Ultraprocessados', 'Alimentação equilibrada', 
             'Não planejo, mas faço 3 refeições', 'Planejo 3 refeições saudáveis', 'Acompanhamento nutricional')
        )

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        dias_corrida = st.radio(
            "Quantos dias na semana você já pratica corrida?",
            ('Não pratico', '1 dia', '2 a 3 dias', '4 a 6 dias', '7 dias')
        )
        
        st.write("Insira seus recordes pessoais:")
        recorde_5k_tempo = st.text_input("5km (Exemplo: 00:25:00)", "")
        recorde_5k_nao_possui = st.checkbox("Não possuo recorde nos 5km")
        
        recorde_3k_tempo = st.text_input("3km (Exemplo: 00:15:00)", "")
        recorde_3k_nao_possui = st.checkbox("Não possuo recorde nos 3km")
        
        recorde_10k_tempo = st.text_input("10km (Exemplo: 00:50:00)", "")
        recorde_10k_nao_possui = st.checkbox("Não possuo recorde nos 10km")
    
    with col2:
        objetivo = st.radio(
            "Qual o seu objetivo com o JogSafe?",
            ('Corrida de 1 a 3 km', 'Corrida de até 5 km', 'Pretendo correr até 10 km', 'Correr maratonas longas')
        )
        
        tempo_objetivo = st.radio(
            "Em quanto tempo pretende atingir seu objetivo?",
            ('Até 1 mês', 'Até 3 meses', 'Até 6 meses', 'Não tenho certeza')
        )

with tab3:
    dias_disponiveis = st.multiselect(
        "Quais dias da semana você tem disponíveis para seu novo plano de corrida?",
        ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    )
    
    hora_preferida = st.selectbox(
        "Qual horário você prefere treinar?",
        ['Manhã (5h-8h)', 'Manhã (8h-12h)', 'Tarde (12h-18h)', 'Noite (18h-22h)']
    )

# Botão para gerar o plano
if st.button('Gerar Plano de Corrida'):
    # Verifica se tem informações suficientes
    if not dias_disponiveis:
        st.error("Por favor, selecione pelo menos um dia disponível para treino.")
    else:
        # Processa recordes
        recordes = {
            '5k': None if recorde_5k_nao_possui else recorde_5k_tempo,
            '3k': None if recorde_3k_nao_possui else recorde_3k_tempo,
            '10k': None if recorde_10k_nao_possui else recorde_10k_tempo
        }
        
        # Calcula nível do atleta
        nivel_atleta = calcular_nivel_atleta(idade, peso, altura, nivel_atividade, dias_corrida, recordes)
        
        # Calcula zonas de FC
        fc_max = calcular_frequencia_cardiaca_maxima(idade)
        zonas_fc = calcular_zonas_fc(fc_max)
        
        # Gera plano personalizado
        plano = gerar_plano_treino(dias_disponiveis, objetivo, nivel_atleta, tempo_objetivo)
        
        # Gera recomendações nutricionais
        recomendacoes = gerar_recomendacoes_nutricao(habitos_alimentacao, objetivo, nivel_atleta['nivel'])
        
        # Continuação do if st.button('Gerar Plano de Corrida'):
        # Gera dicas de prevenção
        dicas_prevencao = gerar_dicas_prevencao_lesoes(nivel_atleta['nivel'], nivel_atleta['imc'])
        
        # Exibição dos resultados em seções expansíveis
        with st.expander("📊 Seu Perfil", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Nível:**", nivel_atleta['nivel'])
                st.write("**IMC:**", f"{nivel_atleta['imc']:.1f}")
            with col2:
                st.write("**FC Máxima:**", f"{fc_max} bpm")
            with col3:
                st.write("**Pontuação:**", nivel_atleta['pontuacao'])

        with st.expander("❤️ Suas Zonas de Frequência Cardíaca", expanded=True):
            for zona, (min_fc, max_fc) in zonas_fc.items():
                st.write(f"**{zona}:** {int(min_fc)}-{int(max_fc)} bpm")

        with st.expander("📝 Seu Plano de Treino", expanded=True):
            for semana, treinos in enumerate(plano, 1):
                st.subheader(f"Semana {semana}")
                for treino in treinos:
                    st.write(treino)
                st.write("---")

        with st.expander("🥗 Recomendações Nutricionais", expanded=True):
            for rec in recomendacoes:
                st.write(f"• {rec}")

        with st.expander("⚠️ Dicas de Prevenção de Lesões", expanded=True):
            for dica in dicas_prevencao:
                st.write(f"• {dica}")

        # Adiciona dicas específicas baseadas no horário escolhido
        with st.expander("⏰ Dicas para seu Horário de Treino", expanded=True):
            if hora_preferida.startswith('Manhã'):
                st.write("""
                • Faça um café da manhã leve 1-2 horas antes do treino
                • Hidrate-se bem ao acordar
                • Considere um aquecimento mais longo pela manhã
                • Prepare seu equipamento na noite anterior
                """)
            elif hora_preferida.startswith('Tarde'):
                st.write("""
                • Evite refeições pesadas 2-3 horas antes do treino
                • Mantenha-se hidratado ao longo do dia
                • Proteja-se do sol com protetor solar e boné
                • Escolha roupas leves e de cores claras
                """)
            else:  # Noite
                st.write("""
                • Use roupas e acessórios refletivos
                • Evite refeições pesadas 2-3 horas antes do treino
                • Prefira rotas bem iluminadas e seguras
                • Considere treinar acompanhado
                """)

        # Adiciona botão para download do plano
        st.download_button(
            label="📥 Baixar Plano Completo",
            data=f"""JogSafe - Seu Plano de Corrida Personalizado

Perfil:
- Nível: {nivel_atleta['nivel']}
- IMC: {nivel_atleta['imc']:.1f}
- FC Máxima: {fc_max} bpm

Zonas de Frequência Cardíaca:
{chr(10).join(f'- {zona}: {int(min_fc)}-{int(max_fc)} bpm' for zona, (min_fc, max_fc) in zonas_fc.items())}

Plano de Treino:
{''.join(f'''
Semana {i+1}:
{''.join(f"- {treino}\\n" for treino in semana)}
''' for i, semana in enumerate(plano))}

Recomendações Nutricionais:
{''.join(f"- {rec}\\n" for rec in recomendacoes)}

Dicas de Prevenção de Lesões:
{''.join(f"- {dica}\\n" for dica in dicas_prevencao)}
""",
            file_name="meu_plano_jogsafe.txt",
            mime="text/plain",
        )