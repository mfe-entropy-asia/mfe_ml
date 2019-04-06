import sys
import os
sys.path.append('./createuniverse')
sys.path.append('./fourgram')
sys.path.append('./entropy')
sys.path.append('./sentiment')
from createuniverse import create_universe
from fourgram import train_and_store_model
from entropy import entropy_calc, freq_token


os.chdir("./createuniverse")
# create_universe.run()

os.chdir("../fourgram")
# train_and_store_model.run()

os.chdir("../entropy")
freq_token.run()
entropy_calc.run()

