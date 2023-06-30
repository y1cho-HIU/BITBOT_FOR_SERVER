import statistics

import account
import params_public as pub
import numpy as np

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

close_list = [100, 120, 90, 110]
cl = [0.4707, 0.4699, 0.4712, 0.4713, 0.4699, 0.4697, 0.4694, 0.4695, 0.4705, 0.4711, 0.4706]
npcl = np.array(cl)
print(statistics.stdev(cl))

print(npcl.std())