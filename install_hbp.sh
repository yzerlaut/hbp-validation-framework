git clone https://github.com/HumanBrainProject/hbp-validation-client.git
pip install -r hbp-validation-client/requirements.txt
pip install -U ./hbp-validation-client
git clone https://github.com/HumanBrainProject/pyxus.git pyxus_src
pip install -r pyxus_src/pyxus/requirements.txt
pip install -U pyxus_src/pyxus
git clone https://github.com/HumanBrainProject/fairgraph.git
pip install -r fairgraph/requirements.txt
pip install -U ./fairgraph
# I didn't clone hbp-validation-framework, I copied my version based on the "kg" branch, because it includes the django-keys and the decrypted packages
pip install -r hbp-validation-framework/requirements.txt
cd hbp-validation-framework
pip install -r validation_service/requirements.txt
git checkout dev # to set ENV='dev' in validation_service/validation_service/settings.py
source validation_service/env_local.sh # export the secret keys 
source export_env_variables_from_json_files.sh
# be sure to have set the following tokens:
echo 'HBP_token='$HBP_token
echo 'HBP_STORAGE_TOKEN='$HBP_STORAGE_TOKEN

