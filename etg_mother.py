import time

def launch_charge(init_bn_battery_to_charge=3, p_batteries=[], charging_time=10):
    batteries = p_batteries

    print(init_bn_battery_to_charge)
    nb_battery_charged = 0
    fini = False
    while (nb_battery_charged < init_bn_battery_to_charge):
        for bat in batteries:
            for timer in [0, 100, bat.charging_time]:
                if (bat.etat < bat.max):
                    bat.etat += 1
                    percent = ((bat.etat * 100) / bat.max)
                    print(" La Batterie " + bat.label + " est charge a " + str(percent) + " % ")
                    if (bat.etat >= bat.max):
                        nb_battery_charged += 1
                        print('Batterie ' + bat.label + ' est charge')
                        if nb_battery_charged == init_bn_battery_to_charge:
                            fini = True
                            if (fini):
                                break
                    time.sleep(1)
                    if (fini):
                        break
                if (fini):
                    break
            if (fini):
                break
