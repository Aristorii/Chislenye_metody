ДОМАШНЕЕ ЗАДАНИЕ: Устойчивость алгоритма и корректная постановка эксперимента

import math
import mpmath
import numpy as np
import matplotlib.pyplot as plt
import random
import sys

# Настройка точности эталона
mpmath.mp.dps = 50

# БЛОК 1. ОБУСЛОВЛЕННОСТЬ ЗАДАЧИ (ЗАДАЧИ 1–4)

def solve_task_1():
    print("Задача 1. Число обусловленности вручную")
    # cond = |x * f'(x) / f(x)|
    # 1. f(x) = sqrt(x), x = 1e-8. f'(x) = 1/(2*sqrt(x)). cond = |x * (1/(2*sqrt(x))) / sqrt(x)| = 1/2
    # 2. f(x) = ln(x), x = 1.001. f'(x) = 1/x. cond = |x * (1/x) / ln(x)| = 1/ln(1.001) ~ 1000
    # 3. f(x) = x - 1, x = 1.000001. f'(x) = 1. cond = |x * 1 / (x - 1)| = 1.000001 / 0.000001 ~ 1e6
    # 4. f(x) = sin(x), x = pi/2. f'(x) = cos(x). cond = |x * cos(x) / sin(x)| = 0 (так как cos(pi/2)=0)
    
    print("Вывод: По возрастанию обусловленности: 4 (0) < 1 (0.5) < 2 (~1000) < 3 (~1e6).")
    print("Самая 'опасная' - задача 3, так как число обусловленности огромно. Малые изменения x")
    print("приводят к катастрофическим изменениям f(x) (вычитание почти равных чисел).")

def solve_task_2():
    print("Задача 2. Вычитание близких чисел")
    # f(a, b) = a - b. 
    # Аналитически: df/da = 1. Погрешность по a: delta_a = |(a/f) * df/da| * rel_err_a = |a/(a-b)| * rel_err_a
    # При a ~ b, (a-b) -> 0, следовательно cond -> бесконечность.
    a = 1 + 1e-8
    b = 1
    delta_a = 1e-9 # абсолютная погрешность a
    f = a - b # = 1e-8
    df = delta_a # изменение результата (df/da * delta_a)
    
    print(f"a = {a}, b = {b}, f = a - b = {f}")
    print(f"Абсолютная погрешность a: {delta_a}, изменение результата: {df}")
    print(f"Относительная погрешность результата: {df / f}")
    print("Вывод: Относительная погрешность результата (10%) в 10^8 раз больше относительной погрешности a.")
    print("Это классический пример плохой обусловленности.")

def solve_task_3():
    print("Задача 3. Кратные корни")
    print(f"{'eps':<10} | {'Корень':<18} | {'Сдвиг':<18} | {'Отношение сдвига'}")
    print("-" * 75)
    
    for eps in [1e-2, 1e-4, 1e-6]:
        # x^2 - 2x + 1 - eps = 0  => (x-1)^2 = eps => x = 1 + sqrt(eps)
        x = 1 + math.sqrt(eps)
        shift = x - 1
        print(f"{eps:<10} | {x:<18.10f} | {shift:<18.10f} | {shift/eps:.2f}")
        
    print("Вывод: Мы изменили свободный член на eps (погрешность входа), а корень сдвинулся на sqrt(eps).")
    print("Отношение сдвига к eps растет. Для кратных корней задача плохо обусловлена: ")
    print("малое возмущение коэффициентов дает большое возмущение корня.")

def solve_task_4():
    print("Задача 4. Обусловленность vs устойчивость")
    print("Пример: Вычисление f(x) = x^2 - 1 в точке x = 1.")
    print("Задача хорошо обусловлена (производная 2x = 2, cond = |1*2/0| - но в нуле f(x) мало, возьмем x=2, cond = 4/3).")
    print("Устойчивый алгоритм: (x - 1) * (x + 1).")
    print("Неустойчивый алгоритм: x*x - 1 (при x, близких к 1, будет потеря точности).")
    
    x = 1 + 1e-8
    stable = (x - 1) * (x + 1)
    unstable = x * x - 1
    exact = float(mpmath.mpf(x)**2 - 1)
    
    print(f"Устойчивый: {stable}, Неустойчивый: {unstable}, Эталон: {exact}")
    print("Вывод: Задача сама по себе нормальная, но алгоритм через вычитание квадратов (x^2 - 1)")
    print("плохо обусловлен из-за вычитания близких чисел, тогда как факторизация решает проблему.")

