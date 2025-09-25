
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

tide_data = pd.read_csv('tides_processed.csv')
tide_level = tide_data['tide_level'].values if 'tide_level' in tide_data.columns else tide_data.iloc[:, 1].values


# 心形参数方程
def heart_shape(t, scale=1.0):
    x = scale * 16 * np.sin(t) ** 3
    y = scale * (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    return x, y


fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_aspect('equal')
ax.axis('off')

# 皮粉色
peach_pink = '#FFD1DC'
t = np.linspace(0, 2 * np.pi, 300)
x, y = heart_shape(t, scale=1)
heart, = ax.plot(x, y, color=peach_pink, lw=3, alpha=0.9)
text = ax.text(-19, -18, '', fontsize=16, color=peach_pink, ha='left', va='bottom', fontweight='bold')

# 动画更新函数
def animate(frame):
    idx = frame % len(tide_level)
    value = tide_level[idx]
    # 跳动的缩放因子，随潮汐变化
    scale = 1 + 0.5 * np.sin(frame * 0.3) * (value / (tide_level.max() + 1e-6))
    x, y = heart_shape(t, scale=scale)
    heart.set_data(x, y)
    heart.set_alpha(0.8 + 0.2 * np.sin(frame * 0.3))
    text.set_text(f'Tide Level: {value:.2f}')
    return heart, text

ani = animation.FuncAnimation(fig, animate, frames=len(tide_level)*2, interval=100, blit=True)
plt.show()
