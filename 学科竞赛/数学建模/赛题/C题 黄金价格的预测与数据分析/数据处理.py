import pandas as pd

df = pd.read_csv('C:\\Users\\27047\\Desktop\\data.csv')

col_map = {
    'Date': '日期',
    'Open': '开盘价',
    'High': '最高价',
    'Low': '最低价',
    'Close': '收盘价',
    'Adj Close': '复权收盘价',
    'Volume': '成交量',

    'SP_open': '标普500开盘价',
    'SP_high': '标普500最高价',
    'SP_low': '标普500最低价',
    'SP_close': '标普500收盘价',
    'SP_Ajclose': '标普500复权收盘价',
    'SP_volume': '标普500成交量',

    'DJ_open': '道琼斯开盘价',
    'DJ_high': '道琼斯最高价',
    'DJ_low': '道琼斯最低价',
    'DJ_close': '道琼斯收盘价',
    'DJ_Ajclose': '道琼斯复权收盘价',
    'DJ_volume': '道琼斯成交量',

    'EG_open': '欧元美元开盘价',
    'EG_high': '欧元美元最高价',
    'EG_low': '欧元美元最低价',
    'EG_close': '欧元美元收盘价',
    'EG_Ajclose': '欧元美元复权收盘价',
    'EG_volume': '欧元美元成交量',

    'EU_Price': '欧元兑美元汇率',
    'EU_open': '欧元兑美元开盘',
    'EU_high': '欧元兑美元最高',
    'EU_low': '欧元兑美元最低',
    'EU_Trend': '欧元兑美元趋势',

    'OF_Price': '原油期货价格',
    'OF_Open': '原油期货开盘',
    'OF_High': '原油期货最高',
    'OF_Low': '原油期货最低',
    'OF_Volume': '原油期货成交量',
    'OF_Trend': '原油期货趋势',

    'OS_Price': '白银价格',
    'OS_Open': '白银开盘',
    'OS_High': '白银最高',
    'OS_Low': '白银最低',
    'OS_Trend': '白银趋势',

    'SF_Price': '大豆期货价格',
    'SF_Open': '大豆期货开盘',
    'SF_High': '大豆期货最高',
    'SF_Low': '大豆期货最低',
    'SF_Volume': '大豆期货成交量',
    'SF_Trend': '大豆期货趋势',

    'USB_Price': '美国国债价格',
    'USB_Open': '美国国债开盘',
    'USB_High': '美国国债最高',
    'USB_Low': '美国国债最低',
    'USB_Trend': '美国国债趋势',

    'PLT_Price': '铂金价格',
    'PLT_Open': '铂金开盘',
    'PLT_High': '铂金最高',
    'PLT_Low': '铂金最低',
    'PLT_Trend': '铂金趋势',

    'PLD_Price': '钯金价格',
    'PLD_Open': '钯金开盘',
    'PLD_High': '钯金最高',
    'PLD_Low': '钯金最低',
    'PLD_Trend': '钯金趋势',

    'RHO_PRICE': 'RHO指标',

    'USDI_Price': '美元指数',
    'USDI_Open': '美元指数开盘',
    'USDI_High': '美元指数最高',
    'USDI_Low': '美元指数最低',
    'USDI_Volume': '美元指数成交量',
    'USDI_Trend': '美元指数趋势',

    'GDX_Open': '黄金矿业ETF开盘',
    'GDX_High': '黄金矿业ETF最高',
    'GDX_Low': '黄金矿业ETF最低',
    'GDX_Close': '黄金矿业ETF收盘',
    'GDX_Adj Close': '黄金矿业ETF复权收盘',
    'GDX_Volume': '黄金矿业ETF成交量',

    'USO_Open': '原油ETF开盘',
    'USO_High': '原油ETF最高',
    'USO_Low': '原油ETF最低',
    'USO_Close': '原油ETF收盘',
    'USO_Adj Close': '原油ETF复权收盘',
    'USO_Volume': '原油ETF成交量'
}


df = df.rename(columns=col_map)

print(df.columns)
print(df.head())

df.to_csv('data_zh.csv', index=False, encoding='utf-8-sig')