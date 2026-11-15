"""
Лабораторна робота №4: «Алгоритми розпізнавання образів».
Предметна область: Розпізнавання автомобілів за кількісними та якісними характеристиками.
Метод розпізнавання: евклідова відстань у комбінованому просторі ознак.
Студент: Чисельський Владислав Леонідович, група КН-2327Б.
"""

import math

# Порогове значення для розпізнавання об'єкта
THRESHOLD = 1.05

# Масштабні коефіцієнти для нормалізації кількісних характеристик
SCALES = {
    "power": 300.0,       # Потужність двигуна (к.с.)
    "weight": 2500.0,     # Споряджена маса (кг)
    "acceleration": 12.0, # Розгін 0-100 км/год (с)
    "trunk": 800.0        # Об'єм багажника (л)
}

# Алфавіт якісних категоріальних ознак
BODY_TYPES = ["седан", "кросовер", "хетчбек", "купе", "мінівен", "пікап"]
FUEL_TYPES = ["бензин", "дизель", "електро", "гібрид"]

# База еталонних автомобілів (образів)
CARS = [
    {
        "name": "Toyota Corolla",
        "power": 132,
        "weight": 1340,
        "acceleration": 9.8,
        "trunk": 470,
        "body": "седан",
        "fuel": "бензин",
        "awd": False
    },
    {
        "name": "Toyota RAV4",
        "power": 222,
        "weight": 1680,
        "acceleration": 8.1,
        "trunk": 580,
        "body": "кросовер",
        "fuel": "гібрид",
        "awd": True
    },
    {
        "name": "Porsche 911",
        "power": 450,
        "weight": 1515,
        "acceleration": 3.6,
        "trunk": 132,
        "body": "купе",
        "fuel": "бензин",
        "awd": False
    },
    {
        "name": "Tesla Model 3",
        "power": 283,
        "weight": 1760,
        "acceleration": 5.8,
        "trunk": 425,
        "body": "седан",
        "fuel": "електро",
        "awd": False
    },
    {
        "name": "Volkswagen Golf",
        "power": 150,
        "weight": 1280,
        "acceleration": 8.5,
        "trunk": 380,
        "body": "хетчбек",
        "fuel": "бензин",
        "awd": False
    },
    {
        "name": "Ford F-150",
        "power": 400,
        "weight": 2350,
        "acceleration": 6.2,
        "trunk": 1400,
        "body": "пікап",
        "fuel": "бензин",
        "awd": True
    },
    {
        "name": "Mercedes-Benz V-Class",
        "power": 190,
        "weight": 2150,
        "acceleration": 11.2,
        "trunk": 1030,
        "body": "мінівен",
        "fuel": "дизель",
        "awd": False
    },
    {
        "name": "BMW X5",
        "power": 340,
        "weight": 2185,
        "acceleration": 5.5,
        "trunk": 650,
        "body": "кросовер",
        "fuel": "дизель",
        "awd": True
    }
]


def one_hot(value, categories):
    """Двійкове унітарне кодування якісної ознаки (One-Hot Encoding)."""
    return [1 if value.lower() == cat.lower() else 0 for cat in categories]


def create_vector(car):
    """
    Формування комбінованого вектора ознак:
    - Кількісні ознаки нормалізуються діленням на масштабний коефіцієнт.
    - Якісні ознаки кодуються двійковими векторами 0 або 1.
    """
    vector = [
        car["power"] / SCALES["power"],
        car["weight"] / SCALES["weight"],
        car["acceleration"] / SCALES["acceleration"],
        car["trunk"] / SCALES["trunk"]
    ]

    # Якісні ознаки: тип кузова та тип палива
    vector.extend(one_hot(car["body"], BODY_TYPES))
    vector.extend(one_hot(car["fuel"], FUEL_TYPES))

    # Бінарна ознака: 1 — повний привід (AWD/4WD), 0 — монопривід
    vector.append(1 if car["awd"] else 0)

    return vector


