import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi
import utils
import argparse
import toml
import time
import csv_read_zodiac
from utils import *





def plot_cylindrical_stars(const_list: list[ListOfSkypoints],  proj_vals: ProjVals, hmg, hmg2, a):
    x_list=[]
    y_list=[]
    S_list=[]
    alpha_list=[]

    # star_color="orange"
    star_color2="black"
    star_color="black"
    for list_elem in const_list:
        for i,star in enumerate(list_elem.list_of_skypoints):


            ra_dec_coord = RaDecDegCoord_deg(
            right_ascension_deg=star.ra_dec_deg.right_ascension_deg,
            declination_deg=star.ra_dec_deg.declination_deg
            )

            v = get_transformed_vector(ra_dec_coord, proj_vals)
            
            x_y_z = cylindrical_project(v)

            S,marker,alpha = condition_magnitudes(star,hmg,hmg2)
            s=a*(1+hmg-S)
            x=x_y_z[0]
            y=x_y_z[1]

            if x<0:
                x=x+2*np.pi
            
            if marker == ".":
                S_list.append(s)

                x_list.append(x)
                y_list.append(y)
                alpha_list.append(alpha)
            else:
                plt.scatter(x, y, color=star_color,  s=s, marker=marker, alpha=alpha, zorder=ORDER_OF_STARS_MAJOR)  
                plt.scatter(x-2*pi, y, color=star_color,  s=s, marker=marker, alpha=alpha, zorder=ORDER_OF_STARS_MAJOR) 


    plt.scatter(x_list, y_list, color=star_color2,  s=S_list, marker=".", alpha=alpha_list, zorder=ORDER_OF_STARS_MINOR)
    # plt.scatter(x_y_z[0]+2*pi, x_y_z[1], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha, zorder=3)
    plt.scatter(x_list-2*pi*np.ones(len(x_list)), y_list, color=star_color2,  s=a*(1+hmg-S), marker=marker, alpha=alpha_list, zorder=ORDER_OF_STARS_MINOR)
    # y.append(x_y_z[1])
    # x.append(x_y_z[0])

ecliptic_color="#ddddddff"
def plot_cylindrical_ecliptic(const_list: list[ListOfSkypoints], proj_vals: ProjVals, hmg,hmg2,a):
    x_list=[]
    y_list=[]
    S_list=[]
    alpha_list=[]

    star_color="orange"
    star_color2="black"
    for list_elem in const_list:
        for i,star in enumerate(list_elem.list_of_skypoints):

            ra_dec_coord = RaDecDegCoord_deg(
            right_ascension_deg=star.ra_dec_deg.right_ascension_deg,
            declination_deg=star.ra_dec_deg.declination_deg
            )

            v = get_transformed_vector(ra_dec_coord, proj_vals)
            x_y_z = cylindrical_project(v)

            S,marker,alpha = condition_magnitudes(star,hmg,hmg2)
            s=a*(1+hmg-S)
            x=x_y_z[0]
            y=x_y_z[1]

            if x<0:
                x=x+2*np.pi
            
            S_list.append(s)

            x_list.append(x)
            y_list.append(y)
            alpha_list.append(alpha)

    x_wrapped = np.concatenate([np.array(x_list) - 2*np.pi, x_list])
    y_wrapped = np.concatenate([y_list, y_list])

    idx = np.argsort(x_wrapped)

    x_list = x_wrapped[idx]
    y_list = y_wrapped[idx]


    # plt.scatter(x_list, y_list, color=star_color2,  s=1, marker=".", alpha=1, zorder=5)
    
    for i in range(len(x_list)-1):
        plt.plot([x_list[i],x_list[i+1]],[y_list[i],y_list[i+1]],linewidth=1.0,linestyle="-",alpha=1,color=ecliptic_color,zorder=ORDER_OF_ECLIPTIC_LINE)



