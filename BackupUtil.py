__author__ = 'InMath'
import ConfigParser


def iniconfigparser(inifilename):
    """
    :param inifilename: string
    :return: RawConfigParser
    """
    _cp = ConfigParser.ConfigParser()
    _databasef = file(inifilename)
    _cp.readfp(_databasef)
    return _cp
