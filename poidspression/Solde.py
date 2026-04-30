import os
import traceback
from pathlib import Path

import pandas as pd
from pandas import DataFrame

import poidspression
from poidspression import log

EXTENSION: str = '.csv'

BKP_PATH: str = f"{os.getenv('USERPROFILE')}/Documents/BkpScripts/"
BKP_FILE: str = 'forfait_Ultime'
BKP_FULL_PATH = BKP_PATH + BKP_FILE + EXTENSION

DL_PATH: str = f"{os.getenv('USERPROFILE')}/Downloads/"
DL_FILE_PATTERN: str = f"{BKP_FILE}*{EXTENSION}"

COLS: list[str] = ['Date', 'Description', 'Sous-description', 'Type d’opération', 'Montant', 'Solde']


class Solde:
    def __init__(self):
        pass

    def load_csv(self, file_name: str = BKP_FULL_PATH) -> DataFrame:
        try:
            if os.path.isfile(file_name):
                load_csv_df = DataFrame(pd.read_csv(file_name, header=0))
                if load_csv_df is not None:
                    load_csv_df = load_csv_df[COLS]
                    load_csv_df.astype({'Date': 'datetime64[ns]', 'Montant': 'Float64', 'Solde': 'Float64'})
                    load_csv_df.sort_values(by='Date', ascending=True, inplace=True)
                    poidspression.show_df(load_csv_df, title=file_name, max_rows=10)
                    log.info(f'Loaded file: {file_name}, with {len(load_csv_df)} rows')
                    return load_csv_df
                else:
                    log.warning(f'Could not load file: {file_name}')
            else:
                log.warning(f'Could not find file: {file_name}')

            load_csv_df = pd.DataFrame(columns=COLS)
            load_csv_df.astype({'Date': 'datetime64[ns]', 'Montant': 'Float64', 'Solde': 'Float64'})
            load_csv_df.sort_values(by='Date', ascending=True, inplace=True)
            return load_csv_df
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            raise ex

    def get_df_dl(self) -> dict[str, DataFrame]:
        try:
            dicto: dict[str, DataFrame] = {}
            for path in Path(DL_PATH).glob(DL_FILE_PATTERN):
                df_dict: DataFrame | None = solde.load_csv(path.__str__())
                if df_dict is not None:
                    dicto[path.__str__()] = df_dict
                else:
                    log.warning(f'Could not load file: {path.__str__()}')
            return dicto
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            raise ex

    def drop_duplicates(self, df):
        try:
            df.reset_index(inplace=True)
            len1: int = len(df)
            diff_df = df[df.duplicated(keep='first')]
            log.info(f"Removed Rows: {len(diff_df)}")

            df.drop_duplicates(subset=COLS, keep='first', inplace=True)

            log.info(f'drop_duplicates: removed {len1 - len(df)} rows from {len1}')
            df.set_index('Date')
            df.reindex(columns=['Date'])
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            raise ex

    def prepare_data(self) -> DataFrame:
        try:
            df: DataFrame = solde.load_csv()
            if df is not None:
                df_dict: dict[str, DataFrame] = solde.get_df_dl()
                for path, df_tmp in df_dict.items():
                    df = pd.concat([df_tmp, df], axis=0, ignore_index=True, join='outer')
                    log.info(f'\t\tConcated: {path}, now {len(df)} rows')
                    df.sort_values(by='Date', ascending=True, inplace=True)

                df = df[COLS]
                df.astype({'Date': 'datetime64[ns]', 'Montant': 'Float64', 'Solde': 'Float64'})
                df = df.set_index('Date')
                df.sort_values(by=COLS, ascending=True, inplace=True)

                solde.drop_duplicates(df)

                poidspression.show_df(df, title='Result *********', max_rows=10)

                out_file: str = BKP_PATH + BKP_FILE + EXTENSION
                df.to_csv(out_file, encoding='utf-8', index=True, float_format='%.2f', date_format="%Y/%m/%d %H:%M:%S")
                log.info(f'Saved {out_file} file')

                for path, df_tmp in df_dict.items():
                    log.info(f'\t\tFile {path} deleted')
            else:
                log.error('df is None')

            return df
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            raise ex


if __name__ == "__main__":
    try:
        poidspression.set_up(__file__)
        solde = Solde()
        df: DataFrame = solde.prepare_data()
        print('------------------------------------')
        df.info()
        print('------------------------------------')
        # print(df.describe(include='all'))
        # print('------------------------------------')
        # print(df.shape)
    except Exception as ex:
        log.error(ex)
        log.error(traceback.format_exc())
