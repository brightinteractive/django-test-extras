# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.test import TestCase


class TestStuff(TestCase):
    def test_something(self):
        self.assertEquals(2, 1 + 1)
