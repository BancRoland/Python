import numpy as np
from dataclasses import dataclass, field
import sys
import os
home_directory = os.path.expanduser("~")
sys.path.append(home_directory+"/Desktop/Python/math/matrices/Rodrigues_rot")

import banc_vectorManip as vMp
import matplotlib.pyplot as plt
import csv_read
from utils import *




if __name__:


    observ = madrid_obs
    observ = budapest_obs
    observ = madrid_obs
    observ = oslo_obs
    observ = quito_obs
    observ_list = [madrid_obs,
                   budapest_obs,
                   madrid_obs,
                   oslo_obs,
                   quito_obs]
    
    time_list = [time_format(date=0),
                 time_format(date=90),
                 time_format(date=180),
                 time_format(date=270)]

    get_simple_azimuth_elevation = False
    if get_simple_azimuth_elevation:
        for obs in observ_list:
            for date in time_list:

                azim_list=[]
                elev_list=[]
                time_x = np.arange(0,86400,60)
                for s in time_x:
                    time = date + time_format.get_date_from_sec(s)
                    azel = get_sun_pos_in_horizontal_coordinates__wiki(time,obs)
                    azim_list.append(azel.azimuth.as_float())
                    elev_list.append(azel.elevation.as_float())
                plt.xticks(range(0,25,1))
                plt.yticks(range(-90,360,30))

                plt.plot(time_x/3600,azim_list,label="azimuth")
                plt.plot(time_x/3600,elev_list,label="elevation")
                plt.legend()
                plt.grid()
                plt.axvline(12,linestyle = "--",alpha=0.5, color = "black")
                plt.axhline(0,linestyle = "--",alpha=0.5, color = "black")
                plt.title(f"Sun azimuth and elevation from {obs.name} at {date}")
                plt.xlabel("time [hour]")
                plt.ylabel("angle [degree]")
                plt.ylim([-90,360])
                plt.savefig(f"sun_pos_day_{obs.name}_at_{date}.png")
                plt.close()
                # plt.show()



    if 0:
        recta_list = []
        decli_list = []
        for d in range(0,360,1):
            time = time_format(date=d)
            A = get_sun_pos_in_equatorial_coordinates__adjustable_ecliptic_lon(time)
            recta_list.append((A.rectascense.as_float()+360)%360)
            decli_list.append(A.declination.as_float())

        plt.plot(recta_list,decli_list,"o-")
        plt.grid()
        plt.show()

    if 0:
        for d in range(0,360,10):
            elev_list=[]
            azim_list=[]
        
            time_of_day_list=[]
            for h in range(0,24,1):
                for m in range(0,60,60):
                    time = time_format(date=d, hour=h, min=m)
                    time_of_day = time_format(hour=h, min=m)
                    time_of_day_list.append(time_of_day.get_sec_from_date()/3600)
                    # print(f"\n\nhour = {h}")
                    A = get_sun_pos_in_equatorial_coordinates__adjustable_ecliptic_lon(time)
                    # A.print()
                    B = equat_2_horiz(A,time, observ)
                    # B.print()
                    # plt.scatter(A.rectascense_deg, A.declination_deg)
                    azim_list.append((B.azimuth.as_float()+360)%360)
                    elev_list.append(B.elevation.as_float())


                    # plt.scatter(B.azimuth,B.elevation,color="C0")
            # plt.plot(azim_list,elev_list,"o-")
            plt.plot(time_of_day_list,elev_list,"o-")
            plt.axvline(12)

            print(d)
        # plt.title(f"day={d}")
        plt.grid()
        plt.show()


    observ = budapest_obs

    def function_horizontal__wiki(time: time_format) -> float:
        return get_sun_pos_in_horizontal_coordinates__wiki(time, observ).elevation.as_float()
    
    def function_horizontal__naive(time: time_format) -> float:
        return get_sun_pos_in_horizontal_coordinates__adjustable_ecliptic_lon(time, observ).elevation.as_float()
    
    def function_equatorial__wiki(time: time_format)->float:
        return get_sun_pos_in_equatorial_coordinates__wiki(time).declination.as_float()

    def function_equatorial__naive(time: time_format)->float:
        return get_sun_pos_in_equatorial_coordinates__adjustable_ecliptic_lon(time).declination.as_float()



    # test_time_sunrise = time_format(date=-80, hour=6).get_day_from_time()
    # time_span = time_format(hour=6)
    # time_resolution = time_format(min=1)
    # function = function_horizontal__wiki

    # sunrise_time_hour = find_zero_crossing_time(function, test_time_sunrise, time_span, time_resolution).get_day_from_time()


          



    rise_and_set_times = True
    if rise_and_set_times:

        fall_equinox__wiki = find_zero_crossing_time(function_equatorial__wiki,test_time=time_format(date=2*180),time_span=time_format(date=90))
        spring_equinox__wiki = find_zero_crossing_time(function_equatorial__wiki,test_time=time_format(date=180),time_span=time_format(date=90))
        prev_spring_equinox__wiki = find_zero_crossing_time(function_equatorial__wiki,test_time=time_format(date=0),time_span=time_format(date=90))
        
        fall_equinox__naive = find_zero_crossing_time(function_equatorial__naive,test_time=time_format(date=2*180),time_span=time_format(date=90))
        spring_equinox__naive = find_zero_crossing_time(function_equatorial__naive,test_time=time_format(date=180),time_span=time_format(date=90))
        prev_spring_equinox__naive = find_zero_crossing_time(function_equatorial__naive,test_time=time_format(date=0*180),time_span=time_format(date=90))


        print("summer_solstice__wiki")
        summer_solstice__wiki = find_extreme_value_time(function_equatorial__wiki,test_time=time_format(date=90),time_span=time_format(date=45),type="max")
        print("winter_solstice__wiki")
        winter_solstice__wiki = find_extreme_value_time(function_equatorial__wiki,test_time=time_format(date=270),time_span=time_format(date=45),type="min")

        print("summer_solstice__naive")
        summer_solstice__naive = find_extreme_value_time(function_equatorial__naive, test_time=time_format(date=90),time_span=time_format(date=45),type="max")
        print("winter_solstice__naive")
        winter_solstice__naive = find_extreme_value_time(function_equatorial__naive, test_time=time_format(date=270),time_span=time_format(date=45),type="min")



        plt.figure(figsize=[10,7])
        rise_time_list=[]
        fall_time_list=[]

        

        x_axis = range(-50,365+50,5)



        # class experiment_setup:
        #     function = None
        #     title: str = "None"
        #     spring_equinox:time_format = field(default_factory = time_format)
        #     fall_equinox: time_format = field(default_factory = time_format)
        #     next_spring_equinox: time_format = field(default_factory= time_format)
        #     filename: str = "None"

        # experiment_setup()

        function = function_horizontal__wiki
        title = f"Rise and set times of the Sun from Budapest"
        spring_equinox = spring_equinox__wiki
        fall_equinox = fall_equinox__wiki
        next_spring_equinox = prev_spring_equinox__wiki
        filename = f"sun_set_rise_real.png"

        # function = function_equatorial__naive
        # title = f"Rise and set times of the Sun from Budapest with perfect orbit"
        # spring_equinox = spring_equinox__naive
        # fall_equinox = fall_equinox__naive
        # filename = f"sun_set_rise_perfect.png"

        for d in x_axis:
            test_time_sunrise = time_format(date=d, hour=6)
            test_time_sunset = time_format(date=d, hour=18)
            time_span = time_format(hour=10)
            time_resolution = time_format(sec=1)

                
            sunrise_time_hour = find_zero_crossing_time(function, test_time_sunrise, time_span, time_resolution).get_day_from_time().get_sec_from_date()
            sunset_time_hour = find_zero_crossing_time(function, test_time_sunset, time_span, time_resolution).get_day_from_time().get_sec_from_date()
            rise_time_list.append(sunrise_time_hour)
            fall_time_list.append(sunset_time_hour)
            # rise_time_list.append(find_sun_set_time(time_format(date=d), pos, time_resolution=1, sunset=True).get_day_from_time().get_sec_from_date()/3600)
            # fall_time_list.append(find_sun_set_time(time_format(date=d), pos, time_resolution=1, sunset=False).get_day_from_time().get_sec_from_date()/3600)



        def find_max(time_list):
            max_idx = time_list.index(max(time_list))
            max_date = x_axis[max_idx]
            return max_date
        
        def find_min(time_list):
            min_idx = time_list.index(min(time_list))
            min_date = x_axis[min_idx]
            return min_date

        max_rise = find_max(rise_time_list[0:365])
        min_rise = find_min(rise_time_list[0:365])

        max_fall = find_max(fall_time_list[0:365])
        min_fall = find_min(fall_time_list[0:365])

        plt.plot(x_axis,np.array(rise_time_list)/3600,"-",label="sunrise time")
        plt.plot(x_axis,np.array(fall_time_list)/3600,"-", label="sunset time")
        plt.plot(x_axis,np.array(fall_time_list)/3600-np.array(rise_time_list)/3600,":",color="C2", label = "length of the daylight")


        plt.axvline(max_rise,color="C0",linestyle="--",label="latest rise")
        plt.axvline(min_rise,color="C0",linestyle=":",label="earliest rise")
        plt.axvline(max_fall,color="C1",linestyle="--",label="latest set")
        plt.axvline(min_fall,color="C1",linestyle=":",label="earliest set")



        distance_arrows2([max_rise,12],[min_fall,12],f"",14,"black")

        plt.text(max_fall+10, 12.5, f"distance:\n{abs(min_rise-max_fall)} day", ha="left", va="bottom")
        plt.text(max_rise+10, 12.5, f"distance:\n{abs(max_rise-min_fall)} day", ha="left", va="bottom")

        

        # plt.title(f"Rise and set times of the Sun from Budapest\nearliest rise date= {min_rise}\nlatest set date= {max_fall}\nlatest rise date = {max_rise}\nearliest set date {min_fall}")
        plt.title(title)
        plt.grid()
        plt.legend(loc='lower left')
        plt.xlabel("Time passed since spring equinox [day]")
        plt.ylabel("time of day [hour]")
        # plt.tight_layout()
        plt.yticks(range(0,24,1))
        plt.ylim([0,24])
        plt.xlim([min(x_axis),max(x_axis)])
        alpha = 0.2
        plt.axhline(12, color="black", linestyle="--",alpha=alpha)
        plt.axvline(fall_equinox__wiki.get_sec_from_date()/86400, color="black", linestyle="--",alpha=alpha)
        plt.axvline(spring_equinox__wiki.get_sec_from_date()/86400, color="black", linestyle="--",alpha=alpha)
        plt.axvline(prev_spring_equinox__wiki.get_sec_from_date()/86400, color="black", linestyle="--",alpha=alpha)
        plt.axvline(summer_solstice__wiki.get_sec_from_date()/86400, color="black", linestyle="--",alpha=alpha)
        plt.axvline(winter_solstice__wiki.get_sec_from_date()/86400, color="black", linestyle="--",alpha=alpha)
        plt.axvline(summer_solstice__naive.get_sec_from_date()/86400, color="black", linestyle=":",alpha=alpha)
        plt.axvline(winter_solstice__naive.get_sec_from_date()/86400, color="black", linestyle=":",alpha=alpha)

        plt.axvline(fall_equinox__naive.get_sec_from_date()/86400, color="gray", linestyle=":")
        plt.axvline(spring_equinox__naive.get_sec_from_date()/86400, color="gray", linestyle=":")
        plt.axvline(prev_spring_equinox__naive.get_sec_from_date()/86400, color="gray", linestyle=":")

        plt.xticks([0,365.25])


        distance_arrows2([min_rise,12],[max_fall,12],f"",14,"black")
        plt.scatter(min_rise,12, marker ="+", color="black",zorder = 10)
        plt.scatter(max_fall,12, marker ="+", color="black",zorder = 10)
        
        
        


        plt.savefig(filename)
        plt.show()



    if 0:
        eot_diff_list=[]
        for d in range(365):
            eot_diff_list.append(get_eot_from_date(time_format(d)).get_sec_from_date())

        plt.plot(eot_diff_list)
        plt.show()



    get_analemma = False
    if get_analemma:

        horiz_list_elev=[]
        horiz_list_azim=[]
        for d in range(365):
            sun = get_sun_pos_in_horizontal_coordinates__adjustable_ecliptic_lon(time_format(d,12,00,00),time_format(),polar_pos)
            horiz_list_azim.append(sun.azimuth.as_float())
            horiz_list_elev.append(sun.elevation.as_float())
        plt.scatter(horiz_list_azim,horiz_list_elev)

        horiz_list_elev=[]
        horiz_list_azim=[]
        for d in range(365):
            sun = get_sun_pos_in_horizontal_coordinates__adjustable_ecliptic_lon(time_format(d,12,00,00),time_format(),polar_pos)
            horiz_list_azim.append(sun.azimuth.as_float())
            horiz_list_elev.append(sun.elevation.as_float())
        plt.scatter(horiz_list_azim,horiz_list_elev)

        plt.axis("equal")
        plt.grid()
        plt.ylabel("elevation [deg]")
        plt.xlabel("azimuth [deg]")
        plt.title("Sun position on the nort pole at every noon")

        plt.show()
    
    test_eot = False
    if test_eot:
        plt.figure(figsize=[10,7])

        simulated_noon_diff_list = []
        list2 = []

        for d in range(365):
            date=time_format(d)
            simulated_noon_diff_list.append(get_sun_pos_in_ecliptic_coordinates__adjustable_ecliptic_lon(date).longitude.as_float())
            list2.append(get_sun_pos_in_ecliptic_coordinates__adjustable_ecliptic_lon(date,eot=True).longitude.as_float())


        plt.plot(simulated_noon_diff_list,'o-')
        plt.plot(list2,'o-')

        plt.show()

    if 0:
        simulated_noon_diff_list = []
        eot_diff_list = []
        time_samples = range(0,365,5)
        for d in time_samples:
            simulated_noon_diff_list.append(find_sun_noon_time(time_format(d),utc_plus=utc_plus, pos=greenwich_pos,time_resolution=1).get_day_from_time().get_sec_from_date()-time_format(0,12).get_sec_from_date())
            eot_diff_list.append(get_eot_from_date(time_format(d)).get_sec_from_date())

        plt.plot(time_samples,simulated_noon_diff_list,"o-")
        plt.plot(time_samples,eot_diff_list,"o-")

        plt.show()

        # plt.plot(time_samples,np.array(eot_diff_list)-np.array(simulated_noon_diff_list))
        # plt.show()

    calculate_ecliptic_longitude_from_eot_table_flag=False
    if calculate_ecliptic_longitude_from_eot_table_flag:
        calculate_ecliptic_longitude_from_eot_table(day_step=1,verbose=True)
        out = np.load("sun_ecliptic_time_corr.npy",allow_pickle=True)
        print(out)

    if 0:
        raw: np.ndarray[EclipticCorrectorTime] = np.load("sun_ecliptic_time_corr.npy",allow_pickle=True)
        out: list[EclipticCorrectorTime] = list(raw)

        dates=[]
        values=[]
        for i in out:
            dates.append(i.time_of_year.get_sec_from_date())
            values.append(i.time_difference.get_sec_from_date())

        plt.plot(dates,np.array(values)/3600)
        plt.show()

    if 0:
        raw: np.ndarray[EclipticCorrectorTime] = np.load("sun_ecliptic_time_corr.npy",allow_pickle=True)
        sun_latitude_lookup: list[EclipticCorrectorTime] = list(raw)
        list0 = []
        x = []
        for i in range(0,365,30):
            for j in range(0,24,4):
                time = time_format(date=i,hour=j)
                list0.append(ecliptic_longitude_time_diff_interpolator(time).get_sec_from_date())
                x.append(time.get_sec_from_date())

        plt.plot(x,list,"o-")
        plt.show()




    comparing_multiple_eot_eclipticlal_longitudes = False
    if comparing_multiple_eot_eclipticlal_longitudes:
        raw: np.ndarray[EclipticCorrectorTime] = np.load("sun_ecliptic_time_corr.npy",allow_pickle=True)
        sun_latitude_lookup: list[EclipticCorrectorTime] = list(raw)
        list_from_table = []
        naive_list = []
        wiki_method_list = []

        for d in range(0,365,1):
            date = time_format(d)
            list_from_table.append(get_sun_pos_in_ecliptic_coordinates__interpolated_eot_table(date).longitude.as_float())
            naive_list.append(get_sun_pos_in_ecliptic_coordinates__adjustable_ecliptic_lon(date).longitude.as_float())

            wiki_method_list.append(get_sun_pos_in_horizontal_coordinates__wiki(date).longitude.as_float())
        # plt.plot(lon_list)
        # plt.plot(lon_list2)
        # plt.plot(lon_list3)
        # plt.plot(np.array(naive_list)-np.array(list_from_table))
        # plt.plot(np.array(naive_list)-np.array(wiki_method_list))
        plt.plot(np.array(list_from_table)-np.array(wiki_method_list))

        plt.grid()
        plt.show()

    get_analemma_wiki = False
    if get_analemma_wiki:
        analemma_pos = greenwich_pos
        plt.figure(figsize=[8,7])

        horiz_list_elev__naive=[]
        horiz_list_azim__naive=[]
        for d in range(365):
            sun = get_sun_pos_in_horizontal_coordinates__adjustable_ecliptic_lon(time_format(d,12,00,00),time_format(),analemma_pos)
            horiz_list_azim__naive.append(sun.azimuth.as_float())
            horiz_list_elev__naive.append(sun.elevation.as_float())
        plt.plot(horiz_list_azim__naive,horiz_list_elev__naive,color="C0")

        horiz_list_elev__wiki=[]
        horiz_list_azim__wiki=[]
        for d in range(365):
            sun = get_sun_pos_in_horizontal_coordinates__wiki(time_format(d,12,00,00),time_format(),analemma_pos)
            horiz_list_azim__wiki.append(sun.azimuth.as_float())
            horiz_list_elev__wiki.append(sun.elevation.as_float())
        plt.plot(horiz_list_azim__wiki,horiz_list_elev__wiki,color="red")

        horiz_list_elev=[]
        horiz_list_azim=[]
        for d in range(0,365,10):
            raw: np.ndarray[EclipticCorrectorTime] = np.load("sun_ecliptic_time_corr.npy",allow_pickle=True)
            sun_latitude_lookup: list[EclipticCorrectorTime] = list(raw)
            sun = get_sun_pos_in_horizontal_coordinates__interpolated_eot_table(time_format(d,12,00,00),time_format(),analemma_pos)
            horiz_list_azim.append(sun.azimuth.as_float())
            horiz_list_elev.append(sun.elevation.as_float())
        plt.plot(horiz_list_azim,horiz_list_elev,".",color="red")

        # plt.axis("equal")
        plt.grid()
        plt.ylabel("elevation [deg]")
        plt.xlabel("azimuth [deg]")
        plt.title("Sun position on the nort pole at every noon")
        plt.axvline(180,color="black")

        plt.axhline(90-analemma_pos.latitude.as_float(),color="black")
        plt.axhline(90-analemma_pos.latitude.as_float()+AXIAL_TILT,color="black")
        plt.axhline(90-analemma_pos.latitude.as_float()-AXIAL_TILT,color="black")

        plt.xlim([176,185])
        plt.ylim([0,70])

        plt.savefig("analemma.png")
        plt.show()

    compare_summer_winter_length = False
    if compare_summer_winter_length:

        


        fall_equinox__wiki = find_zero_crossing_time(function_equatorial__wiki,test_time=time_format(date=180),time_span=time_format(date=90))
        spring_equinox__wiki = find_zero_crossing_time(function_equatorial__wiki,test_time=time_format(date=2*180),time_span=time_format(date=90))
        next_fall_equinox__wiki = find_zero_crossing_time(function_equatorial__wiki,test_time=time_format(date=3*180),time_span=time_format(date=90))
        fall_equinox__naive = find_zero_crossing_time(function_equatorial__naive,test_time=time_format(date=180),time_span=time_format(date=90))
        spring_equinox__naive = find_zero_crossing_time(function_equatorial__naive,test_time=time_format(date=2*180),time_span=time_format(date=90))
        next_fall_equinox__naive = find_zero_crossing_time(function_equatorial__naive,test_time=time_format(date=3*180),time_span=time_format(date=90))


        naive_decli=[]
        wiki_decli=[]
        x = range(365*2)
        for d in range(365*2):
            naive_decli.append(function__naive(time_format(date=d)))
            wiki_decli.append(function__wiki(time_format(date=d)))

        plt.figure(figsize=[10,7])
        plt.plot(x,naive_decli,label="evenly passing year",color = "C0")
        plt.plot(x,wiki_decli,label="actually passing year", color = "C1")
        plt.grid()

        fall_equinox__wiki_day = fall_equinox__wiki.get_sec_from_date()/86400
        spring_equinox__wiki_day = spring_equinox__wiki.get_sec_from_date()/86400
        next_fall_equinox__wiki_day = next_fall_equinox__wiki.get_sec_from_date()/86400

        fall_equinox__naive_day = fall_equinox__naive.get_sec_from_date()/86400
        spring_equinox__naive_day = spring_equinox__naive.get_sec_from_date()/86400
        next_fall_equinox__naive_day = next_fall_equinox__naive.get_sec_from_date()/86400

        plt.axvline(fall_equinox__wiki_day,color="C1", linestyle="--")
        plt.axvline(spring_equinox__wiki_day,color="C1", linestyle=":")
        plt.axvline(next_fall_equinox__wiki_day,color="C1", linestyle="--")

        plt.axvline(fall_equinox__naive_day,color="C0", linestyle = "--")
        plt.axvline(spring_equinox__naive_day,color="C0", linestyle = ":")
        plt.axvline(next_fall_equinox__naive_day,color="C0", linestyle = "--")

        plt.xlabel("date [day]")
        plt.ylabel("Sun ecliptic declination [deg]")

        plt.xlim([100,650])
        plt.ylim([-40,40])


            
        distance_arrows2(beg_pos=[fall_equinox__wiki_day,28],
                        end_pos=[spring_equinox__wiki_day,28],
                        text=f"Winter:\n{spring_equinox__wiki_day-fall_equinox__wiki_day:.2f} days",
                        text_pos_vertical=31,
                        color="C1")

        distance_arrows2(beg_pos=[spring_equinox__wiki_day,28],
                        end_pos=[next_fall_equinox__wiki_day,28],
                        text=f"Summer:\n{next_fall_equinox__wiki_day-spring_equinox__wiki_day:.2f} days",
                        text_pos_vertical=31,
                        color="C1")
        
        distance_arrows2(beg_pos=[fall_equinox__wiki_day,35],
                        end_pos=[next_fall_equinox__wiki_day,35],
                        text=f"Year:\n{next_fall_equinox__wiki_day-fall_equinox__wiki_day:.2f} days",
                        text_pos_vertical=38,
                        color="C1")
        


        distance_arrows2(beg_pos=[fall_equinox__naive_day,-28],
                        end_pos=[spring_equinox__naive_day,-28],
                        text=f"Winter:\n{spring_equinox__naive_day-fall_equinox__naive_day:.2f} days",
                        text_pos_vertical=-31,
                        color="C0")

        distance_arrows2(beg_pos=[spring_equinox__naive_day,-28],
                        end_pos=[next_fall_equinox__naive_day,-28],
                        text=f"Summer:\n{next_fall_equinox__naive_day-spring_equinox__naive_day:.2f} days",
                        text_pos_vertical=-31,
                        color="C0")
        
        
        distance_arrows2(beg_pos=[fall_equinox__naive_day,-35],
                        end_pos=[next_fall_equinox__naive_day,-35],
                        text=f"Year:\n{next_fall_equinox__naive_day-fall_equinox__naive_day:.2f} days",
                        text_pos_vertical=-38,
                        color="C0")
        
        plt.legend()
        plt.savefig("winter_summer_compare.png")
        plt.show()