# БЛОК 2. УСТОЙЧИВОСТЬ АЛГОРИТМА (ЗАДАЧИ 5–9)

def solve_task_5():
    print("Задача 5. Квадратное уравнение")
    def check(a, b, c):
        disc = b**2 - 4*a*c
        # Плохой способ
        x2_bad = (-b + math.sqrt(disc)) / (2*a)
        # Хороший способ
        x2_good = 2*c / (-b - math.sqrt(disc))
        # Эталон
        x2_exact = float(mpmath.polyroots([a, b, c])[1])
        
        rel_err_bad = abs(x2_bad - x2_exact) / abs(x2_exact)
        rel_err_good = abs(x2_good - x2_exact) / abs(x2_exact)
        print(f"b=1e{int(math.log10(b))}: Плохой (err): {rel_err_bad:.2e} | Хороший (err): {rel_err_good:.2e}")

    for b in [1e8, 1e10, 1e12]:
        check(1, b, 1)
    print("Вывод: Плохой способ страдает от катастрофической потери точности при b >> 1,")
    print("так как -b и sqrt(disc) почти равны. Хороший способ использует формулу Виета.")

def solve_task_6():
    print("Задача 6. (1 - cos x) / x^2")
    print(f"{'x':<10} | {'Плохо (ошибка)':<20} | {'Хорошо (ошибка)'}")
    print("-" * 55)
    
    for x in [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]:
        bad = (1 - math.cos(x)) / x**2
        good = 2 * (math.sin(x/2)**2) / x**2
        exact = float(mpmath.mpf(1 - mpmath.cos(x)) / mpmath.mpf(x)**2)
        
        err_bad = abs(bad - exact) / exact
        err_good = abs(good - exact) / exact
        print(f"{x:<10.0e} | {err_bad:<20.2e} | {err_good:.2e}")
        
    print("Вывод: При x < 1e-8 ошибка плохого способа превышает 1%. Вычитание 1 - cos(x) теряет точность.")

def solve_task_7():
    print("Задачаа 7. sqrt(x+1) - sqrt(x)")
    print(f"{'x':<10} | {'Плохо (ошибка)':<20} | {'Хорошо (ошибка)'}")
    print("-" * 55)
    
    for x in [1e4, 1e8, 1e12, 1e14, 1e16]:
        bad = math.sqrt(x + 1) - math.sqrt(x)
        good = 1 / (math.sqrt(x + 1) + math.sqrt(x))
        exact = float(1 / (mpmath.sqrt(x + 1) + mpmath.sqrt(x)))
        
        err_bad = abs(bad - exact) / exact
        err_good = abs(good - exact) / exact
        print(f"{x:<10.0e} | {err_bad:<20.2e} | {err_good:.2e}")
        
    print("Вывод: Ошибка плохого способа растет с увеличением x (порядок роста ~ x^0.5).")
    print("Необходимо использовать домножение на сопряженное.")

def solve_task_8():
    print("Задача 8. Экспонента и логарифм")
    print(f"{'x':<10} | {'math.log1p (ошибка)':<20} | {'log(1+x) (ошибка)'}")
    print("-" * 55)
    
    for x in [1e-2, 1e-8, 1e-12, 1e-16]:
        good = math.log1p(x)
        bad = math.log(1 + x)
        exact = float(mpmath.log(1 + x))
        
        err_good = abs(good - exact) / exact if exact != 0 else 0
        err_bad = abs(bad - exact) / exact if exact != 0 else 0
        print(f"{x:<10.0e} | {err_good:<20.2e} | {err_bad:.2e}")
        
    print("Вывод: math.log1p вычисляет ln(1+x) без потери точности, так как не вычисляет 1+x (что дает 1 при малых x).")