def euclidean_distance(v1, v2):
    """Обчислення евклідової відстані між двома векторами ознак."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def recognize_car(input_car):
    """Порівняння введеного образу з еталонами та визначення класу."""
    input_vector = create_vector(input_car)
    results = []

    for ref_car in CARS:
        ref_vector = create_vector(ref_car)
        dist = euclidean_distance(input_vector, ref_vector)
        results.append({
            "name": ref_car["name"],
            "distance": dist
        })

    # Сортування за зростанням відстані (найближчий еталон першим)
    results.sort(key=lambda item: item["distance"])
    return results


def print_recognition_results(results):
    """Виведення рейтингу відстаней та фінального висновку системи."""
    print("\n--- ВІДСТАНІ ДО ЕТАЛОННИХ АВТОМОБІЛІВ ---")
    print(f"{'Автомобіль':<25} | {'Відстань':<10}")
    print("-" * 38)
    for r in results:
        print(f"{r['name']:<25} | {r['distance']:.4f}")

    best = results[0]
    print("\n--- РЕЗУЛЬТАТ РОЗПІЗНАВАННЯ ---")
    print(f"Найближчий еталон: {best['name']}")
    print(f"Евклідова відстань: {best['distance']:.4f}")

    if best["distance"] <= THRESHOLD:
        print(f"Розпізнаний автомобіль: {best['name']}")
    else:
        print(
            "Автомобіль не розпізнано: "
            "характеристики надто відрізняються від усіх еталонів."
        )


def input_choice(prompt, options):
    """Допоміжна функція вибору якісної характеристики зі списку."""
    print(prompt)
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")
    while True:
        try:
            choice = int(input("Ваш вибір: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print("Помилка! Виберіть номер зі списку.")
        except ValueError:
            print("Помилка! Введіть ціле число.")


def input_car_interactive():
    """Діалогове введення характеристик користувачем."""
    print("\n--- ВВЕДЕННЯ ХАРАКТЕРИСТИК АВТОМОБІЛЯ ---")
    try:
        power = float(input("Потужність двигуна (к.с.): "))
        weight = float(input("Споряджена маса (кг): "))
        acceleration = float(input("Розгін 0-100 км/год (с): "))
        trunk = float(input("Об'єм багажника (л): "))
    except ValueError:
        print("Помилка введення числових даних!")
        return None

    body = input_choice("\nОберіть тип кузова:", BODY_TYPES)
    fuel = input_choice("\nОберіть тип палива:", FUEL_TYPES)

    awd_ans = input_choice("\nЧи має автомобіль повний привід (4WD/AWD)?", ["так", "ні"])
    awd = (awd_ans == "так")

    return {
        "name": "Невідомий автомобіль",
        "power": power,
        "weight": weight,
        "acceleration": acceleration,
        "trunk": trunk,
        "body": body,
        "fuel": fuel,
        "awd": awd
    }


def run_control_examples():
    """Демонстрація контрольних прикладів розпізнавання."""
    print("\n==================================================")
    print("ЗАПУСК КОНТРОЛЬНИХ ПРИКЛАДІВ")
    print("==================================================")

    test_cases = [
        {
            "title": "Контрольний приклад 1 (Кросовер, подібний до Toyota RAV4):",
            "car": {
                "name": "Тестовий кросовер",
                "power": 218,
                "weight": 1650,
                "acceleration": 8.3,
                "trunk": 560,
                "body": "кросовер",
                "fuel": "гібрид",
                "awd": True
            }
        },
        {
            "title": "Контрольний приклад 2 (Спорткар, близький до Porsche 911):",
            "car": {
                "name": "Тестовий спорткар",
                "power": 440,
                "weight": 1530,
                "acceleration": 3.8,
                "trunk": 140,
                "body": "купе",
                "fuel": "бензин",
                "awd": False
            }
        },
        {
            "title": "Контрольний приклад 3 (Аномальний об'єкт — не підходить під жоден еталон):",
            "car": {
                "name": "Трактор/Спецтехніка",
                "power": 65,
                "weight": 5200,
                "acceleration": 25.0,
                "trunk": 50,
                "body": "пікап",
                "fuel": "дизель",
                "awd": False
            }
        }
    ]

    for tc in test_cases:
        print(f"\n>>> {tc['title']}")
        print(f"Характеристики: {tc['car']['power']} к.с., {tc['car']['weight']} кг, {tc['car']['acceleration']} с, "
              f"кузов: {tc['car']['body']}, паливо: {tc['car']['fuel']}, повний привід: {tc['car']['awd']}")
        res = recognize_car(tc["car"])
        print_recognition_results(res)


def show_references():
    """Відображення бази еталонних автомобілів."""
    print("\n--- БАЗА ЕТАЛОННИХ АВТОМОБІЛІВ ---")
    for c in CARS:
        awd_str = "4WD" if c["awd"] else "2WD"
        print(f"• {c['name']:<22}: {c['power']} к.с., {c['weight']} кг, 0-100: {c['acceleration']}с, "
              f"багажник: {c['trunk']}л, {c['body']}, {c['fuel']}, {awd_str}")


def main():
    while True:
        print("\n========================================")
        print("СИСТЕМА РОЗПІЗНАВАННЯ АВТОМОБІЛІВ")
        print("Метод: евклідова відстань")
        print("========================================")
        print("1. Розпізнати автомобіль")
        print("2. Переглянути еталонні автомобілі")
        print("3. Запустити контрольні приклади")
        print("0. Вийти")

        choice = input("\nОберіть дію: ").strip()
        if choice == "1":
            car = input_car_interactive()
            if car:
                res = recognize_car(car)
                print_recognition_results(res)
        elif choice == "2":
            show_references()
        elif choice == "3":
            run_control_examples()
        elif choice == "0":
            print("Роботу завершено.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
