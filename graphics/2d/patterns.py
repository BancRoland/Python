from utils import *

edge_buffer = 0.8
tie_space = 1
tie_leavout = 1

phone_case = sewing_pattern(x_sizes = [ edge_buffer,
                                        17/2,
                                        edge_buffer],

                            y_sizes = [ edge_buffer,
                                        35/2+tie_leavout,
                                        edge_buffer,
                                        tie_space,
                                        tie_space,
                                        edge_buffer])

circumference_parellel_to_opening = 9
circumfernce_perpendicular_to_opening = 18
microscope_slides = sewing_pattern(x_sizes = [ edge_buffer,
                                        circumference_parellel_to_opening/2,
                                        edge_buffer],

                            y_sizes = [ edge_buffer,
                                        circumfernce_perpendicular_to_opening/2+tie_leavout,
                                        edge_buffer,
                                        tie_space,
                                        tie_space,
                                        edge_buffer])