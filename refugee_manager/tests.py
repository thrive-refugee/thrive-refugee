import datetime

from django.test import TestCase

from refugee_manager import admin
from refugee_manager import models


class TestCaseAdmin(TestCase):

    def test_next_assessment_active_1st(self):
        """Verify the 1st assessment is 30 days from the case start."""
        case = models.Case()
        case.active = True
        case.start = datetime.date(2008, 10, 15)
        case.save()

        actual = admin.CaseAdmin.next_assessment(case)

        expected = datetime.date(2008, 11, 14)  # 30 days after the start
        self.assertEqual(expected, actual)

    def test_next_assessment_active_2nd(self):
        """Verify the 2nd assessment is 183 days from the case start"""
        case = models.Case()
        case.active = True
        case.start = datetime.date(2008, 10, 15)
        case.save()

        assessment = models.Assessment()
        assessment.date = datetime.date(2008, 11, 25)
        assessment.case = case
        assessment.save()

        actual = admin.CaseAdmin.next_assessment(case)

        expected = datetime.date(2009, 4, 16)  # 183 days after the start
        self.assertEqual(expected, actual)

    def test_next_assessment_active_3nd_early(self):
        """Verify an assessment can be done early."""
        case = models.Case()
        case.active = True
        case.start = datetime.date(2008, 10, 15)
        case.save()

        assessment = models.Assessment()
        assessment.date = datetime.date(2008, 11, 25)
        assessment.case = case
        assessment.save()

        assessment = models.Assessment()
        assessment.date = datetime.date(2009, 4, 1)  # due on 4/16
        assessment.case = case
        assessment.save()

        actual = admin.CaseAdmin.next_assessment(case)

        expected = datetime.date(2009, 10, 16)  # 183 * 2 days after the start
        self.assertEqual(expected, actual)

    def test_next_assessment_active_3nd_late(self):
        """Verify an assessment can be done late."""
        case = models.Case()
        case.active = True
        case.start = datetime.date(2008, 10, 15)
        case.save()

        assessment = models.Assessment()
        assessment.date = datetime.date(2008, 11, 25)
        assessment.case = case
        assessment.save()

        assessment = models.Assessment()
        assessment.date = datetime.date(2009, 4, 30)  # due on 4/16
        assessment.case = case
        assessment.save()

        actual = admin.CaseAdmin.next_assessment(case)

        expected = datetime.date(2009, 10, 16)  # 183 * 2 days after the start
        self.assertEqual(expected, actual)

    def test_next_assessment_inactive(self):
        """Verify there is no next assessment on an inactive case."""
        case = models.Case()
        case.active = False
        case.start = datetime.date(2008, 10, 15)
        case.save()

        actual = admin.CaseAdmin.next_assessment(case)

        expected = None
        self.assertEqual(expected, actual)
