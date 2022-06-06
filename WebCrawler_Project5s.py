
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import  ssl
import re

j = 1
while j == 1:
    change_acao = input('\nQual ação voçê gostaria de analisar (Caso não saiba o código é só apertar a tecla "q"): ')
    simul_num = False

    if change_acao == 'q' or change_acao == 'Q':
        # Acessa um site com a lista de códigos de diversas empresas
        def  main (): 
            # método para passar pelo certificado ssl
            ssl . _create_default_https_context  =  ssl . _create_unverified_context 
            url_list  =  urllib.request.urlopen( 'https://www.infomoney.com.br/cotacoes/empresas-b3/' ) 
            page_list = url_list.read()
            soup = BeautifulSoup(page_list, "html.parser")
            change = input('\nQual o ramo da empresa que você quer analisar:\n1 - Bens Industriais\n2 - Consumo Cíclico\n3 - Consumo não Cíclico\n4 - Financeiro\n5 - Materiais Básicos\n6 - Outros\n7 - Petróleo, Gás e Biocombustíveis\n8 - Saúde\n9 - Tecnologia da Informação\n10 - Telecomunicações\n11 - Utilidade Pública\nEscolha: ')
            change = int(change)
            change = change - 1
            for i in range(12):
                if i == change:
                    table = soup.find_all('table')[i] 
                    df = pd.read_html(str(table))
                    print(df)
                    
            
        if  __name__  ==  '__main__' : 
            main()
            
    else:
        # Acesso ao Google Finance para coleta de informações da ação
        url_acao = "https://www.google.com/finance/quote/"+change_acao+":BVMF"

        # Caso encontre uma tabela com informações segue o TRY
        try:
            
            data_frame = pd.read_html(url_acao, header=0, flavor='bs4')[0]
            data_frame_titles = data_frame.columns.to_list()

            data_frame_filtred = data_frame[[data_frame_titles[0], data_frame_titles[1], data_frame_titles[2]]]
            df_temp = data_frame_filtred[[data_frame_titles[2]]].to_string(index=False)

            dff_list = df_temp.split()

            dff_numbers = dff_list[2:]

            result = 0
            print('\nNúmeros da empresa ⬇')

            # remoção de caracteres (%), conversão dos valores para float e somatória dos números da empresa analisada
            for i in range(len(dff_numbers)):
                dff_numbers[i] = dff_numbers[i].replace('%', '')
                dff_numbers[i] = dff_numbers[i].replace(',', '')
                dff_numbers[i] = float(dff_numbers[i])
                result = result + dff_numbers[i]
                print(dff_numbers[i])

            print('\nResultado da análise: ', result, '%\nVeredito ⬇')
            analysisf = True
            if result < 0:
                print('No momento essa ação está com tendencias negativas')
                break
            else:
                print('No momento essa ação está com tendncias positivas')
                simul_num = True
                break
        
        # Caso não encontre uma tabela
        except ValueError:
            print('\nEmpresa ou tabela não encontrada. :/ \nDica: caso o código contenha "F" no final, tente sem essa última letra')
            change_except = input('\nGostaria de fazer uma nova consulta:\n1 - Sim\n2 - Não\nResposta:')
            if change_except == '2':
                j = 2
                print('\nAté logo!')

def analysis():
    # Lista de palavras chaves e contador
    pwords = ['duplo', 'positivo', 'otimista', 'alto', 'mais', 'superior', 'pago', 'melhor', 'maior', 'cima',
            'double', 'positive', 'optimistic', 'high', 'higher', 'advances', 'paid', 'better', 'bigger', 'up'] # 20 Palavras positivas
    nwords = ['reduzido', 'perdas', 'perda', 'quedas', 'pior', 'queda', 'inferior', 'declínio', 'menos', 'baixo',
            'reduced', 'losses', 'loss', 'drops', 'worse', 'fall', 'underperforms', 'decline', 'fewer','down']# 20 Palavras negativas 
    positive = 0
    negative = 0

    with urllib.request.urlopen(url_acao) as url:
        page = url.read()
    soup = BeautifulSoup(page, "html.parser")
    text_analysis = soup.find_all("div",{"class":"yY3Lee"})
    print('\nRealizando análise de textos relacionados a ação...')
    for word in pwords:

        # Verificando se a palavra buscada existe no texto
        if re.search(word,  str(text_analysis)):
            positive = +1

    for word in nwords:
        
        # Verificando se a palavra buscada existe no texto
        if re.search(word,  str(text_analysis)):
            negatives = +1

    print("\nPalavras positivas {}.\nPalavras negativas {}".format(positive, negative))
    
    if positive > negative:
        print('\nA análise de palavras é positiva.')
        simul_tex = True
    elif positive == negative:
        print('\nA análise é neutra.')
        simul_tex = False
    else:
        print('\nA análise de palavras é negativa.')
        simul_tex = False

    print("\n\nVeredito final ⬇\n-------------------\n")
    if simul_num == True and simul_tex == True:
        print('Números: APROVADO ✔\nTexto: APROVADO ✔')
    elif simul_num == True and simul_tex != True:
        print('Números: APROVADO ✔\nTexto: REPROVADO ✖')
    elif simul_num != True and simul_tex ==  True:
        print('Números: REPROVADO ✖\nTexto: APROVADO ✔')
    else:
        print('Números: REPROVADO ✖\nTexto: REPROVADO ✖')

    print('A posse da ação só é recomendada se ambos os testes forem positivos.\n\nOBSERVAÇÕES: Não nos responsabilizamos por perdas encima de ações recomendadas, lembre-se que isto é uma previsão/simulação e a exposição ao mercado de ações pode levá-lo a grandes prejuisos financeiros.')
if analysisf == True:
    analysis()