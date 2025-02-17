# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2025 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

from os import PathLike
from typing import Any

import pandas as pd


class CSVTickDataLoader:
    """
    Provides a generic tick data CSV file loader.
    """

    @staticmethod
    def load(
        file_path: PathLike[str] | str,
        index_col: str | int = "timestamp",
        parse_dates: bool = True,
        datetime_format: str = "mixed",
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Return a tick `pandas.DataFrame` loaded from the given CSV `file_path`.

        Parameters
        ----------
        file_path : str, path object or file-like object
            The path to the CSV file.
        index_col : str or int, default 'timestamp'
            The column to use as the row labels of the DataFrame.
        parse_dates : bool, default True
            If True, attempt to parse the index.
        datetime_format : str, default 'mixed'
            The timestamp column format.
        **kwargs : Any
            The additional parameters to be passed to pd.read_csv.

        Returns
        -------
        pd.DataFrame

        """
        df = pd.read_csv(
            file_path,
            index_col=index_col,
            parse_dates=parse_dates,
            **kwargs,
        )
        df.index = pd.to_datetime(df.index, format=datetime_format)
        return df


class CSVBarDataLoader:
    """
    Provides a generic bar data CSV file loader.
    """

    @staticmethod
    def load(
        file_path: PathLike[str] | str,
        index_col: str | int = "timestamp",
        parse_dates: bool = True,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Return the bar `pandas.DataFrame` loaded from the given CSV `file_path`.

        Parameters
        ----------
        file_path : str, path object or file-like object
            The path to the CSV file.
        index_col : str | int, default 'timestamp'
            The column to use as the row labels of the DataFrame.
        parse_dates : bool, default True
            If True, attempt to parse the index.
        **kwargs : Any
            The additional parameters to be passed to pd.read_csv.

        Returns
        -------
        pd.DataFrame

        """
        df = pd.read_csv(
            file_path,
            index_col=index_col,
            parse_dates=parse_dates,
            **kwargs,
        )
        df.index = pd.to_datetime(df.index, format="mixed")
        return df


class ParquetTickDataLoader:
    """
    Provides a generic tick data Parquet file loader.
    """

    @staticmethod
    def load(
        file_path: PathLike[str] | str,
        timestamp_column: str = "timestamp",
    ) -> pd.DataFrame:
        """
        Return the tick `pandas.DataFrame` loaded from the given Parquet `file_path`.

        Parameters
        ----------
        file_path : str, path object or file-like object
            The path to the Parquet file.
        timestamp_column: str
            Name of the timestamp column in the parquet data

        Returns
        -------
        pd.DataFrame

        """
        df = pd.read_parquet(file_path)
        df = df.set_index(timestamp_column)
        return df


class ParquetBarDataLoader:
    """
    Provides a generic bar data Parquet file loader.
    """

    @staticmethod
    def load(file_path: PathLike[str] | str) -> pd.DataFrame:
        """
        Return the bar `pandas.DataFrame` loaded from the given Parquet `file_path`.

        Parameters
        ----------
        file_path : str, path object or file-like object
            The path to the Parquet file.

        Returns
        -------
        pd.DataFrame

        """
        df = pd.read_parquet(file_path)
        df = df.set_index("timestamp")
        return df
