from django.db import models

class Data(models.Model):    
	# class Meta:
	# 	constraints = [models.UniqueConstraint(fields = ['data_id', 'stream_id'], name = "id")]

	d_id = models.CharField(max_length = 20,  default = '')
	stream_id = models.CharField(max_length = 30, default = '') #models.IntegerField(default = 0)    
	title = models.CharField(max_length = 50, default = '')
	text = models.CharField(max_length = 200, default = '')

	def __str__(self):
		return self.data_id