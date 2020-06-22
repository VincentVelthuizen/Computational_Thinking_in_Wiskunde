from django.db import models

# Create your models here.

class Level(models.Model):
    super_level = models.ForeignKey('self', related_name='sub_level', blank=True, null=True)
    sub_level_name_single = models.CharField(max_length=63, blank=True)
    sub_level_name_multiple = models.CharField(max_length=63, blank=True)

    short_name = models.CharField(max_length=7)
    long_name = models.CharField(max_length=63)
    description = models.CharField(max_length=1023)

    full_name = models.CharField(max_length=128*4, blank=True)

    def save(self, *args, **kwargs):
        self.full_name = self.get_fullname()
        super(Level, self).save(*args, **kwargs)

    def super_level_short_name(self):
        if self.super_level is None:
            return ''
        return self.super_level.short_name

    def get_fullname(self):
        if self.super_level is None:
            return self.long_name
        return u'%s - %s' % (self.super_level.get_fullname(), self.long_name)

    def get_covering(self):
        score = 0
        minimum = 4
        total = 0
        print(self)

        for covering in self.covers.all():
            score += covering.measure.score
            minimum = minimum if minimum < covering.measure.score else covering.measure.score
            total += 1

        for level in self.sub_level.all():
            sub_covering = level.get_covering()
            score += sub_covering['score']
            minimum = minimum if minimum < sub_covering['minimum'] else sub_covering['minimum']
            total += sub_covering['score']

        average = score/total if total > 0 else 'NA'
        return_dict = {'score': score, 'average': average, 'minimum': minimum}
        return return_dict

    def get_covered(self):
        score = 0
        minimum = 4
        total = 0

        for covering in self.covered:
            score += covering.measure.score
            minimum = minimum if minimum < covering.measure.score else covering.measure.score
            total += 1

        for level in self.sub_level:
            sub_covering = level.get_covered()
            score += sub_covering['score']
            minimum = minimum if minimum < sub_covering['minimum'] else sub_covering['minimum']
            total += sub_covering['score']

        average = score/total if total > 0 else 'NA'
        return_dict = {'score': score, 'average': average, 'minimum': minimum}
        return return_dict

    def __str__(self):
        return self.long_name

    class Meta:
        ordering = ['full_name']

class Measure(models.Model):
    name = models.CharField(max_length=63)
    score = models.IntegerField()

    def __str__(self):
        return self.name

class Covering(models.Model):
    covering_level = models.ForeignKey(Level, related_name='covers')
    covered_level = models.ForeignKey(Level, related_name='covered')

    nature = models.CharField(max_length=63)
    description = models.CharField(max_length=1023)
    measure = models.ForeignKey(Measure)

    def __str__(self):
        return u'%s covers %s' % (self.covering_level, self.covered_level)

class Sector(models.Model):
    name = models.CharField(max_length=7)
    long_name = models.CharField(max_length=63)

    def __str__(self):
        return self.long_name

class Vak(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=7)
    sector = models.ForeignKey(Sector)

    def __str__(self):
        return u'%s %s' % (self.sector, self.name)

class Domein(models.Model):
    name = models.CharField(max_length=255)
    vak = models.ForeignKey(Vak, related_name='domeinen')

    def __str__(self):
        return u'%s %s' % (self.vak, self.name)

class Kern(models.Model):
    name = models.CharField(max_length=255)
    domein = models.ForeignKey(Domein, related_name="kernen")

    def __str__(self):
        return u'%s %s' % (self.domein, self.name)

class Dekking(models.Model):
    bestaandeKern = models.ForeignKey(Kern, related_name='dektInDekking')
    gedekteKern = models.ForeignKey(Kern, related_name='gedektInDekking')
    mateVanDekking = models.IntegerField()

    def __str__(self):
        return u'%s dekt %s met een mate van %s' % (self.bestaandeKern, self.gedekteKern, self.mateVanDekking)
