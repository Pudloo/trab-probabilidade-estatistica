# Trabalho 1 - Probabilidade e Estatística (UFFS)
# Para executar: python trabalho_probabilidade.py  (Python 3.8 ou mais novo, só usa bibliotecas padrão)
import math
import random


def ler_float(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if not math.isfinite(valor):
                print("Digite um número comum (sem inf ou nan).")
                continue
            if minimo is not None and valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Digite um valor menor ou igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("Valor inválido. Tente novamente.")


def ler_int(mensagem, minimo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"Digite um inteiro maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Digite um número inteiro.")


def procurar_nome(nomes, texto):
    # procura o nome na lista sem diferenciar maiúscula de minúscula; devolve -1 se não achar
    for i, nome in enumerate(nomes):
        if nome.lower() == texto.lower():
            return i
    return -1


def normal_cdf(z):
    # P(Z <= z) da normal padrão, usando a função erro
    return (1 + math.erf(z / math.sqrt(2))) / 2


def prob_binomial(n, x, p):
    # P(X = x) = C(n,x) * p^x * (1-p)^(n-x)
    if n < 0 or x < 0 or x > n or not 0 <= p <= 1:
        raise ValueError("Verifique n, x e p.")
    try:
        return math.comb(n, x) * (p ** x) * ((1 - p) ** (n - x))
    except OverflowError:
        # n muito grande: o número combinatório não cabe em float, então usa logaritmos
        if p == 0 or p == 1:
            return 0.0
        log_comb = math.lgamma(n + 1) - math.lgamma(x + 1) - math.lgamma(n - x + 1)
        return math.exp(log_comb + x * math.log(p) + (n - x) * math.log(1 - p))


def prob_poisson(x, taxa):
    # P(X = x) = e^(-lambda) * lambda^x / x!
    if x < 0 or taxa < 0:
        raise ValueError("x e a taxa devem ser não negativos.")
    try:
        return math.exp(-taxa) * (taxa ** x) / math.factorial(x)
    except OverflowError:
        # x grande: fatorial não cabe em float, então usa logaritmos
        if taxa == 0:
            return 0.0
        return math.exp(-taxa + x * math.log(taxa) - math.lgamma(x + 1))


def mostrar_probabilidade(valor):
    valor = max(0.0, min(1.0, valor))  # arredondamento pode dar -0.0000000001
    print(f"Probabilidade: {valor:.8f} ({valor * 100:.4f}%)")


def p1():
    # União, interseções e complemento com conjuntos do Python
    print("\nP1 - Operações com conjuntos")
    modo = ler_int("1 - digitar os conjuntos | 2 - gerar valores aleatórios: ", 1)
    if modo == 2:
        tamanho = ler_int("Tamanho do universo (números de 1 até N): ", 1)
        universo = set(range(1, tamanho + 1))
        A = set(random.sample(sorted(universo), random.randint(1, tamanho)))
        B = set(random.sample(sorted(universo), random.randint(1, tamanho)))
        C = set(random.sample(sorted(universo), random.randint(1, tamanho)))
        print("Universo:", sorted(universo))
        print("A:", sorted(A))
        print("B:", sorted(B))
        print("C:", sorted(C))
    else:
        universo = set(item.strip() for item in input("Elementos do universo, separados por vírgula: ").split(",") if item.strip())
        A = set(item.strip() for item in input("Elementos de A, separados por vírgula: ").split(",") if item.strip())
        B = set(item.strip() for item in input("Elementos de B, separados por vírgula: ").split(",") if item.strip())
        C = set(item.strip() for item in input("Elementos de C, separados por vírgula: ").split(",") if item.strip())
        if not (A <= universo and B <= universo and C <= universo):
            print("Erro: todos os elementos de A, B e C devem estar no universo informado.")
            return

    print("A união B:", sorted(A | B))
    print("A interseção B:", sorted(A & B))
    print("A interseção C:", sorted(A & C))
    print("Complemento de A (em relação ao universo):", sorted(universo - A))


def p2():
    # cada grupo tem total/grupos elementos; P(não ser do grupo) = (total - grupo) / total
    print("\nP2 - Probabilidade de não pertencer a um grupo")
    total = ler_int("Tamanho total da população: ", 1)
    grupos = ler_int("Quantidade de grupos iguais: ", 1)
    if total % grupos != 0:
        print("Para grupos iguais, o total precisa ser divisível pela quantidade de grupos.")
        return
    nomes = input("Nomeie os grupos separados por vírgula (ou pressione Enter): ").strip()
    lista_nomes = [nome.strip() for nome in nomes.split(",")] if nomes else []
    if len(lista_nomes) != grupos:
        if nomes:
            print("A quantidade de nomes não bate com o número de grupos. Usando nomes numerados.")
        lista_nomes = [f"Grupo {i + 1}" for i in range(grupos)]

    escolhido = ler_int(f"Qual grupo excluir? Digite um número de 1 a {grupos}: ", 1)
    if escolhido > grupos:
        print("Número de grupo inválido.")
        return
    por_grupo = total // grupos
    p = (total - por_grupo) / total
    print(f"Cada grupo tem {por_grupo} elementos.")
    print(f"Grupo excluído: {lista_nomes[escolhido - 1]}")
    mostrar_probabilidade(p)


def p3():
    # P(empresa) = funcionários da empresa / total de funcionários
    print("\nP3 - Seleção proporcional ao número de funcionários")
    quantidade = ler_int("Quantidade de empresas: ", 1)
    nomes = []
    pesos = []
    for i in range(quantidade):
        nome = input(f"Nome da empresa {i + 1}: ").strip() or f"Empresa {i + 1}"
        peso = ler_float(f"Número de funcionários de {nome}: ", 0)
        nomes.append(nome)
        pesos.append(peso)
    total = sum(pesos)
    if total == 0:
        print("A soma dos funcionários precisa ser maior que zero.")
        return
    for nome, peso in zip(nomes, pesos):
        print(f"P({nome}) = {peso / total:.6f} ({peso / total * 100:.2f}%)")
    escolhido = input("Nome da empresa para calcular a chance de NÃO ser selecionada (Enter para pular): ").strip()
    if escolhido:
        indice = procurar_nome(nomes, escolhido)
        if indice == -1:
            print("Nome não encontrado.")
        else:
            mostrar_probabilidade(1 - pesos[indice] / total)


def p4():
    # sem reposição: P = C(favoráveis, n) / C(total, n)
    print("\nP4 - Amostragem sem reposição: todos de um grupo")
    favoraveis = ler_int("Quantidade de estudantes do grupo desejado: ", 0)
    outros = ler_int("Quantidade de estudantes dos outros grupos: ", 0)
    n = ler_int("Quantidade de estudantes sorteados: ", 1)
    total = favoraveis + outros
    if n > total:
        print("A amostra não pode ser maior que a população.")
        return
    if n > favoraveis:
        print("Não há estudantes suficientes no grupo, então a probabilidade é 0.")
        mostrar_probabilidade(0)
        return
    p = math.comb(favoraveis, n) / math.comb(total, n)
    mostrar_probabilidade(p)


def p5():
    # pelo menos um resolve = 1 - P(nenhum resolve) = 1 - (1 - pA)(1 - pB)
    print("\nP5 - Pelo menos uma pessoa resolve, tentativas independentes")
    prob_a = ler_float("Probabilidade da primeira pessoa resolver (0 a 1): ", 0, 1)
    prob_b = ler_float("Probabilidade da segunda pessoa resolver (0 a 1): ", 0, 1)
    p = 1 - (1 - prob_a) * (1 - prob_b)
    mostrar_probabilidade(p)


def p6():
    # P(não precisar de reparo) = 1 - reparos / total
    print("\nP6 - Probabilidade complementar")
    total = ler_int("Total de itens observados: ", 1)
    quantidade = ler_int("Quantidade que exigiu reparo: ", 0)
    if quantidade > total:
        print("A quantidade com reparo não pode exceder o total.")
        return
    mostrar_probabilidade(1 - quantidade / total)


def p7():
    # probabilidade total: P(erro) = soma de P(cliente) * P(erro | cliente)
    # Bayes: P(cliente | erro) = P(cliente) * P(erro | cliente) / P(erro)
    print("\nP7 - Probabilidade total e Bayes")
    n = ler_int("Quantidade de clientes: ", 1)
    nomes, participacoes, taxas_erro = [], [], []
    for i in range(n):
        nome = input(f"Nome do cliente {i + 1}: ").strip() or f"Cliente {i + 1}"
        participacao = ler_float(f"Percentual dos pedidos de {nome} (0 a 100): ", 0, 100) / 100
        taxa = ler_float(f"Percentual de pedidos inadequados de {nome} (0 a 100): ", 0, 100) / 100
        nomes.append(nome)
        participacoes.append(participacao)
        taxas_erro.append(taxa)
    if not math.isclose(sum(participacoes), 1.0, abs_tol=1e-6):
        print(f"Erro: as participações somam {sum(participacoes) * 100:.2f}%, e devem somar 100%.")
        print("Execute a questão novamente e confira os percentuais informados.")
        return
    p_erro = sum(a * b for a, b in zip(participacoes, taxas_erro))
    print("Probabilidade de o sistema apresentar erro:")
    mostrar_probabilidade(p_erro)
    escolhido = input("Cliente para calcular a probabilidade sabendo que houve erro: ").strip()
    i = procurar_nome(nomes, escolhido)
    if i == -1:
        print("Nome não encontrado; parte de Bayes não calculada.")
    elif p_erro == 0:
        print("Não é possível aplicar Bayes porque a probabilidade de erro é zero.")
    else:
        print(f"P({nomes[i]} | erro):")
        mostrar_probabilidade(participacoes[i] * taxas_erro[i] / p_erro)


def p8():
    # mesma ideia da P7: probabilidade total de defeito e depois Bayes para cada máquina
    print("\nP8 - Bayes: origem de um parafuso defeituoso")
    n = ler_int("Quantidade de máquinas: ", 1)
    nomes, producoes, defeitos = [], [], []
    for i in range(n):
        nome = input(f"Nome da máquina {i + 1}: ").strip() or f"Máquina {i + 1}"
        producao = ler_float(f"Percentual da produção de {nome} (0 a 100): ", 0, 100) / 100
        defeito = ler_float(f"Percentual defeituoso de {nome} (0 a 100): ", 0, 100) / 100
        nomes.append(nome)
        producoes.append(producao)
        defeitos.append(defeito)
    if not math.isclose(sum(producoes), 1.0, abs_tol=1e-6):
        print(f"Erro: as produções somam {sum(producoes) * 100:.2f}%, e devem somar 100%.")
        print("Execute a questão novamente e confira os percentuais informados.")
        return
    p_defeituoso = sum(p * d for p, d in zip(producoes, defeitos))
    print("Probabilidade de um parafuso escolhido ser defeituoso:")
    mostrar_probabilidade(p_defeituoso)
    if p_defeituoso == 0:
        print("Nenhum parafuso tem chance de defeito; não é possível calcular a origem dado defeito.")
        return
    for nome, p, d in zip(nomes, producoes, defeitos):
        print(f"P({nome} | defeituoso) = {(p * d / p_defeituoso):.6f} ({p * d / p_defeituoso * 100:.2f}%)")


def p9():
    # série: multiplica as probabilidades; paralelo: 1 - (1 - p1)(1 - p2)
    print("\nP9 - Confiabilidade de sistemas")
    print("Posição dos componentes: C1 (em cima, esquerda), C2 (em cima, direita),")
    print("                         C3 (embaixo, esquerda), C4 (embaixo, direita).")
    print("Configuração 1: dois ramos em paralelo (C1-C2 e C3-C4), cada ramo com os componentes em série.")
    print("Configuração 2: duas etapas em série; etapa 1 = C1 e C3 em paralelo, etapa 2 = C2 e C4 em paralelo.")
    opcao = ler_int("Escolha a configuração (1 ou 2): ", 1)
    if opcao not in (1, 2):
        print("Configuração inválida.")
        return
    ps = [ler_float(f"Probabilidade de funcionamento do componente C{i + 1} (0 a 1): ", 0, 1) for i in range(4)]
    if opcao == 1:
        ramo1 = ps[0] * ps[1]
        ramo2 = ps[2] * ps[3]
        sistema = 1 - (1 - ramo1) * (1 - ramo2)
    else:
        etapa1 = 1 - (1 - ps[0]) * (1 - ps[2])
        etapa2 = 1 - (1 - ps[1]) * (1 - ps[3])
        sistema = etapa1 * etapa2
    print("Probabilidade de o sistema funcionar:")
    mostrar_probabilidade(sistema)


def p10():
    # média da soma = soma das médias; variância da soma (independentes) = soma das variâncias
    print("\nP10 - Soma de pesos independentes")
    m1 = ler_float("Média do peso líquido: ")
    d1 = ler_float("Desvio-padrão do peso líquido: ", 0)
    m2 = ler_float("Média do peso da embalagem: ")
    d2 = ler_float("Desvio-padrão da embalagem: ", 0)
    media = m1 + m2
    dp = math.sqrt(d1 ** 2 + d2 ** 2)
    print(f"Média do peso bruto: {media:.4f}")
    print(f"Desvio-padrão do peso bruto: {dp:.4f}")


def p11():
    # binomial: média = n*p, variância = n*p*(1-p)
    print("\nP11 - Distribuição Binomial")
    n = ler_int("Quantidade de itens no lote: ", 0)
    p = ler_float("Probabilidade de defeito por item (0 a 1): ", 0, 1)
    x = ler_int("Quantidade de itens defeituosos (para 'exatamente x' e 'mais de x'): ", 0)
    if x > n:
        print("x não pode ser maior que n.")
        return
    p_algum = 1 - prob_binomial(n, 0, p)
    p_exato = prob_binomial(n, x, p)
    p_mais_x = 1 - sum(prob_binomial(n, k, p) for k in range(x + 1))
    media_defeitos = n * p
    media_bons = n * (1 - p)
    variancia = n * p * (1 - p)
    print("Probabilidade de haver algum item com defeito:")
    mostrar_probabilidade(p_algum)
    print(f"Probabilidade de exatamente {x} defeituosos:")
    mostrar_probabilidade(p_exato)
    print(f"Probabilidade de mais de {x} defeituosos:")
    mostrar_probabilidade(p_mais_x)
    print(f"Número esperado de defeituosos: {media_defeitos:.6f}")
    print(f"Número esperado de itens bons: {media_bons:.6f}")
    print(f"Variância do número de defeituosos: {variancia:.6f}")


def p12():
    # hipergeométrica: P = C(M, k) * C(H, s-k) / C(M+H, s)
    print("\nP12 - Hipergeométrica: mulheres na amostra")
    mulheres = ler_int("Quantidade de mulheres: ", 0)
    homens = ler_int("Quantidade de homens: ", 0)
    sorteios = ler_int("Quantidade de pessoas sorteadas: ", 1)
    mulheres_desejadas = ler_int("Quantidade de mulheres desejada na amostra: ", 0)
    total = mulheres + homens
    homens_desejados = sorteios - mulheres_desejadas
    if (sorteios > total or mulheres_desejadas > mulheres
            or homens_desejados < 0 or homens_desejados > homens):
        print("Combinação impossível, então a probabilidade é 0.")
        mostrar_probabilidade(0)
        return
    p = (math.comb(mulheres, mulheres_desejadas) *
         math.comb(homens, homens_desejados) / math.comb(total, sorteios))
    mostrar_probabilidade(p)


def p13():
    # Poisson: lambda = taxa por minuto * tempo em minutos (segundos / 60)
    print("\nP13 - Distribuição de Poisson")
    taxa = ler_float("Taxa média de chegadas por minuto: ", 0)
    segundos = ler_float("Duração do intervalo em segundos: ", 0)
    x = ler_int("Quantidade exata de chegadas desejada: ", 0)
    lam = taxa * (segundos / 60)
    print(f"Intervalo de {segundos:g} s = {segundos / 60:g} min -> lambda = {lam:.6f}")
    mostrar_probabilidade(prob_poisson(x, lam))


def p14():
    # P(X > limite) = 1 - P(X <= limite), com X binomial
    print("\nP14 - Mais de x erros em n bits (Binomial)")
    n = ler_int("Quantidade de bits transmitidos: ", 1)
    p = ler_float("Probabilidade de erro por bit (0 a 1): ", 0, 1)
    limite = ler_int("Calcular probabilidade de mais de quantos erros? ", 0)
    if limite >= n:
        print("Não existe como ter mais erros do que bits, então a probabilidade é 0.")
        mostrar_probabilidade(0)
        return
    cauda_esquerda = sum(prob_binomial(n, k, p) for k in range(limite + 1))
    mostrar_probabilidade(1 - cauda_esquerda)


def p15():
    # uniforme em [A,B]: E = (A+B)/2, Var = (B-A)^2/12, P(C<X<D) = parte de [C,D] dentro de [A,B] / (B-A)
    print("\nP15 - Distribuição Uniforme")
    a = ler_float("Limite inferior A: ")
    b = ler_float("Limite superior B: ")
    if b <= a:
        print("B deve ser maior que A.")
        return
    c = ler_float("Limite inferior C para o intervalo desejado: ")
    d = ler_float("Limite superior D para o intervalo desejado: ")
    if d < c:
        c, d = d, c
    media = (a + b) / 2
    variancia = (b - a) ** 2 / 12
    inferior = max(a, c)
    superior = min(b, d)
    p = max(0.0, superior - inferior) / (b - a)
    print(f"Valor esperado: {media:.6f}")
    print(f"Variância: {variancia:.6f}")
    print("Probabilidade de C < X < D:")
    mostrar_probabilidade(p)


def p16():
    # exponencial: P(T > t) = e^(-lambda * t)
    print("\nP16 - Distribuição Exponencial: sobrevivência")
    taxa = ler_float("Taxa de falha lambda por hora: ", 0)
    c = ler_float("Tempo C em horas: ", 0)
    d = ler_float("Tempo D em horas: ", 0)
    print(f"Probabilidade de sobreviver mais de {c:g} horas:")
    mostrar_probabilidade(math.exp(-taxa * c))
    print(f"Probabilidade de sobreviver mais de {d:g} horas:")
    mostrar_probabilidade(math.exp(-taxa * d))


def p17():
    # soma de normais independentes é normal: média = M1 + M2, desvio = raiz(D1^2 + D2^2)
    # padronização: Z = (x - média) / desvio
    print("\nP17 - Soma de variáveis Normais independentes")
    m1 = ler_float("Média do peso líquido: ")
    d1 = ler_float("Desvio-padrão do peso líquido: ", 0)
    m2 = ler_float("Média do peso da embalagem: ")
    d2 = ler_float("Desvio-padrão da embalagem: ", 0)
    media = m1 + m2
    dp = math.sqrt(d1 ** 2 + d2 ** 2)
    if dp == 0:
        print("O desvio-padrão total é zero; não dá para usar a normal.")
        return
    print(f"Peso bruto: média = {media:.4f}; desvio-padrão = {dp:.4f}")
    referencia = ler_float("Referência MS para calcular P(peso bruto > MS): ")
    z = (referencia - media) / dp
    p_maior = 1 - normal_cdf(z)
    print(f"Z da referência MS = {z:.6f}")
    print("Probabilidade de peso bruto superior a MS:")
    mostrar_probabilidade(p_maior)
    usar_intervalo = input("Calcular também a probabilidade entre dois limites? (s/n): ").strip().lower()
    if usar_intervalo == "s":
        i1 = ler_float("Limite inferior I1: ")
        i2 = ler_float("Limite superior I2: ")
        if i2 < i1:
            i1, i2 = i2, i1
        z1 = (i1 - media) / dp
        z2 = (i2 - media) / dp
        p = normal_cdf(z2) - normal_cdf(z1)
        print(f"Z1 = {z1:.6f}; Z2 = {z2:.6f}")
        print("Probabilidade de I1 < peso bruto < I2:")
        mostrar_probabilidade(p)


def ler_limite(nome):
    # lê um limite de Z; aceita inf e -inf para infinito
    while True:
        texto = input(f"Limite {nome} (use inf ou -inf para infinito): ").strip().lower().replace(",", ".")
        if texto in ("inf", "+inf"):
            return math.inf
        if texto == "-inf":
            return -math.inf
        try:
            valor = float(texto)
        except ValueError:
            print("Valor inválido. Tente novamente.")
            continue
        if math.isfinite(valor):
            return valor
        print("Valor inválido. Tente novamente.")


def p18():
    # P(a < Z < b) = F(b) - F(a), onde F é a função de distribuição acumulada da normal padrão
    print("\nP18 - Intervalos da Normal padrão")
    a = ler_limite("inferior")
    b = ler_limite("superior")
    if b < a:
        a, b = b, a
    mostrar_probabilidade(normal_cdf(b) - normal_cdf(a))


def p19():
    # padroniza com Z = (x - média) / desvio e usa a acumulada da normal padrão
    print("\nP19 - Probabilidades para uma Normal geral")
    media = ler_float("Média mu: ")
    dp = ler_float("Desvio-padrão sigma: ", 0)
    if dp == 0:
        print("O desvio-padrão precisa ser maior que zero.")
        return
    print("1 - entre dois valores; 2 - maior que um valor; 3 - menor que um valor")
    opcao = ler_int("Escolha a opção: ", 1)
    if opcao == 1:
        a = ler_float("Limite inferior: ")
        b = ler_float("Limite superior: ")
        if b < a:
            a, b = b, a
        za = (a - media) / dp
        zb = (b - media) / dp
        p = normal_cdf(zb) - normal_cdf(za)
        print(f"Z inferior = {za:.6f}; Z superior = {zb:.6f}")
    elif opcao == 2:
        x = ler_float("Valor de referência: ")
        z = (x - media) / dp
        p = 1 - normal_cdf(z)
        print(f"Z = {z:.6f}")
    elif opcao == 3:
        x = ler_float("Valor de referência: ")
        z = (x - media) / dp
        p = normal_cdf(z)
        print(f"Z = {z:.6f}")
    else:
        print("Opção inválida.")
        return
    mostrar_probabilidade(p)


def menu():
    opcoes = {
        1: p1, 2: p2, 3: p3, 4: p4, 5: p5, 6: p6, 7: p7,
        8: p8, 9: p9, 10: p10, 11: p11, 12: p12, 13: p13,
        14: p14, 15: p15, 16: p16, 17: p17, 18: p18, 19: p19
    }
    while True:
        print("\n" + "=" * 55)
        print("TRABALHO 1 - PROBABILIDADE E ESTATÍSTICA")
        print("=" * 55)
        for i in range(1, 20):
            print(f"{i:2}. P{i}")
        print(" 0. Sair")
        escolha = ler_int("Escolha a questão para executar: ", 0)
        if escolha == 0:
            print("Programa encerrado.")
            break
        if escolha in opcoes:
            try:
                opcoes[escolha]()
            except (ValueError, OverflowError) as erro:
                print("Não foi possível calcular:", erro)
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
