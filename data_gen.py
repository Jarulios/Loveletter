
class Data(object):

    def __init__(self, hand, deck, vision, opponent_vision, opponent_hand, handmaid_flag, focus_person,
                 max_depth=6):
        self.hand = hand
        self.deck = deck
        self.vision = vision
        self.opponent_vision = opponent_vision
        self.opponent_hand = opponent_hand
        self.handmaid_flag = handmaid_flag
        self.depth = 0
        self.max_depth = max_depth
        self.focus_person = focus_person

    def switch(self):
        self.hand, \
            self.vision, \
            self.opponent_hand, \
            self.opponent_vision = \
            self.opponent_hand, \
            self.opponent_vision, \
            self.hand, \
            self.vision
        if self.focus_person == 'player':
            self.focus_person = 'opponent'
        else:
            self.focus_person = 'player'


def countess_check(hand):
    flag1, flag2 = False, False
    for i in hand:
        if i == 5:
            flag2 = True
        elif i == 6:
            flag1 = True
        elif i == 7:
            flag2 = True
        elif i == 8:
            flag2 = True
        else:
            return False
    if flag1 and flag2:
        return True
    else:
        return False


def guard_check(hand, vision):
    flag1, flag2 = False, False
    if not vision == 0 and not vision == 1:
        flag1 = True
    if hand[0] == 1 or hand[1] == 1:
        flag2 = True
    if flag1 and flag2:
        return True
    else:
        return False


def turn(info):
    win_count = 0
    loss_count = 0
    draw_count = 0
    if not info.depth > info.max_depth:
        info.depth += 1
        if not len(current_deck) == 0:

            info.switch()
            for card in range(len(info.deck)):
                info.hand.append(info.deck[card])

                decision_flag = False
                if not info.handmaid_flag:
                    # checks for hard rules
                    if not info.vision == 0:
                        if guard_check(info.hand, info.vision):
                            if info.hand[0] == 1:
                                del info.hand[0]
                            else:
                                del info.hand[1]
                            decision_flag = True
                            win_count += 1

                        elif info.vision == 8:
                            if info.hand[0] == 5 or info.hand[1] == 5:
                                if info.hand[0] == 5:
                                    del info.hand[0]
                                else:
                                    del info.hand[1]
                                decision_flag = True
                                win_count += 1

                        elif info.hand[0] == 3:
                            if info.hand[1] > info.vision:
                                del info.hand[0]
                                decision_flag = True
                                win_count += 1
                        elif info.hand[1] == 3:
                            if info.hand[0] > info.vision:
                                del info.hand[1]
                                decision_flag = True
                                win_count += 1

                elif countess_check(info.hand):
                    if info.hand[0] == 7:
                        del info.hand[0]
                    else:
                        del info.hand[1]
                    decision_flag = True

                # plays a card
                if not decision_flag:
                    for x in (0, 1):
                        temp_hand = info.hand
                        decision = temp_hand.pop(x)
                        if info.handmaid_flag:
                            info.handmaid_flag = False

                            if decision == 4:
                                info.handmaid_flag = True

                            elif decision == 5:
                                for choice in ['self', 'opponent']:
                                    if choice == 'self':
                                        if temp_hand[0] == 8:
                                            loss_count += 1
                                        else:
                                            info.opponent_vision = 0
                                            for new_card in info.deck:
                                                info.hand = [new_card]
                                                win_count, loss_count, draw_count = turn(info)
                                    else:
                                        win_count, loss_count, draw_count = turn(info)

                            elif decision == 8:
                                loss_count += 1

                            win_count, loss_count, draw_count = turn(info)

                        else:
                            if decision == 1:
                                for guess in [2, 3, 4, 5, 6, 7, 8]:
                                    if guess == info.opponent_hand:
                                        win_count += 1
                                    else:
                                        win_count, loss_count, draw_count = turn(info)

                            elif decision == 2:
                                info.vision = info.opponent_hand
                                win_count, loss_count, draw_count = turn(info)

                            elif decision == 3:
                                if temp_hand > info.opponent_hand:
                                    win_count += 1
                                elif temp_hand < info.opponent_hand:
                                    loss_count += 1
                                else:
                                    info.vision = info.opponent_hand
                                    info.opponent_vision = temp_hand
                                    win_count, loss_count, draw_count = turn(info)

                            elif decision == 4:
                                info.handmaid_flag = True
                                win_count, loss_count, draw_count = turn(info)

                            elif decision == 5:
                                for choice in ['self', 'opponent']:
                                    if choice == 'self':
                                        if temp_hand[0] == 8:
                                            loss_count += 1
                                        else:
                                            for new_card in info.deck:
                                                temp_hand = new_card
                                                info.opponent_vision = 0
                                                win_count, loss_count, draw_count = turn(info)
                                    else:
                                        if info.opponent_hand[0] == 8:
                                            win_count += 1
                                        else:
                                            for new_card in info.deck:
                                                info.opponent_hand = new_card
                                                info.vision = 0
                                                win_count, loss_count, draw_count = turn(info)

                            elif decision == 6:
                                temp_hand, opponent_hand = info.opponent_hand, temp_hand
                                info.vision = enemy_hand
                                info.opponent_vision = temp_hand
                                win_count, loss_count, draw_count = turn(info)

                            elif decision == 8:
                                loss_count += 1
                        # end of play script
                    # end of for
                else:
                    win_count, loss_count, draw_count = turn(info)
            if info.hand > info.opponent_hand:
                win_count += 1
            elif info.hand > info.opponent_hand:
                loss_count += 1
            else:
                draw_count += 1

    info.depth -= 1
    return win_count, loss_count, draw_count


cards = [1, 2, 3, 4, 5, 6, 7, 8]
current_deck = [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]
player_hand = []
player_guard_flag = False
player_countess_drop_flag = False
player_countess_flag = False
enemy_hand = []
enemy_guard_flag = False
enemy_countess_drop_flag = False
enemy_countess_flag = False

max_run_depth = 4


# deals first hand
for player_card in current_deck:
    player_hand.append(current_deck.pop(player_card))
    for enemy_card in current_deck:
        enemy_hand.append(current_deck.pop(enemy_card))

        setup_data = Data(player_hand, current_deck, 0, 0, enemy_hand, False, 'player', max_run_depth)
        print(5*'-'+'new game'+5*'-')
        print(turn(setup_data))
