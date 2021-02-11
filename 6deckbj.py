import random
global bet
global bank
global d_hand
global p_hand
global d_val
global p_val
global insbet
global split
global ace11
bank = 0
deck = ['K','Q','J','T','9','8','7','6','5','4','3','2','A']*4
shoe = deck*6
discard = []
pencards = []
bet = 0


def setup():        # shuffle and penetration
    random.shuffle(shoe)

    while len(shoe) > 273:      # Penetration is a gratuitous .75 cut (39 cards)
        pen = random.choice(shoe)
        pencards.append(pen)
        shoe.remove(pen)
    return shoe


def bank():     #safeguard
    global bank
    if bank <= 0:
        return buyin()


def buyin():        # buy in
    global bank
    x = input("Buy in: ")
    try:
        x = int(x)
        if x == int(x):
            x = int(x)
            if x > 0:
                bank =+ x
           
            else:
                print("Oops!")
                return buyin()
    except ValueError:
        try:
            x = str(x)
            if x == str(x):
                x = str(x)
                ## buy in exit
                return buyin()
        except ValueError:
            return buyin()


def p_drawcheck():      #drawcheck ---- # aces need to be fixed
                        # ex: 4A = 15, 4AA = 16, 4AA7 = 13, != 23
    global p_val
    global draw
    global ace11
    draw = random.choice(shoe)
    p_hand.append(draw)
    shoe.remove(draw)
    discard.append(draw)

    if draw == 'K' or draw == 'Q' or draw == 'J' or draw == 'T':
        p_val += 10
    if draw == '9':
        p_val += 9
    if draw == '8':
        p_val += 8
    if draw == '7':
        p_val += 7
    if draw == '6':
        p_val += 6
    if draw == '5':
        p_val += 5
    if draw == '4':
        p_val += 4
    if draw == '3':
        p_val += 3
    if draw == '2':
        p_val += 2
    if draw == 'A':
        if 'A' in p_hand and p_val <= 10:
            p_val += 11
        else:
            p_val += 1

    if p_val > 21 and 'A' in p_hand and ace11==True:
        p_val -= 10
        ace11==False
            
                
        

def d_drawcheck():
    global d_val
    global draw
    global ace11
    draw = random.choice(shoe)
    d_hand.append(draw)
    shoe.remove(draw)
    discard.append(draw)
    
    if draw == 'K' or draw == 'Q' or draw == 'J' or draw == 'T':
        d_val += 10
    if draw == '9':
        d_val += 9
    if draw == '8':
        d_val += 8
    if draw == '7':
        d_val += 7
    if draw == '6':
        d_val += 6
    if draw == '5':
        d_val += 5
    if draw == '4':
        d_val += 4
    if draw == '3':
        d_val += 3
    if draw == '2':
        d_val += 2
    if draw == 'A':
        if 'A' in d_hand and d_val <= 10:
            d_val += 11
        else:
            d_val += 1


    if d_val > 21 and d_hand.count('A') >= 2 and ace11==True:
        d_val -= 11
        ace11==False


# 1 or 2 hands
##def hands():
##    x = input("(1) or (2) hands?")
##    try:
##        x = int(x)
##        if x == int(x):
##            x == int(x)
##            if x == 1:
##                return round1()
##            elif x == 2:
##                return round2()
##    except ValueError:
##        print("[Exit]")


def bet1():     # single hand bet
    global bet
    global bank
    if bank > 0:
        print("Chips: $" + str(bank))
        x = input("Bet: ")
        try:
            x = float(x)
            if x == float(x):
                x = float(x)
                if x <= bank:
                    bet += x
                else:
                    return buyin()
        except ValueError:
            try:
                x = str(x)
                if x == str(x):
                    x == str(x)
                    if x == 'b':
                        print("Bet amount: " +str(bet))
                        return bet1()
                    else:
                        return bet1()
            except ValueError:
                print("Enter a valid bet or 'b' to view bet amount.")
                return bet1()

    elif bank <= 0:
        return buyin()
                

def dealer():       # dealer upcard, insurance, 'T' blackjack, last hand after pentration card #untested
    global draw
    global d_hand
    d_hand = []  
    global d_val
    d_val = 0
    
    for i in range(2):

        if len(shoe) > 0:
            d_drawcheck()

        elif len(pencards) == 0:
            print("Shoe over. gg.")
            #return outro()
        
        elif len(shoe) == 0:
            shoe.append(pencards)
            print("Last hand.")
            d_drawcheck()

    upcard = [d_hand[0]]
    print("Dealer Upcard: " + str(upcard))
    
    
def player():       # player hand/decision
    global draw
    global p_hand
    global p_val
    p_hand = []
    p_val = 0
            
    for i in range(2):
        p_drawcheck()
    print("Hand: " + str(p_hand))
    

