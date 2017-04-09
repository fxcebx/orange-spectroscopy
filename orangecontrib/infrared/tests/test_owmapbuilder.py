import numpy as np
import Orange
from Orange.widgets.tests.base import WidgetTest
from orangecontrib.infrared.widgets.owmapbuilder import OWMapBuilder


class TestOWFiles(WidgetTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.collagen = Orange.data.Table("collagen.csv")

    def setUp(self):
        self.widget = self.create_widget(OWMapBuilder)

    def test_load_unload(self):
        # just to load the widget (it has no inputs)
        pass

    def test_no_data_warning(self):
        self.assertTrue(self.widget.Warning.nodata.is_shown())
        self.send_signal("Data", self.collagen)
        self.assertFalse(self.widget.Warning.nodata.is_shown())

    def test_line(self):
        self.send_signal("Data", self.collagen)
        self.widget.controls.xpoints.setText("1")
        self.widget.controls.ypoints.setText("731")
        self.widget.commit()
        m = self.get_output("Map data")
        np.testing.assert_equal(m[:, "X"].metas[:, 0], 0)
        np.testing.assert_equal(m[:, "Y"].metas[:, 0], range(len(self.collagen)))
        # the other direction
        self.widget.controls.ypoints.setText("1")
        self.widget.controls.xpoints.setText("731")
        self.widget.commit()
        m = self.get_output("Map data")
        np.testing.assert_equal(m[:, "Y"].metas[:, 0], 0)
        np.testing.assert_equal(m[:, "X"].metas[:, 0], range(len(self.collagen)))

    def test_wrong_dimensions(self):
        self.send_signal("Data", self.collagen)
        self.widget.controls.xpoints.setText("2")
        self.widget.controls.ypoints.setText("400")
        self.widget.le1_changed()  # get warnings activated
        self.assertEqual(self.widget.xpoints, 2)
        self.assertEqual(self.widget.ypoints, 400)
        self.widget.commit()
        self.assertTrue(self.widget.Warning.wrong_div.is_shown())
        self.assertIsNone(self.get_output("Map data"))

    def test_rect(self):
        self.send_signal("Data", self.collagen[:500])
        self.widget.controls.xpoints.setText("5")
        self.widget.le1_changed()
        self.assertEqual(self.widget.ypoints, 100)
        self.widget.commit()
        m = self.get_output("Map data")
        self.assertTrue(m[2]["X"].value, 2)
        self.assertTrue(m[2]["Y"].value, 0)
        self.assertTrue(m[102]["X"].value, 2)
        self.assertTrue(m[102]["Y"].value, 20)