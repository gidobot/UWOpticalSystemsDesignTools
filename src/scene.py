__author__ = 'gbillings'

from wateratenuationmodel import WaterPropagation

class Scene:
    def __init__(self):
        self.altitude = 1.
        self.overlap = 0.25
        self.speed = 0.
        self.motion_blur = 1.
        self.depthoffield = (0., 0.)
        self.bottom_type = 'Benthic Average'

        self.axis = 'x'

        # Bottom type reflection coarsley estimated from http://www.ioccg.org/training/SLS-2016/Dierssen_IOCCG_Lecture1_webLO.pdf
        self.bottom_type_dict = {'Benthic Average': 0.2, 'Sand': 0.35, 'Hard': 0.3, 'Coral': 0.15, 'Organic': 0.1}

        self.water = WaterPropagation()

    def initialize(self, alt, ovr, spe, mot, dep, bot):
        self.altitude = alt
        self.overlap = ovr
        self.speed = spe
        self.motion_blur = mot
        self.depthoffield = dep
        self.bottom_type = self.set_bottom_type(bot)

    def set_bottom_type(self, bot):
        if bot in self.bottom_type_dict.keys():
            self.bottom_type = bot
        else:
            self.bottom_type = 'Benthic Average'

    def get_reflectance(self):
        return self.bottom_type_dict[self.bottom_type]

