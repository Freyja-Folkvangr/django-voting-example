from django.db import models
import django.utils.timezone as timezone

#This is the voting process
class Question(models.Model):
	question_text = models.CharField(max_length=256)
	pub_date = models.DateTimeField('date published', default=timezone.now())
	budget = models.FloatField(null=False)

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - timezone.timedelta(days=1)

#This is the project choice
class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=256)
	description = models.CharField(max_length=512, default='No description provided')
	cost = models.FloatField()
	votes = models.IntegerField(default=0)

class Votes(models.Model):
	process = models.ForeignKey(Question, on_delete=models.CASCADE)
	name = models.CharField(max_length=256, null=True)
	votes = models.CharField(max_length=256)

	def get_vote_list(self):
		# 1: remove spaces.
		# 2: convert to list separated by comma.
		# 3: remove duplicates
		# 4: convert each to int.
		# 5: convert map obj to list
		return list(map(int, dict.fromkeys(self.votes.replace(' ', '').split(','))))
