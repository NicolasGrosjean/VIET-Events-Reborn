import pandas as pd
import os

wtwsms_loc_dir = os.path.join('..', '..', 'WtWSMS', 'WTWSMS', 'localisation')
viet_loc_dir = os.path.join('..', 'VIET Events', 'localisation')

wtwsms_files = ['ACR_cybrxkhan_misc.csv', 'VIET_ordepchains.csv', 'VIET_Regency_localisations.csv',
                'VIET_Republics_text.csv', 'VIET_jewish.csv']
viet_files = ['ACR_cybrxkhan_misc.csv', 'ordepchains.csv', 'Regency_localisations.csv',
              'VIET_Republics_flavor_events.csv', 'VIET_jewish2.csv']

for i in range(len(wtwsms_files)):
    wtwsms_file = wtwsms_files[i]
    viet_file = viet_files[i]

    # Read files
    df_wtwsms = pd.read_csv(os.path.join(wtwsms_loc_dir, wtwsms_file), sep=';', encoding='ansi', header=None)
    df_viet = pd.read_csv(os.path.join(viet_loc_dir, viet_file), sep=';', encoding='ansi', header=None)

    # Check there is no translation yet
    if len(df_viet) != df_viet[2].apply(lambda s: pd.isnull(s) or 'Xxxxxxffff' == s or 'xxxxx' == s).sum():
        print(f'VIET file {viet_file} has already a French localisation')
        continue

    # Merge on English text
    df_merged = pd.merge(df_viet, df_wtwsms, how='left', on=1)

    # Extract VIET code and WtWSMS texts
    df_merged = df_merged[pd.Index(['0_x', 1]).union(df_merged.columns[df_viet.shape[1]+1:])]

    # Remove duplicate codes
    df_merged = df_merged.loc[df_merged['0_x'].drop_duplicates().index]

    # Export result
    df_merged.to_csv(os.path.join(viet_loc_dir, viet_file), sep=';', encoding='ansi', header=None, index=None)
    print(f'VIET file {viet_file} overrided')
