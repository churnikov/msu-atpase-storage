from enum import Enum
from typing import Tuple
from aiogram import types as aiotypes
from .types_ import Device, Protocol, Organism, TodayOrNot
import random as rnd

def get_device_kb() -> Tuple[str, aiotypes.ReplyKeyboardMarkup]:
    """"
    Возвращает клавиатуру для выбора прбора
    """
    
    reply_kb_cols = make_table_output(Device)

    text_reply = 'На каком приборе были получены эти данные?'

    return text_reply, reply_kb_cols

def get_protocol_kb() -> Tuple[str, aiotypes.ReplyKeyboardMarkup]:
    """"
    Возвращает клавиатуру для выбора протокола
    """
    
    reply_kb_cols = make_table_output(Protocol)

    text_reply = 'Какого типа протокол был использован?'

    return text_reply, reply_kb_cols

def get_organism_kb() -> Tuple[str, aiotypes.ReplyKeyboardMarkup]:
    """"
    Возвращает клавиатуру для выбора организма
    """
    
    reply_kb_cols = make_table_output(Organism)
    
    text_reply = 'Из какого организма взяты образцы?'

    return text_reply, reply_kb_cols    

def was_run_this_day() -> Tuple[str, aiotypes.ReplyKeyboardMarkup]:
    """"
    Возвращает клавиатуру для ответа, сегодня проходило измрние или нет
    """
    
    reply_kb_cols = make_table_output(TodayOrNot, 2)
    
    text_reply = 'Измерение проходило сегодня?'

    return text_reply, reply_kb_cols    

def make_table_output(vals: Enum, ncol:int=3):
    reply_kb = aiotypes.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    butttons_list = []
    for num, col_val in enumerate(vals, 1):
        btn_1 = aiotypes.KeyboardButton(col_val.value)
        butttons_list.append(btn_1)
        if num%ncol == 0:
            reply_kb.row(*butttons_list)
            butttons_list = []
    if len(butttons_list) != 0:
        reply_kb.row(*butttons_list)
    return reply_kb