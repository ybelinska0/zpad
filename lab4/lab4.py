import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

# 1. Початкові параметри
init_amplitude = 1.0
init_frequency = 1.0
init_phase = 0.0
init_noise_mean = 0.0
init_noise_cov = 0.1
init_cutoff = 2.0 # Частота зрізу для фільтра

# 2. Налаштування часу та "базового" шуму
# Генеруємо масив часу (10 секунд, 1000 точок)
t = np.linspace(0, 10, 1000)

# Генеруємо базовий шум лише один раз
# Це гарантує, що при зміні гармоніки шум залишиться на своїх місцях
np.random.seed(42)
base_noise = np.random.normal(0, 1, len(t))

# 3. Основні функції
def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    # Чиста гармоніка: y(t) = A * sin(2*pi*f*t + phase)
    y_clean = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    
    # Формуємо поточний шум з базового масиву
    current_noise = base_noise * np.sqrt(noise_covariance) + noise_mean
    
    if show_noise:
        return y_clean + current_noise, y_clean
    return y_clean, y_clean

def apply_filter(data, cutoff, fs=100.0):
    # Фільтр Баттерворта низьких частот
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    if normal_cutoff <= 0 or normal_cutoff >= 1:
        return data # Запобіжник від помилок слайдера
    b, a = butter(3, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# 4. Налаштування вікна графіка
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
plt.subplots_adjust(left=0.1, bottom=0.45, wspace=0.2)

# Отримуємо початкові дані
y_initial, y_clean_initial = harmonic_with_noise(
    init_amplitude, init_frequency, init_phase, 
    init_noise_mean, init_noise_cov, True
)
y_filtered_initial = apply_filter(y_initial, init_cutoff)

# Малюємо початкові лінії
line_original, = ax1.plot(t, y_initial, lw=2, color='blue', label='Сигнал')
line_clean1, = ax1.plot(t, y_clean_initial, lw=2, color='black', linestyle='--', alpha=0.5, label='Чиста гармоніка')
ax1.set_title("Оригінальний сигнал")
ax1.set_xlabel("Час (t)")
ax1.set_ylabel("Амплітуда")
ax1.legend()
ax1.grid(True)

line_filtered, = ax2.plot(t, y_filtered_initial, lw=2, color='red', label='Відфільтрований')
line_clean2, = ax2.plot(t, y_clean_initial, lw=2, color='black', linestyle='--', alpha=0.5, label='Чиста гармоніка')
ax2.set_title("Відфільтрований сигнал")
ax2.set_xlabel("Час (t)")
ax2.legend()
ax2.grid(True)

# 5. Створення інтерфейсу (слайдери)
axcolor = 'lightgoldenrodyellow'
ax_amp = plt.axes([0.1, 0.35, 0.35, 0.03], facecolor=axcolor)
ax_freq = plt.axes([0.1, 0.30, 0.35, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.1, 0.25, 0.35, 0.03], facecolor=axcolor)

ax_mean = plt.axes([0.55, 0.35, 0.35, 0.03], facecolor=axcolor)
ax_cov = plt.axes([0.55, 0.30, 0.35, 0.03], facecolor=axcolor)
ax_cutoff = plt.axes([0.55, 0.25, 0.35, 0.03], facecolor=axcolor)

samp = Slider(ax_amp, 'Амплітуда', 0.1, 10.0, valinit=init_amplitude)
sfreq = Slider(ax_freq, 'Частота', 0.1, 10.0, valinit=init_frequency)
sphase = Slider(ax_phase, 'Фаза', 0.0, 2*np.pi, valinit=init_phase)

smean = Slider(ax_mean, 'Шум (Середнє)', -2.0, 2.0, valinit=init_noise_mean)
scov = Slider(ax_cov, 'Шум (Дисперсія)', 0.0, 5.0, valinit=init_noise_cov)
scutoff = Slider(ax_cutoff, 'Фільтр (Зріз)', 0.1, 20.0, valinit=init_cutoff)

# Чекбокс
ax_check = plt.axes([0.1, 0.10, 0.15, 0.1])
check = CheckButtons(ax_check, ['Показувати шум'], [True])

# Кнопка Reset
ax_reset = plt.axes([0.8, 0.12, 0.1, 0.04])
btn_reset = Button(ax_reset, 'Reset', color=axcolor, hovercolor='0.975')

# 6. Логіка оновлення графіків
def update(val):
    show_noise_flag = check.get_status()[0]
    
    # Отримуємо нові дані
    y_new, y_clean_new = harmonic_with_noise(
        samp.val, sfreq.val, sphase.val, 
        smean.val, scov.val, show_noise_flag
    )
    
    # Фільтруємо
    y_filt_new = apply_filter(y_new, scutoff.val)
    
    # Оновлюємо лінії на графіках
    line_original.set_ydata(y_new)
    line_clean1.set_ydata(y_clean_new)
    
    line_filtered.set_ydata(y_filt_new)
    line_clean2.set_ydata(y_clean_new)
    
    # Перемальовуємо вікно
    fig.canvas.draw_idle()

# Прив'язуємо функцію оновлення до всіх елементів
samp.on_changed(update)
sfreq.on_changed(update)
sphase.on_changed(update)
smean.on_changed(update)
scov.on_changed(update)
scutoff.on_changed(update)
check.on_clicked(update)

# Логіка кнопки Reset
def reset(event):
    samp.reset()
    sfreq.reset()
    sphase.reset()
    smean.reset()
    scov.reset()
    scutoff.reset()
    if not check.get_status()[0]:
        check.set_active(0) # Повертаємо галочку
btn_reset.on_clicked(reset)

plt.show()