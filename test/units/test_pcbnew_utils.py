import importlib
import pcbnew
import kikit

from kikit.pcbnew_utils import duplicateZone


def testMissingSwigIteratorNext(monkeypatch):
    board = pcbnew.BOARD()
    board.Add(pcbnew.PCB_SHAPE(board))
    monkeypatch.delattr(pcbnew.SwigPyIterator, "next")

    importlib.reload(kikit)

    assert len(board.GetDrawings()) == 1


def testDuplicateZoneUsesNewSignature():
    duplicate = object()

    class BoardItem:
        def Cast(self):
            return duplicate

    class Zone:
        def Duplicate(self, addToParentGroup):
            assert addToParentGroup is False
            return BoardItem()

    assert duplicateZone(Zone()) is duplicate


def testDuplicateZoneFallsBackToOldSignature():
    duplicate = object()

    class Zone:
        def Duplicate(self):
            return duplicate

    assert duplicateZone(Zone()) is duplicate


def testDuplicateZoneCanBeAddedToZoneContainer():
    board = pcbnew.BOARD()
    zone = pcbnew.ZONE(board)
    zones = pcbnew.ZONES()

    zones.append(duplicateZone(zone))

    assert len(zones) == 1
