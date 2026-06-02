"""
center.py — ставит все 4 сервопривода в 90° (центр).

Запускай ПЕРЕД тем, как надевать качалки и собирать суставы: так у каждого сустава
будет полный ход в обе стороны. Это замена старому скетчу center_all.ino — теперь
центровка делается из Python через Firmata.

Запусти:  python center.py
"""
import time
from arm import connect

arm = connect()

for i in range(4):
    arm.set(i, 90)               # центр для каждого сустава
    print(f"{arm.joints[i].name}: 90°")

time.sleep(1)                    # дать серво доехать
arm.close()
print("✅ Все суставы в центре. Можно надевать качалки.")