def plot_cylindrical_equinox(const_list: list[ListOfSkypoints], proj_vals: ProjVals, hmg,hmg2,a):
    star_color=ecliptic_color

    for list_elem in const_list:
        for i,star in enumerate(list_elem.list_of_skypoints):

            ra_dec_coord = RaDecDegCoord_deg(
            right_ascension_deg=star.ra_dec_deg.right_ascension_deg,
            declination_deg=star.ra_dec_deg.declination_deg
            )

            v = get_transformed_vector(ra_dec_coord, proj_vals)
            x_y_z = cylindrical_project(v)

            S=1
            lw = 1.5
            x=x_y_z[0]
            y=x_y_z[1]

            if x<0:
                x=x+2*np.pi
            
            plt.scatter(x, y, color=star_color,  s=S, marker="o", alpha=1, zorder=ORDER_OF_STARS_MAJOR,linewidths=lw)   # <— skinny!)  
            plt.scatter(x-2*pi, y, color=star_color,  s=S, marker="o", alpha=1, zorder=ORDER_OF_STARS_MAJOR,linewidths=lw)   # <— skinny!) 



def plot_cylindrical_lines(lines: ListOfSkylines, proj_vals: ProjVals, *,Break_line=0):
    
    segmentation_flag = False
    lines_to_print_list=[]
    # alpha_list=[]
    width_list=[]
    for idx,line in enumerate(lines.list_of_skylines):
        if idx%10 == 0:
            print(f"cylindrical lines:\t{idx/len(lines.list_of_skylines)*100:.2f}%")

        v1 = get_transformed_vector(line.point_data_1.ra_dec_deg, proj_vals)
        xyz_1 = cylindrical_project(v1)


        v2 = get_transformed_vector(line.point_data_2.ra_dec_deg, proj_vals)
        xyz_2 = cylindrical_project(v2)

        x1=xyz_1[0]
        x2=xyz_2[0]
        y1=xyz_1[1]
        y2=xyz_2[1]

        if abs(x1-x2)>np.pi:    
            segmentation_flag = True
            print("FLAG!!!")

        lines_to_print_list.append([[x1,x2],[y1,y2]])
        width_list.append(line.width)
        # alpha_list.append(alpha)


    for idx,lines_to_print in enumerate(lines_to_print_list):

        x1 = lines_to_print[0][0]       
        x2 = lines_to_print[0][1]
        y1 = lines_to_print[1][0]
        y2 = lines_to_print[1][1]

        if segmentation_flag:
            if x1<0:
                x1=x1+2*np.pi
            if x2<0:
                x2=x2+2*np.pi

        teasing_lines = False

        width=width_list[idx]
        if width == "1":
            width=0.6  
        else:
            width = 0.4

        if teasing_lines:
            # R=0.02
            R=0.0
            
            v1 = np.array([x1,y1,0])
            v2 = np.array([x2,y2,0])
            if abs_vector(v1-v2)> 2*R:
                v3 = norm_vector(v2-v1)*R
                v10 = v1 + v3
                v20 = v2 - v3

                x1,y1,_ = disolve_vector(v10)
                x2,y2,_ = disolve_vector(v20)

                plt.plot([x1,x2],[y1,y2],linewidth=width,linestyle=line.linestyle ,alpha=1,color=line.color,zorder=ORDER_OF_LINES)
        else:   
            plt.plot([x1,x2],[y1,y2],linewidth=width,linestyle=line.linestyle, alpha=1,color=line.color,zorder=ORDER_OF_LINES)