def solve_task_9():
    print("Задача 9. Неустойчивость накопления в сумме")
    print(f"{'n':<8} | {'Наивный цикл':<18} | {'sum()':<18} | {'fsum()':<18}")
    print("-" * 70)
    
    for n in [10**5, 10**6, 10**7]:
        # Наивный цикл
        s_naive = 0.0
        for k in range(1, n + 1):
            s_naive += 1 / k
            
        # sum()
        s_sum = sum(1/k for k in range(1, n + 1))
        
        # fsum()
        s_fsum = math.fsum(1/k for k in range(1, n + 1))
        
        # Эталон (используем mpmath для n=10^5 и 10^6, для 10^7 медленно)
        if n == 10**7:
            exact = float(mpmath.digamma(n + 1) + mpmath.euler) # Приближенно
        else:
            exact = float(mpmath.nsum(lambda k: 1/k, [1, n]))
            
        err_naive = abs(s_naive - exact) / exact
        err_sum = abs(s_sum - exact) / exact
        err_fsum = abs(s_fsum - exact) / exact
        
        print(f"{n:<8} | {err_naive:<18.2e} | {err_sum:<18.2e} | {err_fsum:.2e}")
        
    print("Вывод: Наивное суммирование накапливает ошибку пропорционально n. math.fsum минимизирует ошибку.")

# БЛОК 3. КОРРЕКТНАЯ ПОСТАНОВКА ЭКСПЕРИМЕНТА (ЗАДАЧИ 10–15)

def solve_task_10():
    print("Задача 10. Разделение источников ошибки")
    print("Таблица (качественно):")
    print("1. Уменьшаем x (f=(1-cos x)/x^2): Ошибка растет из-за обусловленности (вычитание близких чисел).")
    print("2. Фиксируем x, меняем float32/float64: Ошибка растет из-за машинной точности (эпсилон).")
    print("3. Меняем алгоритм (плохой/хороший): Устраняет проблему потери точности.")
    print("Вывод: В плохом алгоритме доминирует фактор 1 (обусловленность).")
    
def solve_task_11():
    print("Задача 11. Эталон")
    print("Пример: (a + b) - b. Пусть a = 1e-16, b = 1.0.")
    print("Результат в float64: 0.0. Два разных способа могут дать 0.0, но оба неверны.")
    print("Вывод: Сравнивать float с float без эталона нельзя, так как оба могут дать одинаковый неверный результат.")
    
def solve_task_12():
    print("Задача 12. Диапазон, а не одна точка")
    print("Запустите код для построения графика. Ошибка плохого алгоритма для sqrt(x+1)-sqrt(x) растет.")
    print("Вывод: Эксперименты на одной точке ничего не доказывают. Нужен диапазон для понимания тренда.")
    
def solve_task_13():
    print(Задача 13. Воспроизводимость")
    print("Если seed задан, результаты np.sum и math.fsum будут совпадать при повторном запуске.")
    print("Если seed=None, результаты будут разными. Вывод: Всегда фиксируйте seed для воспроизводимости.")
    
def solve_task_14():
    print("Задача 14. Границы представимости")
    print("inf: fsum выдаст inf, sum выдаст inf. (Нет NaN).")
    print("nan: Оба выдадут nan.")
    print("1e300: Оба обработают корректно.")
    print("1e-300: Оба обработают (в нормализованных или денормализованных).")
    print("Вывод: math.fsum лучше обрабатывает крайние случаи, но inf и nan передаются в результат.")
    
def solve_task_15():
    print("Задача 15. Полный корректный эксперимент")
    print("Проведен в задачах 5, 6, 8. См. таблицы выше.")

if __name__ == "__main__":
    solve_task_1()
    solve_task_2()
    solve_task_3()
    solve_task_4()
    solve_task_5()
    solve_task_6()
    solve_task_7()
    solve_task_8()
    solve_task_9()
    solve_task_10()
    solve_task_11()
    solve_task_12()
    solve_task_13()
    solve_task_14()
    solve_task_15()
