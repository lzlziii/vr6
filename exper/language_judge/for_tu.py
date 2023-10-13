import pandas as pd
import sys

def for_tu():
    df = pd.read_csv('./language_analyse_result.csv')
    df = df[df.iloc[:, 0] != 'steam.txt']
    csv_data = []
    for index, row in df.iterrows():
        w = []
        for col in df.columns:
            w.append(row[col])
        if w[2] == "-1":
            continue
        csv_data.append(w)
    df = None

    all_language = dict()
    all_platform = []
    for w in csv_data:
        all_language[w[2]] = 1 if w[2] not in all_language else all_language[w[2]] + 1
        if (len(all_platform) == 0 or w[0] != all_platform[-1]):
            all_platform.append(w[0])

    for i in all_platform:
        print(i)

    all_language_ordered = list(all_language.keys())
    all_language_ordered.sort(key=lambda x: all_language[x], reverse=True)
    for i in all_language_ordered:
        print(i, all_language[i])

    cnt = []
    for i in range(len(all_platform)):
        w = []
        for j in range(len(all_language_ordered)):
            w.append(0)
        cnt.append(w)

    # df = pd.read_csv('./language_analyse_result.csv')
    for i in range(len(all_platform)):
        for j in range(len(all_language_ordered)):
            print(i, j, all_platform[i], all_language_ordered[j])
            for w in csv_data:
                if w[0] == all_platform[i] and w[2] == all_language_ordered[j]:
                    cnt[i][j] += 1

    for i in range(len(cnt)):
        for j in range(8, len(cnt[i])):
            cnt[i][7] += cnt[i][j]
        cnt[i] = cnt[i][:8]

    all_language_ordered = all_language_ordered[:7]
    all_language_ordered.append("other")

    for i in all_language_ordered:
        print(f"'{i}',", end=' ')
    print()

    row_labels = list(all_platform)
    col_labels = list(all_language_ordered)
    data = pd.DataFrame(cnt, index=row_labels, columns=col_labels)
    print(data)
    return row_labels, col_labels, cnt

