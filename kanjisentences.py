# -*- coding: utf-8 -*-
import unicodedata
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

_ignore = set(
    u"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" +
    u"ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ" +
    u"ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ" +
    u"1234567890１２３４５６７８９０" +
    u"あいうゔえおぁぃぅぇぉかきくけこがぎぐげごさしすせそざじずぜぞ" +
    u"たちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽ" +
    u"まみむめもやゃゆゅよょらりるれろわをんっ" +
    u"アイウヴエオァィゥェォカキクケコガギグゲゴサシスセソザジズゼゾ" +
    u"タチツテトダヂヅデドナニヌネノハヒフヘホバビブベボパピプペポ" +
    u"マミムメモヤャユュヨョラリルレロワヲンッ" +
    u"!\"$%&'()|=~-^@[;:],./`{+*}<>?\\_" +
    u"＠「；：」、。・‘｛＋＊｝＜＞？＼＿！”＃＄％＆’（）｜＝．〜～ー" +
    u"☆★＊○●◎〇◯“…『』#♪ﾞ〉〈→》《π×")


# returns true is the card is not new
def isKnownCard(card):
    return card.type > 0


# returns true if a given character is kanji
def isKanji(ch):
    if ch in _ignore:
        return False
    try:
        return unicodedata.name(ch).find('CJK UNIFIED IDEOGRAPH') >= 0
    except ValueError:
        return False


class KanjiSentences:
    def __init__(self, mw):
        if mw:
            self.suspendAction = QAction(
                "Suspend sentences with unknown kanji", mw
            )
            self.unsuspendAction = QAction(
                "Unsuspend sentences with known kanji", mw
            )
            mw.connect(
                self.suspendAction, SIGNAL("triggered()"), self.suspendUnknown
            )
            mw.connect(
                self.unsuspendAction, SIGNAL("triggered()"), self.unsuspendKnown
            )
            mw.form.menuTools.addSeparator()
            mw.form.menuTools.addAction(self.suspendAction)
            mw.form.menuTools.addAction(self.unsuspendAction)

    def suspendUnknown(self):
        knownKanji = self.knownKanji()
        idsToSuspend = list()

        cardIds = mw.col.db.list("select id from cards")
        for id, i in enumerate(cardIds):
            card = mw.col.getCard(i)
            if card.queue >= 0:
                keys = card.note().keys()
                expressionField = None
                for s, key in ((key.lower(), key) for key in keys):
                    if s.strip().lower() == "expression":
                        expressionField = card.note()[key]
                        break
                if expressionField is not None:
                    for ch in expressionField:
                        if ch in _ignore or not isKanji(ch):
                            continue
                        if ch not in knownKanji:
                            idsToSuspend.append(i)
                            break
        mw.col.sched.suspendCards(idsToSuspend)
        mw.reset()
        showInfo("Suspended {num} cards!".format(num=len(idsToSuspend)))

    def unsuspendKnown(self):
        knownKanji = self.knownKanji()
        idsToUnsuspend = list()

        cardIds = mw.col.db.list("select id from cards")
        for id, i in enumerate(cardIds):
            card = mw.col.getCard(i)
            if card.queue == -1:
                keys = card.note().keys()
                expressionField = None
                for s, key in ((key.lower(), key) for key in keys):
                    if s.strip().lower() == "expression":
                        expressionField = card.note()[key]
                        break
                if expressionField is not None:
                    unsuspend = True
                    for ch in expressionField:
                        if ch in _ignore or not isKanji(ch):
                            continue
                        if ch not in knownKanji:
                            unsuspend = False
                            break
                    if unsuspend is True:
                        idsToUnsuspend.append(i)
        mw.col.sched.unsuspendCards(idsToUnsuspend)
        mw.reset()
        showInfo("Unsuspended {num} cards!".format(num=len(idsToUnsuspend)))

    def knownKanji(self):
        knownKanji = set()

        cardIds = mw.col.db.list("select id from cards")
        for id, i in enumerate(cardIds):
            card = mw.col.getCard(i)
            if isKnownCard(card):
                keys = card.note().keys()
                kanjiField = None
                for s, key in ((key.lower(), key) for key in keys):
                    if s.strip().lower() == "kanji":
                        kanjiField = card.note()[key]
                        break
                if kanjiField is not None:
                    for kanji in kanjiField:
                        knownKanji.add(kanji)
        return knownKanji


if __name__ != "__main__":
    # Save a reference to the toolkit onto the mw, preventing garbage collection
    # of PyQT objects
    if mw:
        mw.kanjiSentences = KanjiSentences(mw)
else:
    print("This is a plugin for the Anki Spaced Repetition learning system and"
          "cannot be run directly.")
    print("Please download Anki2 from <http://ankisrs.net/>")
