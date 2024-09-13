import random


def martingale(balance, inital_bet):
    table = ["RED"] * 18 + ["BLACK"] * 18 + ["ZERO"]

    spins = 0

    bet = inital_bet

    total_red = 0
    total_black = 0
    total_zero = 0

    step = 0
    max_step = 0  # Max muliplies times

    max_bet = 0
    max_balance = 0

    while balance > 0:
        spins += 1  # Spins counter

        if bet > balance:
            bet = balance

        if bet > max_bet:
            max_bet = bet

        if balance > max_balance:
            max_balance = balance

        balance -= bet

        win = random.choice(table)

        if win == "RED":
            balance += bet * 2
            bet = inital_bet
            step = 0
            total_red += 1
        else:
            bet *= 2
            step += 1
            if step > max_step:
                max_step = step
            if win == "BLACK":
                total_black += 1
            else:
                total_zero += 1
    result = (f"Ваша стратегія мартінгейлу:\n\n"
              f"Кількість раундів до втрати балансу: {spins}\n"
              f"Максимальна ставка: {round(max_bet, 2)}\n"
              f"Максимальний баланс на кармані: {round(max_balance, 2)}\n"
              f"Найбільша кількість мартінгейлу: {max_step}\n\n"
              f"Статистика:\n"
              f"⚫️ ЧОРНЕ випало {total_black} разів.\n"
              f"🔴 ЧЕРВОНЕ випало {total_red} разів.\n"
              f"🟢 0 випало {total_zero} разів.")

    return result
