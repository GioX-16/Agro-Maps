from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web3 import Web3
from models import SoilFertility, Macronutrients, Micronutrients, PhLevel, OrganicMatter
from django.conf import settings

# Conectarse a Scroll Sepolia
w3 = Web3(Web3.HTTPProvider('https://sepolia.scroll.io/eth_rpc'))
contract_address = "0x8E1dAc352D0acFfFc78eBa1090e362f7bb355E86"
contract_abi = settings.CONTRACTABI

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

@csrf_exempt  # Deshabilitar CSRF para pruebas; en producción maneja CSRF adecuadamente
def send_to_blockchain(request, study_id):
    if request.method == 'POST':
        user_wallet = request.POST.get('account')

        if not user_wallet:
            return JsonResponse({'success': False, 'error': 'No wallet address provided'})

        # Obtener el estudio y los datos relacionados
        try:
            study = SoilFertility.objects.get(id=study_id)
            macronutrients = study.macronutrients
            micronutrients = study.micronutrients
            phlevel = study.phlevel
            organicmatter = study.organicmatter
        except SoilFertility.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Study not found'})

        # Crear la transacción
        tx = contract.functions.storeStudyData(
            study.name,
            macronutrients.nitrogen, macronutrients.phosphorus, macronutrients.potassium,
            micronutrients.calcium, micronutrients.magnesium,
            phlevel.ph_value, phlevel.ph_kcl,
            organicmatter.percentage,
        ).buildTransaction({
            'from': user_wallet,
            'nonce': w3.eth.getTransactionCount(user_wallet),
            'gas': 2000000,
            'gasPrice': w3.toWei('50', 'gwei')
        })

        # Firmar la transacción
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=settings.WALLET_PRIVATE_KEY)

        # Enviar la transacción
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return JsonResponse({'success': True, 'tx_hash': tx_hash.hex()})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
