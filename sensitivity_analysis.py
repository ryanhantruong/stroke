from pathlib import Path
import main
from argparse import Namespace
from stroke import constants
import os
import paths
from types import SimpleNamespace

SEX_MALE = constants.Sex.MALE
SEX_FEMALE = constants.Sex.FEMALE
AGE_MIN = 75
AGE_MAX = 75
RACE_MIN = 4
RACE_MAX = 9
SYMP_MIN = 40
SYMP_MAX = 40

if __name__ == '__main__':
    # get file paths base on OS
    res_name_prefix = paths.RES_NAME_PREFIX
    hospital_path = paths.HOSPITAL_PATH
    times_path = paths.TIMES_PATH
    #s_default - 'auto' for automatic mode or else enter an integer
    s_default = 2000 #'auto'
    upper = 1

    # Input in boolean and model parameters, the rest will be taken care of by code logic
    resume = False
    resume_parameters={}
    resume_parameters["sex"] = SEX_MALE
    resume_parameters["age"] = 65
    resume_parameters["race"] = 0
    resume_parameters["symp"] = 50

    if resume:
        resume_parameters["sex_resume"] = True
        resume_parameters["age_resume"]= True
        resume_parameters["race_resume"] = True
        resume_parameters["symp_resume"] = True
    else:
        # loops wont use these parameters
        resume_parameters["sex_resume"] = False
        resume_parameters["age_resume"]= False
        resume_parameters["race_resume"]= False
        resume_parameters["symp_resume"]= False
    resume_parameters = SimpleNamespace(**resume_parameters)

    sex_list = [SEX_MALE,SEX_FEMALE]
    if resume_parameters.sex_resume & (resume_parameters.sex == SEX_FEMALE):
        sex_list = [SEX_FEMALE]
    for sex in sex_list:
        s_age = AGE_MIN
        e_age = AGE_MAX
        if resume_parameters.age_resume: s_age = resume_parameters.age
        for age in range(s_age, e_age + upper, 5):  # 30 to 85
            s_race = RACE_MIN
            e_race = RACE_MAX
            if resume_parameters.race_resume: s_race = resume_parameters.race
            for race in range(s_race, e_race + upper, 1):  # 0 to 9
                s_symp = SYMP_MIN
                e_symp = SYMP_MAX
                if resume_parameters.symp_resume: s_symp = resume_parameters.symp
                for time_since_symptoms in range(s_symp, e_symp + upper, 10):  # 10 to 100
                    sex_str = 'male' if sex==constants.Sex.MALE else 'female'
                    res_name=str(res_name_prefix/
                    f'times={times_path.stem}_hospitals={hospital_path.stem}_sex={sex_str}_age={age}_race={race}_symptom={time_since_symptoms}_nsim={s_default}_beAHA.csv')
                    args = Namespace(
                        patients=1,
                        simulations=s_default,
                        multicore=True,
                        hospital_file=str(hospital_path),
                        times_file=str(times_path),
                        sex=sex,
                        age=age,
                        race=race,
                        time_since_symptoms=time_since_symptoms,
                        res_name=res_name)
                    main.main_default_dtn(args)

                    res_name=str(res_name_prefix/
                    f'times={times_path.stem}_hospitals={hospital_path.stem}_sex={sex_str}_age={age}_race={race}_symptom={time_since_symptoms}_nsim={s_default}_afAHA.csv')
                    args = Namespace(
                        patients=1,
                        simulations=s_default,
                        multicore=True,
                        hospital_file=str(hospital_path),
                        times_file=str(times_path),
                        sex=sex,
                        age=age,
                        race=race,
                        time_since_symptoms=time_since_symptoms,
                        res_name=res_name)
                    main.main(args)

                    # if in resume modecheck off that resuming is done once loop finished
                    if resume_parameters.symp_resume & (time_since_symptoms==resume_parameters.symp):
                         resume_parameters.symp_resume = False
                if resume_parameters.race_resume & (race==resume_parameters.race):
                     resume_parameters.race_resume = False
            if resume_parameters.age_resume & (age == resume_parameters.age):
                 resume_parameters.age_resume = False
    resume = False
