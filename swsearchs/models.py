from django.db import models

class imovel(models.Model):
    id = models.IntegerField(primary_key=True)
    contribuinte = models.CharField(max_length=12)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=30)
    complemento = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cep = models.CharField(max_length=9)
    area = models.IntegerField()
    valorm2 = models.IntegerField()

    class Meta:
        db_table = 'imovel'  # Nome da tabela no banco de dados

    def __str__(self):
        return f"{self.id}: {self.logradouro}, {self.numero}, {self.bairro}"