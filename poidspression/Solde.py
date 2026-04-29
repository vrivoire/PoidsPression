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
DL_FILE_PATTERN: str = f"{BKP_FILE}_*{EXTENSION}"


class Solde:
    def __init__(self):
        pass

    def load_csv(self, file_name: str = BKP_FULL_PATH) -> DataFrame:
        try:
            if os.path.isfile(file_name):
                log.info(f'Found file: {file_name}')
                load_csv_df = DataFrame(pd.read_csv(file_name))
                if load_csv_df is not None:
                    log.info(f'Loaded file: {file_name}, with {len(load_csv_df)} rows')
                    return load_csv_df
                else:
                    raise Exception(f'Could not load file: {file_name}')
            else:
                raise Exception(f'Could not find file: {file_name}')
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            raise ex

    def drop_duplicates(self, df):
        len1 = len(df)
        # poidspression.show_df(df[df.duplicated(subset=['Date', 'Description', 'Sous-description', 'Type d’opération', 'Montant', 'Solde'], keep='first')], title='drop_duplicates')
        df = df.drop_duplicates(subset=['Date', 'Description', 'Sous-description', 'Type d’opération', 'Montant', 'Solde'], keep='first', inplace=False, ignore_index=True)
        log.info(f'drop_duplicates: removed {len1 - len(df)} rows')
        return df

    def get_df_dl(self) -> dict[str, DataFrame]:
        try:
            dicto: dict[str, DataFrame] = {}
            for path in Path(DL_PATH).glob(DL_FILE_PATTERN):
                df_dict: DataFrame | None = solde.load_csv(path.__str__())
                if df_dict is not None:
                    dicto[path.__str__()] = df_dict
                    log.info(f'Loaded: path: {path}, size: {len(df_dict)} rows')
                else:
                    log.warning(f'Could not load file: {path.__str__()}')
            return dicto
        except Exception as ex:
            log.error(ex)
            log.error(traceback.format_exc())
            raise ex


if __name__ == "__main__":
    try:
        poidspression.set_up(__file__)
        solde = Solde()

        df: DataFrame = solde.load_csv()
        if df is not None:
            df_dict: dict[str, DataFrame] = solde.get_df_dl()
            for path, df_tmp in df_dict.items():
                df = pd.concat([df, df_tmp], axis=0, ignore_index=True)
                log.info(f'Concated: {path}, now {len(df)} rows')

            df = solde.drop_duplicates(df)
            # df = df.drop_duplicates(subset=['Date', 'Description', 'Sous-description', 'Type d’opération', 'Montant', 'Solde'], keep='first', inplace=False, ignore_index=True)
            # log.info(f'drop_duplicates: removed {len1 - len(df)} rows')

            df = df.astype({'Date': 'datetime64[ns]'})
            df = df.set_index('Date')
            df.sort_values(by='Date', ascending=True, inplace=True)

            # df = df.drop(columns=['Filtre'])
            poidspression.show_df(df, title='Result *********', max_rows=10)

            out_file: str = BKP_PATH + BKP_FILE + '_2' + EXTENSION
            df.to_csv(out_file, encoding='utf-8', index=True, float_format='%.2f', date_format="%Y/%m/%d %H:%M:%S")
            log.info(f'Saved {out_file} file')

            for path, df_tmp in df_dict.items():
                log.info(f'File {path} deleted')
        else:
            log.error('df is None')
    except Exception as ex:
        log.error(ex)
        log.error(traceback.format_exc())
        raise ex
