import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Player(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', False)
        # deduce that from Matchtype
        self.points = 0
        self.match = kwargs.get('match', None)

    def print_points(self):
        print(bcolors.OKGREEN + "You have {} points".format(self.points) + bcolors.ENDC)
        
class Match(object):
    def __init__(self):
        self.players = []
        self.mode = Matchtype()
        self.turns = 3

    def add_player(self, player):
        self.players.append(player)

    def show_players(self):
        if self.players:
            for player in self.players:
                print(player.name)

    def show_stats(self):
        if self.players:
            for player in self.players:
                print(bcolors.OKGREEN + "Player {} has {} points".format(player.name, player.points) + bcolors.ENDC)
        
    def set_matchtype(self, matchtype):
        if matchtype == 'topdown':
            self.mode = Hunt()
        else:
            raise StandardError("You want to play {}.. Can't compute".format(matchtype))

    def turn(self):
        wrong_input = True
        while wrong_input:
            inp = raw_input("How many points did you throw: ")
            try:
                inp = int(inp)
                if type(inp) is int:
                    wrong_input = False
            except:
                print(bcolors.FAIL + "Only use integers" + bcolors.ENDC)
                wront_input = True
        return inp

    def check_points(self, current_player):
        # only take players list - current_player without removing him permanently -> copy list
        players = list(self.players)
        players.remove(current_player)
        if players:
            for player in players:
                if current_player.points == player.points and player.points != 0:
                    print(bcolors.FAIL + "BOOM. Player {} resets {} to 0 points".format(current_player.name, player.name) + bcolors.ENDC)
                    player.points = 0
                    print(bcolors.WARNING + "Player {} has now {} points".format(player.name, player.points) + bcolors.ENDC)
        else:
            print("There seem to be no players left :/")
            sys.exit(1)
        
    def check_win_condition(self, current_player):
        if current_player.points == self.mode.max_points:
            print(bcolors.OKGREEN + ("winner winner chicken dinner") + bcolors.ENDC)
            print(bcolors.OKGREEN + ("Player: {} won".format(current_player.name)) + bcolors.ENDC)
            sys.exit(1)

    def check_validity_of_turn(self, current_player, points_scored, mode):
        if (current_player.points + points_scored) > mode.max_points:
            return False
        else:
            return True

    def start(self):
        for player in self.players:
            print("It's {}'s turn.".format(player.name))
            self.show_stats()

            turns = self.mode.turns
            while turns > 0:
                # depending on the throw it needs to be handled differently
                # ignoring that for now
                print("Turn # {}".format(turns))
                points_scored = self.turn()
                if self.check_validity_of_turn(player, points_scored,  player.match.mode):
                    player.points = player.points + points_scored
                    player.print_points()
                    self.check_points(player)
                    self.check_win_condition(player)
                else:
                    print(bcolors.WARNING + "You overtopped. Points won't be added." + bcolors.ENDC)
                    break
                turns = turns - 1

class Matchtype(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('matchtype', 'topdown')

    def rules(self):
        print("Dart. I'm being overwritten by my child class")

    def present_gametypes(self):
        print("1) Something else")
        print("2) Hunt")

class Hunt(Matchtype):
    def __init__(self, **kwargs):
        self.name = kwargs.get('matchtype', 'topdown')
        self.max_points = 101
        self.turns = 3

    def set_max_points(self):
        # validate generic INT/STR inputs
        self.max_points = int(raw_input(">Enter winning condition -> Points: "))

    def rules(self):
        print(bcolors.WARNING + "Reset the opponents points by throwing the same points as one of your opponents has." + bcolors.ENDC)

def add_new_players(match):
    inp = None
    while inp != 'n' or inp != 'N':
        print("To continue press N/n")
        inp = raw_input("> New player:").strip('\n')
        if inp == "n" or inp == "N":
            return match
        p = Player(name=inp, match=match)
        match.add_player(p)
        match.show_players()
    print(chr(27) + "[2J")

def select_matchtype():
    print(chr(27) + "[2J")
    match = Match()
    matchtype = Matchtype()
    matchtype.present_gametypes()
    inp = raw_input(">Select gametype: ")
    if int(inp) == 2:
        match.set_matchtype('topdown')
        match.mode.rules()
        match.mode.set_max_points()
    else:
        print("Can't handle {} right now.".format(inp))
        sys.exit()
    return match

def main():
    # supposed to be the gameloop
    match = select_matchtype()
    match = add_new_players(match)
    
    while(True):
        match.start()

main()
