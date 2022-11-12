from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime
import uuid
from .utils import create_shortcode, code_generator
from django.utils.text import slugify
from django.urls import reverse
from autoslug import AutoSlugField
from django.db.utils import IntegrityError
from django.db import transaction
from django.forms import ValidationError


class Year(models.Model):
    # year = models.CharField(max_length=4,
    #                         default=datetime.now().year, unique=True)
    year = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return str(self.year)

    class Meta:
        ordering = ('-id',)


class EventDetail(models.Model):
    year = models.ForeignKey(
        Year, on_delete=models.SET_NULL, related_name='events', null=True)
    event_name = models.CharField(max_length=100, unique=True)
    date = models.DateField(default=datetime.now)
    slug = models.SlugField(blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.event_name

    class Meta:
        unique_together = (('year', 'event_name'),)
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.event_name) + '-%s' % self.year.year
        super(EventDetail, self).save(*args, **kwargs)  # calling save method

    def get_absolute_url(self):
        return reverse('event_attendant', kwargs={'slug': self.slug})


class Attendant(models.Model):
    STATUS_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )

    SEX_CHOICE = (
        ('brother', 'Brother'),
        ('sister', 'Sister')
    )

    LEVEL_CHOICE = (
        ('100', '100'),
        ('200', '200'),
        ('300', '300'),
        ('400', '400'),
        ('500', '500'),
        ('600', '600'),
        ('graduate', 'Graduate'),
    )

    DAY_CHOICE = (
        ('day1', 'Day 1'),
        ('day2', 'Day 2'),
        ('day3', 'Day 3'),
        ('day4', 'Day 4'),
        ('day5', 'Day 5'),
        ('day6', 'Day 6'),
        ('day7', 'Day 7'),

    )

    DEPARTMENT_CHOICE = (
        ('Accounting Technology', 'Accounting Technology'),
        ('Agricultural Economics', 'Agricultural Economics'),
        ('Agricultural Economics and Extension', 'Agricultural Economics and Extension'),
        ('Agricultural Engineering', 'Agricultural Engineering'),
        ('Agricultural Extension and Rural Development', 'Agricultural Extension and Rural Development'),
        ('Agriculture', 'Agriculture'),
        ('Anatomy', 'Anatomy'),
        ('Animal Nutrition and Biotechnology', 'Animal Nutrition and Biotechnology'),
        ('Animal Production and Health', 'Animal Production and Health'),
        ('Architecture', 'Architecture'),
        ('Biochemistry', 'Biochemistry'),
        ('Chemical Engineering', 'Chemical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Computer Engineering', 'Computer Engineering'),
        ('Computer Science', 'Computer Science'),
        ('Crop And Environmental Protection', 'Crop And Environmental Protection'),
        ('Crop Production And Soil Science', 'Crop Production And Soil Science'),
        ('Earth Science', 'Earth Science'),
        ('Economics', 'Economics'),
        ('Electrical / Electronic Engineering', 'Electrical / Electronic Engineering'),
        ('Fine / Applied Art', 'Fine / Applied Art'),
        ('Food Science and Engineering', 'Food Science and Engineering'),
        ('Information Systems', 'Information Systems'),
        ('Marketing', 'Marketing'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Medical Biochemistry', 'Medical Biochemistry'),
        ('Medical Laboratory Technology / Science', 'Medical Laboratory Technology / Science'),
        ('Medicine and Surgery', 'Medicine and Surgery'),
        ('Nursing / Nursing Science', 'Nursing / Nursing Science'),
        ('Nutrition and Dietetics', 'Nutrition and Dietetics'),
        ('Physics', 'Physics'),
        ('Physiology', 'Physiology'),
        ('Pure / Applied Biology', 'Pure / Applied Biology'),
        ('Pure / Applied Chemistry', 'Pure / Applied Chemistry'),
        ('Pure / Applied Mathematics', 'Pure / Applied Mathematics'),
        ('Pure and Industrial Chemistry', 'Pure and Industrial Chemistry'),
        ('Science Laboratory Technology', 'Science Laboratory Technology'),
        ('Transport Management Technology', 'Transport Management Technology'),
        ('Urban and Regional Planning', 'Urban and Regional Planning'),
        ('Fine and Applied Arts', 'Fine and Applied Arts'),
        ('Cyber Security', 'Cyber Security'),

    )
    eventdetail = models.ForeignKey(
        EventDetail, on_delete=models.SET_NULL, null=True, related_name='attendants')
    day = models.CharField(max_length=5, choices=DAY_CHOICE, default='day1')
    name = models.CharField(max_length=100)
    level = models.CharField(
        max_length=10, choices=LEVEL_CHOICE, default='100')
    phone_regex = RegexValidator(
        regex='^[0]\d{10}$', message="Phone number should be in the format: 08105506606")
    phone_number = models.CharField(max_length=11, validators=[phone_regex])
    visitor = models.CharField(
        max_length=3, choices=STATUS_CHOICES, default='no')
    department = models.CharField(max_length=200, choices=DEPARTMENT_CHOICE, default='Accounting Technology')
    email = models.EmailField()
    sex = models.CharField(
        max_length=10, choices=SEX_CHOICE, default='brother', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        unique_together = (('eventdetail', 'name', 'day', 'phone_number', 'level'),)

    # def get_absolute_url(self):
    #     return reverse('event_attendant', kwargs={'slug': self.slug, 'id': self.day,})
