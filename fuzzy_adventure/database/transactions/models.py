from django.db import models

class Components(models.Model):
    name = models.CharField(max_length=90, blank=True)

    def __unicode__(self):
    	return self.name;

    class Meta:
        db_table = u'Component'


class Programmers(models.Model):
    name = models.CharField(max_length=240, blank=True)

    def __unicode__(self):
    	return self.name;

    class Meta:
        db_table = u'Programmer'


class Transactions(models.Model):
    trans_number = models.CharField(max_length=150, blank=True)
    programmer = models.ForeignKey(Programmers)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=90, blank=True)
    priority = models.CharField(max_length=60, blank=True)
    contract_priority = models.CharField(max_length=30, blank=True)
    product = models.CharField(max_length=90, blank=True)
    os = models.CharField(max_length=45, blank=True)
    system_type = models.CharField(max_length=3, blank=True)
    attribute = models.CharField(max_length=30, blank=True)
    solving_level = models.CharField(max_length=30, blank=True)
    flag_24h = models.CharField(max_length=3, blank=True)
    component = models.ForeignKey(Components)

    def __unicode__(self):
    	return self.trans_number;

    class Meta:
        db_table = u'Transaction'

