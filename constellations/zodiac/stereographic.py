from utils import *

def generate_stars_str_grph_3d(stars: list[PointDatas], proj_vals, hmg, hmg2, clearance, base_thickness_mm, radius=0.01, multiplier=1):

    star_body_list = []

    for star in stars:

        v = get_transformed_vector(star.ra_dec_deg, proj_vals)
        x_y_z = upproject(v)
        # S,marker,alpha = condition_magnitudes(star, hmg,hmg2)
        # plt.scatter(x_y_z[1], x_y_z[0], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha, zorder=3)
        x=(x_y_z[1])
        y=(x_y_z[0])

        current_projected_point = Vector(y,x,z=0)
        object = current_projected_point.get_dots(width=radius)
        object.multiply_with_scalar(multiplier)

        star_polygon = Polygon(object.points)
        # star_polygon = star_polygon.buffer(-clearance)
        star_body = trimesh.creation.extrude_polygon(star_polygon, height = base_thickness_mm*2)
        star_body_list.append(star_body)

    combined_star_body = trimesh.boolean.union(star_body_list, engine="manifold")
    return combined_star_body




    

def plot_borders_str_grph_3D(borders: ListOfSkylines, 
                             constellation_lines: ListOfSkylines, 
                             stars: list[PointDatas], 
                             proj_vals: ProjVals, 
                             hmg,
                             hmg2):

    multiplier = 103.27
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


    combined_star_body = generate_stars_str_grph_3d(stars, proj_vals, hmg, hmg2, clearance, base_thickness_mm, radius=0.004, multiplier=multiplier)


    remover_element_list=[]
    for constellation in list_of_separated_constellations:
        stripes: list[ClosedDrawing] = []

        print(constellation)

        only_given_lines: list[SkyLine]
        only_given_lines = constellation_lines.get_only_the_lines_from_this_constellation(constellation)
        for line in only_given_lines:

            v1 = get_transformed_vector(line.point_data_1.ra_dec_deg, proj_vals)
            xyz_1 = upproject(v1)

            v2 = get_transformed_vector(line.point_data_2.ra_dec_deg, proj_vals)
            xyz_2 = upproject(v2)

            x1=xyz_1[0]
            x2=xyz_2[0]
            y1=xyz_1[1]
            y2=xyz_2[1]

            start_point = Vector(x=x1,y=y1,z=0)
            end_point = Vector(x=x2, y=y2, z=0)
            descartes_line = Line(start_point=start_point,end_point=end_point)

            stripe = descartes_line.get_stripe(width=stripe_width)
            stripes.append(stripe)

            dots = descartes_line.get_dots(width=stripe_width/2)
            stripes.append(dots[0])
            stripes.append(dots[1])

        for stripe in stripes:
            stripe = stripe.multiply_with_scalar(multiplier)



        # remover_poly = Polygon(lines[0].points)
        # remover_element = trimesh.creation.extrude_polygon(remover_poly, height = line_depth_mm)
        # remover_element.apply_translation([0, 0, base_thickness_mm-line_depth_mm])
        
        # ultimate_remover = trimesh.boolean.union([remover_element], engine="manifold")
        for idx, line in enumerate(stripes):

            remover_poly = Polygon(line.points)

            remover_element = trimesh.creation.extrude_polygon(remover_poly, height = line_depth_mm)
            remover_element.apply_translation([0, 0, base_thickness_mm-line_depth_mm])
            remover_element_list.append(remover_element)
            # print(remover_element)

            # print(idx)

    remover_element_list.append(combined_star_body)
    ultimate_remover = trimesh.boolean.union(remover_element_list, engine="manifold")




    for constellation in list_of_separated_constellations:

        base_contour = ClosedDrawing(points=[], name=constellation)

        only_given_borders = borders.get_only_the_lines_from_this_constellation(constellation)
        for line in only_given_borders:

            ra_step_rad, dec_step_rad, iteration_num = get_radec_step_rad(line)
            one_line = get_a_fragmented_line(iteration_num, line, ra_step_rad, dec_step_rad, proj_vals)
            base_contour.points.extend(reversed(one_line))



        #define a piece
        one_piece_of_puzzle = OnePieceOfPuzzle(border = base_contour,lines = stripes)

        #scale up
        one_piece_of_puzzle.border.multiply_with_scalar(multiplier)
        for line in one_piece_of_puzzle.lines:
            line.multiply_with_scalar(multiplier)

        #separate and create the base of piece
        base_contour = one_piece_of_puzzle.border
        base_countour_polygon = Polygon(base_contour.points)
        base_countour_polygon = base_countour_polygon.buffer(-clearance)
        base_plate = trimesh.creation.extrude_polygon(base_countour_polygon, height = base_thickness_mm)

        one_piece_of_puzzle.plot_my_drawing()

        #remove the things
        base_plate = trimesh.boolean.difference([base_plate, ultimate_remover],engine="manifold")   

        combined = base_plate

        # # Save as STL
        combined.export(f"{base_contour.name}.stl")
        # to_remove.export(f"{contour.name}.stl")

        print(f"Created {base_contour.name}.stl")

        
        

