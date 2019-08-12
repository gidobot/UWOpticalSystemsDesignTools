import unittest
import os
import src.lights as lights

class MyTest(unittest.TestCase):

    def setUp(self):
        self.light = lights.LightSource()
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../cfg/test_light.json")
        self.light.load(path)

    def test_beamarea(self):
        area = self.light.compute_beam_area(4)
        self.assertAlmostEqual(area, 3.367148, places=4)

    def test_radiance_scale_factor(self):
        scale = self.light.compute_spectral_radiance_scale()
        print(scale)

    def test_irradiance_scale_factor(self):
        area = self.light.compute_beam_area(4)
        scale = self.light.compute_spectral_radiance_scale()
        print(scale/scale)

if __name__ == '__main__':
    unittest.main()