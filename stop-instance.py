import boto3

# define ec2
ec2 = boto3.resource('ec2')

# Defini a procura por instâncias com status RUNNING e com base na TAG ambiente=SHUTDOWN
def lambda_handler(event, context): 
    filters = [{
        'Name': 'tag:SHUTDOWN',
        'Values': ['18HOURS']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    # Faz uma varredura pelos IDs das instâncias na zona de disponibilidade AZ onde a regra foi criada
    instances = ec2.instances.filter(Filters=filters)   
    
    # Pega o ID da instância
    RunningInstances = [instance.id for instance in instances]
    
    # Loga a execução das instância(s) impactadas
    print(RunningInstances)

    # Verificar se existem instâncias com base na TAG: SHUTDOWN ligada
    if len(RunningInstances) > 0:
        
        # Comando que executa stop na instância
        shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
        print("Parando instância")
    else:
        print("Não foram encontradas instâncias em RUNNING")

    return 'Stop da instância realizado com sucesso!'