def plot_cylindrical_borders(border_line_list: ListOfSkylines, proj_vals: ProjVals, used_borders_list):
    # used_borders=[]
    crossing_border_flag = False
    break_flag = False
    segmented_lines_to_print_list=[]
    possibly_broken_lines_list=[]
    unsegmented_lines_to_print_list=[]
    current_constellation_used_lines=[]

    for border_line in (border_line_list.list_of_skylines):
        
        v1 = get_transformed_vector(border_line.point_data_1.ra_dec_deg, proj_vals)
        xyz_1 = cylindrical_project(v1)

        v2 = get_transformed_vector(border_line.point_data_2.ra_dec_deg, proj_vals)
        xyz_2 = cylindrical_project(v2)

        x1=xyz_1[0]
        x2=xyz_2[0]
        y1=xyz_1[1]
        y2=xyz_2[1]

        if abs(x1-x2)>np.pi:    
            break_flag = True
            print("FLAG!!!")

        possibly_boken_line = [x1,x2],[y1,y2]

        possibly_broken_lines_list.append(possibly_boken_line)
    
    for possibly_boken_line in possibly_broken_lines_list:

        x1 = possibly_boken_line[0][0]       
        x2 = possibly_boken_line[0][1]
        y1 = possibly_boken_line[1][0]
        y2 = possibly_boken_line[1][1]

        if break_flag:
            if x1<0:
                x1=x1+2*np.pi
            if x2<0:
                x2=x2+2*np.pi

        unsegmented_line = [x1,x2],[y1,y2]

        unsegmented_lines_to_print_list.append(unsegmented_line)

        
        if is_not_yet_used_line(unsegmented_line,used_borders_list):
            
            used_borders_list.append(unsegmented_line)  
            current_constellation_used_lines.append(unsegmented_line)




    for line_coordinate in current_constellation_used_lines:
        x_coordinates = line_coordinate[0]+np.random.random(2)/20*0
        y_coordinates = line_coordinate[1]+np.random.random(2)/20*0
        
        plt.plot(x_coordinates, y_coordinates, linewidth=0.5, linestyle="-", alpha=1, color="red", zorder=ORDER_OF_BORDES)




def print_cyl(constellations_for_borders_list, 
              center_Dec_deg, 
              root, 
              center_ra_deg, 
              zrot_deg, 
              constellation_line_list,
              constellations_for_stars_list,
              hmg,
              hmg2,
              a,
              DPI):

    x_realm = [-3.3, 4]
    y_realm = [-1.8, 1.5]
    x_span = abs(x_realm[0]-x_realm[1])
    y_span = abs(y_realm[0]-y_realm[1])
    x_y_scale=x_span/y_span
    base_scale=5

    plt.figure(figsize=(x_y_scale*base_scale, base_scale))

    if 1:
        # print()
        # print(constellations_for_borders_list)
        used_borders_list = []
        for idx,constellation_for_borders in enumerate(constellations_for_borders_list):
            print(f"Borders\t{idx} len: {len(constellations_for_borders_list)}\t{constellation_for_borders}")
            data_file_path=f"{root}/constellations/prev/borders/{constellation_for_borders}.csv"

            borders = csv_read_zodiac.read_lines_csv(data_file_path)
            # print("B")

            proj_vals=utils.ProjVals(center_Dec_deg,center_ra_deg,zrot_deg)
            utils.plot_cylindrical_borders(borders, proj_vals, used_borders_list)
            # print(used_borders_list)
            # print("A")

    if 1:
        for idx,constellation_for_line in enumerate(constellation_line_list):
            print(f"lines\t{idx} len: {len(constellation_line_list)}")
            data_file_path = f"{root}/constellations/prev/{constellation_for_line}.csv"

            data = csv_read_zodiac.read_lines_csv(data_file_path)
            utils.plot_cylindrical_lines(data, proj_vals, Break_line=0.1)


    if 1:
        DATA=[]
        for idx, constellation_for_stars in enumerate(constellations_for_stars_list):
            print(f"stars\t{idx} len: {len(constellations_for_stars_list)}")
            data_file_path=f"{root}/constellations/prev/{constellation_for_stars}.csv"

            data = csv_read_zodiac.read_stars_csv(data_file_path)
            DATA.append(data)
        utils.plot_cylindrical_stars(DATA, proj_vals,hmg,hmg2,a)


    if 1:
        DATA=[]

        data_file_path=f"{root}/constellations/prev/ecliptic.csv"
        data = csv_read_zodiac.read_stars_csv(data_file_path)
        DATA.append(data)
        utils.plot_cylindrical_ecliptic(DATA,proj_vals,hmg,hmg2,a)

        DATA=[]

        data_file_path=f"{root}/constellations/prev/eqinox.csv"
        data = csv_read_zodiac.read_stars_csv(data_file_path)
        DATA.append(data)
        utils.plot_cylindrical_equinox(DATA,proj_vals,hmg,hmg2,a)


    # plt.xlim([0*np.pi,2.25*np.pi])

    # plt.ylim([-np.pi/2,np.pi/2])

    # for i in range(-6,6):
    #     plt.axvline(i/6*np.pi,linestyle="--",color="gray",linewidth=0.5)
    # for i in range(-3,3):
    #     plt.axhline(i/6*np.pi,linestyle="--",color="gray",linewidth=0.5)

    plt.gca().set_aspect('equal', adjustable='box')
 
    plt.xlim(x_realm)
    plt.ylim(y_realm)
    plt.tight_layout(pad=0)
    plt.axis('off')
    plt.margins(0)
    
    # plt.savefig("cylindrical.pdf", dpi=DPI)
    plt.savefig("cylindrical.pdf", dpi=DPI, bbox_inches='tight', pad_inches=0)

    # plt.show()



