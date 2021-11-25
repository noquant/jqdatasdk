# -*- coding: utf-8 -*-

from __future__ import print_function

from jqdatasdk import opt, finance, macro, bond, sup, query


def test_opt():
    df = opt.run_query(query(opt.OPT_CONTRACT_INFO).limit(6).offset(20000))
    print(df)
    assert len(df) == 6
    assert df.iloc[-1, 0] >= 20000  # id 列
    assert df["code"].tolist() == [
        'C2101-C-2780.XDCE', 'C2101-C-2800.XDCE', 'C2101-C-2820.XDCE',
        'C2101-C-2840.XDCE', 'C2101-P-2780.XDCE', 'C2101-P-2800.XDCE'
    ]
    df = df.set_index("code").drop("id", axis=1)
    item = df.loc["C2101-C-2800.XDCE"]
    assert item["name"] == "玉米购1月2800"
    assert item.underlying_symbol == "C2101.XDCE"
    assert str(item.delist_date) == "2020-12-08"


def test_fin():
    q = query(finance.FINANCE_BALANCE_SHEET).limit(5).offset(100)
    df = finance.run_query(q)
    print(df)
    assert len(df) == 5
    assert set(df["company_id"]) == {300002081}
    assert set(df["code"]) == {"601166.XSHG"}
    assert df["report_type"].iloc[0] == 1 and df["report_type"].iloc[4] == 0


def test_macro():
    df = macro.run_query(query(macro.MAC_AREA_DIV).limit(5).offset(1000))
    print(df)
    assert len(df) == 5
    assert df["area_code"].tolist() == ['330101', '330102', '330103', '330104', '330105']
    assert set(df["province_name"]) == {"浙江省"}
    assert set(df["city_name"]) == {"杭州市"}


def test_bond():
    df = bond.run_query(query(bond.BOND_BASIC_INFO).limit(10))
    print(df)
    assert len(df) == 10
    df = df.set_index("code").drop("id", axis=1)
    item = df.loc["131801"]
    assert item.short_name == "花呗01A1" and str(item.maturity_date) == "2017-06-15"
    item = df.loc["131811"]
    assert item.short_name == "R-002" and item.maturity_date is None


def test_sup():
    df = sup.run_query(query(sup.STK_FINANCE_SUPPLEMENT).limit(10))
    print(df)
    assert len(df) == 10
    assert set(df["company_id"]) == {300000062}
    assert set(df["code"]) == {"002054.XSHE"}
    assert df["report_type"].iloc[3] == 1 and df["report_type"].iloc[8] == 0
