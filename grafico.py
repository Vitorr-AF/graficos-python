import pandas as pd
import plotly.express as px

def plot_race(season, race):
    # Carrega os dados do arquivo CSV
    df = pd.read_csv(f'bancos-de-dados/season{season}/season{season}Race{race}.csv', sep=';')

    # Converte a coluna ' LAP_TIME' para o formato datetime
    df[' LAP_TIME'] = pd.to_datetime(df[' LAP_TIME'], format='%M:%S.%f')

    # Converte o tempo de volta para minutos e segundos
    df['LAP_TIME'] = df[' LAP_TIME'].dt.strftime('%M:%S')

    # Remover valores extremos (maiores que 10 minutos)
    df = df[df[' LAP_TIME'] <= '00:10:00']

    # Criando um dicionário de dataframes, um para cada corredor
    driver_dfs = {}
    for name, group in df.groupby(['NUMBER', 'DRIVER_NAME']):
        driver_dfs[name] = pd.DataFrame({'Volta': range(1, group[' LAP_NUMBER'].max() + 1)})
        driver_dfs[name] = pd.merge(driver_dfs[name], group[[' LAP_NUMBER', ' LAP_TIME']], left_on='Volta', right_on=' LAP_NUMBER', how='left')
        driver_dfs[name] = driver_dfs[name].rename(columns={' LAP_TIME': f'{name[1]}'})
        driver_dfs[name]['Volta'] += 1  # Adiciona 1 ao número de volta
        driver_dfs[name].drop(columns=[' LAP_NUMBER'], inplace=True)

    # Unindo os dataframes
    merged_df = pd.DataFrame({'Volta': range(1, max([group[' LAP_NUMBER'].max() for name, group in df.groupby(['NUMBER', 'DRIVER_NAME'])]) + 1)})
    for driver, driver_df in driver_dfs.items():
        merged_df = pd.merge(merged_df, driver_df, on='Volta', how='left')

    # Remove a coluna 'Volta' para evitar a plotagem indevida
    merged_df = merged_df.drop(columns=['Volta'])

    # Plota o gráfico
    fig = px.line(merged_df, title=f'Corrida {race} - Temporada {season}', labels={'index': 'Volta', 'value': 'Tempo da Volta'})
    fig.update_yaxes(tickformat='%M:%S')
    fig.update_xaxes(dtick=1)  # Define o intervalo do eixo x como 1
    fig.show()


auto = int(input("1. Manual\n2. Automático"))
if auto == 1:
    # Solicita o número da temporada ao usuário
    season = int(input("Digite o número da temporada que deseja visualizar (1 a 9): "))

    race = int(input("Número da corrida: "))
    race = f'{race:02d}'


    # Plota o gráfico da corrida 1 da temporada selecionada
    plot_race(season, race)
else:
    season = 1
    raceInt = 1
    while season < 10:
        try:
            # Solicita o número da temporada ao usuário
            # season = int(input("Digite o número da temporada que deseja visualizar (1 a 9): "))

            # race = int(input("Número da corrida: "))
            race = f'{raceInt:02d}'
            



            # Plota o gráfico da corrida 1 da temporada selecionada
            plot_race(season, race)
            raceInt += 1
        except ValueError:
            print(f'Erro de valor em season: {season}, corrida: {race}')
            raceInt += 1
        except FileNotFoundError:
            print(f'Arquivo não encontrado em season: {season}, corrida: {race}')
            season += 1
            raceInt = 1
