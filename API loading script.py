import requests
import json
import pandas as pd
from datetime import datetime
import numpy as np
import plotly.express as px
from io import StringIO ## for Python 3
import quantstats as qs
from tqdm import tqdm
import importlib
import dotenv
from dotenv import load_dotenv # use for api key
import os #provides ways to access the Operating System and allows us to read the environment variables

################################
# load api key from .env file
################################

load_dotenv()

my_secret_key = os.getenv("input_key")

################################
# get historical gas fee
################################


headers = {
    "Accept": "application/json",
    "x-api-key": my_secret_key
}


def get_pair_info(input_exchange="uniswapv2", input_asset="USDC", input_format="csv"):
    url = f"https://web3api.io/api/v2/market/defi/dex/pairs?exchange={input_exchange}&asset={input_asset}&format={input_format}"
    response = requests.get(url, headers=headers)
    response = response.text
    csvStringIO = StringIO(response)
    df = pd.read_csv(csvStringIO, sep=",", header=0)

    return df


def get_all_pairs_info(input_exchange="uniswapv2", input_asset="USDC", input_format="csv"):
    url = f"https://web3api.io/api/v2/market/defi/dex/pairs?exchange={input_exchange}&format={input_format}"
    response = requests.get(url, headers=headers)
    response = response.text
    csvStringIO = StringIO(response)
    df = pd.read_csv(csvStringIO, sep=",", header=0)

    return df


def get_pair_price(input_exchange="uniswapv2", input_pair="DAI_WETH", input_start_date="2022-12-01",
                   input_end_date="2022-12-31", format_type="csv"):
    url = f"https://web3api.io/api/v2/market/defi/ohlcv/{input_pair}/historical/?exchange={input_exchange}&startDate={input_start_date}&endDate={input_end_date}&format={format_type}"

    response = requests.get(url, headers=headers)
    response = response.text
    # response  = response['payload']
    csvStringIO = StringIO(response)
    df = pd.read_csv(csvStringIO, sep=",", header=0)

    return df


def get_pair_tvl_volume(input_exchange="uniswapv2", input_pair="0xa478c2975ab1ea89e8196811f51a7b7ade33eb11",
                        input_start_date="2022-09-01T00%3A00%3A00", input_end_date="2022-09-02T00%3A00%3A00",
                        input_format="csv"):
    url = f"https://web3api.io/api/v2/market/defi/metrics/exchanges/{input_exchange}/pairs/{input_pair}/historical?startDate={input_start_date}&endDate={input_end_date}&format={input_format}"
    response = requests.get(url, headers=headers)
    response = response.text
    csvStringIO = StringIO(response)
    df = pd.read_csv(csvStringIO, sep=",", header=0)

    return df

def clean_data( df_tvl_volume):


    df_tvl_volume = df_tvl_volume.drop_duplicates()
    #df_tvl_volume['timestamp'] = df_tvl_volume['timestamp'].apply(lambda x: x[:-4])
    df_tvl_volume['timestamp'] = pd.to_datetime(df_tvl_volume['timestamp'],unit='ms')
    df_tvl_volume = df_tvl_volume.sort_values('timestamp')

    return df_tvl_volume




########################################## get UniV2 pool pair price #######################################

DAI_WETH_pool_price = get_pair_price(input_exchange = "uniswapv2", input_pair="DAI_WETH", input_start_date = "2022-12-01", input_end_date="2022-12-31")
DAI_WETH_pool_price['timestamp'] = pd.to_datetime(DAI_WETH_pool_price['timestamp'],unit='ms')

DAI_WETH_pool_price.head()


########################################## get UniV2 pool trade statistics #######################################

DAI_WETH_UNI_V2 = get_pair_tvl_volume(  input_exchange = "uniswapv2", input_pair="0xa478c2975ab1ea89e8196811f51a7b7ade33eb11", input_start_date = "2022-09-01T00%3A00%3A00", input_end_date = "2022-09-10T00%3A00%3A00")


########################################## show pool statistics on Uni V2 and Uni V3 #######################################

DAI_WETH_UNI_V2_volume = get_pair_tvl_volume(  input_exchange = "uniswapv2", input_pair="0x147cfb9bf524aef1ed2d0921e79abba7bfb4d950", input_start_date = "2022-12-01T00%3A00%3A00", input_end_date = "2022-12-31T00%3A00%3A00")

DAI_WETH_UNI_V2_volume.head()

DAI_USDT_UNI_V2_volume = get_pair_tvl_volume(  input_exchange = "uniswapv2", input_pair="0xb20bd5d04be54f870d5c0d3ca85d82b34b836405", input_start_date = "2022-12-01T00%3A00%3A00", input_end_date = "2022-12-31T00%3A00%3A00")


####################################### GET TVL_VOLUME_FEE per pool #######################################

# DAI_ETH UNI V2

