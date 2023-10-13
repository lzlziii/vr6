import sys
sys.path.append("./for_tu")
import for_tu
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.ticker import FuncFormatter


map_to = dict()
pname_list = ['microsoft.txt', 'oculus.txt', 'pico.txt', 'playstation.txt', 'viveport.txt']
pname_list_to = ['Microsoft', 'Oculus', 'Pico', 'PlayStation', 'Viveport']
language_list = ['en', 'zh-cn', 'ja', 'de', 'et', 'vi', 'fr', 'no', 'other']
language_list_to = ['English', 'Chinese', 'Japanese', 'German', 'Estonian', 'Vietnamese', 'French', 'Norwegian', 'Others']
for i in range(len(pname_list)):
    assert len(pname_list) == len(pname_list_to)
    map_to[pname_list[i]] = pname_list_to[i]
for i in range(len(language_list)):
    assert len(language_list) == len(language_list_to)
    map_to[language_list[i]] = language_list_to[i]

# 设置Matplotlib字体
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 20  # 设置字体大小
plt.rcParams['xtick.labelsize'] = 18  # x轴刻度的字体大小
plt.rcParams['ytick.labelsize'] = 18  # y轴刻度的字体大小


row_labels, col_labels, cnt = for_tu.for_tu()
for i in range(len(row_labels)):
    row_labels[i] = map_to[row_labels[i]]
for i in range(len(col_labels)):
    col_labels[i] = map_to[col_labels[i]]

for i in range(len(cnt)):
    for j in range(len(cnt[i])):
        cnt[i][j] += 1

platform_country = {
    'Microsoft': 'USA',
    'Oculus': 'USA',
    'Pico': 'China',
    'PlayStation': 'Japan',
    'Steam': 'USA',
    'Viveport': 'Taiwan'
}

print(row_labels)

data = np.array(cnt)
platform_pp_ratios = data.sum(axis=1) / data.sum()
new_row_labels = []
for idx, label in enumerate(row_labels):
    country = platform_country.get(label, "")
    pp_ratio = platform_pp_ratios[idx]
    new_label = f"{label}\n{country}, {pp_ratio:.1%}"
    if "Taiwan" in new_label:
        new_label = f"{label}\n{country}, {pp_ratio:.1%}"
    new_row_labels.append(new_label)
row_labels = new_row_labels

data_log = np.log2(data)

df = pd.DataFrame(data, index=row_labels, columns=col_labels)
df_log = pd.DataFrame(data_log, index=row_labels, columns=col_labels)

gap_pixels = 5

colors = [
    (253/255, 253/255, 228/255),
    (158/255, 218/255, 175/255),
    (37/255, 173/255, 188/255),
    (10/255, 36/255, 99/255)
]
custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=256)

df_annot = df - 1

# 剩余代码保持不变
fig, ax = plt.subplots(dpi=200, figsize=(10, 6))
cax = sns.heatmap(df_log, annot=df_annot, vmax=np.log2(1000), vmin=0, xticklabels=True, yticklabels=True,
            square=True, cmap=custom_cmap, linewidths=gap_pixels, linecolor='white', cbar_kws={"norm": LogNorm()},
            fmt='.0f', ax=ax, annot_kws={"size": 18}, cbar=False)  # 注意这里的 cbar=False
cax.set_xticklabels(cax.get_xticklabels(), rotation=15)

cbar_ax = cax.figure.add_axes([.91, .127, .03, .73])  # x, y, width, height
cbar = cax.figure.colorbar(cax.collections[0], cax=cbar_ax, norm=LogNorm())
def fmt(x, pos):
    return r'$2^{{{}}}$ = {}'.format(int(np.round(x)), int(np.exp2(x)))
cbar.formatter = FuncFormatter(fmt)
cbar.update_ticks()
cbar.ax.tick_params(labelsize=16)

plt.title('', fontdict={'fontsize': 20, 'fontweight': 'bold'})
plt.tick_params(axis='x', bottom=False, top=True, labelbottom=True, labeltop=False)
cax.yaxis.set_ticks_position('none')  # 移除y轴上的刻度线
cax.xaxis.set_ticks_position('none')  # 移除y轴上的刻度线
cbar.ax.tick_params(labelsize=16)

plt.savefig("heatmap.pdf", format='pdf', dpi=200, bbox_inches='tight')
plt.show()
