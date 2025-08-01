from django.core.management.base import BaseCommand
from planos.models import Marca, Veiculo

class Command(BaseCommand):
    help = 'Popula o banco com 10 veículos para cada marca'

    def handle(self, *args, **kwargs):
        marcas = {
            'Chevrolet': [
                {
                    'modelo': 'Onix',
                    'versoes': [
                        {'nome': 'LT 1.0 MT', 'fipe': 72000, 'categoria': 'POPULAR'},
                        {'nome': 'Premier 1.0 Turbo AT', 'fipe': 95000, 'categoria': 'MEDIO'}
                    ],
                    'anos': [2022, 2023]
                },
                {
                    'modelo': 'Tracker',
                    'versoes': [
                        {'nome': 'LT 1.2 Turbo', 'fipe': 110000, 'categoria': 'MEDIO'},
                        {'nome': 'Premier 1.4 Turbo', 'fipe': 140000, 'categoria': 'LUXO'}
                    ],
                    'anos': [2021, 2022]
                },
                {
                    'modelo': 'S10',
                    'versoes': [
                        {'nome': 'Cabine Dupla 2.8', 'fipe': 220000, 'categoria': 'LUXO'}
                    ],
                    'anos': [2020, 2021]
                },
                {
                    'modelo': 'Spin',
                    'versoes': [
                        {'nome': 'LT 1.8', 'fipe': 90000, 'categoria': 'POPULAR'}
                    ],
                    'anos': [2020, 2021]
                },
                {
                    'modelo': 'Cruze',
                    'versoes': [
                        {'nome': 'LT 1.4 Turbo', 'fipe': 105000, 'categoria': 'MEDIO'}
                    ],
                    'anos': [2019, 2020]
                }
            ],
            'Hyundai': [
                {
                    'modelo': 'HB20',
                    'versoes': [
                        {'nome': 'Sense 1.0 MT', 'fipe': 68000, 'categoria': 'POPULAR'},
                        {'nome': 'Vision 1.0 Turbo AT', 'fipe': 89000, 'categoria': 'MEDIO'}
                    ],
                    'anos': [2021, 2022]
                },
                {
                    'modelo': 'Creta',
                    'versoes': [
                        {'nome': 'Smart 1.6', 'fipe': 120000, 'categoria': 'MEDIO'},
                        {'nome': 'Premium 1.6', 'fipe': 150000, 'categoria': 'LUXO'}
                    ],
                    'anos': [2020, 2021]
                },
                {
                    'modelo': 'Tucson',
                    'versoes': [
                        {'nome': 'GL 2.0', 'fipe': 160000, 'categoria': 'LUXO'}
                    ],
                    'anos': [2019, 2020]
                },
                {
                    'modelo': 'Kona',
                    'versoes': [
                        {'nome': 'Elite 1.6', 'fipe': 155000, 'categoria': 'LUXO'}
                    ],
                    'anos': [2021, 2022]
                },
                {
                    'modelo': 'Santa Fé',
                    'versoes': [
                        {'nome': 'Limited 3.5', 'fipe': 250000, 'categoria': 'LUXO'}
                    ],
                    'anos': [2018, 2019]
                }
            ],
            'Fiat': [
                {
                    'modelo': 'Argo',
                    'versoes': [
                        {'nome': 'Drive 1.3 MT', 'fipe': 65000, 'categoria': 'POPULAR'},
                        {'nome': 'Trekking 1.8 AT', 'fipe': 92000, 'categoria': 'MEDIO'}
                    ],
                    'anos': [2020, 2021]
                },
                {
                    'modelo': 'Mobi',
                    'versoes': [
                        {'nome': 'Like 1.0', 'fipe': 50000, 'categoria': 'POPULAR'},
                        {'nome': 'Trekking 1.0', 'fipe': 62000, 'categoria': 'POPULAR'}
                    ],
                    'anos': [2021, 2022]
                },
                {
                    'modelo': 'Toro',
                    'versoes': [
                        {'nome': 'Ultra 2.4', 'fipe': 170000, 'categoria': 'LUXO'}
                    ],
                    'anos': [2019, 2020]
                },
                {
                    'modelo': 'Cronos',
                    'versoes': [
                        {'nome': 'Precision 1.8', 'fipe': 95000, 'categoria': 'MEDIO'}
                    ],
                    'anos': [2020, 2021]
                },
                {
                    'modelo': 'Pulse',
                    'versoes': [
                        {'nome': 'Audace 1.3', 'fipe': 105000, 'categoria': 'MEDIO'}
                    ],
                    'anos': [2022, 2023]
                }
            ],
            'Volkswagen': [
                {
                    'modelo': 'Gol',
                    'versoes': [
                        {'nome': '1.0 MSI Trend', 'fipe': 60000, 'categoria': 'POPULAR'},
                        {'nome': '1.6 MI Power AT', 'fipe': 78000, 'categoria': 'POPULAR'}
                    ],
                    'anos': [2019, 2020]
                },
                {
                    'modelo': 'T-Cross',
                    'versoes': [
                        {'nome': 'Highline 1.4 TSI', 'fipe': 150000, 'categoria': 'LUXO'}
                    ],
                    'anos': [2020, 2021]
                },
                {
                    'modelo': 'Virtus',
                    'versoes': [
                        {'nome': 'GT 1.4 TSI', 'fipe': 130000, 'categoria': 'LUXO'}
                    ],
                    'anos': [2021, 2022]
                },
                {
                    'modelo': 'Nivus',
                    'versoes': [
                        {'nome': 'Highline 1.0', 'fipe': 135000, 'categoria': 'LUXO'}
                    ],
                    'anos': [2020, 2021]
                },
                {
                    'modelo': 'Amarok',
                    'versoes': [
                        {'nome': 'V6 3.0', 'fipe': 300000, 'categoria': 'LUXO'}
                    ],
                    'anos': [2018, 2019]
                }
            ]
        }

        for marca_nome, modelos in marcas.items():
            marca, _ = Marca.objects.get_or_create(nome=marca_nome)
            
            for modelo_data in modelos:
                for versao in modelo_data['versoes']:
                    for ano in modelo_data['anos']:
                        Veiculo.objects.get_or_create(
                            marca=marca,
                            modelo=modelo_data['modelo'],
                            versao=versao['nome'],
                            ano=ano,
                            categoria=versao['categoria'],
                            valor_fipe=versao['fipe']
                        )
        
        self.stdout.write(self.style.SUCCESS(f'Total de veículos criados: {Veiculo.objects.count()}'))