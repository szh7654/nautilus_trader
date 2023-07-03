# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2023 Nautech Systems Pty Ltd. All rights reserved.
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

import pandas as pd
import pyarrow as pa
import pytest
from fsspec.utils import pathlib

from nautilus_trader.core.nautilus_pyo3.persistence import QuoteTickDataWrangler
from nautilus_trader.core.nautilus_pyo3.persistence import TradeTickDataWrangler
from nautilus_trader.persistence.loaders_v2 import QuoteTickDataFrameProcessor
from nautilus_trader.persistence.loaders_v2 import TradeTickDataFrameLoader
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from tests import TESTS_PACKAGE_ROOT


TEST_DATA_DIR = pathlib.Path(TESTS_PACKAGE_ROOT).joinpath("test_data")
AUDUSD_SIM = TestInstrumentProvider.default_fx_ccy("AUD/USD")
ETHUSDT_BINANCE = TestInstrumentProvider.ethusdt_binance()


def test_quote_tick_data_wrangler() -> None:
    # Arrange
    path = TEST_DATA_DIR / "truefx-audusd-ticks.csv"
    df: pd.DataFrame = pd.read_csv(path)
    df = QuoteTickDataFrameProcessor.process(df)

    # Convert DataFrame to Arrow Table
    table = pa.Table.from_pandas(df)

    # Act (not any kind of final API, just experimenting with IPC)
    sink = pa.BufferOutputStream()
    writer: pa.RecordBatchStreamWriter = pa.ipc.new_stream(sink, table.schema)
    writer.write_table(table)
    writer.close()

    data = sink.getvalue().to_pybytes()

    wrangler = QuoteTickDataWrangler(
        instrument_id=AUDUSD_SIM.id.value,
        price_precision=AUDUSD_SIM.price_precision,
        size_precision=AUDUSD_SIM.size_precision,
    )
    ticks = wrangler.process_record_batches_bytes(data)

    # Assert
    assert len(ticks) == 100_000
    assert str(ticks[0]) == "AUD/USD.SIM,0.67067,0.67070,1000000,1000000,1580398089820000000"
    assert str(ticks[-1]) == "AUD/USD.SIM,0.66934,0.66938,1000000,1000000,1580504394501000000"


@pytest.mark.skip
def test_trade_tick_data_wrangler() -> None:
    # Arrange
    path = TEST_DATA_DIR / "binance-ethusdt-trades.csv"
    tick_data: pd.DataFrame = TradeTickDataFrameLoader.read_csv(path)

    wrangler = TradeTickDataWrangler(
        instrument_id=ETHUSDT_BINANCE.id.value,
        price_precision=ETHUSDT_BINANCE.price_precision,
        size_precision=ETHUSDT_BINANCE.size_precision,
    )

    # Act (not any kind of final API, just experimenting with IPC)
    ticks = wrangler.process_pandas(tick_data)

    # Assert
    assert len(ticks) == 69806
    assert str(ticks[0]) == "ETHUSDT.BINANCE,423.76,2.67900,BUYER,148568980,1597399200223000000"
    assert str(ticks[-1]) == "ETHUSDT.BINANCE,426.89,0.16100,BUYER,148638715,1597417198693000000"