DAI_ETH_UNI_V2_volume = get_pair_tvl_volume(  input_exchange = "uniswapv2", input_pair="0xa478c2975ab1ea89e8196811f51a7b7ade33eb11", input_start_date = "2022-12-01T00%3A00%3A00", input_end_date = "2022-12-31T00%3A00%3A00")
DAI_ETH_UNI_V2_volume  = clean_data(DAI_ETH_UNI_V2_volume)
DAI_ETH_UNI_V2_volume.to_csv("./api_load/DAI_ETH_UNI_V2_VOL_12_01_to_12_31.csv")



# WETH_USDC UNI V2

WETH_USDC_UNI_V2_volume = get_pair_tvl_volume(  input_exchange = "uniswapv2", input_pair="0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc", input_start_date = "2022-12-01T00%3A00%3A00", input_end_date = "2022-12-31T00%3A00%3A00")
WETH_USDC_UNI_V2_volume  = clean_data(WETH_USDC_UNI_V2_volume)
WETH_USDC_UNI_V2_volume.to_csv("./api_load/WETH_USDC_UNI_V2_VOL_12_01_to_12_31.csv")



# DAI_USDT UNI V2

DAI_USDT_UNI_V2_volume = get_pair_tvl_volume(  input_exchange = "uniswapv2", input_pair="0xb20bd5d04be54f870d5c0d3ca85d82b34b836405", input_start_date = "2022-12-01T00%3A00%3A00", input_end_date = "2022-12-31T00%3A00%3A00")
DAI_USDT_UNI_V2_volume  = clean_data(DAI_USDT_UNI_V2_volume)
DAI_USDT_UNI_V2_volume.to_csv("./api_load/DAI_USDT_UNI_V2_VOL_12_01_to_12_31.csv")

# DAI_USDC UNI V2

DAI_USDC_UNI_V2_volume = get_pair_tvl_volume(  input_exchange = "uniswapv2", input_pair="0xae461ca67b15dc8dc81ce7615e0320da1a9ab8d5", input_start_date = "2022-12-01T00%3A00%3A00", input_end_date = "2022-12-31T00%3A00%3A00")
DAI_USDC_UNI_V2_volume  = clean_data(DAI_USDC_UNI_V2_volume)
DAI_USDC_UNI_V2_volume.to_csv("./api_load/DAI_USDC_UNI_V2_VOL_12_01_to_12_31.csv")



####################################### GET POOL PRICE #######################################


# dai_weth UNI V2
# get_pair_tvl_volume(  input_exchange = "uniswapv2", input_pair="0xa478c2975ab1ea89e8196811f51a7b7ade33eb11", input_start_date = "2022-09-01T00%3A00%3A00", input_end_date = "2022-09-10T00%3A00%3A00")


# DAI_WETH UNI V2
DAI_ETH_UNI_V2_pool_price = get_pair_price(input_exchange = "uniswapv2", input_pair="0xa478c2975ab1ea89e8196811f51a7b7ade33eb11", input_start_date = "2022-12-01", input_end_date="2022-12-31")

DAI_ETH_UNI_V2_pool_price = clean_data(DAI_ETH_UNI_V2_pool_price)
DAI_ETH_UNI_V2_pool_price.to_csv("./api_load/DAI_ETH_UNI_V2_pool_price_12_01_to_12_31.csv")



# WETH_USDC UNI V2

WETH_USDC_UNI_V2_pool_price = get_pair_price(input_exchange = "uniswapv2", input_pair="0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc", input_start_date = "2022-12-01", input_end_date="2022-12-31")


WETH_USDC_UNI_V2_pool_price  = clean_data(WETH_USDC_UNI_V2_pool_price )
WETH_USDC_UNI_V2_pool_price.to_csv("./api_load/WETH_USDC_UNI_V2_pool_price_12_01_to_12_31.csv")


# DAI_USDT UNI V2


DAI_USDT_UNI_V2_pool_price = get_pair_price(input_exchange = "uniswapv2", input_pair="0xb20bd5d04be54f870d5c0d3ca85d82b34b836405", input_start_date = "2022-12-01", input_end_date="2022-12-31")

DAI_USDT_UNI_V2_pool_price  = clean_data(DAI_USDT_UNI_V2_pool_price )
DAI_USDT_UNI_V2_pool_price.to_csv("./api_load/DAI_USDT_UNI_V2_pool_price_12_01_to_12_31.csv")


# DAI_USDC UNI V2


DAI_USDC_UNI_V2_pool_price = get_pair_price(input_exchange = "uniswapv2", input_pair="0xae461ca67b15dc8dc81ce7615e0320da1a9ab8d5", input_start_date = "2022-12-01", input_end_date="2022-12-31")

DAI_USDC_UNI_V2_pool_price  = clean_data(DAI_USDC_UNI_V2_pool_price )
DAI_USDC_UNI_V2_pool_price.to_csv("./api_load/DAI_USDC_UNI_V2_pool_price_12_01_to_12_31.csv")


DAI_USDT_UNI_V2_pool_price.head()