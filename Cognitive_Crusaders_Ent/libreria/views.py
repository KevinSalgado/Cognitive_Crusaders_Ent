from django.shortcuts import render
from django.http.response import JsonResponse

from .models import Caudal

from .predict import transf
from .predict import predic

def index(request):
# Obtener los valores únicos de la columna INF_Label
    labels = Caudal.objects.values('INF_Label').distinct()
    context = {
        'labels': labels
    }
    return render(request, 'graph_index.html', context)

def get_chart(request):
    label = request.GET.get('label')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    data = Caudal.objects.filter(INF_Label=label, RowKey__date__range=[fecha_inicio, fecha_fin]).values('RowKey', 'INF_Value').order_by('RowKey')
    data2 = transf(label)
    prediccion = predic(data2)
    #print(prediccion)
    #print(data2)
    # Resto del código
    #colors = ['blue', 'orange', 'red', 'black', 'yellow', 'green', 'magenta', 'lightblue', 'purple', 'brown']
    #random_color = colors[randrange(0, (len(colors)-1))]

    chart = {
        'tooltip':{
            'show':True,
            'trigger':"axis",
            'triggerOn':"mousemove|click"
        },
        'xAxis':[
            {
                'type': "category",
                'data': [d['FECHA'] for d in prediccion]
            }
        ],
        'yAxis':[
            {
                'type': "value"
            }
        ],
        'series':[
            {
                'data': [d['DATO'] for d in prediccion],
                'type':"line",
                'showSymbol': False,
                'itemStyle':{
                    'color':'red'
                },
                'lineStyle':{
                    'color':'blue'
                }
            }
        ]
    }
    return JsonResponse(chart)