def insurance():        # insurance and "T" upcard dealer blackjacks
    global d_val
    global p_val
    global bet
    global insbet
    global bank
    insbet = (bet)/2
    ins=False
    
    #Dealer Ace w/o player blackjack
    if ins==False and d_hand[0] == "A":
        if p_val == 21:
            x = input("Even Money? y/n: ")
            try:
                x = str(x)
                if x == str(x):
                    x = str(x)
                    if x == 'y':
                        bank += bet
                        print("Dealer Hand: " + str(d_hand))
                        print("You win " + str(bet) + "!")
                        bet = 0
                        return orbit()
                    elif x == 'n':
                        if d_val == 21:
                            print("Dealer Blackjack. Push.")
                            return orbit()
                        elif d_val < 21:
                            print("Player Blackjack pays out 3 to 2!")
                            bj = (3/2)*(sum(bet))
                            bank += float(bj)
                            print("You win " + str(bj) + "!")
                            bet = 0
                            return orbit()
            except ValueError:
                return x

        elif p_val < 21:
            x = input("Insurance? y/n: ")
            try:
                x = str(x)
                if x == str(x):
                    x == str(x)
                    if x == 'y':
                        if sum(bank) > insbet:
                            ins=True
                        else:
                            buyin()
                            return insurance()
                    elif x == 'n':
                        ins=False
                        if d_val == 21:
                            bank -= bet
                            print("Dealer Blackjack.")
                            print("You lose -" + str(bet))
                            bet = 0
                            return orbit()
                        elif d_val < 21:
                            print("Don't have it.")
                            print("Dealer Upcard: " + str(d_hand[0]))
                            print("Hand: " + str(p_hand))
                            return decision1()
                        
            except ValueError:
                try:
                    x = int(x)
                    if x == int(x):
                        return insurance()
                except ValueError:
                    return insurance()
        
                
    elif ins==True and d_hand[0] == "A":
        if d_val == 21:
            print("Dealer Blackjack. Insurance pays 2 to 1.")
            return orbit()

        elif d_val < 21:
            insbet -= bank
            insbet = 0
            return decision1()

    elif d_hand[0] == "A" and ins==False:
        if d_val == 21:
            bank -= bet
            print("Dealer Blackjack.")
            print("House takes " + str(bet))
            bet = 0
            return orbit()

    elif d_val == 21 and p_val < 21:
        print("Dealer blackjack." + str(d_hand))
        bank -= bet
        bet = 0
        return orbit()

    elif d_val < 21 and p_val < 21:
        return decision1()

    elif d_val < 21 and p_val == 21:
        print("Blackjack!")
        bj = (3/2)*bet
        bank += bj
        bet = 0
        return orbit()


def p_hit():
    global p_val
    global draw
    p_drawcheck()
    print("Hand: " + str(p_hand))
    print("[test] p_val: " + str(p_val)) ## test


def d_hit():
    global d_val
    global draw
    d_drawcheck()
    return d_val and stand()


def stand():
    global bet
    global bank
    global d_val
    global p_val
    global dub
    global d
    dub=False
    print("Dealer Hand: " + str(d_hand))
    print('[test] d_val: ' + str(d_val)) ## test
    
    while d_val < 17:
        d_hit()
    
    if d_val > 21:
        if dub==True:
            bank += d
            print("Dealer bust! +" + str(d))
            dub==False
            return orbit()
        else:
            bank += bet
            print("Dealer bust! +" + str(bet))
            bet = 0
            return orbit()
    elif d_val > p_val and d_val <= 21:
        if dub==True:
            print("Dealer wins. -" + str(d))
            bank -= d
            bet = 0
            dub==False
            return orbit()
        else:
            print("Dealer wins. -" + str(bet))
            bank -= bet
            bet = 0
            return orbit()
    elif p_val > d_val:
        if dub==True:
            print("You win! +" + str(d))
            bank += d
            bet = 0
            dub==False
            return orbit()
        else:
            print("You win! +" + str(bet))
            bank += bet
            bet = 0
            return orbit()
    elif p_val == d_val:
        print("Push.")
        bet = 0
        return orbit()


def surrender():
    global p_hand
    global bet
    global bank
    if len(p_hand) <= 2:
        u = bet/2
        bank -= u
        print("Surrender. Dealer hand: " + str(d_hand))
        bet = 0
        return orbit()
    else:
        print("Can only surrender with first two cards.")
        return decision1()

# def split(): # build in with two hand function


def doub():
    global bet
    global bank
    global p_val
    global dub
    d = bet*2
    if bank > d:
        p_hit()
        if p_val > 21:
            print("Bust!")
            print("Dealer Hand: " + str(d_hand))
            bank -= d
            bet = 0
            dub=False
            return orbit()
        else:
            return dub==True and stand()
            
def decision1():
    global bet
    global bank
    global d_val
    global p_val
    
    x = input("(h)it, (s)tand, s(u)rrender, sp(l)it, (d)ouble down: ")
    try:
        x = str(x)
        if x == str(x):
            x == str(x)
            if x == 'h':        #hit 
                p_hit()
                if p_val > 21:
                    print("Bust!")
                    print("Dealer hand: " + str(d_hand))
                    bank -= bet
                    bet = 0
                    return orbit()
                else:
                    return decision2()
            elif x == 's':      #stand
                stand()
                
            elif x == 'u':      #surrender
                surrender()
                
            # elif x == 'l': # split
                # split()

            elif x == 'd':      # double down
                doub()
                
    except ValueError:
        return decision1()


def decision2():
    global bet
    global bank
    global d_val
    global p_val
    
    x = input("(h)it or (s)tand: ")
    
    try:
        x = str(x)
        if x == str(x):
            x == str(x)
            if x == 'h':
                p_hit()
                if p_val > 21:
                    print("Bust!")
                    print("Dealer hand: " + str(d_hand))
                    bank -= bet
                    bet = 0
                    return orbit()
                else:
                    return decision2()
            elif x == 's':
                stand()
                    
    except ValueError:
        return decision2()


def orbit(): # one hand round
    global ace11
    ace11=True
    bet1()
    dealer()
    player()
    insurance()


def game():     #self explanatory
    setup()
    buyin()
    orbit()

game()
