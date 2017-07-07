"""
"""

class SnowmanBaseException(Exception):
    """"""

class WrongStatusCode(SnowmanBaseException):
    """"""

class LoginError(SnowmanBaseException):
    """"""

class JsonLoadError(SnowmanBaseException):
    """"""

class ContentError(SnowmanBaseException):
    """"""

class InfoContentError(SnowmanBaseException):
    """"""

class AnalysisContentError(SnowmanBaseException):
    """"""

class ProfitContentError(SnowmanBaseException):
    """"""