from utils import *




def generate_stars_cyl_3d(stars: ListOfSkypoints, proj_vals, hmg, hmg2, clearance, base_thickness_mm, radius=0.01, multiplier=1):

    star_body_list = []

    for star in stars.list_of_skypoints:

        v = get_transformed_vector(star.ra_dec_deg, proj_vals)
        x_y_z = cylindrical_project(v)
        # S,marker,alpha = condition_magnitudes(star, hmg,hmg2)
        # plt.scatter(x_y_z[1], x_y_z[0], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha, zorder=3)
        x=(x_y_z[1])
        y=(x_y_z[0])

        current_projected_point = Vector(y,x,z=0)
        star_circles = current_projected_point.get_dots(width=radius)
        star_circles.multiply_with_scalar(multiplier)
        # star_circles.just_plot_dont_show()

        star_polygon = Polygon(star_circles.points)
        # star_polygon = star_polygon.buffer(-clearance)
        star_body = trimesh.creation.extrude_polygon(star_polygon, height = base_thickness_mm*2)
        star_body_list.append(star_body)

    combined_star_body = trimesh.boolean.union(star_body_list, engine="manifold")
    return combined_star_body



def get_cyl_projection_for_star(stars: SkyPoint, 
                                proj_vals, 
                                radius=0.01, 
                                thickness=1, 
                                offset=0, 
                                segmentation_flag: bool = False)->tuple[list[ClosedDrawing],Vector]:

    star_body_list = []

    v = get_transformed_vector(stars.ra_dec_deg, proj_vals)
    x_y_z = cylindrical_project(v)
    # S,marker,alpha = condition_magnitudes(star, hmg,hmg2)
    # plt.scatter(x_y_z[1], x_y_z[0], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha, zorder=3)
    x=(x_y_z[1])
    y=(x_y_z[0])

    if segmentation_flag:
        if y<0:
            y=y+2*np.pi
    

    current_projected_point = Vector(y,x,z=0)
    star_circles = current_projected_point.get_star_shaped_dots(width=radius, thickness=thickness, offset=offset)
    star_body_list.append(star_circles)

    return star_body_list, current_projected_point


def get_cyl_projection_for_stars(stars_of_constellation: ListOfSkypoints, 
                                 proj_vals, 
                                 base_thickness_mm, 
                                 hmg2, 
                                 hmg, 
                                 segmentation_flag = False)->tuple[list[ClosedDrawing],ListOfVectors]:
    out=[]
    out_points=[]
    for star in stars_of_constellation.list_of_skypoints:
        if star.apparent_mag < hmg2:
            rad=0.008
        elif star.apparent_mag < hmg:
            rad=0.006
        else:
            rad=0.004

        star_contours, star_points = get_cyl_projection_for_star(star, proj_vals, 
                                                    radius=rad, 
                                                    thickness= base_thickness_mm*3, 
                                                    offset=-base_thickness_mm, 
                                                    segmentation_flag = segmentation_flag)
        # constellation_puzzle_piece.star_contours.extend(star_contours)
        out.extend(star_contours)
        out_points.append(star_points)

    return out, ListOfVectors(out_points)

 