def plot_borders_str_grph(borders: ListOfSkylines, proj_vals: ProjVals, ax):
    used_borders = []
    for idx,line in enumerate(borders.list_of_skylines):
        if idx%100 == 0:
            print(f"str_graph_borders:\t{idx/len(borders.list_of_skylines)*100:.2f}%")

        ra1_rad  = line.point_data_1.ra_dec_deg.right_ascension_deg/180*pi
        dec1_rad = line.point_data_1.ra_dec_deg.declination_deg/180*pi
        ra2_rad  = line.point_data_2.ra_dec_deg.right_ascension_deg/180*pi
        dec2_rad = line.point_data_2.ra_dec_deg.declination_deg/180*pi


        # print(f"ra1= {ra1:.3f}\tra2= {ra2:.3f}\tdec1= {dec1:.3f}\tdec2= {dec2:.3f}")

        line_not_used = [[ra1_rad,dec1_rad],[ra2_rad,dec2_rad]] not in used_borders and [[ra2_rad,dec2_rad],[ra1_rad,dec1_rad]] not in used_borders

        if line_not_used:

            used_borders.append([[ra1_rad,dec1_rad],[ra2_rad,dec2_rad]])       

            ra_diff_rad = (ra2_rad-ra1_rad)
            if abs(ra_diff_rad)>pi:
                if ra1_rad<ra2_rad:
                    ra1_rad=ra1_rad+2*pi
                else:
                    ra1_rad=ra1_rad-2*pi  
                ra_diff_rad = (ra2_rad-ra1_rad)

            dec_diff_rad = (dec2_rad-dec1_rad)
            if abs(dec_diff_rad)>pi:
                if dec1_rad<dec2_rad:
                    dec1_rad=dec1_rad+2*pi
                else:
                    dec1_rad=dec1_rad-2*pi   
                dec_diff_rad = (dec2_rad-dec1_rad)
            iteration_num = max((np.floor(abs(ra_diff_rad)/(2*np.pi)*360))+1 , (np.floor(abs(dec_diff_rad)/(2*np.pi)*360))+1)

            ra_step_rad = ra_diff_rad/iteration_num
            dec_step_rad = dec_diff_rad/iteration_num
            ra_now_rad = ra1_rad
            dec_now_rad = dec1_rad

            for i in range(int(iteration_num)):
                ra_next_rad = ra_now_rad + ra_step_rad
                dec_next_rad = dec_now_rad + dec_step_rad

                ra_dec_now_deg = RaDecDegCoord_deg(right_ascension_deg=ra_now_rad/np.pi*180,
                                                   declination_deg=dec_now_rad/np.pi*180)

                v1 = get_transformed_vector(ra_dec_now_deg, proj_vals)
                # theta_R1 = polar_upproject(v1)
                x_y_z__1 = upproject(v1)

                ra_dec_next_deg = RaDecDegCoord_deg(right_ascension_deg=    ra_next_rad/np.pi*180,
                                                    declination_deg=        dec_next_rad/np.pi*180)

                v2 = get_transformed_vector(ra_dec_next_deg, proj_vals)
                # theta_R2 = polar_upproject(v2)
                x_y_z__2 = upproject(v2)


                x1=x_y_z__1[0]
                x2=x_y_z__2[0]
                y1=x_y_z__1[1]
                y2=x_y_z__2[1]
                color="red"
                plt.plot([y1,y2],[x1,x2],linewidth=0.5,linestyle="-",alpha=1,color=color)

                ra_now_rad = ra_next_rad
                dec_now_rad = dec_next_rad


def plot_lines_str_grph(lines: ListOfSkylines, proj_vals: ProjVals, ax):
    for idx,line in enumerate(lines.list_of_skylines):
        print(f"str_grp lines:\t{idx/len(lines.list_of_skylines)*100:.2f}%")

        v1 = get_transformed_vector(line.point_data_1.ra_dec_deg, proj_vals)
        xyz_1 = upproject(v1)

        v2 = get_transformed_vector(line.point_data_2.ra_dec_deg, proj_vals)
        xyz_2 = upproject(v2)

        x1=xyz_1[0]
        x2=xyz_2[0]
        y1=xyz_1[1]
        y2=xyz_2[1]
        plt.plot([y1,y2],[x1,x2], linewidth=line.width, linestyle=line.linestyle, alpha=0.9, color=line.color, zorder=ORDER_OF_LINES)
           