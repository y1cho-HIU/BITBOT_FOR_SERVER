import account
import params_public as pub

myAccount = account.MockAccount()


def test_pos_in(position, price):
    myAccount.pos_in(position, price)
    myAccount.display_state()


def test_pos_out(price):
    myAccount.pos_out(price)
    myAccount.display_state()


test_pos_in(pub.POS_LONG, 100)
test_pos_out(500)
test_pos_in(pub.POS_SHORT, 50)
test_pos_out(40)
myAccount.display_win_rate()