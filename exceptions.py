"""Кастомные исключения, генерируемые приложением"""


class NotCorrectMessage(Exception):
    """Некорректное сообщение в бот, которое не удалось распарсить"""
    pass


class NotCorrectTaskID(Exception):
    """Некорректное id задачи"""
    pass
