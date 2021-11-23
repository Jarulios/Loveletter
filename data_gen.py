
def countess_check(hand):
    flag1, flag2 = False, False
    for i in hand:
        if i == 5:
            flag2 = True
        elif i == 7:
            flag1 = True
        elif i == 8:
            flag2 = True
        elif i == 6:
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


def turn(hand, deck, vision, opponent_vision, opponent_hand, handmaid_flag, turn_win_count, turn_loss_count,
         turn_draw_count, current_depth, max_depth=6):
    print('new turn')
    if not depth > max_depth:
        if not len(current_deck) == 0:

            temp_deck = deck
            for card in range(len(deck)):
                hand.append(temp_deck.pop(card))

                decision_flag = False

                if not handmaid_flag:
                    # checks for hard rules
                    if not vision == 0:
                        if guard_check(hand, vision):
                            if hand[0] == 1:
                                del hand[0]
                            else:
                                del hand[1]
                            decision_flag = True
                            turn_win_count += 1

                        elif vision == 8:
                            if hand[0] == 5 or hand[1] == 5:
                                if hand[0] == 5:
                                    del hand[0]
                                else:
                                    del hand[1]
                                decision_flag = True
                                turn_win_count += 1

                        elif hand[0] == 3:
                            if hand[1] > vision:
                                del hand[0]
                                decision_flag = True
                                turn_win_count += 1
                        elif hand[1] == 3:
                            if hand[0] > vision:
                                del hand[1]
                                decision_flag = True
                                turn_win_count += 1

                elif countess_check(hand):
                    if hand[0] == 7:
                        del hand[0]
                    else:
                        del hand[1]
                    decision_flag = True

                # plays a card
                if not decision_flag:
                    for x in (0, 1):
                        temp_hand = hand
                        print(hand)
                        print(x)
                        decision = temp_hand.pop(x)
                        if handmaid_flag:
                            handmaid_flag = False
                            print('handmaid')
                            print(decision)

                            if decision == 4:
                                handmaid_flag = True

                            elif decision == 5:
                                for choice in ['self', 'opponent']:
                                    if choice == 'self':
                                        if temp_hand[0] == 8:
                                            turn_loss_count += 1
                                        else:
                                            for new_card in temp_deck:
                                                temp_hand = [new_card]
                                                opponent_vision = 0
                                                temp_hand, vision, turn_win_count, opponent_hand, opponent_vision, \
                                                    turn_loss_count = opponent_hand, opponent_vision, turn_loss_count, \
                                                    temp_hand, vision, turn_win_count
                                                current_depth += 1
                                                turn(temp_hand, deck, vision, opponent_vision, opponent_hand,
                                                     turn_win_count, turn_loss_count, turn_draw_count, depth, max_depth)
                                                current_depth -= 1
                                    temp_hand, vision, turn_win_count, opponent_hand, opponent_vision, turn_loss_count \
                                        = opponent_hand, opponent_vision, turn_loss_count, temp_hand, vision, \
                                        turn_win_count
                                    current_depth += 1
                                    turn(temp_hand, deck, vision, opponent_vision, opponent_hand, turn_win_count,
                                         turn_loss_count, turn_draw_count, depth, max_depth)
                                    current_depth -= 1

                            elif decision == 8:
                                turn_loss_count += 1

                            temp_hand, vision, turn_win_count, opponent_hand, opponent_vision, turn_loss_count = \
                                opponent_hand, opponent_vision, turn_loss_count, temp_hand, vision, turn_win_count
                            current_depth += 1
                            turn(temp_hand, deck, vision, opponent_vision, opponent_hand, turn_win_count,
                                 turn_loss_count, turn_draw_count, depth, max_depth)
                            current_depth -= 1

                        else:
                            if decision == 1:
                                for guess in [2, 3, 4, 5, 6, 7, 8]:
                                    if guess == opponent_hand:
                                        turn_win_count += 1
                                    else:
                                        temp_hand, vision, turn_win_count, opponent_hand, opponent_vision, \
                                            turn_loss_count = opponent_hand, opponent_vision, turn_loss_count, \
                                            temp_hand, vision, turn_win_count
                                        current_depth += 1
                                        turn(temp_hand, deck, vision, opponent_vision, opponent_hand, turn_win_count,
                                             turn_loss_count,
                                             turn_draw_count, depth, max_depth)
                                        current_depth -= 1

                            elif decision == 2:
                                vision = opponent_hand
                                temp_hand, vision, turn_win_count, opponent_hand, opponent_vision, turn_loss_count = \
                                    opponent_hand, opponent_vision, turn_loss_count, temp_hand, vision, turn_win_count
                                current_depth += 1
                                turn(temp_hand, deck, vision, opponent_vision, opponent_hand, turn_win_count,
                                     turn_loss_count,
                                     turn_draw_count, depth, max_depth)
                                current_depth -= 1

                            elif decision == 3:
                                if temp_hand > opponent_hand:
                                    turn_win_count += 1
                                elif temp_hand < opponent_hand:
                                    turn_loss_count += 1
                                else:
                                    vision = opponent_hand
                                    opponent_vision = temp_hand
                                    temp_hand, vision, turn_win_count, opponent_hand, opponent_vision, turn_loss_count \
                                        = opponent_hand, opponent_vision, turn_loss_count, temp_hand, vision, \
                                        turn_win_count
                                    current_depth += 1
                                    turn(temp_hand, deck, vision, opponent_vision, opponent_hand, turn_win_count,
                                         turn_loss_count, turn_draw_count, depth, max_depth)
                                    current_depth -= 1

                            elif decision == 4:
                                handmaid_flag = True
                                temp_hand, vision, turn_win_count, opponent_hand, opponent_vision, turn_loss_count = \
                                    opponent_hand, opponent_vision, turn_loss_count, temp_hand, vision, turn_win_count
                                current_depth += 1
                                turn(temp_hand, deck, vision, opponent_vision, opponent_hand, turn_win_count,
                                     turn_loss_count, turn_draw_count, depth, max_depth)
                                current_depth -= 1

                            elif decision == 5:
                                for choice in ['self', 'opponent']:
                                    if choice == 'self':
                                        if temp_hand[0] == 8:
                                            turn_loss_count += 1
                                        else:
                                            for new_card in temp_deck:
                                                temp_hand = new_card
                                                opponent_vision = 0
                                                temp_hand, vision, turn_win_count, opponent_hand, opponent_vision, \
                                                    turn_loss_count = opponent_hand, opponent_vision, turn_loss_count, \
                                                    temp_hand, vision, turn_win_count
                                                current_depth += 1
                                                turn(temp_hand, deck, vision, opponent_vision, opponent_hand,
                                                     turn_win_count, turn_loss_count, turn_draw_count, depth, max_depth)
                                                current_depth -= 1
                                    else:
                                        if opponent_hand[0] == 8:
                                            turn_win_count += 1
                                        else:
                                            for new_card in temp_deck:
                                                opponent_hand = new_card
                                                vision = 0
                                                temp_hand, vision, turn_win_count, opponent_hand, opponent_vision, \
                                                    turn_loss_count = opponent_hand, opponent_vision, turn_loss_count, \
                                                    temp_hand, vision, turn_win_count
                                                current_depth += 1
                                                turn(temp_hand, deck, vision, opponent_vision, opponent_hand,
                                                     turn_win_count, turn_loss_count, turn_draw_count, depth, max_depth)
                                                current_depth -= 1

                            elif decision == 6:
                                temp_hand, opponent_hand = opponent_hand, temp_hand
                                vision = enemy_hand
                                opponent_vision = temp_hand
                                temp_hand, vision, turn_win_count, opponent_hand, opponent_vision, turn_loss_count = \
                                    opponent_hand, opponent_vision, turn_loss_count, temp_hand, vision, turn_win_count
                                current_depth += 1
                                turn(temp_hand, deck, vision, opponent_vision, opponent_hand, turn_win_count,
                                     turn_loss_count, turn_draw_count, depth, max_depth)
                                current_depth -= 1

                            elif decision == 8:
                                turn_loss_count += 1
                        # end of play script
                    # end of for
                else:
                    hand, vision, turn_win_count, opponent_hand, opponent_vision, turn_loss_count = \
                        opponent_hand, opponent_vision, turn_loss_count, hand, vision, turn_win_count
                    current_depth += 1
                    turn(hand, deck, vision, opponent_vision, opponent_hand, turn_win_count, turn_loss_count,
                         turn_draw_count, depth, max_depth)
                    current_depth -= 1

    return turn_win_count, turn_loss_count


cards = [1, 2, 3, 4, 5, 6, 7, 8]
current_deck = [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]
player_hand = []
player_vision = 0
player_guard_flag = False
player_countess_drop_flag = False
player_countess_flag = False
enemy_hand = []
enemy_vision = 0