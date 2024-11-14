from django.db import models
import csv
import os
from django.conf import settings
from datetime import datetime

class Voter(models.Model):
    last_name = models.CharField(max_length=500)
    first_name = models.CharField(max_length=500)
    street_number = models.CharField(max_length=500)
    street_name = models.CharField(max_length=500)
    apartment_number = models.CharField(max_length=500, blank=True, null=True)
    zip_code = models.CharField(max_length=500)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    party_affiliation = models.CharField(max_length=500)
    precinct_number = models.CharField(max_length=500)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def load_data():
    file_path = os.path.join(settings.BASE_DIR, 'newton_voters.csv')

    def get_field(row, field_name, default=''):
        return row.get(field_name, default).strip()

    #Had data loading errors, wrote helper functions
    def parse_date(date_str):
        date_str = date_str.strip()
        if date_str:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return None
        return None

    def str_to_bool(s):
        return s.strip().upper() == 'TRUE' if s else False

    def str_to_int(s):
        s = s.strip()
        try:
            return int(s)
        except ValueError:
            return 0

    voter_list = []
    batch_size = 1000
    count = 0

    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            last_name = get_field(row, 'Last Name')
            first_name = get_field(row, 'First Name')
            street_number = get_field(row, 'Residential Address - Street Number')
            street_name = get_field(row, 'Residential Address - Street Name')
            apartment_number = get_field(row, 'Residential Address - Apartment Number') or None
            zip_code = get_field(row, 'Residential Address - Zip Code')
            date_of_birth = parse_date(get_field(row, 'Date of Birth'))
            date_of_registration = parse_date(get_field(row, 'Date of Registration'))
            party_affiliation = get_field(row, 'Party Affiliation')
            precinct_number = get_field(row, 'Precinct Number')
            v20state = str_to_bool(get_field(row, 'v20state'))
            v21town = str_to_bool(get_field(row, 'v21town'))
            v21primary = str_to_bool(get_field(row, 'v21primary'))
            v22general = str_to_bool(get_field(row, 'v22general'))
            v23town = str_to_bool(get_field(row, 'v23town'))
            voter_score = str_to_int(get_field(row, 'voter_score'))

            voter = Voter(
                last_name=last_name,
                first_name=first_name,
                street_number=street_number,
                street_name=street_name,
                apartment_number=apartment_number,
                zip_code=zip_code,
                date_of_birth=date_of_birth,
                date_of_registration=date_of_registration,
                party_affiliation=party_affiliation,
                precinct_number=precinct_number,
                v20state=v20state,
                v21town=v21town,
                v21primary=v21primary,
                v22general=v22general,
                v23town=v23town,
                voter_score=voter_score
            )
            voter_list.append(voter)
            count += 1

            if count % batch_size == 0:
                Voter.objects.bulk_create(voter_list)
                voter_list = []

        if voter_list:
            Voter.objects.bulk_create(voter_list)
