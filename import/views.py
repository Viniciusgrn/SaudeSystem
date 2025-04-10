from pyexpat.errors import messages
from django.shortcuts import render
from cadastros.models import Paciente
import pandas as pd

    # cns = models.CharField(max_length=19, unique=True, verbose_name="Cartao Sus")
    # nome = models.CharField(max_length=255, verbose_name="Nome")
    # dataNascimento = models.DateField(verbose_name="Data de Nascimento")
    # telefone = models.CharField(max_length=16, verbose_name="Telefone/Celular")
    
    
    


# Create your views here.
def importPacientes(request):
    if request.method == 'POST':
        if  len(request.FILES) != 0:
            file = request.FILES['file']
            #file = file.read().decode('utf-8')
            
            #clearProducts()   
            # Paciente.objects.all().delete()
        
            #df = pd.read_csv(file, sep=';')
            df = pd.read_csv(file, error_bad_lines=False,delimiter=';')
            aux = []
            for row in df.values:
                if row[23] >= 3:
                    obj = Paciente(
                        data_solicitacao=row[9], #cns
                        descricao=row[11], #nome
                        cns=row[19], #dataNascimento
                        cod_class=row[23], #telefone
                        posicao=row[24], #telefone2
                         #celular1
                         #celular2
                         #allowMessage
                         #altura
                         #peso
                         #comment
                         #isVisible
                         #isActive
                         #createdBy_user Atilio                        
                    )
                    aux.append(obj)           
            Paciente.objects.bulk_create(aux)
            messages.success(request, 'Pacientes importados concluída com sucesso.')
            
            return render(request, "cadastros/importar.html")
        else:
            messages.error(request, 'Selecione um arquivo para importar.')            
            return render(request, "cadastros/importar.html")
        
    return render(request, "cadastros/importar.html")