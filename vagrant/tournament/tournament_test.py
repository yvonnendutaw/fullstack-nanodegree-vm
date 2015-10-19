#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def testAvoidRematches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Alice")    # ids[0]
    registerPlayer("Bob")      # ids[1]
    registerPlayer("Clive")    # ids[2]
    registerPlayer("Dave")     # ids[3]
    registerPlayer("Evan")     # ids[4]
    registerPlayer("Frank")    # ids[5]
    registerPlayer("Geo")      # ids[6]
    registerPlayer("Hank")     # ids[7]
    registerPlayer("Indingo")  # ids[8]
    registerPlayer("Jim")      # ids[9]
    registerPlayer("Kim")      # ids[10]
    registerPlayer("Lin")      # ids[11]
    registerPlayer("Mather")   # ids[12]
    registerPlayer("Nick")     # ids[13]
    registerPlayer("Oscar")    # ids[14]
    registerPlayer("Peter")    # ids[15]
    standings = playerStandings()
    ids = [row[0] for row in standings]

    # First round matches
    reportMatch(ids[6], ids[13])
    reportMatch(ids[8], ids[14])
    reportMatch(ids[15], ids[2])
    reportMatch(ids[0], ids[10])
    reportMatch(ids[12], ids[3])
    reportMatch(ids[1], ids[7])
    reportMatch(ids[5], ids[11])
    reportMatch(ids[4], ids[9])

    # Second round matches
    reportMatch(ids[3], ids[7])
    reportMatch(ids[14], ids[13])
    reportMatch(ids[10], ids[9])
    reportMatch(ids[2], ids[11])
    reportMatch(ids[1], ids[4])
    reportMatch(ids[12], ids[5])
    reportMatch(ids[0], ids[6])
    reportMatch(ids[15], ids[8])

    # Third round matches
    reportMatch(ids[11], ids[9])
    reportMatch(ids[13], ids[7])
    reportMatch(ids[5], ids[8])
    reportMatch(ids[14], ids[4])
    reportMatch(ids[6], ids[3])
    reportMatch(ids[10], ids[2])
    reportMatch(ids[1], ids[12])
    reportMatch(ids[0], ids[15])

    pairings = swissPairings()

    is_rematch = False
    for pair in pairings:
        is_rematch = check_for_rematch(pair[0], pair[2])
        if is_rematch is True:
            break

    if is_rematch is True:
        raise ValueError(
            "Pairings contained one or more rematches from previous rounds.")
    print("9. Given a tournament that would have produced a rematch, "
          "swissPairings() avoided any rematches.")


def testOddNumPlayers():
    deleteMatches()
    deletePlayers()
    registerPlayer("Alice")    # ids[0]
    registerPlayer("Bob")      # ids[1]
    registerPlayer("Clive")    # ids[2]
    registerPlayer("Dave")     # ids[3]
    registerPlayer("Evan")     # ids[4]

    standings = playerStandings()
    ids = [row[0] for row in standings]

    pairings = swissPairings()
    if pairings[0][0] != pairings[0][2] and pairings[0][3] != 'Give a Bye':
        raise ValueError(
            "First paring should be a bye with odd number of players.")

    reportMatch(ids[0])  # Give Alice a Bye
    reportMatch(ids[4], ids[1])
    reportMatch(ids[3], ids[2])

    pairings = swissPairings()
    if pairings[0][0] != pairings[0][2] and pairings[0][3] != 'Give a Bye':
        raise ValueError(
            "First paring should be a bye with odd number of players.")

    print("10. Given an odd number of players, a bye should be given "
          "to a player.")


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testAvoidRematches()
    testOddNumPlayers()
    print "Success!  All tests pass!"


