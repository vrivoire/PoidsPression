import os
import traceback
import zipfile
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

COLS: dict[str, str] = {
    'Date': 'datetime64[ns]',
    'Description': 'str',
    'Sous-description': 'str',
    'Type d’opération': 'str',
    'Montant': 'Float64',
    'Solde': 'Float64'
}


class Solde:
    def __init__(self):
        pass

    def setup_columns(self, df: DataFrame):
        df.astype(COLS)
        df.sort_values(by=list(COLS.keys()), ascending=True, inplace=True)

    def load_csv(self, file_name: str = BKP_FULL_PATH) -> DataFrame:
        try:
            if os.path.isfile(file_name):
                load_csv_df = DataFrame(pd.read_csv(file_name, header=0))
                if load_csv_df is not None:
                    load_csv_df = load_csv_df[list(COLS.keys())]
                    self.setup_columns(load_csv_df)
                    poidspression.show_df(load_csv_df, title=file_name, max_rows=10)
                    log.info(f'Loaded file: {file_name}, with {len(load_csv_df)} rows')
                    return load_csv_df
                else:
                    log.warning(f'Could not load file: {file_name}')
            else:
                log.warning(f'Could not find file: {file_name}')

            load_csv_df = pd.DataFrame(columns=list(COLS.keys()))
            self.setup_columns(load_csv_df)
            return load_csv_df
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            raise ex

    def get_df_dl(self) -> dict[str, DataFrame]:
        try:
            dicto: dict[str, DataFrame] = {}
            for path in Path(DL_PATH).glob(DL_FILE_PATTERN):
                df_dict: DataFrame | None = self.load_csv(path.__str__())
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

            df.drop_duplicates(subset=list(COLS.keys()), keep='first', inplace=True)

            log.info(f'drop_duplicates: removed {len1 - len(df)} rows from {len1}')
            df.set_index('Date')
            df.reindex(columns=['Date'])
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            raise ex

    def prepare_data(self) -> DataFrame:
        try:
            df: DataFrame = self.load_csv()
            if df is not None:
                df_dict: dict[str, DataFrame] = self.get_df_dl()
                for path, df_tmp in df_dict.items():
                    df = pd.concat([df_tmp, df], axis=0, ignore_index=True, join='outer')
                    log.info(f'\t\tConcated: {path}, now {len(df)} rows')

                self.setup_columns(df)
                df = df.set_index('Date')

                self.drop_duplicates(df)

                poidspression.show_df(df, title='Result *********', max_rows=10)

                out_file: str = BKP_PATH + BKP_FILE + EXTENSION
                df.to_csv(out_file, encoding='utf-8', index=True, float_format='%.2f', date_format="%Y-%m-%d")
                df.to_csv(out_file + '.zip', index=True, float_format='%.2f', date_format="%Y-%m-%d",
                          compression={
                              'method': 'zip',
                              'compression': zipfile.ZIP_LZMA,
                              'compresslevel': 9
                          })
                log.info(f'Saved {out_file} file')

                for path in df_dict.keys():
                    log.info(f'\t\tFile {path} deleted')
                    Path(path).unlink(missing_ok=True)
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
