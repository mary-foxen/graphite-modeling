import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval
from scipy import interpolate
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

plt.style.use(['science', 'grid'])


def plot_sample_data(sample_num):
    df = pd.read_csv('S'+str(sample_num)+'_k_model_fast.csv')
    df['possible_k'] = df['possible_k'].apply(literal_eval)
    df['possible_k'] = df['possible_k'].apply(lambda x: np.nan if len(x) == 0 else x)
    df = df.dropna()
    df['min_k'] = df['possible_k'].apply(lambda x: min(x)-0.5)
    df['max_k'] = df['possible_k'].apply(lambda x: max(x)+0.5)
    df['mean_k'] = df['possible_k'].apply(lambda x: np.mean(x))
    df.to_csv('S'+str(sample_num)+'_k_model_fast_processed.csv', index=False)
    # f = interpolate.interp1d(df['T'], np.vstack((df['min_k'], df['max_k'], df['mean_k'])), axis=1, kind='linear', fill_value='extrapolate')
    # T = np.linspace(min(df['T']), max(df['T']), 1000)
    # min_k = f(T)[0]
    # max_k = f(T)[1]
    # mean_k = f(T)[2]

    T = df['T']
    min_k = df['min_k']
    max_k = df['max_k']
    mean_k = df['mean_k']

    fig = plt.figure(num=1, clear=True)
    ax = fig.add_subplot(111)
    plt.plot(T, mean_k, '.-', label='S%d mean k' % sample_num)
    ax.fill_between(T, min_k, max_k, alpha=0.5)
    # plt.fill_between(df['T'], df['min_k'], df['max_k'], alpha=0.5, label='min/max k')
    # plt.plot(df['T'], df['min_k'], label='min k')
    # plt.plot(df['T'], df['max_k'], label='max k')
    plt.xlabel('Temperature (C)')
    plt.ylabel('Thermal Conductivity (W/mK)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('S'+str(sample_num)+'_k_model.png')
    # plt.show()
    pass


def plot_all_samples():
    fig1 = plt.figure(num=1, clear=True)
    
    df_all = None
    for index, sample_num in enumerate([3, 2, 8]):
        df = pd.read_csv('S'+str(sample_num)+'_k_model_fast.csv')
        df['possible_k'] = df['possible_k'].apply(literal_eval)
        df['possible_k'] = df['possible_k'].apply(lambda x: np.nan if len(x) == 0 else x)
        df = df.dropna()
        df['min_k'] = df['possible_k'].apply(lambda x: min(x)-0.5)
        df['max_k'] = df['possible_k'].apply(lambda x: max(x)+0.5)
        df['mean_k'] = df['possible_k'].apply(lambda x: np.mean(x))
        df_sample = df[['T','mean_k', 'min_k', 'max_k']]
        df_sample = df_sample.rename(columns={'mean_k': 'S'+str(sample_num), 'min_k': 'S'+str(sample_num)+'_min', 'max_k': 'S'+str(sample_num)+'_max'})
        if df_all is None:
            df_all = df_sample
        else:
            df_all = df_all.merge(df_sample, how='outer')
        df.to_csv('S'+str(sample_num)+'_k_model_fast_processed.csv', index=False)
        # f = interpolate.interp1d(df['T'], np.vstack((df['min_k'], df['max_k'], df['mean_k'])), axis=1, kind='linear', fill_value='extrapolate')
        # T = np.linspace(min(df['T']), max(df['T']), 1000)
        # min_k = f(T)[0]
        # max_k = f(T)[1]
        # mean_k = f(T)[2]

        T = df['T']
        min_k = df['min_k']
        max_k = df['max_k']
        mean_k = df['mean_k']
        plt.figure(num=1)
        # ax = fig1.add_subplot(2, 2, index+1)
        plt.plot(T, mean_k, '.-', label='Sample %d' % sample_num)
        plt.fill_between(T, min_k, max_k, alpha=0.2)
        plt.xlabel('Temperature (C)')
        plt.ylabel('Thermal Conductivity (W/mK)')
        plt.legend(loc='upper left')
        plt.xlim([0,1200])
        plt.ylim([5, 20])
        plt.tight_layout()

        # plt.figure(num=2)
        # plt.plot(T, mean_k, '.-', label='Sample %d' % sample_num)
        # plt.fill_between(df['T'], df['min_k'], df['max_k'], alpha=0.2)
        # plt.plot(df['T'], df['min_k'], label='min k')
        # plt.plot(df['T'], df['max_k'], label='max k')

    plt.figure(num=1)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig('all_S_k_model.pdf')

    fig2 = plt.figure(num=2, clear=True)
    ax = fig2.add_subplot(111)
    df_all['min_k'] = df_all[['S3_min', 'S2_min', 'S8_min']].min(axis=1)
    df_all['max_k'] = df_all[['S3_max', 'S2_max', 'S8_max']].max(axis=1)
    df_all['mean_k'] = df_all[['S3', 'S2', 'S8']].mean(axis=1)
    df_all = df_all[['T', 'mean_k', 'min_k', 'max_k']]
    df_all.to_csv('all_S_k_model.csv', index=False)
    df = pd.read_csv('k_5.csv')
    T = df['T']
    k = df['k']
    plt.plot(df_all['T'], df_all['mean_k'], '.-', label='Coated sample mean')
    plt.fill_between(df_all['T'], df_all['min_k'], df_all['max_k'], alpha=0.5)
    plt.plot(T, k, 'r.-', label='Sample 5')
    plt.xlabel('Temperature (C)')
    plt.ylabel('Thermal Conductivity (W/mK)')
    plt.xlim([0,1200])
    plt.ylim([5, 20])
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig('all_S_k_model_compiled.pdf')

    df_err = df_all.merge(df, how='inner')
    print(mean_absolute_percentage_error(df_err['mean_k'], df_err['k']))
    plt.show()


# plot_sample_data(3)
# plot_sample_data(2)
# plot_sample_data(8)
plot_all_samples()