def get_cyl_projection_for_lines(line: SkyLine, proj_vals, segmentation_flag = False) -> Line :
    v1 = get_transformed_vector(line.point_data_1.ra_dec_deg, proj_vals)
    xyz_1 = cylindrical_project(v1)

    v2 = get_transformed_vector(line.point_data_2.ra_dec_deg, proj_vals)
    xyz_2 = cylindrical_project(v2)

    x1=xyz_1[0]
    x2=xyz_2[0]
    y1=xyz_1[1]
    y2=xyz_2[1]

    if segmentation_flag:
        if x1<0:
            x1=x1+2*np.pi
        if x2<0:
            x2=x2+2*np.pi

    # if abs(x1-x2)>np.pi:    
    #     if x1<0:
    #         x1=x1+2*np.pi
    #     if x2<0:
    #         x2=x2+2*np.pi

    start_point     = Vector(x=x1, y=y1, z=0)
    end_point       = Vector(x=x2, y=y2, z=0)

    descartes_line  = Line(start_point=start_point,end_point=end_point)

    return(descartes_line)


def get_cyl_projection_for_constellation_line_contours(line_list: ListOfSkylines, 
                                                       proj_vals, 
                                                       stripe_width, 
                                                       thickness: float, 
                                                       offset: float, 
                                                       segmentation_flag: bool) -> tuple[list[ClosedDrawing], ListOfLines]:
    # segmentation_flag = is_this_linestack_segmented(line_list, proj_vals)

    out_close_drawing_list: list[ClosedDrawing] = []
    line_skeleton_list: list[Line] = []
    for line in line_list.list_of_skylines:
        descartes_line: Line = get_cyl_projection_for_lines(line, proj_vals, segmentation_flag=segmentation_flag)
        line_skeleton_list.append(descartes_line)

        stripes = descartes_line.get_stripes_and_dots(width=stripe_width, thickness=thickness, offset=offset)
        out_close_drawing_list.extend(stripes)

    return out_close_drawing_list, ListOfLines(line_skeleton_list)

def is_this_linestack_segmented(line_list: ListOfSkylines, proj_vals):

    for sl in line_list.list_of_skylines:
        descartes_line = get_cyl_projection_for_lines(sl, proj_vals)
        x1 = descartes_line.start_point.x
        x2 = descartes_line.end_point.x

        if abs(x1-x2)>180.0:    
            return True

    return False


def get_cyl_projection_for_list_of_lines(line_list: ListOfSkylines, proj_vals, thickness: float, offset: float, segmentation_flag: bool) -> ClosedDrawing:

    out0=[]
    for sl in line_list.list_of_skylines:
        descartes_line = get_cyl_projection_for_lines(sl, proj_vals, segmentation_flag=segmentation_flag)
        # out0.append((descartes_line.start_point.y, descartes_line.start_point.x))
        point = Vector(x = descartes_line.start_point.y, y = descartes_line.start_point.x, z = 0)
        out0.append(point)

    out = ClosedDrawing(points=out0, name=line_list.list_of_skylines[0].point_data_1.constellation, thickness=thickness, offset=offset)

    return out

#TODO: szóval ki kéne találni, hogy lehet egy csillagképről összességében megállapítani, hogy az darabolt-e. ennek az eredényét egyesével beadni az egyes részek rajzolóinak, hogy úgy készüljenek, 
# különben lehet olyan, hogy a kép egyik oldalán van a border, 
# másikon a csillagok, harmadikon meg a lineok
def generate_stars_linestack(stars: ListOfSkypoints) -> ListOfSkylines:
    out: ListOfSkylines = ListOfSkylines([])
    out_list=[]
    line_list = []
    for s1 in stars.list_of_skypoints:
        for s2 in stars.list_of_skypoints:
            line = SkyLine(point_data_1=s1, point_data_2=s2)
            # line_list.append(line)
            # print(line)
            out_list.append(line)
            # out.list_of_skylines.extend(line)
    # print_this = ListOfSkylines(line_list)
    # print_this.print_points()
    out.list_of_skylines=out_list
    return out


