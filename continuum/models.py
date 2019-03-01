from django.db import models

class Project(models.Model):
	name = models.CharField(max_length=50, null=True)
	amount = models.FloatField()
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name + ' - '+str(self.amount)

# class Vote(models.Model):
# 	name = models.CharField(max_length=256, null=True)
# 	project = models.ForeignKey(Project, on_delete=models.CASCADE)
# 	suma = models.IntegerField()

class Votes(models.Model):
	name = models.CharField(max_length=255, null=True)
	votes = models.CharField(max_length=255)

class Presupuesto(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	qty = models.FloatField()

