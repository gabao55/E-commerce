def CPF_validate(new_cpf):
    list = []

    for i in new_cpf:

        if i.isnumeric():
            list.append(int(i))

    if len(list) < 11:
        return False

    list.pop(), list.pop()

    c = 10
    acumulator = 0

    for value in list:

        mult = value*c
        acumulator += mult
        c -= 1

    digit_1 = 11 - (acumulator%11)

    if digit_1 > 9:

        digit_1 = 0

    list.append(digit_1)

    acumulator = 0
    c = 11

    for value in list:

        mult = value*c
        acumulator += mult
        c -= 1

    digit_2 = 11 - (acumulator%11)

    if digit_2 > 9:

        digit_2 = 0

    list.append(digit_2)

    l = list

    cpf = f'{l[0]}{l[1]}{l[2]}.{l[3]}{l[4]}{l[5]}.{l[6]}{l[7]}{l[8]}-{l[9]}{l[10]}'

    return True if (new_cpf == cpf) else False