def is_this_star_formation_segmented(stars: ListOfSkypoints, proj_vals):
    stars_linestack: ListOfSkylines = generate_stars_linestack(stars)
    stars_seg_flag = is_this_linestack_segmented(stars_linestack, proj_vals)
    return stars_seg_flag


def is_this_contellation_segmented(borders, constellation_lines, stars: ListOfSkypoints, proj_vals, constellation):
    border_segmentation_flag = is_this_linestack_segmented(borders, proj_vals)
    lines_seg_flag = is_this_linestack_segmented(constellation_lines, proj_vals)
    stars_seg_flag = is_this_star_formation_segmented(stars, proj_vals)

    return border_segmentation_flag or stars_seg_flag or lines_seg_flag




def extract_puzzle_piece_object(constellation, 
                                constellation_line_list, 
                                constellation_stars_list, 
                                constellation_borders_list,
                                proj_vals,
                                line_depth_mm,
                                base_thickness_mm,
                                hmg2,
                                hmg,
                                segmentation_flag = False
                                )-> OnePieceOfPuzzle:

    constellation_puzzle_piece = OnePieceOfPuzzle(border=ClosedDrawing([]), 
                                                  line_skeleton= ListOfLines(list_of_lines=[]),
                                                  line_contours=[],
                                                  star_points=ListOfVectors(list_of_vector=[]),
                                                  star_contours=[], 
                                                  name = constellation)


    # for constellation_line in constellation_line_list:
    constellation_puzzle_piece.line_contours, constellation_puzzle_piece.line_skeleton = get_cyl_projection_for_constellation_line_contours(constellation_line_list, 
                                                                                proj_vals, 
                                                                                stripe_width=0.005, 
                                                                                thickness= line_depth_mm*2, 
                                                                                offset=base_thickness_mm-line_depth_mm,
                                                                                segmentation_flag = segmentation_flag)

        
    
    constellation_puzzle_piece.star_contours, constellation_puzzle_piece.star_points = get_cyl_projection_for_stars(constellation_stars_list, 
                                                                            proj_vals, 
                                                                            base_thickness_mm, 
                                                                            hmg2, 
                                                                            hmg, 
                                                                            segmentation_flag)


        # remover_list_of_drawing.extend(get_projection_for_star(star, proj_vals, radius=rad, thickness= base_thickness_mm*3, offset=-base_thickness_mm))

    constellation_puzzle_piece.border = get_cyl_projection_for_list_of_lines(  constellation_borders_list,
                                                    proj_vals=proj_vals, 
                                                    thickness=base_thickness_mm,
                                                    offset=0,
                                                    segmentation_flag = segmentation_flag)

    return constellation_puzzle_piece








