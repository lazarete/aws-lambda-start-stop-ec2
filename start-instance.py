import boto3

# define ec2
ec2 = boto3.resource('ec2')

# Defini a procura por instâncias com status STOPPED e com base na TAG ambiente=START
def lambda_handler(event, context):
    filters = [{
        'Name': 'tag:START',
        'Values': ['09HOURS']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        }
    ]
    
    # Faz uma varredura pelos IDs das instâncias na zona de disponibilidade AZ onde a regra foi criada
    instances = ec2.instances.filter(Filters=filters)   
    
    # Pega o ID da instância
    RunningInstances = [instance.id for instance in instances]
    
    # Loga a execução das instância(s) impactadas
    print(RunningInstances)

    # Verificar se existem instâncias com base na TAG: START desligada
    if len(RunningInstances) > 0:
        
        # Comando que executa start na instância
        shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).start()
        print("Inicializando instância")
    else:
        print("Não foram encontradas instâncias com status STOPPED")

    return 'Start da instância realizado com sucesso!'
