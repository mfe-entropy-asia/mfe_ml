import sys
import os
sys.path.append('./createuniverse')
sys.path.append('./fourgram')
sys.path.append('./entropy')
sys.path.append('./sentiment')
from createuniverse import create_universe
from fourgram import train_and_store_model
from entropy import entropy_calc, freq_token


def first_time_run():
    os.chdir("./createuniverse")
    create_universe.run()

    os.chdir("../fourgram")
    train_and_store_model.run()

    os.chdir("../entropy")
    freq_token.run()

    os.chdir("..")


def run_global():
    os.chdir("./entropy")
    entropy_calc.run()
    os.chdir("..")


def run_tech_port():
    profile = "tech"
    os.chdir("./createuniverse")
    create_universe.create_target([
        "apple",
        "google",
        "facebook",
        "amazon",
        "microsoft",
        "netflix",
        "oracle",
        "ibm"
    ], profile)
    os.chdir("..")

    os.chdir("./entropy")
    freq_token.run(target="/targets", profile="_" + profile)
    entropy_calc.run(target="/targets", profile="_" + profile)
    os.chdir("..")


# run_global()
run_tech_port()