def generate_3d(borders: ListOfSkylines, 
                constellation_lines: ListOfSkylines, 
                stars: ListOfSkypoints, 
                proj_vals: ProjVals, 
                hmg,
                hmg2):

    multiplier = 103.27*69.5/71.6
    clearance = 0.02
    base_thickness_mm = 2
    line_depth_mm = 0.1
    stripe_width = 0.001

    # borders.print_points()
    list_of_separated_constellations = borders.get_a_list_of_separated_constellations()
    # print(list_of_separated_constellations)
    # import time
    # time.sleep(10000)
    # list_of_separated_constellations = ["UMI", "DRA", "CAS"]
    # list_of_separated_constellations = ["DRA", "LMI"]
    # list_of_separated_constellations = ['CAS', 'AND', 'CVN', 'CMI', 'DRA', 'LMI', 'CNC', 'GEM', 'ARI', 'CAM', 'BOO', 'AUR', 'PEG', 'PER', 'CEP', 'COM', 'LAC', 'HER', 'EQU', 'TRI', 'LYN', 'UMI', 'CYG', 'LYR', 'SGE', 'VUL', 'DEL', 'UMA', 'CRB', 'SER1']
    # list_of_separated_constellations = ['LMI', 'CNC', 'GEM', 'ARI', 'CAM', 'BOO']
    list_of_separated_constellations = ['SER1']
    # list_of_separated_constellations = ['SGE_VUL', 'DEL_EQU']



    # combined_star_body = generate_stars_str_grph_3d(stars, proj_vals, hmg, hmg2, clearance, base_thickness_mm, radius=0.004, multiplier=multiplier)

    remover_element_list=[]
    remover_list_of_drawing: list[ClosedDrawing] = []

    for constellation in list_of_separated_constellations:
        # remover_list_of_drawing: list[ClosedDrawing] = []

        # Get the stripes of constellation_lines
        constellation_line_list: ListOfSkylines = constellation_lines.get_only_the_lines_realted_to_this_constellation(constellation)

        # Get the holes of stars
        constellation_stars_list: ListOfSkypoints = stars.get_only_the_stars_from_this_constellation(constellation)

        #Get the base contour
        constellation_borders_list: ListOfSkylines = borders.get_only_the_lines_realted_to_this_constellation(constellation)



        constellation_puzzle_piece = extract_puzzle_piece_object(   constellation, 
                                                                    constellation_line_list, 
                                                                    constellation_stars_list, 
                                                                    constellation_borders_list,
                                                                    proj_vals,
                                                                    line_depth_mm,
                                                                    base_thickness_mm,
                                                                    hmg2,
                                                                    hmg,
                                                                    segmentation_flag = False
                                                                    )





        if constellation_puzzle_piece.is_this_piece_segmented():
            constellation_puzzle_piece = extract_puzzle_piece_object(   constellation, 
                                                                                constellation_line_list, 
                                                                                constellation_stars_list, 
                                                                                constellation_borders_list,
                                                                                proj_vals,
                                                                                line_depth_mm,
                                                                                base_thickness_mm,
                                                                                hmg2,
                                                                                hmg,
                                                                                segmentation_flag = True
                                                                                )











        constellation_puzzle_piece.plot_my_drawing(save=True, dest = f"pieces/{constellation}.png")
        print(constellation)
        

    # plot_a_list_of_closedDrawing(remover_list_of_drawing)


    # Generate 3d objects from remover drawings
    for constellation_line in remover_list_of_drawing:

        constellation_line.multiply_with_scalar(multiplier)

        remover_poly = Polygon(constellation_line.points)

        remover_element = trimesh.creation.extrude_polygon(remover_poly, height = constellation_line.thickness)
        remover_element.apply_translation([0, 0, constellation_line.offset])
        remover_element_list.append(remover_element)


    ultimate_remover = trimesh.boolean.union(remover_element_list, engine="manifold")



    for constellation in list_of_separated_constellations:

        border = ClosedDrawing(points=[], name=constellation)
        constellation_borders_list = borders.get_only_the_lines_realted_to_this_constellation(constellation)


        border=get_cyl_projection_for_list_of_lines(constellation_borders_list,
                                                    proj_vals=proj_vals, 
                                                    thickness=base_thickness_mm,
                                                    offset=0)
        # print(type(remover_list_of_drawing))
        # print(len(remover_list_of_drawing))


        plot_a_list_of_closedDrawing(border)

        #define a piece
        one_piece_of_puzzle = OnePieceOfPuzzle( border = border,
                                                line_contours =  remover_list_of_drawing,
                                                )
                                                        
            

        #scale up
        one_piece_of_puzzle.border.multiply_with_scalar(multiplier)
        for constellation_line in one_piece_of_puzzle.line_contours:
            constellation_line.multiply_with_scalar(multiplier)

        #separate and create the base of piece
        border = one_piece_of_puzzle.border
        base_countour_polygon = Polygon(border.points)
        base_countour_polygon = base_countour_polygon.buffer(-clearance)
        base_plate = trimesh.creation.extrude_polygon(base_countour_polygon, height = base_thickness_mm)


        one_piece_of_puzzle.plot_my_drawing()

        #remove the things
        base_plate = trimesh.boolean.difference([base_plate, ultimate_remover],engine="manifold")   

        combined = base_plate

        # # Save as STL
        combined.export(f"{border.name}.stl")
        # to_remove.export(f"{contour.name}.stl")

        print(f"Created {border.name}.stl")