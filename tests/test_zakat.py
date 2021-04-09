# -*- coding: utf-8 -*-

from pyIslam.zakat import Zakat


def test_zakat():
    zakat = Zakat()
    assert zakat.calculate_zakat(10000) == 250.0  # $


def test_zakat_harvest():
    zakat = Zakat()
    assert zakat.calculate_zakat_harvest(10000) == 500.0  # kg
    assert zakat.calculate_zakat_harvest(10000, "natural", "other") == 1000.0  # kg
