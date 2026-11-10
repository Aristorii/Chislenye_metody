import time
import math
import numpy as np

def measure(fn, x, repeat=3):
    best = float("inf")
    result = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        result = fn(x)
        t1 = time.perf_counter()
        best = min(best, t1 - t0)
    return result, best

def run_task(task_name, loop_fn, np_fn, data):
    print(f"\n--- {task_name} ---")
    r_loop, t_loop = measure(loop_fn, data)
    r_np, t_np = measure(np_fn, data)
    
    # Проверка совпадения
    if isinstance(r_loop, np.ndarray):
        ok = np.allclose(r_loop, r_np)
    else:
        ok = np.isclose(r_loop, r_np) if isinstance(r_loop, (int, float)) else True
        
    print(f"Цикл:   {t_loop*1000:10.2f} мс")
    print(f"NumPy:  {t_np*1000:10.2f} мс")
    print(f"Ускорение: {t_loop / t_np:.1f}×")
    print(f"Результаты совпадают: {ok}")


# ЗАДАЧИ 1-10

# Данные
a = np.random.default_rng(42).normal(size=1_000_000)
m = np.random.default_rng(42).normal(size=(100_000, 10))
ints = np.random.default_rng(42).integers(0, 100, size=1_000_000)

# Задача 1: Сумма массива
def loop1(arr):
    total = 0.0
    for x in arr:
        total += x
    return total
def np1(arr):
    return arr.sum()
run_task("Задача 1", loop1, np1, a)

# Задача 2: 
def loop2(arr):
    n = len(arr)
    mean = sum(arr) / n
    sum_sq_diff = sum((x - mean) ** 2 for x in arr)
    variance = sum_sq_diff / n  # или (n-1) для несмещённой оценки
    std = math.sqrt(variance)
    return mean, std
def np2(arr):
    return arr.mean(), arr.std()
run_task("Задача 2,", loop2, np2, a)

# Задача 3: 
def loop3(arr): return [math.sin(x) + x*x for x in arr]
def np3(arr): return np.sin(arr) + arr**2
run_task("Задача 3", loop3, np3, a)

# Задача 4: 
def loop4(arr): return [0 if x < 0 else (1 if x > 1 else x) for x in arr]
def np4(arr): return np.clip(arr, 0, 1)
run_task("Задача 4", loop4, np4, a)

# Задача 5: 
def loop5(mat): return [sum(row) for row in mat]
def np5(mat): return mat.sum(axis=1)
run_task("Задача 5", loop5, np5, m)

# Задача 6:
def loop6(mat):
    means = [sum(mat[:, j])/len(mat) for j in range(mat.shape[1])]
    return [[mat[i, j] - means[j] for j in range(mat.shape[1])] for i in range(mat.shape[0])]
def np6(mat): return mat - mat.mean(axis=0)
run_task("Задача 6", loop6, np6, m)

# Задача 7:
def loop7(arr):
    max_val = max(arr)
    return max_val, list(arr).index(max_val)
def np7(arr): return arr.max(), arr.argmax()
run_task("Задача 7", loop7, np7, a)

# Задача 8:
def loop8(arr): return [x for x in arr if x > 0]
def np8(arr): return arr[arr > 0]
run_task("Задача 8", loop8, np8, a)

# Задача 9: 
def loop9(arr):
    for i in range(len(arr)):
        if arr[i] < 0: arr[i] = -arr[i]
    return arr
def np9(arr):
    arr[arr < 0] *= -1
    return arr
run_task("Задача 9", loop9, np9, a.copy())

# Задача 10:
def loop10(arr): return [x for x in arr if -1 < x < 1]
def np10(arr): return arr[(arr > -1) & (arr < 1)]
run_task("Задача 10", loop10, np10, a)
