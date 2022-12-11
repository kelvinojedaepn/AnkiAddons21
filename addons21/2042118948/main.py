#!/usr/bin/env python3

# Copyright: Tobias Haupenthal
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
###############################################################################

import sys
from pathlib import Path

# noinspection PyUnresolvedReferences
import aqt.utils as ankiutils
# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import QAction
# noinspection PyUnresolvedReferences
from aqt import mw, utils

from .Papercard import IntendedException
from .Papercard import Papercard


def get_cards(deck: str):
    ids = mw.col.findCards('deck:"' + str(deck) + '"')
    questions = []
    answers = []
    for i in ids:
        card = mw.col.getCard(i)
        questions.append(card.q())
        answers.append(card.a())
    return questions, answers


def export_papercards():
    version = (Path(__file__).parent / 'VERSION').read_text()
    deck = mw.col.decks.current()['name']
    cards = get_cards(deck)
    try:
        papercard = Papercard.get_instance(utils, mw.addonManager, Path(mw.col.media.dir()))
        papercard.export_paper(deck, cards)
    except IntendedException as e1:
        ankiutils.showCritical('<b>Papercards Plugin Exception (V:{})</b><br/>\n {}'.format(version, e1))
    # noinspection PyBroadException
    except Exception as e2:
        msg = 'Papercards Plugin Exception (V:{})\n'.format(version)
        msg += '<class \'{}\'>: {}'.format(type(e2).__name__, e2)
        raise Exception(msg).with_traceback(sys.exc_info()[2])


action = QAction("Export to papercards", mw)
# noinspection PyUnresolvedReferences
action.triggered.connect(export_papercards)
mw.form.menuTools.addAction(action)
